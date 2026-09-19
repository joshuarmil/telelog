from pydantic import BaseModel
from datetime import datetime

class DeviceCreate(BaseModel):
    name: str
    location: str | None = None


# Pydantic Schema for Response
class DeviceResponse(BaseModel):
    id: int
    name: str
    location: str | None
    created_at: datetime

    class Config:
        from_attributes = True