from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, validator, HttpUrl
import sys
import os

# Add parent directory to path to import common modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


class PreferenceBase(BaseModel):
    """
    Base schema for customer preference data
    """
    default_latitude: Optional[float] = Field(None, ge=-90, le=90)
    default_longitude: Optional[float] = Field(None, ge=-180, le=180)
    search_radius: float = Field(5.0, gt=0, le=50)  # Default 5 km, max 50 km


class PreferenceCreate(PreferenceBase):
    """
    Schema for customer preference creation
    """
    pass


class PreferenceUpdate(BaseModel):
    """
    Schema for customer preference update
    """
    default_latitude: Optional[float] = Field(None, ge=-90, le=90)
    default_longitude: Optional[float] = Field(None, ge=-180, le=180)
    search_radius: Optional[float] = Field(None, gt=0, le=50)


class PreferenceResponse(PreferenceBase):
    """
    Schema for customer preference response
    """
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class LocationQuery(BaseModel):
    """
    Schema for location-based queries
    """
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    radius: Optional[float] = Field(5.0, gt=0, le=50)  # Default 5 km, max 50 km
