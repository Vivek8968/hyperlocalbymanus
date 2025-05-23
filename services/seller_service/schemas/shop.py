from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, validator, HttpUrl
import sys
import os

# Add parent directory to path to import common modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


class ShopBase(BaseModel):
    """
    Base schema for shop data
    """
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = None
    whatsapp_number: Optional[str] = Field(None, pattern=r'^\+?[0-9]{10,15}$')
    address: Optional[str] = Field(None, max_length=255)
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)


class ShopCreate(ShopBase):
    """
    Schema for shop creation
    """
    pass


class ShopUpdate(BaseModel):
    """
    Schema for shop update
    """
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = None
    whatsapp_number: Optional[str] = Field(None, pattern=r'^\+?[0-9]{10,15}$')
    address: Optional[str] = Field(None, max_length=255)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    image_url: Optional[HttpUrl] = None
    banner_url: Optional[HttpUrl] = None


class ShopResponse(ShopBase):
    """
    Schema for shop response
    """
    id: int
    user_id: int
    image_url: Optional[HttpUrl] = None
    banner_url: Optional[HttpUrl] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ShopWithInventoryResponse(ShopResponse):
    """
    Schema for shop response with inventory
    """
    inventory_items: List["InventoryItemResponse"] = []

    class Config:
        from_attributes = True


class ImageUploadResponse(BaseModel):
    """
    Schema for image upload response
    """
    presigned_url: str
    image_url: str
    field_name: str
