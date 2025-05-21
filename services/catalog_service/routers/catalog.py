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
from common.exceptions.http_exceptions import ResourceNotFoundException, UnauthorizedException

# Import schemas and services
from schemas.catalog import (
    CatalogItemCreate, 
    CatalogItemUpdate, 
    CatalogItemResponse, 
    CatalogItemWithCategoryResponse,
    CatalogSearchResponse
)
from services.catalog_service import CatalogService

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.post("", response_model=CatalogItemResponse, status_code=status.HTTP_201_CREATED)
async def create_catalog_item(
    item_data: CatalogItemCreate,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new catalog item (admin only)
    """
    # Check if user is admin
    if current_user.get("role") != "admin":
        raise UnauthorizedException("Only admins can create catalog items")
    
    catalog_service = CatalogService(db)
    item = await catalog_service.create_catalog_item(**item_data.dict())
    
    return item

@router.get("", response_model=CatalogSearchResponse)
async def get_catalog_items(
    query: Optional[str] = None,
    category_id: Optional[int] = None,
    brand: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """
    Get catalog items with optional filtering
    """
    catalog_service = CatalogService(db)
    
    # Calculate offset for pagination
    offset = (page - 1) * page_size
    
    # Get catalog items
    items, total = await catalog_service.get_catalog_items(
        query=query,
        category_id=category_id,
        brand=brand,
        skip=offset,
        limit=page_size
    )
    
    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "query": query
    }

@router.get("/search", response_model=CatalogSearchResponse)
async def search_catalog(
    query: str = Query(..., min_length=2),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """
    Search catalog items by name, description, brand, or model
    """
    catalog_service = CatalogService(db)
    
    # Calculate offset for pagination
    offset = (page - 1) * page_size
    
    # Search catalog items
    items, total = await catalog_service.search_catalog_items(
        query=query,
        skip=offset,
        limit=page_size
    )
    
    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "query": query
    }

@router.get("/{item_id}", response_model=CatalogItemWithCategoryResponse)
async def get_catalog_item(
    item_id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_db)
):
    """
    Get catalog item by ID
    """
    catalog_service = CatalogService(db)
    item = await catalog_service.get_catalog_item_by_id(item_id)
    
    if not item:
        raise ResourceNotFoundException(f"Catalog item with ID {item_id} not found")
    
    return item

@router.put("/{item_id}", response_model=CatalogItemResponse)
async def update_catalog_item(
    item_data: CatalogItemUpdate,
    item_id: int = Path(..., gt=0),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update catalog item (admin only)
    """
    # Check if user is admin
    if current_user.get("role") != "admin":
        raise UnauthorizedException("Only admins can update catalog items")
    
    catalog_service = CatalogService(db)
    item = await catalog_service.update_catalog_item(
        item_id=item_id,
        item_data=item_data.dict(exclude_unset=True)
    )
    
    return item

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_catalog_item(
    item_id: int = Path(..., gt=0),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete catalog item (admin only)
    """
    # Check if user is admin
    if current_user.get("role") != "admin":
        raise UnauthorizedException("Only admins can delete catalog items")
    
    catalog_service = CatalogService(db)
    await catalog_service.delete_catalog_item(item_id)
    
    return None
