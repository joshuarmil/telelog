from sqlalchemy import String, func, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from pydantic import BaseModel
from app.db.base import Base
from datetime import datetime

# SQLAlchemy Table Model
class Device(Base):
    __tablename__ = "devices"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    location: Mapped[str] = mapped_column(String(50))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

# Pydantic Schema for Response
class DeviceResponse(BaseModel):
    id: int
    name: str
    location: str | None
    created_at: datetime | None

    class Config:
        from_attributes = True