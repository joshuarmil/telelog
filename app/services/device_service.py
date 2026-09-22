from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models import Device
from app.schemas.device import DeviceCreate
import logging

logger = logging.getLogger(__name__)

class DeviceService:
    def __init__(self, db: Session):
        self.db = db

    def get_devices(self, skip: int, limit: int) -> list(Device):
        # Clamp query
        limit = 100 if limit > 100 or limit < 1 else limit
        
        # Add pagination
        query = select(Device).offset(skip).limit(limit)
        
        result = self.db.execute(query)
        
        return result.scalars().all()

    def get_device_by_id(self, device_id: int):
        query = select(Device).where(requested_id == Device.id)
        
        result = self.db.execute(query)
        
        device = result.scalar_one_or_none()
        
        if not device:
            raise ValueError(f"Device index {device_id} not found in database.")
            
        return device

    def add_device(self, payload: DeviceCreate) -> Device:
        new_device = Device(name=payload.name, location=payload.location)

        try:
            self.db.add(new_device)
            self.db.commit()
            self.db.refresh(new_device)

            logger.info(f"Successfully persisted Device ID: {new_device.id} for Device: {new_device.name}")

            return new_device

        except Exception as e:
            self.db.rollback()
            raise
