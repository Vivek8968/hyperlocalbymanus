from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, and_, or_
from typing import Optional, List, Dict, Any, Tuple
from datetime import datetime

from models.admin_log import AdminLog
from schemas.admin_log import AdminLogFilter
from common.exceptions.http_exceptions import (
    ResourceNotFoundException,
    DatabaseException,
    ValidationException
)


class AdminLogService:
    """
    Service for admin log operations
    """
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_log(
        self,
        admin_id: int,
        action: str,
        entity_type: str,
        entity_id: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None
    ) -> AdminLog:
        """
        Create a new admin log entry
        """
        # Create new log
        log = AdminLog(
            admin_id=admin_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            details=details
        )
        
        try:
            self.db.add(log)
            await self.db.flush()
            await self.db.refresh(log)
            return log
        except IntegrityError as e:
            await self.db.rollback()
            raise DatabaseException(f"Error creating admin log: {str(e)}")
    
    async def get_log_by_id(self, log_id: int) -> Optional[AdminLog]:
        """
        Get admin log by ID
        """
        query = select(AdminLog).where(AdminLog.id == log_id)
        result = await self.db.execute(query)
        log = result.scalars().first()
        
        return log
    
    async def get_logs(
        self,
        log_filter: AdminLogFilter,
        skip: int = 0,
        limit: int = 20
    ) -> Tuple[List[AdminLog], int]:
        """
        Get admin logs with filtering
        
        Returns a tuple of (logs, total_count)
        """
        # Build query
        query = select(AdminLog)
        
        # Apply filters
        if log_filter.admin_id:
            query = query.where(AdminLog.admin_id == log_filter.admin_id)
        
        if log_filter.action:
            query = query.where(AdminLog.action == log_filter.action)
        
        if log_filter.entity_type:
            query = query.where(AdminLog.entity_type == log_filter.entity_type)
        
        if log_filter.entity_id:
            query = query.where(AdminLog.entity_id == log_filter.entity_id)
        
        if log_filter.start_date:
            query = query.where(AdminLog.created_at >= log_filter.start_date)
        
        if log_filter.end_date:
            query = query.where(AdminLog.created_at <= log_filter.end_date)
        
        # Order by created_at descending
        query = query.order_by(AdminLog.created_at.desc())
        
        # Get total count
        count_query = select(func.count()).select_from(query.subquery())
        count_result = await self.db.execute(count_query)
        total = count_result.scalar()
        
        # Apply pagination
        query = query.offset(skip).limit(limit)
        
        # Execute query
        result = await self.db.execute(query)
        logs = result.scalars().all()
        
        return list(logs), total
    
    async def get_recent_logs(self, limit: int = 10) -> List[AdminLog]:
        """
        Get recent admin logs
        """
        query = select(AdminLog).order_by(AdminLog.created_at.desc()).limit(limit)
        result = await self.db.execute(query)
        logs = result.scalars().all()
        
        return list(logs)
    
    async def get_entity_count(self, table_name: str) -> int:
        """
        Get count of entities in a table
        """
        query = f"SELECT COUNT(*) FROM {table_name}"
        result = await self.db.execute(query)
        count = result.scalar()
        
        return count
    
    async def get_activity_stats(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> Dict[str, Any]:
        """
        Get activity statistics for a time period
        """
        # Get action counts
        action_query = select(
            AdminLog.action,
            func.count().label("count")
        ).where(
            and_(
                AdminLog.created_at >= start_date,
                AdminLog.created_at <= end_date
            )
        ).group_by(AdminLog.action)
        
        action_result = await self.db.execute(action_query)
        action_counts = {row[0]: row[1] for row in action_result}
        
        # Get entity type counts
        entity_query = select(
            AdminLog.entity_type,
            func.count().label("count")
        ).where(
            and_(
                AdminLog.created_at >= start_date,
                AdminLog.created_at <= end_date
            )
        ).group_by(AdminLog.entity_type)
        
        entity_result = await self.db.execute(entity_query)
        entity_counts = {row[0]: row[1] for row in entity_result}
        
        # Get admin counts
        admin_query = select(
            AdminLog.admin_id,
            func.count().label("count")
        ).where(
            and_(
                AdminLog.created_at >= start_date,
                AdminLog.created_at <= end_date
            )
        ).group_by(AdminLog.admin_id)
        
        admin_result = await self.db.execute(admin_query)
        admin_counts = {str(row[0]): row[1] for row in admin_result}
        
        return {
            "actions": action_counts,
            "entities": entity_counts,
            "admins": admin_counts,
            "period": {
                "start": start_date,
                "end": end_date
            }
        }
