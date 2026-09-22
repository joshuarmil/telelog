from pydantic import BaseModel, ConfigDict
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

    model_config = ConfigDict(from_attributes=True)