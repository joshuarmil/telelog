from fastapi import FastAPI, status, Depends
from contextlib import asynccontextmanager
from app.db.base import Base, engine
from pydantic import BaseModel


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"Hello": "World"}

