from fastapi import FastAPI
from app.routers import weather
from db import crud, models, schemas
from db.database import SessionLocal, engine
from fastapi.staticfiles import StaticFiles

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(weather.router)