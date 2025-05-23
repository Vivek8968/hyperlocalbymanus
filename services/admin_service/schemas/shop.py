from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator, HttpUrl
import sys
import os

# Add parent directory to path to import common modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


class ShopAdminBase(BaseModel):
    """
    Base schema for shop admin operations
    """
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = None
    whatsapp_number: Optional[str] = Field(None, min_length=10, max_length=15)
    address: Optional[str] = None
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    image_url: Optional[HttpUrl] = None
    banner_url: Optional[HttpUrl] = None
    is_active: Optional[bool] = None


class ShopAdminUpdate(ShopAdminBase):
    """
    Schema for shop update by admin
    """
    pass


class ShopAdminResponse(BaseModel):
    """
    Schema for shop response in admin panel
    """
    id: int
    user_id: int
    name: str
    description: Optional[str] = None
    whatsapp_number: Optional[str] = None
    address: Optional[str] = None
    latitude: float
    longitude: float
    image_url: Optional[HttpUrl] = None
    banner_url: Optional[HttpUrl] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ShopAdminSearchResponse(BaseModel):
    """
    Schema for shop search response in admin panel
    """
    shops: List[ShopAdminResponse]
    total: int
    page: int
    page_size: int
