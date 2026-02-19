from pydantic import BaseModel, EmailStr, ConfigDict, constr
from datetime import datetime
from typing import Optional
from pydantic.types import conint



class CreateUser(BaseModel):
    email: EmailStr
    password: constr(min_length=8)
    confirm_password: str

    transaction_pin: str
    confirm_transaction_pin: str
    phone_number: str
    
    nin: Optional[str] = None
    bvn: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)
    
    

class CreateUserResponse(BaseModel):
    id: str
    email: EmailStr
    account_number: int
    phone_number: str
    created_at: datetime
    balance: str
    message: str
    
    model_config = ConfigDict(from_attributes=True)
    
    
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    

class TokenData(BaseModel):
    id: str


# In schemas.py
class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: str
    email: str
    last_login: datetime
    
    model_config = ConfigDict(from_attributes=True)
    
    
class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: str
    email: str
    last_login: datetime
    
    model_config = ConfigDict(from_attributes=True)
    
    
    
class UserProfileResponse(BaseModel):
    id: str
    email: str
    phone_number: Optional[str] = None
    account_number: int
    balance: str
    is_verified: bool
    is_frozen: bool
    role: str
    created_at: datetime
    last_login: Optional[datetime] = None
    nin: Optional[str] = None
    bvn: Optional[str] = None
    
    
    model_config = ConfigDict(from_attributes=True)