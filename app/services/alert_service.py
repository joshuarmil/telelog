import logging
from sqlalchemy.orm import Session
from app.models import Alert, TelemetryReading
from sqlalchemy import select

logger = logging.getLogger(__name__)

class AlertService:
    TEMP_CRITICAL_THRESHOLD = 85.0
    VOLTAGE_LOW_THRESHOLD = 3.0

    @staticmethod
    def evaluate_reading(reading: TelemetryReading, db: Session) -> None:
        if reading.temperature > AlertService.TEMP_CRITICAL_THRESHOLD:
            msg = f'Device {reading.device_id} is overheating! Reading: {reading.temperature}°C'
            logger.warning(f'ALERT: {msg}')

            overheat_alert = Alert(
                device_id=reading.device_id,
                telemetry_reading_id=reading.id,
                alert_type="CRITICAL_OVERHEAT",
                message=msg
            )
            db.add(overheat_alert)
        
        if reading.battery_voltage < AlertService.VOLTAGE_LOW_THRESHOLD:
            msg = f'Device {reading.device_id} voltage dropped to {reading.battery_voltage}V'
            logger.warning(f'ALERT: {msg}')

            battery_alert = Alert(
                device_id=reading.device_id,
                telemetry_reading_id=reading.id,
                alert_type="LOW_BATTERY",
                message=msg
            )
            db.add(battery_alert)

    @staticmethod
    def get_active_alerts(db: Session):
        query = select(Alert).where(Alert.resolved == False).order_by(Alert.created_at.desc())
        return list(db.execute(query).scalars().all())

    @staticmethod
    def resolve_alert(alert_id: int, db: Session):
        # Allows operator to clear active incidents
        try:
            alert = db.get(Alert, alert_id)
            if not alert:
                return None

            alert.resolved = True
            db.commit()
            db.refresh(alert)

            logger.info(f'Human operator marked Alert ID {alert_id} as RESOLVED.')
            return alert
        
        except Exception as e:
            db.rollback()
            raise