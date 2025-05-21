import asyncio
import sys
import os
from sqlalchemy.ext.asyncio import AsyncSession
import json

# Add parent directory to path to import common modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.category import Category
from models.catalog import CatalogItem
from common.database.session import async_session_factory
from seed.seed_data import generate_seed_data

async def seed_database():
    """
    Seed the database with categories and catalog items
    """
    print("Starting database seeding...")
    
    # Get seed data
    seed_data = generate_seed_data()
    categories = seed_data["categories"]
    catalog_items = seed_data["catalog_items"]
    
    # Create async session
    async with async_session_factory() as session:
        # Seed categories
        print(f"Seeding {len(categories)} categories...")
        category_map = {}  # Map category names to IDs
        
        for category_data in categories:
            # Check if category already exists
            category = await get_category_by_name(session, category_data["name"])
            
            if not category:
                # Create new category
                category = Category(
                    name=category_data["name"],
                    description=category_data["description"]
                )
                session.add(category)
                await session.flush()
                await session.refresh(category)
                print(f"Created category: {category.name}")
            
            # Store category ID
            category_map[category.name] = category.id
        
        # Commit categories
        await session.commit()
        
        # Seed catalog items
        print(f"Seeding {len(catalog_items)} catalog items...")
        
        for item_data in catalog_items:
            # Check if item already exists
            item = await get_catalog_item_by_name_and_brand(
                session, 
                item_data["name"],
                item_data.get("brand")
            )
            
            if not item:
                # Create new catalog item
                item = CatalogItem(
                    name=item_data["name"],
                    description=item_data["description"],
                    category_id=item_data["category_id"],
                    brand=item_data.get("brand"),
                    model=item_data.get("model"),
                    image_url=item_data.get("image_url"),
                    specifications=item_data.get("specifications")
                )
                session.add(item)
                await session.flush()
                await session.refresh(item)
                print(f"Created catalog item: {item.name}")
        
        # Commit catalog items
        await session.commit()
    
    print("Database seeding completed successfully!")

async def get_category_by_name(session: AsyncSession, name: str):
    """
    Get category by name
    """
    result = await session.execute(f"SELECT * FROM categories WHERE name = '{name}'")
    category = result.mappings().first()
    
    if category:
        return Category(
            id=category["id"],
            name=category["name"],
            description=category["description"]
        )
    
    return None

async def get_catalog_item_by_name_and_brand(session: AsyncSession, name: str, brand: str = None):
    """
    Get catalog item by name and brand
    """
    query = f"SELECT * FROM catalog_items WHERE name = '{name}'"
    
    if brand:
        query += f" AND brand = '{brand}'"
    
    result = await session.execute(query)
    item = result.mappings().first()
    
    if item:
        return CatalogItem(
            id=item["id"],
            name=item["name"],
            description=item["description"],
            category_id=item["category_id"],
            brand=item.get("brand"),
            model=item.get("model"),
            image_url=item.get("image_url"),
            specifications=item.get("specifications")
        )
    
    return None

if __name__ == "__main__":
    # Run seeding
    asyncio.run(seed_database())
