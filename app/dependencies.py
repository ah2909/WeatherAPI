import requests
from fastapi import HTTPException
from db.database import SessionLocal, engine
from fastapi.security import OAuth2PasswordBearer
from ..config import *


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def call_api(q: str):
    url = "https://weatherapi-com.p.rapidapi.com/forecast.json"
    querystring = {"q": q}
    response = requests.get(url, headers=headers, params=querystring).json()
    return response

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
