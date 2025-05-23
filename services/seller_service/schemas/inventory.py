from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, validator, HttpUrl
import sys
import os

# Add parent directory to path to import common modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


class InventoryItemBase(BaseModel):
    """
    Base schema for inventory item data
    """
    catalog_item_id: int
    price: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)


class InventoryItemCreate(InventoryItemBase):
    """
    Schema for inventory item creation
    """
    pass


class InventoryItemUpdate(BaseModel):
    """
    Schema for inventory item update
    """
    price: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)


class InventoryItemResponse(InventoryItemBase):
    """
    Schema for inventory item response
    """
    id: int
    shop_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CatalogItemBrief(BaseModel):
    """
    Brief schema for catalog item data (used in inventory responses)
    """
    id: int
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    brand: Optional[str] = None
    image_url: Optional[HttpUrl] = None

    class Config:
        from_attributes = True


class InventoryItemWithCatalogResponse(InventoryItemResponse):
    """
    Schema for inventory item response with catalog item data
    """
    catalog_item: Optional[CatalogItemBrief] = None

    class Config:
        from_attributes = True
