from fastapi import FastAPI, status
from app.routes import devices, telemetry, alerts
from contextlib import asynccontextmanager
from app.db.base import Base
from app.db.session import engine
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title="Telelog", lifespan=lifespan)
app.include_router(devices.router)
app.include_router(telemetry.router)
app.include_router(alerts.router)

@app.get("/", status_code=status.HTTP_200_OK)
def read_root():
    return {
        "status": "healthy",
        "service": "telelog-telemetry-api",
        "version": "1.0.0",
        "documentation": "/docs"
    }