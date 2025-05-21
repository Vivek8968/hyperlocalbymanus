from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, func
import sys
import os

# Add parent directory to path to import common modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.database.session import Base


class CustomerPreference(Base):
    """
    Customer preference model for storing default location and search radius
    """
    __tablename__ = "customer_preferences"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True, nullable=False, index=True)
    default_latitude = Column(Float, nullable=True)
    default_longitude = Column(Float, nullable=True)
    search_radius = Column(Float, default=5.0, nullable=False)  # Default 5 km radius
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<CustomerPreference {self.id}: user_id={self.user_id}>"
