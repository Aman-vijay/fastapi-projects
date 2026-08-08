from fastapi import APIRouter,Depends,HTTPException
from sqlmodel import Session,select
from db import get_session
from models.user import User,UserCreate,UserRead,UserUpdate
from auth import verify_api_key
import os

#Rest Api for user registration
users_router = APIRouter(prefix="/users",tags=["users"])

@users_router.post("/register",response_model=UserRead)
def register_user(user:UserCreate,session:Session=Depends(get_session),api_key:str=Depends(verify_api_key)):
    if api_key != os.getenv("API_KEY"):
        raise HTTPException(status_code=401,detail="Invalid API key")
    #Check if user already exists
    existing_user = session.exec(select(User).where(User.email == user.email)).first()
    if existing_user:
        raise HTTPException(status_code=400,detail="User already exists")
    #Create new user
    new_user = User.model_validate(user)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

#Rest Api for get user
@users_router.get("/",response_model=list[UserRead])
def list_users(session:Session=Depends(get_session)):
    users = session.exec(select(User)).all()
    return users


