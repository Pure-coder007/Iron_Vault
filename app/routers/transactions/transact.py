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
    tags=['Transactions']
)


# Get user account details
@router.get("/search_by_account/{account_number}", response_model=schemas.AccountDetailsResponse)
def search_user_by_account(
    account_number: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        account_num = int(account_number)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account number must contain only digits"
        )
    
    user = db.query(models.User).filter(
        models.User.account_number == account_num
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )
    
    # Return public information only
    return {
        "account_number": user.account_number,
        "account_name": user.email.split('@')[0],  # Username part of email
        "bank_name": "Iron Vault Bank",
        "account_exists": True,
        "message": "Account verified"
    }