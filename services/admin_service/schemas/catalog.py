from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator, HttpUrl
import sys
import os

# Add parent directory to path to import common modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


class CatalogAdminBase(BaseModel):
    """
    Base schema for catalog admin operations
    """
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = None
    category_id: Optional[int] = None
    brand: Optional[str] = Field(None, max_length=100)
    model: Optional[str] = Field(None, max_length=100)
    image_url: Optional[HttpUrl] = None
    specifications: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


class CatalogAdminUpdate(CatalogAdminBase):
    """
    Schema for catalog item update by admin
    """
    pass


class CatalogAdminResponse(BaseModel):
    """
    Schema for catalog item response in admin panel
    """
    id: int
    name: str
    description: Optional[str] = None
    category_id: int
    brand: Optional[str] = None
    model: Optional[str] = None
    image_url: Optional[HttpUrl] = None
    specifications: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True


class CatalogAdminSearchResponse(BaseModel):
    """
    Schema for catalog item search response in admin panel
    """
    items: List[CatalogAdminResponse]
    total: int
    page: int
    page_size: int
