from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    username : str = Field(..., min_length=5, max_length=20)
    email : EmailStr = Field(..., max_length=50)
    password : str = Field(..., min_length=8, max_length=128)
    
class UserResponse(BaseModel):
    id : int
    username : str
    email : EmailStr
    is_active : bool
    created_at : datetime
    updated_at : datetime
    
    model_config = {
        "from_attributes": True
    }
    
class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=5, max_length=20)
    email: Optional[EmailStr] = Field(None, max_length=50)
    password: Optional[str] = Field(None, min_length=8, max_length=128)

class UserLogin(BaseModel):
    identifier: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=8, max_length=128)