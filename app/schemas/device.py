from pydantic import BaseModel
class DeviceCreate(BaseModel):
    name: str
    location: str | None = None