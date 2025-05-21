from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator, HttpUrl
import sys
import os

# Add parent directory to path to import common modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


class CategoryBase(BaseModel):
    """
    Base schema for category data
    """
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = None


class CategoryCreate(CategoryBase):
    """
    Schema for category creation
    """
    pass


class CategoryUpdate(BaseModel):
    """
    Schema for category update
    """
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = None


class CategoryResponse(CategoryBase):
    """
    Schema for category response
    """
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
