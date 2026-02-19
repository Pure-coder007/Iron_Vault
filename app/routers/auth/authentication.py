from fastapi import FastAPI, Response, status, Depends, APIRouter
from pydantic import BaseModel
from typing import Optional, List
from random import randrange
from fastapi.exceptions import HTTPException
import psycopg2, random
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from ...database import get_db
from app import models, schemas, utils



router = APIRouter(
    prefix="/auth",
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