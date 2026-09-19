from pydantic import BaseModel
from datetime import datetime

class TelemetryCreate(BaseModel):
    device_id: int
    temperature: float | None
    battery_voltage: float | None
    timestamp: datetime | None

# Pydantic Schema for Response
class TelemetryResponse(BaseModel):
    id: int
    device_id: int
    temperature: float | None
    battery_voltage: float | None
    timestamp: datetime | None

    class Config:
        from_attributes = True