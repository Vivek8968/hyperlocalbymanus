from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from typing import Optional, List, Dict, Any

from models.shop import Shop
from common.exceptions.http_exceptions import (
    ResourceNotFoundException,
    DatabaseException,
    ValidationException
)


class ShopService:
    """
    Service for shop operations
    """
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_shop(
        self,
        user_id: int,
        name: str,
        latitude: float,
        longitude: float,
        description: Optional[str] = None,
        whatsapp_number: Optional[str] = None,
        address: Optional[str] = None,
        image_url: Optional[str] = None,
        banner_url: Optional[str] = None
    ) -> Shop:
        """
        Create a new shop
        """
        # Check if user already has a shop
        existing_shop = await self.get_shop_by_user_id(user_id)
        if existing_shop:
            return existing_shop
        
        # Create new shop
        shop = Shop(
            user_id=user_id,
            name=name,
            description=description,
            whatsapp_number=whatsapp_number,
            address=address,
            latitude=latitude,
            longitude=longitude,
            image_url=image_url,
            banner_url=banner_url
        )
        
        try:
            self.db.add(shop)
            await self.db.flush()
            await self.db.refresh(shop)
            return shop
        except IntegrityError as e:
            await self.db.rollback()
            raise DatabaseException(f"Error creating shop: {str(e)}")
    
    async def get_shop_by_id(self, shop_id: int) -> Optional[Shop]:
        """
        Get shop by ID
        """
        query = select(Shop).where(Shop.id == shop_id)
        result = await self.db.execute(query)
        shop = result.scalars().first()
        
        return shop
    
    async def get_shop_by_user_id(self, user_id: int) -> Optional[Shop]:
        """
        Get shop by user ID
        """
        query = select(Shop).where(Shop.user_id == user_id)
        result = await self.db.execute(query)
        shop = result.scalars().first()
        
        return shop
    
    async def update_shop(self, shop_id: int, shop_data: Dict[str, Any]) -> Shop:
        """
        Update shop data
        """
        shop = await self.get_shop_by_id(shop_id)
        if not shop:
            raise ResourceNotFoundException(f"Shop with ID {shop_id} not found")
        
        # Update shop attributes
        for key, value in shop_data.items():
            if hasattr(shop, key) and value is not None:
                setattr(shop, key, value)
        
        try:
            await self.db.flush()
            await self.db.refresh(shop)
            return shop
        except IntegrityError as e:
            await self.db.rollback()
            raise DatabaseException(f"Error updating shop: {str(e)}")
    
    async def delete_shop(self, shop_id: int) -> bool:
        """
        Delete shop
        """
        shop = await self.get_shop_by_id(shop_id)
        if not shop:
            raise ResourceNotFoundException(f"Shop with ID {shop_id} not found")
        
        try:
            await self.db.delete(shop)
            await self.db.flush()
            return True
        except Exception as e:
            await self.db.rollback()
            raise DatabaseException(f"Error deleting shop: {str(e)}")
    
    async def get_all_shops(self, skip: int = 0, limit: int = 100) -> List[Shop]:
        """
        Get all shops with pagination
        """
        query = select(Shop).offset(skip).limit(limit)
        result = await self.db.execute(query)
        shops = result.scalars().all()
        
        return list(shops)
    
    async def get_shops_by_location(
        self,
        latitude: float,
        longitude: float,
        radius_km: float,
        skip: int = 0,
        limit: int = 100
    ) -> List[Shop]:
        """
        Get shops near a location
        
        Note: This is a simplified implementation. In a real-world scenario,
        you would use a spatial database like PostGIS for efficient geo queries.
        """
        # Get all shops
        shops = await self.get_all_shops(skip=skip, limit=limit)
        
        # Filter shops by distance (this would be done at the database level in a real implementation)
        # For now, we'll return all shops and let the geo service handle filtering
        return shops
