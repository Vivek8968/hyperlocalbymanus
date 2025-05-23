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
from services.admin_service.schemas.user import UserAdminUpdate, UserAdminResponse, UserAdminSearchResponse
from services.admin_service.services.user_service import AdminUserService
from services.admin_service.services.admin_log_service import AdminLogService

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.get("", response_model=UserAdminSearchResponse)
async def get_users(
    query: Optional[str] = None,
    role: Optional[str] = None,
    is_active: Optional[bool] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all users with optional filtering (admin only)
    """
    # Check if user is admin
    if current_user.get("role") != "admin":
        raise UnauthorizedException("Only admins can access this endpoint")
    
    # Calculate offset for pagination
    offset = (page - 1) * page_size
    
    user_service = AdminUserService(db)
    users, total = await user_service.get_users(
        query=query,
        role=role,
        is_active=is_active,
        skip=offset,
        limit=page_size
    )
    
    return {
        "users": users,
        "total": total,
        "page": page,
        "page_size": page_size
    }

@router.get("/{user_id}", response_model=UserAdminResponse)
async def get_user(
    user_id: int = Path(..., gt=0),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get user by ID (admin only)
    """
    # Check if user is admin
    if current_user.get("role") != "admin":
        raise UnauthorizedException("Only admins can access this endpoint")
    
    user_service = AdminUserService(db)
    user = await user_service.get_user_by_id(user_id)
    
    if not user:
        raise ResourceNotFoundException(f"User with ID {user_id} not found")
    
    return user

@router.put("/{user_id}", response_model=UserAdminResponse)
async def update_user(
    user_data: UserAdminUpdate,
    user_id: int = Path(..., gt=0),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update user (admin only)
    """
    # Check if user is admin
    if current_user.get("role") != "admin":
        raise UnauthorizedException("Only admins can access this endpoint")
    
    user_service = AdminUserService(db)
    admin_log_service = AdminLogService(db)
    
    # Update user
    user = await user_service.update_user(
        user_id=user_id,
        user_data=user_data.dict(exclude_unset=True)
    )
    
    # Log admin action
    await admin_log_service.create_log(
        admin_id=current_user["user_id"],
        action="update",
        entity_type="user",
        entity_id=user_id,
        details=user_data.dict(exclude_unset=True)
    )
    
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int = Path(..., gt=0),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete user (admin only)
    """
    # Check if user is admin
    if current_user.get("role") != "admin":
        raise UnauthorizedException("Only admins can access this endpoint")
    
    user_service = AdminUserService(db)
    admin_log_service = AdminLogService(db)
    
    # Delete user
    await user_service.delete_user(user_id)
    
    # Log admin action
    await admin_log_service.create_log(
        admin_id=current_user["user_id"],
        action="delete",
        entity_type="user",
        entity_id=user_id
    )
    
    return None
