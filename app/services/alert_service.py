import logging
from sqlalchemy.orm import Session
from app.models.telemetry import TelemetryReading

logger = logging.getLogger(__name__)

class AlertService:
    TEMP_CRITICAL_THRESHOLD = 85.0
    VOLTAGE_LOW_THRESHOLD = 3.0

    @staticmethod
    def evaluate_reading(reading: TelemetryReading, db: Session) -> None:
        if reading.temperature > AlertService.TEMP_CRITICAL_THRESHOLD:
            logger.warning(f"CRITICAL ALERT: Device {reading.device_id} is overheating! " 
                f"Reading: {reading.temperature}°C")
        
        if reading.battery_voltage < AlertService.VOLTAGE_LOW_THRESHOLD:
            logger.warning(f"LOW BATTERY: Device {reading.device_id} voltage dropped to {reading.battery_voltage}V")