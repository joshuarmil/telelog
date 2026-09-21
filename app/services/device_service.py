from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models import Device
from app.schemas.device import DeviceCreate
import logging

logger = logging.getLogger(__name__)

class DeviceService:
    @staticmethod
    def get_devices(skip: int, limit: int, db: Session):
        # Clamp query
        limit = 100 if limit > 100 or limit < 1 else limit
        
        # Construct the query with pagination
        query = select(Device).offset(skip).limit(limit)
        
        # Execute query
        result = db.execute(query)
        
        # Return all fetched records
        return result.scalars().all()

    @staticmethod
    def get_device_by_id(device_id: int, db: Session):
        query = select(Device).where(requested_id == Device.id)
        
        # Execute query
        result = db.execute(query)
        
        # Fetch all records
        device = result.scalar_one_or_none()
        
        if not device:
            raise ValueError(f"Device asset index {device_id} non-existent in database.")
            
        return device

    @staticmethod
    def add_device(payload: DeviceCreate, db: Session):
        new_device = Device(name=payload.name, location=payload.location)

        try:
            db.add(new_device)
            db.commit()
            db.refresh(new_device)

            logger.info(f"Successfully persisted Device ID: {new_device.id} for Device: {new_device.name}")

            return new_device

        except Exception as e:
            db.rollback()
            raise
