from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.device import DeviceCreate, DeviceResponse
from app.services.device_service import DeviceService
from typing import List
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/devices", tags=["Device Management Cluster"])

def get_device_service(db: Session = Depends(get_db)):
    return DeviceService(db)

@router.get("/", response_model=List[DeviceResponse])
def get_devices(skip: int = 0, limit: int = 100, service: DeviceService = Depends(get_device_service)):
    return service.get_devices(skip, limit)

@router.get("/{requested_id}", response_model=DeviceResponse)
def get_specific_device(requested_id: int, service: DeviceService = Depends(get_device_service)):
    try:
        return service.get_device_by_id(requested_id)
    except ValueError as e:
        logger.error(f"Failed to fetch device registry payload. Error: {str(e)}")
        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requested hardware device identifier not found."
        )


@router.post("/", response_model=DeviceResponse, status_code=status.HTTP_201_CREATED)
def add_device(payload: DeviceCreate, service: DeviceService = Depends(get_device_service)):
    logger.info(f"Received new device: {payload.name}")

    try:
        return service.add_device(payload)
    except Exception as e:
        logger.error(f"Failed to persist new Device {payload.name}. Error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database write operation failed during ingestion pipeline."
        )

