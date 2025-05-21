from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, validator
import sys
import os

# Add parent directory to path to import common modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from services.user_service.models.user import UserRole


class UserBase(BaseModel):
    """
    Base schema for user data
    """
    name: str = Field(..., min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, pattern=r'^\+?[0-9]{10,15}$')
    role: UserRole = UserRole.CUSTOMER


class UserCreate(UserBase):
    """
    Schema for user creation
    """
    firebase_token: str = Field(..., min_length=10)


class UserUpdate(BaseModel):
    """
    Schema for user update
    """
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, pattern=r'^\+?[0-9]{10,15}$')


class UserResponse(UserBase):
    """
    Schema for user response
    """
    id: int
    firebase_uid: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class FirebaseAuthRequest(BaseModel):
    """
    Schema for Firebase authentication request
    """
    firebase_token: str = Field(..., min_length=10)


class TokenResponse(BaseModel):
    """
    Schema for token response
    """
    access_token: str
    token_type: str
    user_id: int
    role: UserRole
