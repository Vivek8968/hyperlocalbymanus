from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import json
import random
from datetime import datetime, timedelta
import os

# Create FastAPI app
app = FastAPI(
    title="LocalMarket API Gateway",
    description="API Gateway for LocalMarket App",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sample data
USERS = [
    {
        "id": "user1",
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "1234567890",
        "role": "customer"
    },
    {
        "id": "user2",
        "name": "Jane Smith",
        "email": "jane@example.com",
        "phone": "9876543210",
        "role": "vendor"
    }
]

SHOPS = [
    {
        "id": "shop1",
        "name": "Grocery Store",
        "description": "Fresh groceries and daily essentials",
        "address": "123 Main St, City",
        "latitude": 28.6139,
        "longitude": 77.2090,
        "distance": 1.2,
        "distanceFormatted": "1.2 km",
        "category": "Grocery",
        "rating": 4.5,
        "imageUrl": "https://images.unsplash.com/photo-1542838132-92c53300491e?q=80&w=1000&auto=format&fit=crop",
        "ownerId": "user2",
        "isOpen": True,
        "openingTime": "09:00",
        "closingTime": "21:00"
    },
    {
        "id": "shop2",
        "name": "Electronics Shop",
        "description": "Latest electronics and gadgets",
        "address": "456 Tech St, City",
        "latitude": 28.6219,
        "longitude": 77.2190,
        "distance": 2.5,
        "distanceFormatted": "2.5 km",
        "category": "Electronics",
        "rating": 4.2,
        "imageUrl": "https://images.unsplash.com/photo-1550009158-9ebf69173e03?q=80&w=1000&auto=format&fit=crop",
        "ownerId": "user2",
        "isOpen": True,
        "openingTime": "10:00",
        "closingTime": "20:00"
    },
    {
        "id": "shop3",
        "name": "Fashion Boutique",
        "description": "Trendy clothes and accessories",
        "address": "789 Fashion Ave, City",
        "latitude": 28.6319,
        "longitude": 77.2290,
        "distance": 3.8,
        "distanceFormatted": "3.8 km",
        "category": "Fashion",
        "rating": 4.7,
        "imageUrl": "https://images.unsplash.com/photo-1567401893414-76b7b1e5a7a5?q=80&w=1000&auto=format&fit=crop",
        "ownerId": "user2",
        "isOpen": False,
        "openingTime": "11:00",
        "closingTime": "19:00"
    }
]

PRODUCTS = [
    {
        "id": "product1",
        "name": "Fresh Apples",
        "description": "Organic fresh apples from local farms",
        "price": 2.99,
        "category": "Fruits",
        "imageUrl": "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?q=80&w=1000&auto=format&fit=crop",
        "shopId": "shop1",
        "inStock": True,
        "quantity": 100,
        "unit": "kg"
    },
    {
        "id": "product2",
        "name": "Whole Wheat Bread",
        "description": "Freshly baked whole wheat bread",
        "price": 3.49,
        "category": "Bakery",
        "imageUrl": "https://images.unsplash.com/photo-1509440159596-0249088772ff?q=80&w=1000&auto=format&fit=crop",
        "shopId": "shop1",
        "inStock": True,
        "quantity": 50,
        "unit": "loaf"
    },
    {
        "id": "product3",
        "name": "Smartphone",
        "description": "Latest smartphone with advanced features",
        "price": 699.99,
        "category": "Electronics",
        "imageUrl": "https://images.unsplash.com/photo-1598327105666-5b89351aff97?q=80&w=1000&auto=format&fit=crop",
        "shopId": "shop2",
        "inStock": True,
        "quantity": 10,
        "unit": "piece"
    },
    {
        "id": "product4",
        "name": "Wireless Earbuds",
        "description": "High-quality wireless earbuds with noise cancellation",
        "price": 129.99,
        "category": "Electronics",
        "imageUrl": "https://images.unsplash.com/photo-1606220588913-b3aacb4d2f46?q=80&w=1000&auto=format&fit=crop",
        "shopId": "shop2",
        "inStock": True,
        "quantity": 15,
        "unit": "piece"
    },
    {
        "id": "product5",
        "name": "T-Shirt",
        "description": "Cotton t-shirt in various colors",
        "price": 19.99,
        "category": "Clothing",
        "imageUrl": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?q=80&w=1000&auto=format&fit=crop",
        "shopId": "shop3",
        "inStock": True,
        "quantity": 30,
        "unit": "piece"
    }
]

CATALOG_ITEMS = [
    {
        "id": "catalog1",
        "name": "Rice",
        "description": "White basmati rice",
        "category": "Grocery",
        "imageUrl": "https://images.unsplash.com/photo-1586201375761-83865001e8ac?q=80&w=1000&auto=format&fit=crop",
        "suggestedPrice": 5.99,
        "unit": "kg"
    },
    {
        "id": "catalog2",
        "name": "Milk",
        "description": "Fresh cow milk",
        "category": "Dairy",
        "imageUrl": "https://images.unsplash.com/photo-1550583724-b2692b85b150?q=80&w=1000&auto=format&fit=crop",
        "suggestedPrice": 2.49,
        "unit": "liter"
    },
    {
        "id": "catalog3",
        "name": "Eggs",
        "description": "Farm fresh eggs",
        "category": "Dairy",
        "imageUrl": "https://images.unsplash.com/photo-1582722872445-44dc5f7e3c8f?q=80&w=1000&auto=format&fit=crop",
        "suggestedPrice": 3.99,
        "unit": "dozen"
    }
]

CATEGORIES = ["Grocery", "Electronics", "Fashion", "Dairy", "Bakery", "Fruits", "Vegetables", "Clothing"]

# Helper function to create API response
def create_response(data, message="Success", status=True):
    return {
        "status": status,
        "message": message,
        "data": data
    }

# Root endpoint
@app.get("/")
async def root():
    return {"message": "LocalMarket API Gateway"}

# API prefix middleware
@app.middleware("http")
async def add_api_prefix(request: Request, call_next):
    path = request.url.path
    if path.startswith("/api"):
        request.scope["path"] = path[4:]  # Remove /api prefix
    response = await call_next(request)
    return response

# Auth Endpoints
@app.post("/auth/register")
async def register_user(request: Request):
    data = await request.json()
    user = {
        "id": f"user{len(USERS) + 1}",
        "name": data.get("name", ""),
        "email": data.get("email", ""),
        "phone": data.get("phone", ""),
        "role": data.get("role", "customer")
    }
    USERS.append(user)
    return create_response(user)

@app.post("/auth/login")
async def login_user(request: Request):
    data = await request.json()
    phone = data.get("phone", "")
    
    # Find user by phone
    user = next((u for u in USERS if u["phone"] == phone), None)
    
    if not user:
        # Create new user if not found
        user = {
            "id": f"user{len(USERS) + 1}",
            "name": "",
            "email": "",
            "phone": phone,
            "role": "customer"
        }
        USERS.append(user)
    
    # Generate token
    token = "mock_token_" + str(random.randint(10000, 99999))
    
    return create_response({
        "token": token,
        "user": user
    })

@app.post("/auth/verify-token")
async def verify_token():
    # Always return success for mock
    return create_response(USERS[0])

# User Endpoints
@app.get("/users/me")
async def get_current_user():
    return create_response(USERS[0])

@app.put("/users/me")
async def update_user_profile(request: Request):
    data = await request.json()
    user = USERS[0].copy()
    user.update(data)
    USERS[0] = user
    return create_response(user)

# Shop Endpoints
@app.get("/shops")
async def get_all_shops(latitude: float = None, longitude: float = None):
    return create_response(SHOPS)

@app.get("/shops/{shop_id}")
async def get_shop_by_id(shop_id: str):
    shop = next((s for s in SHOPS if s["id"] == shop_id), None)
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    return create_response(shop)

@app.post("/shops")
async def create_shop(request: Request):
    data = await request.json()
    shop = {
        "id": f"shop{len(SHOPS) + 1}",
        "name": data.get("name", ""),
        "description": data.get("description", ""),
        "address": data.get("address", ""),
        "latitude": data.get("latitude", 0.0),
        "longitude": data.get("longitude", 0.0),
        "distance": random.uniform(0.5, 5.0),
        "distanceFormatted": f"{random.uniform(0.5, 5.0):.1f} km",
        "category": data.get("category", ""),
        "rating": 0.0,
        "imageUrl": data.get("imageUrl", "https://images.unsplash.com/photo-1542838132-92c53300491e?q=80&w=1000&auto=format&fit=crop"),
        "ownerId": USERS[0]["id"],
        "isOpen": True,
        "openingTime": data.get("openingTime", "09:00"),
        "closingTime": data.get("closingTime", "21:00")
    }
    SHOPS.append(shop)
    return create_response(shop)

@app.put("/shops/{shop_id}")
async def update_shop(shop_id: str, request: Request):
    data = await request.json()
    shop = next((s for s in SHOPS if s["id"] == shop_id), None)
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    
    shop_index = SHOPS.index(shop)
    updated_shop = shop.copy()
    updated_shop.update(data)
    SHOPS[shop_index] = updated_shop
    
    return create_response(updated_shop)

# Product Endpoints
@app.get("/shops/{shop_id}/products")
async def get_shop_products(shop_id: str, search: str = None, category: str = None, sort: str = None):
    products = [p for p in PRODUCTS if p["shopId"] == shop_id]
    
    # Apply search filter
    if search:
        products = [p for p in products if search.lower() in p["name"].lower() or search.lower() in p["description"].lower()]
    
    # Apply category filter
    if category:
        products = [p for p in products if p["category"] == category]
    
    # Apply sorting
    if sort:
        if sort == "price_asc":
            products.sort(key=lambda p: p["price"])
        elif sort == "price_desc":
            products.sort(key=lambda p: p["price"], reverse=True)
        elif sort == "name_asc":
            products.sort(key=lambda p: p["name"])
        elif sort == "name_desc":
            products.sort(key=lambda p: p["name"], reverse=True)
    
    return create_response(products)

@app.get("/products/{product_id}")
async def get_product_by_id(product_id: str):
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return create_response(product)

@app.post("/shops/{shop_id}/products")
async def add_product_to_shop(shop_id: str, request: Request):
    data = await request.json()
    product = {
        "id": f"product{len(PRODUCTS) + 1}",
        "name": data.get("name", ""),
        "description": data.get("description", ""),
        "price": data.get("price", 0.0),
        "category": data.get("category", ""),
        "imageUrl": data.get("imageUrl", "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?q=80&w=1000&auto=format&fit=crop"),
        "shopId": shop_id,
        "inStock": data.get("inStock", True),
        "quantity": data.get("quantity", 0),
        "unit": data.get("unit", "piece")
    }
    PRODUCTS.append(product)
    return create_response(product)

@app.put("/shops/{shop_id}/products/{product_id}")
async def update_shop_product(shop_id: str, product_id: str, request: Request):
    data = await request.json()
    product = next((p for p in PRODUCTS if p["id"] == product_id and p["shopId"] == shop_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product_index = PRODUCTS.index(product)
    updated_product = product.copy()
    updated_product.update(data)
    PRODUCTS[product_index] = updated_product
    
    return create_response(updated_product)

@app.delete("/shops/{shop_id}/products/{product_id}")
async def remove_product_from_shop(shop_id: str, product_id: str):
    product = next((p for p in PRODUCTS if p["id"] == product_id and p["shopId"] == shop_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    PRODUCTS.remove(product)
    return create_response({"message": "Product removed successfully"})

# Catalog Endpoints
@app.get("/catalog")
async def get_catalog_items(search: str = None, category: str = None):
    items = CATALOG_ITEMS
    
    # Apply search filter
    if search:
        items = [i for i in items if search.lower() in i["name"].lower() or search.lower() in i["description"].lower()]
    
    # Apply category filter
    if category:
        items = [i for i in items if i["category"] == category]
    
    return create_response(items)

@app.get("/catalog/categories")
async def get_catalog_categories():
    return create_response(CATEGORIES)

# Vendor Endpoints
@app.get("/vendor/shop")
async def get_vendor_shop():
    # Return the first shop owned by the current user
    shop = next((s for s in SHOPS if s["ownerId"] == USERS[0]["id"]), None)
    if not shop:
        # Create a default shop if none exists
        shop = {
            "id": f"shop{len(SHOPS) + 1}",
            "name": "My Shop",
            "description": "My shop description",
            "address": "My shop address",
            "latitude": 28.6139,
            "longitude": 77.2090,
            "distance": 0.0,
            "distanceFormatted": "0.0 km",
            "category": "Grocery",
            "rating": 0.0,
            "imageUrl": "https://images.unsplash.com/photo-1542838132-92c53300491e?q=80&w=1000&auto=format&fit=crop",
            "ownerId": USERS[0]["id"],
            "isOpen": True,
            "openingTime": "09:00",
            "closingTime": "21:00"
        }
        SHOPS.append(shop)
    
    return create_response(shop)

@app.get("/vendor/products")
async def get_vendor_products():
    # Get the vendor's shop
    shop = next((s for s in SHOPS if s["ownerId"] == USERS[0]["id"]), None)
    if not shop:
        return create_response([])
    
    # Get products for the shop
    products = [p for p in PRODUCTS if p["shopId"] == shop["id"]]
    return create_response(products)

@app.post("/vendor/products/add-from-catalog")
async def add_product_from_catalog(request: Request):
    data = await request.json()
    catalog_id = data.get("catalogId", "")
    shop_id = data.get("shopId", "")
    
    # Find catalog item
    catalog_item = next((c for c in CATALOG_ITEMS if c["id"] == catalog_id), None)
    if not catalog_item:
        raise HTTPException(status_code=404, detail="Catalog item not found")
    
    # Create new product from catalog item
    product = {
        "id": f"product{len(PRODUCTS) + 1}",
        "name": catalog_item["name"],
        "description": catalog_item["description"],
        "price": catalog_item["suggestedPrice"],
        "category": catalog_item["category"],
        "imageUrl": catalog_item["imageUrl"],
        "shopId": shop_id,
        "inStock": True,
        "quantity": data.get("quantity", 0),
        "unit": catalog_item["unit"]
    }
    PRODUCTS.append(product)
    
    return create_response(product)

@app.put("/vendor/shop")
async def update_vendor_shop(request: Request):
    data = await request.json()
    
    # Get the vendor's shop
    shop = next((s for s in SHOPS if s["ownerId"] == USERS[0]["id"]), None)
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    
    shop_index = SHOPS.index(shop)
    updated_shop = shop.copy()
    updated_shop.update(data)
    SHOPS[shop_index] = updated_shop
    
    return create_response(updated_shop)

@app.post("/vendor/shop")
async def create_vendor_shop(request: Request):
    data = await request.json()
    
    # Create new shop
    shop = {
        "id": f"shop{len(SHOPS) + 1}",
        "name": data.get("name", ""),
        "description": data.get("description", ""),
        "address": data.get("address", ""),
        "latitude": data.get("latitude", 0.0),
        "longitude": data.get("longitude", 0.0),
        "distance": 0.0,
        "distanceFormatted": "0.0 km",
        "category": data.get("category", ""),
        "rating": 0.0,
        "imageUrl": data.get("imageUrl", "https://images.unsplash.com/photo-1542838132-92c53300491e?q=80&w=1000&auto=format&fit=crop"),
        "ownerId": USERS[0]["id"],
        "isOpen": True,
        "openingTime": data.get("openingTime", "09:00"),
        "closingTime": data.get("closingTime", "21:00")
    }
    SHOPS.append(shop)
    
    return create_response(shop)

# Serve APK file
@app.get("/download")
async def download_apk():
    apk_path = "/workspace/apk/localmarket.apk"
    if not os.path.exists(apk_path):
        raise HTTPException(status_code=404, detail="APK file not found")
    
    with open(apk_path, "rb") as f:
        apk_data = f.read()
    
    return JSONResponse(
        content={"message": "APK file is available for download"},
        headers={
            "Content-Disposition": "attachment; filename=localmarket.apk",
            "Content-Type": "application/vnd.android.package-archive"
        }
    )

if __name__ == "__main__":
    uvicorn.run(
        "api_gateway:app",
        host="0.0.0.0",
        port=12000,
        reload=True
    )