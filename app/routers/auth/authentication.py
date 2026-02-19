from fastapi import FastAPI, Response, status, Depends, APIRouter
from pydantic import BaseModel
from typing import Optional, List
from random import randrange
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException
import psycopg2, random
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from ...database import get_db
from datetime import datetime, timedelta, timezone
from app import models, schemas, utils, oauth2



router = APIRouter(
    # prefix="/auth",
    tags=['Authentication']
)




@router.post("/register", status_code=201, response_model=schemas.CreateUserResponse)
async def register(user: schemas.CreateUser, db: Session = Depends(get_db)):

    if  utils.email_exists(user.email, db):
        raise HTTPException(status_code=409, detail=f"Email '{user.email}' is already in use.")

    if  utils.phone_number_exists(user.phone_number, db):
        raise HTTPException(status_code=409, detail=f"Phone number '{user.phone_number}' is already in use.")

    # centralized validation
    utils.validate_user_registration(
        password=user.password,
        confirm_password=user.confirm_password,
        transaction_pin=user.transaction_pin,
        confirm_transaction_pin=user.confirm_transaction_pin, 
        phone_number=user.phone_number,
        nin=user.nin,
        bvn=user.bvn
    )

    # hash sensitive info
    hashed_password = utils.hash(user.password)
    hashed_pin = utils.hash(str(user.transaction_pin))
    account_number = utils.generate_account_number(db)

    user_data = user.dict(exclude={"confirm_password", "confirm_transaction_pin"})
    user_data.update({
        "password": hashed_password,
        "transaction_pin": hashed_pin,
        "account_number": account_number
    })

    new_user = models.User(**user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    formatted_balance = f"₦{new_user.balance:,.2f}"
    
    response = schemas.CreateUserResponse(
        id=new_user.id,
        email=new_user.email,
        account_number=new_user.account_number,
        phone_number=new_user.phone_number,
        created_at=new_user.created_at,
        balance=formatted_balance,
        message="Registration successful please verify your email"
    )

    return response




@router.post("/login", response_model=schemas.TokenResponse)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials"
        )
        
    if not utils.verify_hashed_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials"
        )
        
    user.last_login = datetime.now(timezone.utc)
    db.commit()
    
    formatted_time = user.last_login.strftime("%Y-%m-%d %H:%M:%S")
    
        
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    
    return {"access_token": access_token, "token_type": "bearer", "user_id": user.id, "email": user.email, "last_login": formatted_time}