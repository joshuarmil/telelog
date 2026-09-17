from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
# from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import SessionLocal, get_db
from app.models.device import Device, DeviceResponse
import logging
from typing import List


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger("telemetry_api")


router = APIRouter(prefix="/devices", tags=["Device Management Cluster"])

# @router.post("/devices")
# def create_event(event: dict, db: Session = Depends(get_db)):
#     db_event = Event(**event)
#     db.add(db_event)
#     db.commit()
#     db.refresh(db_event)
#     return db_event


@router.get("/", response_model=List[DeviceResponse])
async def get_devices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Clamp query
    limit = 100 if limit > 100 or limit < 1 else limit
    
    # Construct the query with pagination
    query = select(Device).offset(skip).limit(limit)
    
    # Execute query
    result = db.execute(query)
    
    # Return all fetched records
    return result.scalars().all()

@router.get("/{requested_id}")
async def get_specific_device(requested_id: int, db: Session = Depends(get_db)):
    # Construct the query with pagination
    query = select(Device).where(requested_id == Device.id)
    
    # Execute query
    result = db.execute(query)
    
    # Fetch all records
    device = result.scalars().all()
    
    return device


@router.post("/", status_code=status.HTTP_201_CREATED)
def add_device(device: dict, db: Session = Depends(get_db)):
    # device_dict = device.model_dump()

    # if device.temp:
    #     pass
    logger.info("test")

    # db_device = Device(name=device.name, location=device.location)
    db_device = Device(**device)
    db.add(db_device)
    db.commit()
    db.refresh(db_device)

    return {"message": "Device saved successfully", "id": db_device.id}

