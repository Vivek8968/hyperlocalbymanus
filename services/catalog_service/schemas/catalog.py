from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator, HttpUrl
import sys
import os

# Add parent directory to path to import common modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


class CatalogItemBase(BaseModel):
    """
    Base schema for catalog item data
    """
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = None
    category_id: int
    brand: Optional[str] = Field(None, max_length=100)
    model: Optional[str] = Field(None, max_length=100)
    image_url: Optional[HttpUrl] = None
    specifications: Optional[Dict[str, Any]] = None


class CatalogItemCreate(CatalogItemBase):
    """
    Schema for catalog item creation
    """
    pass


class CatalogItemUpdate(BaseModel):
    """
    Schema for catalog item update
    """
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = None
    category_id: Optional[int] = None
    brand: Optional[str] = Field(None, max_length=100)
    model: Optional[str] = Field(None, max_length=100)
    image_url: Optional[HttpUrl] = None
    specifications: Optional[Dict[str, Any]] = None


class CatalogItemResponse(CatalogItemBase):
    """
    Schema for catalog item response
    """
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class CatalogItemWithCategoryResponse(CatalogItemResponse):
    """
    Schema for catalog item response with category
    """
    category: Optional["CategoryResponse"] = None

    class Config:
        orm_mode = True


class CatalogSearchResponse(BaseModel):
    """
    Schema for catalog search response
    """
    items: List[CatalogItemWithCategoryResponse]
    total: int
    page: int
    page_size: int
    query: Optional[str] = None


# Import CategoryResponse to avoid circular import issues
from .category import CategoryResponse
CatalogItemWithCategoryResponse.update_forward_refs()
