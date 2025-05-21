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
from schemas.catalog import CatalogAdminUpdate, CatalogAdminResponse, CatalogAdminSearchResponse
from services.catalog_service import AdminCatalogService
from services.admin_log_service import AdminLogService

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.get("", response_model=CatalogAdminSearchResponse)
async def get_catalog_items(
    query: Optional[str] = None,
    category_id: Optional[int] = None,
    brand: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all catalog items with optional filtering (admin only)
    """
    # Check if user is admin
    if current_user.get("role") != "admin":
        raise UnauthorizedException("Only admins can access this endpoint")
    
    # Calculate offset for pagination
    offset = (page - 1) * page_size
    
    catalog_service = AdminCatalogService(db)
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
        "page_size": page_size
    }

@router.get("/{item_id}", response_model=CatalogAdminResponse)
async def get_catalog_item(
    item_id: int = Path(..., gt=0),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get catalog item by ID (admin only)
    """
    # Check if user is admin
    if current_user.get("role") != "admin":
        raise UnauthorizedException("Only admins can access this endpoint")
    
    catalog_service = AdminCatalogService(db)
    item = await catalog_service.get_catalog_item_by_id(item_id)
    
    if not item:
        raise ResourceNotFoundException(f"Catalog item with ID {item_id} not found")
    
    return item

@router.put("/{item_id}", response_model=CatalogAdminResponse)
async def update_catalog_item(
    item_data: CatalogAdminUpdate,
    item_id: int = Path(..., gt=0),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update catalog item (admin only)
    """
    # Check if user is admin
    if current_user.get("role") != "admin":
        raise UnauthorizedException("Only admins can access this endpoint")
    
    catalog_service = AdminCatalogService(db)
    admin_log_service = AdminLogService(db)
    
    # Update catalog item
    item = await catalog_service.update_catalog_item(
        item_id=item_id,
        item_data=item_data.dict(exclude_unset=True)
    )
    
    # Log admin action
    await admin_log_service.create_log(
        admin_id=current_user["user_id"],
        action="update",
        entity_type="catalog_item",
        entity_id=item_id,
        details=item_data.dict(exclude_unset=True)
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
        raise UnauthorizedException("Only admins can access this endpoint")
    
    catalog_service = AdminCatalogService(db)
    admin_log_service = AdminLogService(db)
    
    # Delete catalog item
    await catalog_service.delete_catalog_item(item_id)
    
    # Log admin action
    await admin_log_service.create_log(
        admin_id=current_user["user_id"],
        action="delete",
        entity_type="catalog_item",
        entity_id=item_id
    )
    
    return None
