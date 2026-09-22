import logging
from fastapi import APIRouter, Depends, HTTPException, status
from app.models import Alert
from app.schemas.alert import AlertResponse
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.services.alert_service import AlertService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/alerts", tags=["Alerts"])

@router.get("/", response_model=List[AlertResponse])
def get_active_alerts(db: Session = Depends(get_db)):
    return AlertService.get_active_alerts(db)

@router.post("/{alert_id}/resolve", response_model=AlertResponse)
def resolve_alert(alert_id: int, db: Session = Depends(get_db)):
    try:
        resolved_alert = AlertService.resolve_alert()
        if not resolved_alert:
            raise ValueError
        
        logger.info(f'Operator successfully cleared active Alert {alert_id}')
        return resolved_alert

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert event record not found."
        )
    except Exception as e:
        logger.error(f"Failed to persist alert resolution for Alert {alert_id}. Error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database write operation failed during data ingestion pipeline."
        )