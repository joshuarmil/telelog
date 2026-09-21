import time
import logging
from app.db.session import SessionLocal
from sqlalchemy import select
from app.models import TelemetryReading
from app.services.alert_service import AlertService

logger = logging.getLogger(__name__)

def process_telemetry(batch_limit: int = 100):
    with SessionLocal() as db:
        try:
            query = (select(TelemetryReading).where(TelemetryReading.processed == False).limit(batch_limit).with_for_update(skip_locked=True))
            result = db.execute(query)
            readings = result.scalars().all()

            if not readings:
                return False

            logger.info(f"Retrieved {len(readings)} unprocessed telemetry packets.")

            for reading in readings:
                logger.info(f"Processing Reading ID: {reading.id} for Device ID: {reading.device_id}")
                time.sleep(0.05) # simulate latency
                AlertService.evaluate_reading(reading, db)
                reading.processed = True

            db.commit()
            logger.info(f"Successfully processed and committed batch of {len(readings)} entries.")
            return True
        
        except Exception as e:
            db.rollback()
            logger.error(f"Catastrophic transactional error encountered in worker loop: {str(e)}")
            return False

def main():
    logger.info("Initializing asynchronous background processing node engine")

    while True:
        try:
            did_work = process_telemetry()
            if not did_work:
                time.sleep(5) # Give more time if db is empty
            else:
                time.sleep(0.5)
        except KeyboardInterrupt:
            logger.info("Graceful shutdown sequence initialized by system operator.")
            break
        except Exception as e:
            logger.critical(f"Unhandled operational exception in master runtime loop: {str(e)}")
            time.sleep(10) # Give more time for infrastructure error

if __name__ == "__main__":
    main()