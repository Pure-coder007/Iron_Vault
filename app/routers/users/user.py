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
    tags=['Users']
)



@router.get("/profile/{id}", response_model=schemas.UserProfileResponse)
def get_user_profile(
    id: str, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)  
):
    
    if current_user.id != id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this profile"
        )
    
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found"
        )
        
    formatted_balance = f"₦{user.balance:,.2f}"
    
    formatted_time = user.last_login.strftime("%Y-%m-%d %H:%M:%S")
    created_formatted_time = user.created_at.strftime("%Y-%m-%d %H:%M:%S")
    
    
    
    response = schemas.UserProfileResponse(
        id=user.id,
        email=user.email,
        role=user.role,
        account_number=user.account_number,
        last_login=formatted_time,
        created_at=created_formatted_time,
        nin=user.nin,
        bvn=user.bvn,
        balance=formatted_balance,
        is_verified=user.is_verified,
        is_frozen=user.is_frozen,
        phone_number=user.phone_number
    )
    
    return response