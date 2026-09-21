from pydantic import BaseModel
from datetime import datetime

class AlertResponse(BaseModel):
    id: int
    device_id: int
    telemetry_reading_id: int
    alert_type: str
    message: str
    resolved: bool
    created_at: datetime

    class Config:
        from_attributes = True