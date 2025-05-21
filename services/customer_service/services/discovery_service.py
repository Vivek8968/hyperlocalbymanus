from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from typing import Optional, List, Dict, Any, Tuple
import sys
import os

# Import common modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.utils.geo import GeoService


class DiscoveryService:
    """
    Service for shop discovery operations
    """
    def __init__(self, db: AsyncSession):
        self.db = db
        self.geo_service = GeoService()
    
    async def get_shops_near_location(
        self,
        latitude: float,
        longitude: float,
        radius_km: float = 5.0,
        skip: int = 0,
        limit: int = 10
    ) -> Tuple[List[Dict[str, Any]], int]:
        """
        Get shops near a location
        
        Returns a tuple of (shops, total_count)
        """
        # In a real implementation, this would use a spatial database query
        # For now, we'll simulate by fetching all shops and filtering in memory
        
        # This is a simplified implementation that would call the seller service
        # to get shop data. In a real microservices architecture, this would be
        # an API call to the seller service.
        
        # Simulate fetching shops from seller service
        query = """
        SELECT 
            id, user_id, name, description, whatsapp_number, 
            address, latitude, longitude, image_url, banner_url,
            created_at, updated_at
        FROM shops
        """
        result = await self.db.execute(query)
        shops_data = result.mappings().all()
        
        # Convert to list of dicts
        shops = [dict(shop) for shop in shops_data]
        
        # Filter and sort by distance
        if shops:
            # Calculate distance for each shop
            shops_with_distance = await self.geo_service.sort_by_distance(
                reference_lat=latitude,
                reference_lon=longitude,
                locations=shops
            )
            
            # Filter by radius
            filtered_shops = [
                shop for shop in shops_with_distance
                if shop['distance'] <= radius_km
            ]
            
            # Apply pagination
            paginated_shops = filtered_shops[skip:skip+limit]
            
            return paginated_shops, len(filtered_shops)
        
        return [], 0
    
    async def search_shops(
        self,
        query: str,
        skip: int = 0,
        limit: int = 10
    ) -> Tuple[List[Dict[str, Any]], int]:
        """
        Search shops by name or products
        
        Returns a tuple of (shops, total_count)
        """
        # In a real implementation, this would use a full-text search
        # For now, we'll simulate with a simple LIKE query
        
        # Simulate fetching shops from seller service
        sql_query = f"""
        SELECT 
            id, user_id, name, description, whatsapp_number, 
            address, latitude, longitude, image_url, banner_url,
            created_at, updated_at
        FROM shops
        WHERE 
            LOWER(name) LIKE LOWER('%{query}%') OR
            LOWER(description) LIKE LOWER('%{query}%')
        """
        result = await self.db.execute(sql_query)
        shops_data = result.mappings().all()
        
        # Convert to list of dicts
        shops = [dict(shop) for shop in shops_data]
        
        # Apply pagination
        paginated_shops = shops[skip:skip+limit]
        
        return paginated_shops, len(shops)
    
    async def search_shops_with_location(
        self,
        query: str,
        latitude: float,
        longitude: float,
        radius_km: float = 5.0,
        skip: int = 0,
        limit: int = 10
    ) -> Tuple[List[Dict[str, Any]], int]:
        """
        Search shops by name or products with location filtering
        
        Returns a tuple of (shops, total_count)
        """
        # Get search results
        shops, _ = await self.search_shops(query=query)
        
        # Filter and sort by distance
        if shops:
            # Calculate distance for each shop
            shops_with_distance = await self.geo_service.sort_by_distance(
                reference_lat=latitude,
                reference_lon=longitude,
                locations=shops
            )
            
            # Filter by radius
            filtered_shops = [
                shop for shop in shops_with_distance
                if shop['distance'] <= radius_km
            ]
            
            # Apply pagination
            paginated_shops = filtered_shops[skip:skip+limit]
            
            return paginated_shops, len(filtered_shops)
        
        return [], 0
    
    async def get_shop_by_id(self, shop_id: int) -> Optional[Dict[str, Any]]:
        """
        Get shop by ID
        """
        # Simulate fetching shop from seller service
        query = f"""
        SELECT 
            id, user_id, name, description, whatsapp_number, 
            address, latitude, longitude, image_url, banner_url,
            created_at, updated_at
        FROM shops
        WHERE id = {shop_id}
        """
        result = await self.db.execute(query)
        shop_data = result.mappings().first()
        
        if shop_data:
            return dict(shop_data)
        
        return None
    
    async def get_shop_with_products(
        self,
        shop_id: int,
        skip: int = 0,
        limit: int = 20
    ) -> Optional[Dict[str, Any]]:
        """
        Get shop with its products
        """
        # Get shop details
        shop = await self.get_shop_by_id(shop_id)
        
        if not shop:
            return None
        
        # Simulate fetching products from inventory and catalog services
        query = f"""
        SELECT 
            si.id, si.shop_id, si.catalog_item_id, si.price, si.stock,
            'Product Name' as name,
            'Product Description' as description,
            'Category' as category,
            'Brand' as brand,
            'https://example.com/image.jpg' as image_url
        FROM shop_inventory si
        WHERE si.shop_id = {shop_id}
        LIMIT {limit} OFFSET {skip}
        """
        result = await self.db.execute(query)
        products_data = result.mappings().all()
        
        # Convert to list of dicts
        products = [dict(product) for product in products_data]
        
        # Add products to shop
        shop['products'] = products
        
        return shop
