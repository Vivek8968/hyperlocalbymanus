from fastapi import APIRouter, Depends, HTTPException, status, Path, Query
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any, Optional
import uuid

# Import common modules
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.database.session import get_db
from common.auth.jwt import get_current_user
from common.exceptions.http_exceptions import ResourceNotFoundException, UnauthorizedException
from common.utils.s3 import S3Service

# Import schemas and services
from schemas.shop import ShopCreate, ShopUpdate, ShopResponse, ImageUploadResponse
from services.shop_service import ShopService

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.post("", response_model=ShopResponse, status_code=status.HTTP_201_CREATED)
async def create_shop(
    shop_data: ShopCreate,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Register a new shop for the current seller
    """
    shop_service = ShopService(db)
    
    # Check if user already has a shop
    existing_shop = await shop_service.get_shop_by_user_id(current_user["user_id"])
    if existing_shop:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already has a registered shop"
        )
    
    # Create shop
    shop = await shop_service.create_shop(
        user_id=current_user["user_id"],
        **shop_data.dict()
    )
    
    return shop

@router.get("/me", response_model=ShopResponse)
async def get_my_shop(
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get current seller's shop details
    """
    shop_service = ShopService(db)
    shop = await shop_service.get_shop_by_user_id(current_user["user_id"])
    
    if not shop:
        raise ResourceNotFoundException("Shop not found for current user")
    
    return shop

@router.put("/me", response_model=ShopResponse)
async def update_my_shop(
    shop_data: ShopUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update current seller's shop details
    """
    shop_service = ShopService(db)
    shop = await shop_service.get_shop_by_user_id(current_user["user_id"])
    
    if not shop:
        raise ResourceNotFoundException("Shop not found for current user")
    
    updated_shop = await shop_service.update_shop(
        shop_id=shop.id,
        shop_data=shop_data.dict(exclude_unset=True)
    )
    
    return updated_shop

@router.post("/me/images/upload", response_model=ImageUploadResponse)
async def upload_shop_image(
    field_name: str = Query(..., description="Field name for the image (image_url or banner_url)"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Generate presigned URL for uploading shop images to S3
    """
    if field_name not in ["image_url", "banner_url"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid field name. Must be 'image_url' or 'banner_url'"
        )
    
    shop_service = ShopService(db)
    shop = await shop_service.get_shop_by_user_id(current_user["user_id"])
    
    if not shop:
        raise ResourceNotFoundException("Shop not found for current user")
    
    # Generate unique object name
    object_name = f"shops/{shop.id}/{field_name}/{uuid.uuid4()}"
    
    # Get S3 service
    s3_service = S3Service()
    
    # Generate presigned URL
    presigned_url = await s3_service.generate_presigned_url(object_name)
    
    # Get object URL
    image_url = await s3_service.get_object_url(object_name)
    
    # Update shop with new image URL
    shop_data = {field_name: image_url}
    await shop_service.update_shop(shop.id, shop_data)
    
    return {
        "presigned_url": presigned_url,
        "image_url": image_url,
        "field_name": field_name
    }

@router.get("/{shop_id}", response_model=ShopResponse)
async def get_shop_by_id(
    shop_id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_db)
):
    """
    Get shop details by ID
    """
    shop_service = ShopService(db)
    shop = await shop_service.get_shop_by_id(shop_id)
    
    if not shop:
        raise ResourceNotFoundException(f"Shop with ID {shop_id} not found")
    
    return shop
