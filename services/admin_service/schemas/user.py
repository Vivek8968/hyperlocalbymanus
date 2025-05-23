from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator, HttpUrl, EmailStr
import sys
import os

# Add parent directory to path to import common modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


class UserAdminBase(BaseModel):
    """
    Base schema for user admin operations
    """
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, min_length=10, max_length=15)
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    role: Optional[str] = Field(None, pattern=r'^(customer|seller|admin)$')
    is_active: Optional[bool] = None


class UserAdminUpdate(UserAdminBase):
    """
    Schema for user update by admin
    """
    pass


class UserAdminResponse(BaseModel):
    """
    Schema for user response in admin panel
    """
    id: int
    email: Optional[str] = None
    phone: Optional[str] = None
    full_name: Optional[str] = None
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    firebase_uid: Optional[str] = None
    
    class Config:
        from_attributes = True


class UserAdminSearchResponse(BaseModel):
    """
    Schema for user search response in admin panel
    """
    users: List[UserAdminResponse]
    total: int
    page: int
    page_size: int
