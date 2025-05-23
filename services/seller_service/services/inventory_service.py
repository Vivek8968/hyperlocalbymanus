from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from typing import Optional, List, Dict, Any

from services.seller_service.models.inventory import ShopInventory
from common.exceptions.http_exceptions import (
    ResourceNotFoundException,
    DatabaseException,
    ValidationException
)


class InventoryService:
    """
    Service for inventory operations
    """
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def add_inventory_item(
        self,
        shop_id: int,
        catalog_item_id: int,
        price: float,
        stock: int
    ) -> ShopInventory:
        """
        Add a product to inventory
        """
        # Check if product already exists in inventory
        existing_item = await self.get_inventory_item_by_shop_and_catalog(
            shop_id=shop_id,
            catalog_item_id=catalog_item_id
        )
        
        if existing_item:
            # Update existing item
            existing_item.price = price
            existing_item.stock = stock
            
            try:
                await self.db.flush()
                await self.db.refresh(existing_item)
                return existing_item
            except IntegrityError as e:
                await self.db.rollback()
                raise DatabaseException(f"Error updating inventory item: {str(e)}")
        
        # Create new inventory item
        inventory_item = ShopInventory(
            shop_id=shop_id,
            catalog_item_id=catalog_item_id,
            price=price,
            stock=stock
        )
        
        try:
            self.db.add(inventory_item)
            await self.db.flush()
            await self.db.refresh(inventory_item)
            return inventory_item
        except IntegrityError as e:
            await self.db.rollback()
            raise DatabaseException(f"Error adding inventory item: {str(e)}")
    
    async def get_inventory_item_by_id(self, item_id: int) -> Optional[ShopInventory]:
        """
        Get inventory item by ID
        """
        query = select(ShopInventory).where(ShopInventory.id == item_id)
        result = await self.db.execute(query)
        item = result.scalars().first()
        
        return item
    
    async def get_inventory_item_by_shop_and_catalog(
        self,
        shop_id: int,
        catalog_item_id: int
    ) -> Optional[ShopInventory]:
        """
        Get inventory item by shop ID and catalog item ID
        """
        query = select(ShopInventory).where(
            ShopInventory.shop_id == shop_id,
            ShopInventory.catalog_item_id == catalog_item_id
        )
        result = await self.db.execute(query)
        item = result.scalars().first()
        
        return item
    
    async def get_inventory_items_by_shop_id(
        self,
        shop_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[ShopInventory]:
        """
        Get all inventory items for a shop
        """
        query = select(ShopInventory).where(
            ShopInventory.shop_id == shop_id
        ).offset(skip).limit(limit)
        
        result = await self.db.execute(query)
        items = result.scalars().all()
        
        return list(items)
    
    async def update_inventory_item(
        self,
        item_id: int,
        item_data: Dict[str, Any]
    ) -> ShopInventory:
        """
        Update inventory item
        """
        item = await self.get_inventory_item_by_id(item_id)
        if not item:
            raise ResourceNotFoundException(f"Inventory item with ID {item_id} not found")
        
        # Update item attributes
        for key, value in item_data.items():
            if hasattr(item, key) and value is not None:
                setattr(item, key, value)
        
        try:
            await self.db.flush()
            await self.db.refresh(item)
            return item
        except IntegrityError as e:
            await self.db.rollback()
            raise DatabaseException(f"Error updating inventory item: {str(e)}")
    
    async def delete_inventory_item(self, item_id: int) -> bool:
        """
        Delete inventory item
        """
        item = await self.get_inventory_item_by_id(item_id)
        if not item:
            raise ResourceNotFoundException(f"Inventory item with ID {item_id} not found")
        
        try:
            await self.db.delete(item)
            await self.db.flush()
            return True
        except Exception as e:
            await self.db.rollback()
            raise DatabaseException(f"Error deleting inventory item: {str(e)}")
