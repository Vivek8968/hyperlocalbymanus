from fastapi import APIRouter, Depends, HTTPException, status, Path, Query
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any, Optional

# Import common modules
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.database.session import get_db
from common.auth.jwt import get_current_user
from common.exceptions.http_exceptions import ResourceNotFoundException, UnauthorizedException

# Import schemas and services
from services.seller_service.schemas.inventory import InventoryItemCreate, InventoryItemUpdate, InventoryItemResponse, InventoryItemWithCatalogResponse
from services.seller_service.services.inventory_service import InventoryService
from services.seller_service.services.shop_service import ShopService

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.post("", response_model=InventoryItemResponse, status_code=status.HTTP_201_CREATED)
async def add_product_to_inventory(
    product_data: InventoryItemCreate,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Add a product to the seller's inventory
    """
    # Get seller's shop
    shop_service = ShopService(db)
    shop = await shop_service.get_shop_by_user_id(current_user["user_id"])
    
    if not shop:
        raise ResourceNotFoundException("Shop not found for current user")
    
    # Add product to inventory
    inventory_service = InventoryService(db)
    inventory_item = await inventory_service.add_inventory_item(
        shop_id=shop.id,
        catalog_item_id=product_data.catalog_item_id,
        price=product_data.price,
        stock=product_data.stock
    )
    
    return inventory_item

@router.get("", response_model=List[InventoryItemWithCatalogResponse])
async def get_inventory_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all products in the seller's inventory
    """
    # Get seller's shop
    shop_service = ShopService(db)
    shop = await shop_service.get_shop_by_user_id(current_user["user_id"])
    
    if not shop:
        raise ResourceNotFoundException("Shop not found for current user")
    
    # Get inventory items
    inventory_service = InventoryService(db)
    inventory_items = await inventory_service.get_inventory_items_by_shop_id(
        shop_id=shop.id,
        skip=skip,
        limit=limit
    )
    
    # Fetch catalog item details for each inventory item
    # In a real implementation, this would call the catalog service API
    # For now, we'll return the inventory items without catalog details
    
    return inventory_items

@router.get("/{item_id}", response_model=InventoryItemWithCatalogResponse)
async def get_inventory_item(
    item_id: int = Path(..., gt=0),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific product from the seller's inventory
    """
    # Get seller's shop
    shop_service = ShopService(db)
    shop = await shop_service.get_shop_by_user_id(current_user["user_id"])
    
    if not shop:
        raise ResourceNotFoundException("Shop not found for current user")
    
    # Get inventory item
    inventory_service = InventoryService(db)
    inventory_item = await inventory_service.get_inventory_item_by_id(item_id)
    
    if not inventory_item:
        raise ResourceNotFoundException(f"Inventory item with ID {item_id} not found")
    
    # Check if inventory item belongs to seller's shop
    if inventory_item.shop_id != shop.id:
        raise UnauthorizedException("Not authorized to access this inventory item")
    
    # Fetch catalog item details
    # In a real implementation, this would call the catalog service API
    
    return inventory_item

@router.put("/{item_id}", response_model=InventoryItemResponse)
async def update_inventory_item(
    item_data: InventoryItemUpdate,
    item_id: int = Path(..., gt=0),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update a product in the seller's inventory
    """
    # Get seller's shop
    shop_service = ShopService(db)
    shop = await shop_service.get_shop_by_user_id(current_user["user_id"])
    
    if not shop:
        raise ResourceNotFoundException("Shop not found for current user")
    
    # Get inventory item
    inventory_service = InventoryService(db)
    inventory_item = await inventory_service.get_inventory_item_by_id(item_id)
    
    if not inventory_item:
        raise ResourceNotFoundException(f"Inventory item with ID {item_id} not found")
    
    # Check if inventory item belongs to seller's shop
    if inventory_item.shop_id != shop.id:
        raise UnauthorizedException("Not authorized to update this inventory item")
    
    # Update inventory item
    updated_item = await inventory_service.update_inventory_item(
        item_id=item_id,
        item_data=item_data.dict(exclude_unset=True)
    )
    
    return updated_item

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_inventory_item(
    item_id: int = Path(..., gt=0),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Remove a product from the seller's inventory
    """
    # Get seller's shop
    shop_service = ShopService(db)
    shop = await shop_service.get_shop_by_user_id(current_user["user_id"])
    
    if not shop:
        raise ResourceNotFoundException("Shop not found for current user")
    
    # Get inventory item
    inventory_service = InventoryService(db)
    inventory_item = await inventory_service.get_inventory_item_by_id(item_id)
    
    if not inventory_item:
        raise ResourceNotFoundException(f"Inventory item with ID {item_id} not found")
    
    # Check if inventory item belongs to seller's shop
    if inventory_item.shop_id != shop.id:
        raise UnauthorizedException("Not authorized to delete this inventory item")
    
    # Delete inventory item
    await inventory_service.delete_inventory_item(item_id)
    
    return None
