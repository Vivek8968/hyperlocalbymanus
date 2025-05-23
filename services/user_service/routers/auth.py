from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any

# Import common modules
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.database.session import get_db
from common.auth.firebase import verify_firebase_token
from common.auth.jwt import create_access_token, get_current_user
from common.exceptions.http_exceptions import UnauthorizedException

# Import schemas and services
from services.user_service.schemas.user import UserCreate, UserResponse, TokenResponse, FirebaseAuthRequest
from services.user_service.services.user_service import UserService

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Register a new user
    """
    user_service = UserService(db)
    try:
        # Verify Firebase token
        firebase_data = await verify_firebase_token(user_data.firebase_token)
        
        # Create user in database
        user = await user_service.create_user(
            firebase_uid=firebase_data["uid"],
            name=user_data.name,
            email=firebase_data.get("email"),
            phone=firebase_data.get("phone_number"),
            role=user_data.role
        )
        
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error registering user: {str(e)}"
        )

@router.post("/login", response_model=TokenResponse)
async def login(
    auth_request: FirebaseAuthRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Login with Firebase token
    """
    user_service = UserService(db)
    try:
        # Verify Firebase token
        firebase_data = await verify_firebase_token(auth_request.firebase_token)
        
        # Get user from database
        user = await user_service.get_user_by_firebase_uid(firebase_data["uid"])
        if not user:
            raise UnauthorizedException("User not found")
        
        # Create access token
        access_token = create_access_token(
            data={"sub": str(user.id), "role": user.role}
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": user.id,
            "role": user.role
        }
    except Exception as e:
        raise UnauthorizedException(f"Login failed: {str(e)}")

@router.get("/verify-token", response_model=Dict[str, Any])
async def verify_token(current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    Verify JWT token
    """
    return current_user

@router.post("/refresh-token", response_model=TokenResponse)
async def refresh_token(
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Refresh JWT token
    """
    user_service = UserService(db)
    try:
        user = await user_service.get_user_by_id(current_user["user_id"])
        if not user:
            raise UnauthorizedException("User not found")
        
        # Create new access token
        access_token = create_access_token(
            data={"sub": str(user.id), "role": user.role}
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": user.id,
            "role": user.role
        }
    except Exception as e:
        raise UnauthorizedException(f"Token refresh failed: {str(e)}")
