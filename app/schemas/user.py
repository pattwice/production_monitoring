import pydantic as _pd
import datetime as _dt
from typing import Optional as _Optional

class UserBase(_pd.BaseModel):
    """Base schema with common fields"""
    email: _pd.EmailStr
    username: str = _pd.Field(..., min_length=3, max_length=50)
    fullname: _Optional[str] = None

class UserCreate(UserBase):
    """Schema for creating a new user"""
    password: str = _pd.Field(..., min_length=8)

class UserLogin(_pd.BaseModel):
    """Schema for login"""
    username: str
    password: str

class UserResponse(UserBase):
    """Schema for returning user data (no password)"""
    id: int
    is_active: bool
    created_at: _dt.datetime
    
    class Config:
        from_attributes = True

class Token(_pd.BaseModel):
    """Schema for JWT token response"""
    access_token: str
    token_type: str = "bearer"

class TokenData(_pd.BaseModel):
    """Data stored inside JWT token"""
    username: _Optional[str] = None