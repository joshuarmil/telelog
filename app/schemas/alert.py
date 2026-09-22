from pydantic import BaseModel, ConfigDict
from datetime import datetime

class AlertResponse(BaseModel):
    id: int
    device_id: int
    telemetry_reading_id: int
    alert_type: str
    message: str
    resolved: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)