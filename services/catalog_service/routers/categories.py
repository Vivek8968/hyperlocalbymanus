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
from services.catalog_service.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from services.catalog_service.services.category_service import CategoryService

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.post("", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_data: CategoryCreate,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new category (admin only)
    """
    # Check if user is admin
    if current_user.get("role") != "admin":
        raise UnauthorizedException("Only admins can create categories")
    
    category_service = CategoryService(db)
    category = await category_service.create_category(**category_data.dict())
    
    return category

@router.get("", response_model=List[CategoryResponse])
async def get_categories(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all categories
    """
    category_service = CategoryService(db)
    categories = await category_service.get_all_categories(skip=skip, limit=limit)
    
    return categories

@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(
    category_id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_db)
):
    """
    Get category by ID
    """
    category_service = CategoryService(db)
    category = await category_service.get_category_by_id(category_id)
    
    if not category:
        raise ResourceNotFoundException(f"Category with ID {category_id} not found")
    
    return category

@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_data: CategoryUpdate,
    category_id: int = Path(..., gt=0),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update category (admin only)
    """
    # Check if user is admin
    if current_user.get("role") != "admin":
        raise UnauthorizedException("Only admins can update categories")
    
    category_service = CategoryService(db)
    category = await category_service.update_category(
        category_id=category_id,
        category_data=category_data.dict(exclude_unset=True)
    )
    
    return category

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int = Path(..., gt=0),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete category (admin only)
    """
    # Check if user is admin
    if current_user.get("role") != "admin":
        raise UnauthorizedException("Only admins can delete categories")
    
    category_service = CategoryService(db)
    await category_service.delete_category(category_id)
    
    return None
