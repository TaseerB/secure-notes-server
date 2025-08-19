from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    name: str
    email: str
    is_active: Optional[bool] = True

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    # Note: password is excluded from read model for security
    
    class Config:
        from_attributes = True