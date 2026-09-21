from sqlalchemy import String, ForeignKey, func, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from datetime import datetime

# SQLAlchemy Table Model
class Alert(Base):
    __tablename__ = "alerts"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    device_id: Mapped[int] = mapped_column(ForeignKey('devices.id', ondelete="CASCADE"), nullable=False)
    telemetry_reading_id: Mapped[int] = mapped_column(ForeignKey('telemetry.id', ondelete="CASCADE"), nullable=False)

    alert_type: Mapped[str] = mapped_column(String(50), nullable=False)
    message: Mapped[str] = mapped_column(String(255), nullable=False)
    resolved: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    device: Mapped["Device"] = relationship("Device")
    telemetry_reading: Mapped["TelemetryReading"] = relationship("TelemetryReading")
