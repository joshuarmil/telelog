from fastapi import FastAPI, status
from app.routes import devices, telemetry, alerts
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

app = FastAPI(title="Telelog", version="1.0.0")
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