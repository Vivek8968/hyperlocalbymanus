from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, and_, or_
from typing import Optional, List, Dict, Any, Tuple

# Import shop model from seller service
# In a real implementation, this would be an API call to the seller service
# For simplicity, we're simulating direct database access
class AdminShopService:
    """
    Service for admin shop operations
    """
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_shops(
        self,
        query: Optional[str] = None,
        is_active: Optional[bool] = None,
        skip: int = 0,
        limit: int = 20
    ) -> Tuple[List[Dict[str, Any]], int]:
        """
        Get shops with filtering
        
        Returns a tuple of (shops, total_count)
        """
        # Build query
        sql_query = "SELECT * FROM shops WHERE 1=1"
        
        # Apply filters
        if query:
            sql_query += f" AND (name LIKE '%{query}%' OR description LIKE '%{query}%' OR address LIKE '%{query}%')"
        
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
        shops_data = result.mappings().all()
        
        # Convert to list of dicts
        shops = [dict(shop) for shop in shops_data]
        
        return shops, total
    
    async def get_shop_by_id(self, shop_id: int) -> Optional[Dict[str, Any]]:
        """
        Get shop by ID
        """
        query = f"SELECT * FROM shops WHERE id = {shop_id}"
        result = await self.db.execute(query)
        shop_data = result.mappings().first()
        
        if shop_data:
            return dict(shop_data)
        
        return None
    
    async def update_shop(
        self,
        shop_id: int,
        shop_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update shop data
        """
        # Get shop
        shop = await self.get_shop_by_id(shop_id)
        if not shop:
            raise Exception(f"Shop with ID {shop_id} not found")
        
        # Build update query
        update_parts = []
        for key, value in shop_data.items():
            if key in ["name", "description", "whatsapp_number", "address", "latitude", "longitude", "image_url", "banner_url", "is_active"]:
                if value is None:
                    update_parts.append(f"{key} = NULL")
                elif isinstance(value, bool):
                    update_parts.append(f"{key} = {1 if value else 0}")
                elif isinstance(value, (int, float)):
                    update_parts.append(f"{key} = {value}")
                else:
                    update_parts.append(f"{key} = '{value}'")
        
        if not update_parts:
            return shop
        
        # Execute update
        update_query = f"UPDATE shops SET {', '.join(update_parts)} WHERE id = {shop_id}"
        await self.db.execute(update_query)
        
        # Get updated shop
        updated_shop = await self.get_shop_by_id(shop_id)
        
        return updated_shop
    
    async def delete_shop(self, shop_id: int) -> bool:
        """
        Delete shop
        """
        # Get shop
        shop = await self.get_shop_by_id(shop_id)
        if not shop:
            raise Exception(f"Shop with ID {shop_id} not found")
        
        # Execute delete
        delete_query = f"DELETE FROM shops WHERE id = {shop_id}"
        await self.db.execute(delete_query)
        
        return True
