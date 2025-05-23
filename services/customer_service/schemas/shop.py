from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator, HttpUrl
import sys
import os

# Add parent directory to path to import common modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


class ShopBase(BaseModel):
    """
    Base schema for shop data (customer view)
    """
    id: int
    name: str
    description: Optional[str] = None
    whatsapp_number: Optional[str] = None
    address: Optional[str] = None
    latitude: float
    longitude: float
    image_url: Optional[HttpUrl] = None
    banner_url: Optional[HttpUrl] = None


class ShopDistance(ShopBase):
    """
    Schema for shop with distance information
    """
    distance: float  # Distance in kilometers
    
    class Config:
        from_attributes = True


class ShopSearchResponse(BaseModel):
    """
    Schema for shop search response
    """
    shops: List[ShopDistance]
    total: int
    page: int
    page_size: int
    location: Dict[str, float]  # Contains latitude and longitude


class ShopDetailResponse(ShopBase):
    """
    Schema for detailed shop response
    """
    distance: Optional[float] = None  # Distance in kilometers if location provided
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ProductBrief(BaseModel):
    """
    Brief schema for product data (used in shop detail response)
    """
    id: int
    catalog_item_id: int
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    brand: Optional[str] = None
    image_url: Optional[HttpUrl] = None
    price: float
    stock: int
    
    class Config:
        from_attributes = True


class ShopWithProductsResponse(ShopDetailResponse):
    """
    Schema for shop response with products
    """
    products: List[ProductBrief] = []
    
    class Config:
        from_attributes = True
