from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, and_, or_
from typing import Optional, List, Dict, Any, Tuple

# Import catalog model from catalog service
# In a real implementation, this would be an API call to the catalog service
# For simplicity, we're simulating direct database access
class AdminCatalogService:
    """
    Service for admin catalog operations
    """
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_catalog_items(
        self,
        query: Optional[str] = None,
        category_id: Optional[int] = None,
        brand: Optional[str] = None,
        skip: int = 0,
        limit: int = 20
    ) -> Tuple[List[Dict[str, Any]], int]:
        """
        Get catalog items with filtering
        
        Returns a tuple of (items, total_count)
        """
        # Build query
        sql_query = "SELECT * FROM catalog_items WHERE 1=1"
        
        # Apply filters
        if query:
            sql_query += f" AND (name LIKE '%{query}%' OR description LIKE '%{query}%')"
        
        if category_id:
            sql_query += f" AND category_id = {category_id}"
        
        if brand:
            sql_query += f" AND brand LIKE '%{brand}%'"
        
        # Get total count
        count_query = f"SELECT COUNT(*) FROM ({sql_query}) as count_query"
        count_result = await self.db.execute(count_query)
        total = count_result.scalar()
        
        # Apply pagination
        sql_query += f" ORDER BY created_at DESC LIMIT {limit} OFFSET {skip}"
        
        # Execute query
        result = await self.db.execute(sql_query)
        items_data = result.mappings().all()
        
        # Convert to list of dicts
        items = [dict(item) for item in items_data]
        
        return items, total
    
    async def get_catalog_item_by_id(self, item_id: int) -> Optional[Dict[str, Any]]:
        """
        Get catalog item by ID
        """
        query = f"SELECT * FROM catalog_items WHERE id = {item_id}"
        result = await self.db.execute(query)
        item_data = result.mappings().first()
        
        if item_data:
            return dict(item_data)
        
        return None
    
    async def update_catalog_item(
        self,
        item_id: int,
        item_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update catalog item data
        """
        # Get catalog item
        item = await self.get_catalog_item_by_id(item_id)
        if not item:
            raise Exception(f"Catalog item with ID {item_id} not found")
        
        # Build update query
        update_parts = []
        for key, value in item_data.items():
            if key in ["name", "description", "category_id", "brand", "model", "image_url", "specifications"]:
                if value is None:
                    update_parts.append(f"{key} = NULL")
                elif isinstance(value, (int, float)):
                    update_parts.append(f"{key} = {value}")
                elif isinstance(value, dict):
                    # Handle JSON data
                    json_str = str(value).replace("'", "\"")
                    update_parts.append(f"{key} = '{json_str}'")
                else:
                    update_parts.append(f"{key} = '{value}'")
        
        if not update_parts:
            return item
        
        # Execute update
        update_query = f"UPDATE catalog_items SET {', '.join(update_parts)} WHERE id = {item_id}"
        await self.db.execute(update_query)
        
        # Get updated catalog item
        updated_item = await self.get_catalog_item_by_id(item_id)
        
        return updated_item
    
    async def delete_catalog_item(self, item_id: int) -> bool:
        """
        Delete catalog item
        """
        # Get catalog item
        item = await self.get_catalog_item_by_id(item_id)
        if not item:
            raise Exception(f"Catalog item with ID {item_id} not found")
        
        # Execute delete
        delete_query = f"DELETE FROM catalog_items WHERE id = {item_id}"
        await self.db.execute(delete_query)
        
        return True
