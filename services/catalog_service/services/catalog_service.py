from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_, func
from typing import Optional, List, Dict, Any, Tuple

from services.catalog_service.models.catalog import CatalogItem
from services.catalog_service.models.category import Category
from common.exceptions.http_exceptions import (
    ResourceNotFoundException,
    DatabaseException,
    ValidationException
)


class CatalogService:
    """
    Service for catalog operations
    """
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_catalog_item(
        self,
        name: str,
        category_id: int,
        description: Optional[str] = None,
        brand: Optional[str] = None,
        model: Optional[str] = None,
        image_url: Optional[str] = None,
        specifications: Optional[Dict[str, Any]] = None
    ) -> CatalogItem:
        """
        Create a new catalog item
        """
        # Check if category exists
        category_query = select(Category).where(Category.id == category_id)
        category_result = await self.db.execute(category_query)
        category = category_result.scalars().first()
        
        if not category:
            raise ValidationException(f"Category with ID {category_id} not found")
        
        # Create new catalog item
        catalog_item = CatalogItem(
            name=name,
            description=description,
            category_id=category_id,
            brand=brand,
            model=model,
            image_url=image_url,
            specifications=specifications
        )
        
        try:
            self.db.add(catalog_item)
            await self.db.flush()
            await self.db.refresh(catalog_item)
            return catalog_item
        except IntegrityError as e:
            await self.db.rollback()
            raise DatabaseException(f"Error creating catalog item: {str(e)}")
    
    async def get_catalog_item_by_id(self, item_id: int) -> Optional[CatalogItem]:
        """
        Get catalog item by ID
        """
        query = select(CatalogItem).where(CatalogItem.id == item_id)
        result = await self.db.execute(query)
        item = result.scalars().first()
        
        return item
    
    async def get_catalog_items(
        self,
        query: Optional[str] = None,
        category_id: Optional[int] = None,
        brand: Optional[str] = None,
        skip: int = 0,
        limit: int = 20
    ) -> Tuple[List[CatalogItem], int]:
        """
        Get catalog items with optional filtering
        
        Returns a tuple of (items, total_count)
        """
        # Build query
        stmt = select(CatalogItem)
        
        # Apply filters
        if query:
            stmt = stmt.where(
                or_(
                    CatalogItem.name.ilike(f"%{query}%"),
                    CatalogItem.description.ilike(f"%{query}%")
                )
            )
        
        if category_id:
            stmt = stmt.where(CatalogItem.category_id == category_id)
        
        if brand:
            stmt = stmt.where(CatalogItem.brand.ilike(f"%{brand}%"))
        
        # Get total count
        count_stmt = select(func.count()).select_from(stmt.subquery())
        count_result = await self.db.execute(count_stmt)
        total = count_result.scalar()
        
        # Apply pagination
        stmt = stmt.offset(skip).limit(limit)
        
        # Execute query
        result = await self.db.execute(stmt)
        items = result.scalars().all()
        
        return list(items), total
    
    async def search_catalog_items(
        self,
        query: str,
        skip: int = 0,
        limit: int = 20
    ) -> Tuple[List[CatalogItem], int]:
        """
        Search catalog items by name, description, brand, or model
        
        Returns a tuple of (items, total_count)
        """
        # Build query
        stmt = select(CatalogItem).where(
            or_(
                CatalogItem.name.ilike(f"%{query}%"),
                CatalogItem.description.ilike(f"%{query}%"),
                CatalogItem.brand.ilike(f"%{query}%"),
                CatalogItem.model.ilike(f"%{query}%")
            )
        )
        
        # Get total count
        count_stmt = select(func.count()).select_from(stmt.subquery())
        count_result = await self.db.execute(count_stmt)
        total = count_result.scalar()
        
        # Apply pagination
        stmt = stmt.offset(skip).limit(limit)
        
        # Execute query
        result = await self.db.execute(stmt)
        items = result.scalars().all()
        
        return list(items), total
    
    async def update_catalog_item(
        self,
        item_id: int,
        item_data: Dict[str, Any]
    ) -> CatalogItem:
        """
        Update catalog item data
        """
        item = await self.get_catalog_item_by_id(item_id)
        if not item:
            raise ResourceNotFoundException(f"Catalog item with ID {item_id} not found")
        
        # Check if category_id is being updated and exists
        if "category_id" in item_data and item_data["category_id"] != item.category_id:
            category_query = select(Category).where(Category.id == item_data["category_id"])
            category_result = await self.db.execute(category_query)
            category = category_result.scalars().first()
            
            if not category:
                raise ValidationException(f"Category with ID {item_data['category_id']} not found")
        
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
            raise DatabaseException(f"Error updating catalog item: {str(e)}")
    
    async def delete_catalog_item(self, item_id: int) -> bool:
        """
        Delete catalog item
        """
        item = await self.get_catalog_item_by_id(item_id)
        if not item:
            raise ResourceNotFoundException(f"Catalog item with ID {item_id} not found")
        
        try:
            await self.db.delete(item)
            await self.db.flush()
            return True
        except Exception as e:
            await self.db.rollback()
            raise DatabaseException(f"Error deleting catalog item: {str(e)}")
