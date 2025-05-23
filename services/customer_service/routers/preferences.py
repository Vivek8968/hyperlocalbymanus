from fastapi import APIRouter, Depends, HTTPException, status
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

# Import schemas and services
from services.customer_service.schemas.preference import PreferenceCreate, PreferenceUpdate, PreferenceResponse
from services.customer_service.services.preference_service import PreferenceService

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.post("", response_model=PreferenceResponse, status_code=status.HTTP_201_CREATED)
async def create_preference(
    preference_data: PreferenceCreate,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Create or update customer preferences
    """
    preference_service = PreferenceService(db)
    
    # Check if user already has preferences
    existing_preference = await preference_service.get_preference_by_user_id(current_user["user_id"])
    
    if existing_preference:
        # Update existing preferences
        updated_preference = await preference_service.update_preference(
            preference_id=existing_preference.id,
            preference_data=preference_data.dict(exclude_unset=True)
        )
        return updated_preference
    
    # Create new preferences
    preference = await preference_service.create_preference(
        user_id=current_user["user_id"],
        **preference_data.dict()
    )
    
    return preference

@router.get("", response_model=PreferenceResponse)
async def get_preference(
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get customer preferences
    """
    preference_service = PreferenceService(db)
    preference = await preference_service.get_preference_by_user_id(current_user["user_id"])
    
    if not preference:
        # Create default preferences if not exists
        preference = await preference_service.create_preference(
            user_id=current_user["user_id"],
            default_latitude=None,
            default_longitude=None,
            search_radius=5.0
        )
    
    return preference

@router.put("", response_model=PreferenceResponse)
async def update_preference(
    preference_data: PreferenceUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update customer preferences
    """
    preference_service = PreferenceService(db)
    preference = await preference_service.get_preference_by_user_id(current_user["user_id"])
    
    if not preference:
        # Create preferences if not exists
        preference = await preference_service.create_preference(
            user_id=current_user["user_id"],
            **preference_data.dict(exclude_unset=True)
        )
        return preference
    
    # Update existing preferences
    updated_preference = await preference_service.update_preference(
        preference_id=preference.id,
        preference_data=preference_data.dict(exclude_unset=True)
    )
    
    return updated_preference
