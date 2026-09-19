from sqlalchemy import String, ForeignKey, DateTime, func, Boolean, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from datetime import datetime

# SQLAlchemy Table Model
class TelemetryReading(Base):
    __tablename__ = "telemetry"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    device_id: Mapped[int] = mapped_column(ForeignKey('devices.id', ondelete="CASCADE"), nullable=False)
    temperature: Mapped[float] = mapped_column(Float, nullable=False)
    battery_voltage: Mapped[float] = mapped_column(Float, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Worker flag
    processed: Mapped[bool] = mapped_column(default=False)

    # Relationship link (not an actual DB column)
    device: Mapped["Device"] = relationship("Device", back_populates="readings")
