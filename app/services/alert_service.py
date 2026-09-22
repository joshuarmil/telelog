import logging
from sqlalchemy.orm import Session
from app.models import Alert, TelemetryReading
from sqlalchemy import select

logger = logging.getLogger(__name__)

class AlertService:
    TEMP_CRITICAL_THRESHOLD = 85.0
    VOLTAGE_LOW_THRESHOLD = 3.0

    def __init__(self, db: Session):
        self.db = db

    def evaluate_reading(self, reading: TelemetryReading) -> None:
        if reading.temperature > self.TEMP_CRITICAL_THRESHOLD:
            msg = f'Device {reading.device_id} is overheating! Reading: {reading.temperature}°C'
            logger.warning(f'ALERT: {msg}')

            overheat_alert = Alert(
                device_id=reading.device_id,
                telemetry_reading_id=reading.id,
                alert_type="CRITICAL_OVERHEAT",
                message=msg
            )
            self.db.add(overheat_alert)
        
        if reading.battery_voltage < self.VOLTAGE_LOW_THRESHOLD:
            msg = f'Device {reading.device_id} voltage dropped to {reading.battery_voltage}V'
            logger.warning(f'ALERT: {msg}')

            battery_alert = Alert(
                device_id=reading.device_id,
                telemetry_reading_id=reading.id,
                alert_type="LOW_BATTERY",
                message=msg
            )
            self.db.add(battery_alert)

    def get_active_alerts(self) -> list(Alert):
        query = select(Alert).where(Alert.resolved == False).order_by(Alert.created_at.desc())
        return self.db.execute(query).scalars().all()

    def resolve_alert(self, alert_id: int) -> Alert:
        # Allows operator to clear active incidents
        try:
            alert = self.db.get(Alert, alert_id)
            if not alert:
                return None

            alert.resolved = True
            self.db.commit()
            self.db.refresh(alert)

            logger.info(f'Operator marked Alert ID {alert_id} as RESOLVED.')
            return alert
        
        except Exception as e:
            self.db.rollback()
            raise