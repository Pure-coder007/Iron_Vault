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
    
    