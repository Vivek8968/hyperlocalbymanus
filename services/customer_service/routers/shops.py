from fastapi import APIRouter, Depends, HTTPException, status, Path, Query
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any, Optional

# Import common modules
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.database.session import get_db
from common.auth.jwt import get_current_user
from common.exceptions.http_exceptions import ResourceNotFoundException
from common.utils.geo import GeoService

# Import schemas and services
from schemas.shop import ShopSearchResponse, ShopDetailResponse, ShopWithProductsResponse
from schemas.preference import LocationQuery
from services.discovery_service import DiscoveryService
from services.preference_service import PreferenceService

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.get("/nearby", response_model=ShopSearchResponse)
async def get_nearby_shops(
    location: LocationQuery,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    current_user: Optional[Dict[str, Any]] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get shops near the specified location
    """
    discovery_service = DiscoveryService(db)
    
    # Calculate offset for pagination
    offset = (page - 1) * page_size
    
    # Get shops near location
    shops, total = await discovery_service.get_shops_near_location(
        latitude=location.latitude,
        longitude=location.longitude,
        radius_km=location.radius,
        skip=offset,
        limit=page_size
    )
    
    return {
        "shops": shops,
        "total": total,
        "page": page,
        "page_size": page_size,
        "location": {
            "latitude": location.latitude,
            "longitude": location.longitude
        }
    }

@router.get("/search", response_model=ShopSearchResponse)
async def search_shops(
    query: str = Query(..., min_length=2),
    location: Optional[LocationQuery] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    current_user: Optional[Dict[str, Any]] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Search shops by name or products
    """
    discovery_service = DiscoveryService(db)
    
    # Calculate offset for pagination
    offset = (page - 1) * page_size
    
    # Search shops
    if location:
        # Search with location filtering
        shops, total = await discovery_service.search_shops_with_location(
            query=query,
            latitude=location.latitude,
            longitude=location.longitude,
            radius_km=location.radius,
            skip=offset,
            limit=page_size
        )
        
        location_dict = {
            "latitude": location.latitude,
            "longitude": location.longitude
        }
    else:
        # Search without location filtering
        shops, total = await discovery_service.search_shops(
            query=query,
            skip=offset,
            limit=page_size
        )
        
        location_dict = None
    
    return {
        "shops": shops,
        "total": total,
        "page": page,
        "page_size": page_size,
        "location": location_dict
    }

@router.get("/{shop_id}", response_model=ShopDetailResponse)
async def get_shop_details(
    shop_id: int = Path(..., gt=0),
    location: Optional[LocationQuery] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Get shop details by ID
    """
    discovery_service = DiscoveryService(db)
    shop = await discovery_service.get_shop_by_id(shop_id)
    
    if not shop:
        raise ResourceNotFoundException(f"Shop with ID {shop_id} not found")
    
    # Calculate distance if location provided
    if location:
        geo_service = GeoService()
        distance = await geo_service.calculate_distance(
            location.latitude,
            location.longitude,
            shop.latitude,
            shop.longitude
        )
        shop.distance = round(distance, 2)
    
    return shop

@router.get("/{shop_id}/products", response_model=ShopWithProductsResponse)
async def get_shop_products(
    shop_id: int = Path(..., gt=0),
    location: Optional[LocationQuery] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """
    Get products from a shop
    """
    discovery_service = DiscoveryService(db)
    
    # Calculate offset for pagination
    offset = (page - 1) * page_size
    
    # Get shop with products
    shop_with_products = await discovery_service.get_shop_with_products(
        shop_id=shop_id,
        skip=offset,
        limit=page_size
    )
    
    if not shop_with_products:
        raise ResourceNotFoundException(f"Shop with ID {shop_id} not found")
    
    # Calculate distance if location provided
    if location:
        geo_service = GeoService()
        distance = await geo_service.calculate_distance(
            location.latitude,
            location.longitude,
            shop_with_products.latitude,
            shop_with_products.longitude
        )
        shop_with_products.distance = round(distance, 2)
    
    return shop_with_products
