from fastapi import APIRouter, Depends, HTTPException, status, Path, Query
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

# Import common modules
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.database.session import get_db
from common.auth.jwt import get_current_user
from common.exceptions.http_exceptions import ResourceNotFoundException, UnauthorizedException

# Import schemas and services
from schemas.admin_log import AdminLogResponse, AdminLogSearchResponse, AdminLogFilter
from services.admin_log_service import AdminLogService

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.get("", response_model=AdminLogSearchResponse)
async def get_logs(
    admin_id: Optional[int] = None,
    action: Optional[str] = None,
    entity_type: Optional[str] = None,
    entity_id: Optional[int] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get admin logs with optional filtering (admin only)
    """
    # Check if user is admin
    if current_user.get("role") != "admin":
        raise UnauthorizedException("Only admins can access this endpoint")
    
    # Calculate offset for pagination
    offset = (page - 1) * page_size
    
    # Create filter
    log_filter = AdminLogFilter(
        admin_id=admin_id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        start_date=start_date,
        end_date=end_date
    )
    
    log_service = AdminLogService(db)
    logs, total = await log_service.get_logs(
        log_filter=log_filter,
        skip=offset,
        limit=page_size
    )
    
    return {
        "logs": logs,
        "total": total,
        "page": page,
        "page_size": page_size
    }

@router.get("/recent", response_model=List[AdminLogResponse])
async def get_recent_logs(
    limit: int = Query(10, ge=1, le=50),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get recent admin logs (admin only)
    """
    # Check if user is admin
    if current_user.get("role") != "admin":
        raise UnauthorizedException("Only admins can access this endpoint")
    
    log_service = AdminLogService(db)
    logs = await log_service.get_recent_logs(limit=limit)
    
    return logs

@router.get("/system", response_model=Dict[str, Any])
async def get_system_stats(
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get system statistics (admin only)
    """
    # Check if user is admin
    if current_user.get("role") != "admin":
        raise UnauthorizedException("Only admins can access this endpoint")
    
    log_service = AdminLogService(db)
    
    # Get stats for last 24 hours
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=1)
    
    # Get counts
    user_count = await log_service.get_entity_count("users")
    shop_count = await log_service.get_entity_count("shops")
    catalog_count = await log_service.get_entity_count("catalog_items")
    
    # Get recent activity
    recent_activity = await log_service.get_activity_stats(start_date, end_date)
    
    return {
        "counts": {
            "users": user_count,
            "shops": shop_count,
            "catalog_items": catalog_count
        },
        "recent_activity": recent_activity,
        "timestamp": end_date
    }

@router.get("/{log_id}", response_model=AdminLogResponse)
async def get_log(
    log_id: int = Path(..., gt=0),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get admin log by ID (admin only)
    """
    # Check if user is admin
    if current_user.get("role") != "admin":
        raise UnauthorizedException("Only admins can access this endpoint")
    
    log_service = AdminLogService(db)
    log = await log_service.get_log_by_id(log_id)
    
    if not log:
        raise ResourceNotFoundException(f"Log with ID {log_id} not found")
    
    return log
