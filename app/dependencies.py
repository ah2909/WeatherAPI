import requests
from fastapi import HTTPException
from db.database import SessionLocal, engine
from fastapi.security import OAuth2PasswordBearer

headers = {
        "X-RapidAPI-Key": "202fb9a6bbmshb1e89c18a8a6361p14bac0jsnf36ebc12ea45",
        "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
    }

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
