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


@router.put("/profile", response_model=schemas.UserProfileResponse)
def update_my_profile(
    user_update: schemas.UpdateProfile,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    # Check if email already exists (if updating email)
    if user_update.email and user_update.email != current_user.email:
        existing_user = db.query(models.User).filter(
            models.User.email == user_update.email
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already in use"
            )
    
    # Check if phone number already exists (if updating phone)
    if user_update.phone_number and user_update.phone_number != current_user.phone_number:
        # Validate phone number format
        if not user_update.phone_number.isdigit():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phone number must contain only digits"
            )
        
        if len(user_update.phone_number) != 11:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phone number must be exactly 11 digits"
            )
        
        # Check if it starts with valid Nigerian prefix
        if user_update.phone_number[:3] not in ['070', '080', '090', '081', '091']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phone number must start with 070, 080, 090, 081, or 091"
            )
        
        # Check if already in use
        existing_user = db.query(models.User).filter(
            models.User.phone_number == user_update.phone_number
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Phone number already in use"
            )
    
    # Update only provided fields
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(current_user, field, value)
    
    db.commit()
    db.refresh(current_user)
    
    # Format response
    response = schemas.UserProfileResponse(
        id=current_user.id,
        email=current_user.email,
        role=current_user.role,
        account_number=current_user.account_number,
        last_login=current_user.last_login,
        created_at=current_user.created_at,
        nin=current_user.nin,
        bvn=current_user.bvn,
        balance=f"₦{current_user.balance:,.2f}",
        is_verified=current_user.is_verified,
        is_frozen=current_user.is_frozen,
        phone_number=current_user.phone_number
    )
    
    return response





# Change password
