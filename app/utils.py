from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app import models
import random

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verify_hashed_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)



# Hash Transcation pin

def hash_pin(pin: str):
    return pwd_context.hash(pin)

def verify_hashed_pin(plain_pin: str, hashed_pin: str):
    return pwd_context.verify(plain_pin, hashed_pin)



def validate_user_registration(password: str, confirm_password: str, transaction_pin: int, confirm_transaction_pin: int, phone_number: str, nin: str, bvn: str):
    if password != confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match."
        )

    if len(password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters long."
        )

    if transaction_pin != confirm_transaction_pin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Transaction pins do not match."
        )

    if len(str(transaction_pin)) != 4 :
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Transaction pin must be exactly 4 digits."
        )
        
    if len(str(phone_number)) != 11:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone number must be at exactly 11 digits long."
        )
        
    
    if len(str(nin)) != 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="NIN must be exactly 10 digits long."
        
        )
    
    if len(str(bvn)) != 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="BVN must be exactly 10 digits long."
        )
        
        
        
def generate_account_number(db: Session):
    while True:
        account_number = str(random.randint(1000000000, 9999999999))
        
        existing = db.query(models.User).filter(
            models.User.account_number == account_number
        ).first()

        if not existing:
            return account_number
        
        
        
def email_exists(email: str, db: Session) -> bool:
    return db.query(models.User).filter(
        models.User.email == email
    ).first() is not None


def phone_number_exists(phone_number: str, db: Session) -> bool:
    return db.query(models.User).filter(
        models.User.phone_number == phone_number
    ).first() is not None
        
