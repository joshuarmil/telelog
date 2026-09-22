from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import TelemetryReading
from app.schemas.telemetry import TelemetryCreate
import logging

logger = logging.getLogger(__name__)

class TelemetryService:
    def __init__(self, db: Session):
        self.db = db

    def get_readings(self, skip: int, limit: int) -> list(TelemetryReading):
        # Clamp query
        limit = 100 if limit > 100 or limit < 1 else limit

        # Add pagination
        query = select(TelemetryReading).offset(skip).limit(limit)
        
        result = self.db.execute(query)
        
        return result.scalars().all()

    def create_reading(self, payload: TelemetryCreate) -> TelemetryReading:

        new_telemetry = TelemetryReading(device_id=payload.device_id, temperature=payload.temperature, 
                                    battery_voltage=payload.battery_voltage, timestamp=payload.timestamp)

        try:
            self.db.add(new_telemetry)
            self.db.commit()
            self.db.refresh(new_telemetry)

            logger.info(f"Successfully persisted Telemetry Record ID: {new_telemetry.id} for Device: {new_telemetry.device_id}")

            return new_telemetry

        except Exception as e:
            self.db.rollback()
            raise e