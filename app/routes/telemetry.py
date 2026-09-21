from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
# from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import SessionLocal, get_db
from app.models import TelemetryReading
from app.schemas.telemetry import TelemetryCreate, TelemetryResponse
import logging
from typing import List

logger = logging.getLogger("telemetry_api")

router = APIRouter(prefix="/telemetry", tags=["Telemetry Ingestion Pipeline"])

@router.get("/", response_model=List[TelemetryResponse])
async def get_telemetry(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Clamp query
    limit = 100 if limit > 100 or limit < 1 else limit

    # Construct the query with pagination
    query = select(TelemetryReading).offset(skip).limit(limit)
    
    # Execute query
    result = db.execute(query)
    
    # Return all fetched records
    return result.scalars().all()
    
@router.post("/", response_model=TelemetryResponse, status_code=status.HTTP_201_CREATED)
def add_telemetry(payload: TelemetryCreate, db: Session = Depends(get_db)):
    logger.info(f"Received ingestion payload from Device ID: {payload.device_id}")

    new_telemetry = TelemetryReading(device_id=payload.device_id, temperature=payload.temperature, 
                                    battery_voltage=payload.battery_voltage, timestamp=payload.timestamp)

    try:
        db.add(new_telemetry)
        db.commit()
        db.refresh(new_telemetry)

        logger.info(f"Successfully persisted Telemetry Record ID: {new_telemetry.id} for Device: {new_telemetry.device_id}")

        return new_telemetry

    except Exception as e:
        db.rollback()
        logger.error(f"Failed to persist telemetry payload for Device {payload.device_id}. Error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database write operation failed during data ingestion pipeline."
        )
