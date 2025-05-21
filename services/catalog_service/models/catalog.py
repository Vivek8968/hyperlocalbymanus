from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime, JSON, func
from sqlalchemy.orm import relationship
import sys
import os

# Add parent directory to path to import common modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.database.session import Base


class CatalogItem(Base):
    """
    Catalog item model for product catalog
    """
    __tablename__ = "catalog_items"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    brand = Column(String(100), nullable=True, index=True)
    model = Column(String(100), nullable=True)
    image_url = Column(String(255), nullable=True)
    specifications = Column(JSON, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationship with category
    category = relationship("Category", back_populates="catalog_items")
    
    def __repr__(self):
        return f"<CatalogItem {self.id}: {self.name}>"
