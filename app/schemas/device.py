from pydantic import BaseModel, ConfigDict
from datetime import datetime

class DeviceCreate(BaseModel):
    name: str
    location: str | None = None

class DeviceResponse(BaseModel):
    id: int
    name: str
    location: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)