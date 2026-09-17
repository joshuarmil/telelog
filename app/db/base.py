from sqlalchemy import create_engine, String, ForeignKey, DateTime, func, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/telemetry"

engine = create_engine(DATABASE_URL, echo=True)

class Base(DeclarativeBase):
    pass
