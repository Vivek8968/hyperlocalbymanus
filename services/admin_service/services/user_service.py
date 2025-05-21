from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, and_, or_
from typing import Optional, List, Dict, Any, Tuple

# Import user model from user service
# In a real implementation, this would be an API call to the user service
# For simplicity, we're simulating direct database access
class AdminUserService:
    """
    Service for admin user operations
    """
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_users(
        self,
        query: Optional[str] = None,
        role: Optional[str] = None,
        is_active: Optional[bool] = None,
        skip: int = 0,
        limit: int = 20
    ) -> Tuple[List[Dict[str, Any]], int]:
        """
        Get users with filtering
        
        Returns a tuple of (users, total_count)
        """
        # Build query
        sql_query = "SELECT * FROM users WHERE 1=1"
        
        # Apply filters
        if query:
            sql_query += f" AND (email LIKE '%{query}%' OR full_name LIKE '%{query}%' OR phone LIKE '%{query}%')"
        
        if role:
            sql_query += f" AND role = '{role}'"
        
        if is_active is not None:
            sql_query += f" AND is_active = {1 if is_active else 0}"
        
        # Get total count
        count_query = f"SELECT COUNT(*) FROM ({sql_query}) as count_query"
        count_result = await self.db.execute(count_query)
        total = count_result.scalar()
        
        # Apply pagination
        sql_query += f" ORDER BY created_at DESC LIMIT {limit} OFFSET {skip}"
        
        # Execute query
        result = await self.db.execute(sql_query)
        users_data = result.mappings().all()
        
        # Convert to list of dicts
        users = [dict(user) for user in users_data]
        
        return users, total
    
    async def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Get user by ID
        """
        query = f"SELECT * FROM users WHERE id = {user_id}"
        result = await self.db.execute(query)
        user_data = result.mappings().first()
        
        if user_data:
            return dict(user_data)
        
        return None
    
    async def update_user(
        self,
        user_id: int,
        user_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update user data
        """
        # Get user
        user = await self.get_user_by_id(user_id)
        if not user:
            raise Exception(f"User with ID {user_id} not found")
        
        # Build update query
        update_parts = []
        for key, value in user_data.items():
            if key in ["email", "phone", "full_name", "role", "is_active"]:
                if value is None:
                    update_parts.append(f"{key} = NULL")
                elif isinstance(value, bool):
                    update_parts.append(f"{key} = {1 if value else 0}")
                elif isinstance(value, (int, float)):
                    update_parts.append(f"{key} = {value}")
                else:
                    update_parts.append(f"{key} = '{value}'")
        
        if not update_parts:
            return user
        
        # Execute update
        update_query = f"UPDATE users SET {', '.join(update_parts)} WHERE id = {user_id}"
        await self.db.execute(update_query)
        
        # Get updated user
        updated_user = await self.get_user_by_id(user_id)
        
        return updated_user
    
    async def delete_user(self, user_id: int) -> bool:
        """
        Delete user
        """
        # Get user
        user = await self.get_user_by_id(user_id)
        if not user:
            raise Exception(f"User with ID {user_id} not found")
        
        # Execute delete
        delete_query = f"DELETE FROM users WHERE id = {user_id}"
        await self.db.execute(delete_query)
        
        return True
