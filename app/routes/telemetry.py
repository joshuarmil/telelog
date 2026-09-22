from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.telemetry import TelemetryCreate, TelemetryResponse
import logging
from typing import List
from app.services.telemetry_service import TelemetryService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/telemetry", tags=["Telemetry Ingestion Pipeline"])

@router.get("/", response_model=List[TelemetryResponse])
def get_telemetry(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return TelemetryService.get_readings(skip, limit, db)
    
@router.post("/", response_model=TelemetryResponse, status_code=status.HTTP_201_CREATED)
def add_telemetry(payload: TelemetryCreate, db: Session = Depends(get_db)):
    logger.info(f"Received ingestion payload from Device ID: {payload.device_id}")
    try:
        return TelemetryService.create_reading(payload, db)
    except Exception as e:
        logger.error(f"Failed to persist telemetry payload for Device {payload.device_id}. Error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database write operation failed during ingestion pipeline."
        )
