from fastapi import APIRouter, Request, Form, status, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated, Union
from db import crud, models, schemas
from sqlalchemy.orm import Session
from ..dependencies import *


router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def root(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/")
async def login(request: Request, email: Annotated[str, Form()] = None, password: Annotated[str, Form()] = None):
    if email and password:
        return RedirectResponse("/home", status_code=status.HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
    
@router.get("/home", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db), token: Annotated[str, Depends(oauth2_scheme)] = None):
    return templates.TemplateResponse("home.html", {"request": request})

@router.post("/info")
async def read_info(request: Request, city: Annotated[str, Form()] = None, token: Annotated[str, Depends(oauth2_scheme)] = None):
    if city:
        return RedirectResponse("/info?city=" + city, status_code=status.HTTP_303_SEE_OTHER)   
    else:
        return RedirectResponse("/home")
    
@router.get("/info", response_class=HTMLResponse)
async def display(request: Request, city: str, token: Annotated[str, Depends(oauth2_scheme)] = None):
    response = await call_api(city)
    return templates.TemplateResponse("home.html", {
            "request": request, 
            "city": response["location"]["name"], 
            "temp": response["current"]["temp_c"],
            "feel_like": response["current"]["feelslike_c"],
            "humid": response["current"]["humidity"],
            "icon": response["current"]["condition"]["icon"],
            "text": response["current"]["condition"]["text"],
            "last_updated": response["current"]["last_updated"]
            })

@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@router.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users