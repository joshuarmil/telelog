from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.device import DeviceCreate, DeviceResponse
from app.services.device_service import DeviceService
from typing import List
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/devices", tags=["Device Management Cluster"])

@router.get("/", response_model=List[DeviceResponse])
def get_devices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return DeviceService.get_devices(skip, limit, db)

@router.get("/{requested_id}", response_model=DeviceResponse)
def get_specific_device(requested_id: int, db: Session = Depends(get_db)):
    try:
        return DeviceService.get_device_by_id(requested_id, db)
    except ValueError as e:
        logger.error(f"Failed to fetch device registry payload. Internal Context: {str(e)}")
        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requested hardware device identifier could not be verified."
        )


@router.post("/", response_model=DeviceResponse, status_code=status.HTTP_201_CREATED)
def add_device(payload: DeviceCreate, db: Session = Depends(get_db)):
    logger.info(f"Received new device: {payload.name}")

    try:
        return DeviceService.add_device(payload, db)
    except Exception as e:
        logger.error(f"Failed to persist new Device {payload.name}. Error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database write operation failed during data ingestion pipeline."
        )

