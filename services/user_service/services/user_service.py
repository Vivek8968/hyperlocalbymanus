from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from typing import Optional, List, Dict, Any

from models.user import User, UserRole
from common.exceptions.http_exceptions import (
    ResourceNotFoundException,
    DatabaseException,
    ValidationException
)


class UserService:
    """
    Service for user operations
    """
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_user(
        self,
        firebase_uid: str,
        name: str,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        role: UserRole = UserRole.CUSTOMER
    ) -> User:
        """
        Create a new user
        """
        # Check if user with firebase_uid already exists
        existing_user = await self.get_user_by_firebase_uid(firebase_uid)
        if existing_user:
            return existing_user
        
        # Create new user
        user = User(
            firebase_uid=firebase_uid,
            name=name,
            email=email,
            phone=phone,
            role=role
        )
        
        try:
            self.db.add(user)
            await self.db.flush()
            await self.db.refresh(user)
            return user
        except IntegrityError as e:
            await self.db.rollback()
            if "unique constraint" in str(e).lower():
                if "email" in str(e).lower():
                    raise ValidationException("Email already registered")
                elif "phone" in str(e).lower():
                    raise ValidationException("Phone number already registered")
            raise DatabaseException(f"Error creating user: {str(e)}")
    
    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Get user by ID
        """
        query = select(User).where(User.id == user_id)
        result = await self.db.execute(query)
        user = result.scalars().first()
        
        return user
    
    async def get_user_by_firebase_uid(self, firebase_uid: str) -> Optional[User]:
        """
        Get user by Firebase UID
        """
        query = select(User).where(User.firebase_uid == firebase_uid)
        result = await self.db.execute(query)
        user = result.scalars().first()
        
        return user
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email
        """
        query = select(User).where(User.email == email)
        result = await self.db.execute(query)
        user = result.scalars().first()
        
        return user
    
    async def get_user_by_phone(self, phone: str) -> Optional[User]:
        """
        Get user by phone
        """
        query = select(User).where(User.phone == phone)
        result = await self.db.execute(query)
        user = result.scalars().first()
        
        return user
    
    async def update_user(self, user_id: int, user_data: Dict[str, Any]) -> User:
        """
        Update user data
        """
        user = await self.get_user_by_id(user_id)
        if not user:
            raise ResourceNotFoundException(f"User with ID {user_id} not found")
        
        # Update user attributes
        for key, value in user_data.items():
            if hasattr(user, key) and value is not None:
                setattr(user, key, value)
        
        try:
            await self.db.flush()
            await self.db.refresh(user)
            return user
        except IntegrityError as e:
            await self.db.rollback()
            if "unique constraint" in str(e).lower():
                if "email" in str(e).lower():
                    raise ValidationException("Email already registered")
                elif "phone" in str(e).lower():
                    raise ValidationException("Phone number already registered")
            raise DatabaseException(f"Error updating user: {str(e)}")
    
    async def delete_user(self, user_id: int) -> bool:
        """
        Delete user
        """
        user = await self.get_user_by_id(user_id)
        if not user:
            raise ResourceNotFoundException(f"User with ID {user_id} not found")
        
        try:
            await self.db.delete(user)
            await self.db.flush()
            return True
        except Exception as e:
            await self.db.rollback()
            raise DatabaseException(f"Error deleting user: {str(e)}")
    
    async def get_all_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Get all users with pagination
        """
        query = select(User).offset(skip).limit(limit)
        result = await self.db.execute(query)
        users = result.scalars().all()
        
        return list(users)
