from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional
from pydantic.types import conint



class CreateUser(BaseModel):
    email: EmailStr
    password: str
    
    
    