from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
# from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import SessionLocal, get_db
from app.models.device import Device
from app.schemas.device import DeviceCreate, DeviceResponse
import logging
from typing import List

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/devices", tags=["Device Management Cluster"])

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

@router.get("/{requested_id}", response_model=DeviceResponse)
async def get_specific_device(requested_id: int, db: Session = Depends(get_db)):
    query = select(Device).where(requested_id == Device.id)
    
    # Execute query
    result = db.execute(query)
    
    # Fetch all records
    device = result.scalars().all()
    
    return device


@router.post("/", response_model=DeviceResponse, status_code=status.HTTP_201_CREATED)
def add_device(payload: DeviceCreate, db: Session = Depends(get_db)):
    logger.info(f"Received new device: {payload.name}")
    
    new_device = Device(name=payload.name, location=payload.location)

    try:
        db.add(new_device)
        db.commit()
        db.refresh(new_device)

        logger.info(f"Successfully persisted Device ID: {new_device.id} for Device: {new_device.name}")

        return new_device

    except Exception as e:
        db.rollback()
        logger.error(f"Failed to persist new Device {payload.name}. Error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database write operation failed during data ingestion pipeline."
        )

