from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
import sys
import os

# Add parent directory to path to import common modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.database.session import Base


class ShopInventory(Base):
    """
    Shop inventory model for products in a shop
    """
    __tablename__ = "shop_inventory"
    
    id = Column(Integer, primary_key=True, index=True)
    shop_id = Column(Integer, ForeignKey("shops.id", ondelete="CASCADE"), nullable=False)
    catalog_item_id = Column(Integer, nullable=False, index=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationship with shop
    shop = relationship("Shop", back_populates="inventory_items")
    
    def __repr__(self):
        return f"<ShopInventory {self.id}: shop_id={self.shop_id}, catalog_item_id={self.catalog_item_id}>"
