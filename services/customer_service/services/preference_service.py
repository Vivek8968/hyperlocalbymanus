from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from typing import Optional, List, Dict, Any, Tuple

from services.customer_service.models.preference import CustomerPreference
from common.exceptions.http_exceptions import (
    ResourceNotFoundException,
    DatabaseException,
    ValidationException
)


class PreferenceService:
    """
    Service for customer preference operations
    """
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_preference(
        self,
        user_id: int,
        default_latitude: Optional[float] = None,
        default_longitude: Optional[float] = None,
        search_radius: float = 5.0
    ) -> CustomerPreference:
        """
        Create a new customer preference
        """
        # Check if user already has preferences
        existing_preference = await self.get_preference_by_user_id(user_id)
        if existing_preference:
            return existing_preference
        
        # Create new preference
        preference = CustomerPreference(
            user_id=user_id,
            default_latitude=default_latitude,
            default_longitude=default_longitude,
            search_radius=search_radius
        )
        
        try:
            self.db.add(preference)
            await self.db.flush()
            await self.db.refresh(preference)
            return preference
        except IntegrityError as e:
            await self.db.rollback()
            raise DatabaseException(f"Error creating preference: {str(e)}")
    
    async def get_preference_by_id(self, preference_id: int) -> Optional[CustomerPreference]:
        """
        Get preference by ID
        """
        query = select(CustomerPreference).where(CustomerPreference.id == preference_id)
        result = await self.db.execute(query)
        preference = result.scalars().first()
        
        return preference
    
    async def get_preference_by_user_id(self, user_id: int) -> Optional[CustomerPreference]:
        """
        Get preference by user ID
        """
        query = select(CustomerPreference).where(CustomerPreference.user_id == user_id)
        result = await self.db.execute(query)
        preference = result.scalars().first()
        
        return preference
    
    async def update_preference(
        self,
        preference_id: int,
        preference_data: Dict[str, Any]
    ) -> CustomerPreference:
        """
        Update preference data
        """
        preference = await self.get_preference_by_id(preference_id)
        if not preference:
            raise ResourceNotFoundException(f"Preference with ID {preference_id} not found")
        
        # Update preference attributes
        for key, value in preference_data.items():
            if hasattr(preference, key) and value is not None:
                setattr(preference, key, value)
        
        try:
            await self.db.flush()
            await self.db.refresh(preference)
            return preference
        except IntegrityError as e:
            await self.db.rollback()
            raise DatabaseException(f"Error updating preference: {str(e)}")
    
    async def delete_preference(self, preference_id: int) -> bool:
        """
        Delete preference
        """
        preference = await self.get_preference_by_id(preference_id)
        if not preference:
            raise ResourceNotFoundException(f"Preference with ID {preference_id} not found")
        
        try:
            await self.db.delete(preference)
            await self.db.flush()
            return True
        except Exception as e:
            await self.db.rollback()
            raise DatabaseException(f"Error deleting preference: {str(e)}")
