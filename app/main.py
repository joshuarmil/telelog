from fastapi import FastAPI
from app.routes import devices, telemetry
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

@app.get("/")
def read_root():
    return {"Hello": "World"}

