from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from typing import Optional, List, Dict, Any, Tuple

from services.catalog_service.models.category import Category
from common.exceptions.http_exceptions import (
    ResourceNotFoundException,
    DatabaseException,
    ValidationException
)


class CategoryService:
    """
    Service for category operations
    """
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_category(
        self,
        name: str,
        description: Optional[str] = None
    ) -> Category:
        """
        Create a new category
        """
        # Check if category with name already exists
        existing_category = await self.get_category_by_name(name)
        if existing_category:
            raise ValidationException(f"Category with name '{name}' already exists")
        
        # Create new category
        category = Category(
            name=name,
            description=description
        )
        
        try:
            self.db.add(category)
            await self.db.flush()
            await self.db.refresh(category)
            return category
        except IntegrityError as e:
            await self.db.rollback()
            raise DatabaseException(f"Error creating category: {str(e)}")
    
    async def get_category_by_id(self, category_id: int) -> Optional[Category]:
        """
        Get category by ID
        """
        query = select(Category).where(Category.id == category_id)
        result = await self.db.execute(query)
        category = result.scalars().first()
        
        return category
    
    async def get_category_by_name(self, name: str) -> Optional[Category]:
        """
        Get category by name
        """
        query = select(Category).where(Category.name == name)
        result = await self.db.execute(query)
        category = result.scalars().first()
        
        return category
    
    async def update_category(
        self,
        category_id: int,
        category_data: Dict[str, Any]
    ) -> Category:
        """
        Update category data
        """
        category = await self.get_category_by_id(category_id)
        if not category:
            raise ResourceNotFoundException(f"Category with ID {category_id} not found")
        
        # Check if name is being updated and already exists
        if "name" in category_data and category_data["name"] != category.name:
            existing_category = await self.get_category_by_name(category_data["name"])
            if existing_category:
                raise ValidationException(f"Category with name '{category_data['name']}' already exists")
        
        # Update category attributes
        for key, value in category_data.items():
            if hasattr(category, key) and value is not None:
                setattr(category, key, value)
        
        try:
            await self.db.flush()
            await self.db.refresh(category)
            return category
        except IntegrityError as e:
            await self.db.rollback()
            raise DatabaseException(f"Error updating category: {str(e)}")
    
    async def delete_category(self, category_id: int) -> bool:
        """
        Delete category
        """
        category = await self.get_category_by_id(category_id)
        if not category:
            raise ResourceNotFoundException(f"Category with ID {category_id} not found")
        
        try:
            await self.db.delete(category)
            await self.db.flush()
            return True
        except Exception as e:
            await self.db.rollback()
            raise DatabaseException(f"Error deleting category: {str(e)}")
    
    async def get_all_categories(self, skip: int = 0, limit: int = 100) -> List[Category]:
        """
        Get all categories with pagination
        """
        query = select(Category).offset(skip).limit(limit)
        result = await self.db.execute(query)
        categories = result.scalars().all()
        
        return list(categories)
