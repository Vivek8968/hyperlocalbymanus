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
from services.admin_service.schemas.shop import ShopAdminUpdate, ShopAdminResponse, ShopAdminSearchResponse
from services.admin_service.services.shop_service import AdminShopService
from services.admin_service.services.admin_log_service import AdminLogService

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.get("", response_model=ShopAdminSearchResponse)
async def get_shops(
    query: Optional[str] = None,
    is_active: Optional[bool] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all shops with optional filtering (admin only)
    """
    # Check if user is admin
    if current_user.get("role") != "admin":
        raise UnauthorizedException("Only admins can access this endpoint")
    
    # Calculate offset for pagination
    offset = (page - 1) * page_size
    
    shop_service = AdminShopService(db)
    shops, total = await shop_service.get_shops(
        query=query,
        is_active=is_active,
        skip=offset,
        limit=page_size
    )
    
    return {
        "shops": shops,
        "total": total,
        "page": page,
        "page_size": page_size
    }

@router.get("/{shop_id}", response_model=ShopAdminResponse)
async def get_shop(
    shop_id: int = Path(..., gt=0),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get shop by ID (admin only)
    """
    # Check if user is admin
    if current_user.get("role") != "admin":
        raise UnauthorizedException("Only admins can access this endpoint")
    
    shop_service = AdminShopService(db)
    shop = await shop_service.get_shop_by_id(shop_id)
    
    if not shop:
        raise ResourceNotFoundException(f"Shop with ID {shop_id} not found")
    
    return shop

@router.put("/{shop_id}", response_model=ShopAdminResponse)
async def update_shop(
    shop_data: ShopAdminUpdate,
    shop_id: int = Path(..., gt=0),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update shop (admin only)
    """
    # Check if user is admin
    if current_user.get("role") != "admin":
        raise UnauthorizedException("Only admins can access this endpoint")
    
    shop_service = AdminShopService(db)
    admin_log_service = AdminLogService(db)
    
    # Update shop
    shop = await shop_service.update_shop(
        shop_id=shop_id,
        shop_data=shop_data.dict(exclude_unset=True)
    )
    
    # Log admin action
    await admin_log_service.create_log(
        admin_id=current_user["user_id"],
        action="update",
        entity_type="shop",
        entity_id=shop_id,
        details=shop_data.dict(exclude_unset=True)
    )
    
    return shop

@router.delete("/{shop_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_shop(
    shop_id: int = Path(..., gt=0),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete shop (admin only)
    """
    # Check if user is admin
    if current_user.get("role") != "admin":
        raise UnauthorizedException("Only admins can access this endpoint")
    
    shop_service = AdminShopService(db)
    admin_log_service = AdminLogService(db)
    
    # Delete shop
    await shop_service.delete_shop(shop_id)
    
    # Log admin action
    await admin_log_service.create_log(
        admin_id=current_user["user_id"],
        action="delete",
        entity_type="shop",
        entity_id=shop_id
    )
    
    return None
