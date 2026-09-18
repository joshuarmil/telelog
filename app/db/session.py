from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from app.core.config import db_string

engine = create_engine(db_string, echo=True, 
                       pool_pre_ping=True, pool_size=10, max_overflow=20) # For checking and reviving dead connection

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()