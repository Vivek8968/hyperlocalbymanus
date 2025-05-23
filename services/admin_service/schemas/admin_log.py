from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator, HttpUrl
import sys
import os

# Add parent directory to path to import common modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


class AdminLogBase(BaseModel):
    """
    Base schema for admin log data
    """
    admin_id: int
    action: str = Field(..., min_length=2, max_length=100)
    entity_type: str = Field(..., min_length=2, max_length=50)
    entity_id: Optional[int] = None
    details: Optional[Dict[str, Any]] = None


class AdminLogCreate(AdminLogBase):
    """
    Schema for admin log creation
    """
    pass


class AdminLogResponse(AdminLogBase):
    """
    Schema for admin log response
    """
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class AdminLogFilter(BaseModel):
    """
    Schema for admin log filtering
    """
    admin_id: Optional[int] = None
    action: Optional[str] = None
    entity_type: Optional[str] = None
    entity_id: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class AdminLogSearchResponse(BaseModel):
    """
    Schema for admin log search response
    """
    logs: List[AdminLogResponse]
    total: int
    page: int
    page_size: int
