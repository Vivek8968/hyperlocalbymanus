# Hyperlocal Marketplace Backend - Requirements Analysis

## Project Overview
A hyperlocal marketplace platform where customers can discover nearby local shops and their products based on geo-location. The system will serve both a website and an Android application.

## Technology Stack
- **Language**: Python 3.11+
- **Framework**: FastAPI (with full async support)
- **Validation**: Pydantic
- **ORM**: SQLAlchemy (Async ORM)
- **Database**: MySQL
- **Architecture**: Microservices
- **Authentication**: Firebase Auth (OTP login, Google, Apple)
- **Media Storage**: AWS S3
- **Geo Queries**: Location filtering for shop discovery
- **Deployment**: Docker + Docker Compose

## Microservices Architecture

### 1. User Service
**Responsibilities**:
- User registration and authentication
- User profile management
- Session management with JWT tokens
- Role-based access control (Customer, Seller, Admin)

**Endpoints**:
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login with Firebase (OTP, Google, Apple)
- `GET /auth/verify-token` - Verify JWT token
- `GET /users/me` - Get current user profile
- `PUT /users/me` - Update user profile
- `POST /auth/refresh-token` - Refresh JWT token

**Data Models**:
- User (id, firebase_uid, name, email, phone, role, created_at, updated_at)

### 2. Seller Service
**Responsibilities**:
- Shop registration and management
- Product inventory management
- Image upload to S3
- Shop profile management

**Endpoints**:
- `POST /shops` - Register a new shop
- `GET /shops/me` - Get seller's shop details
- `PUT /shops/me` - Update shop details
- `POST /shops/me/products` - Add product to inventory
- `GET /shops/me/products` - List all products in inventory
- `PUT /shops/me/products/{product_id}` - Update product details
- `DELETE /shops/me/products/{product_id}` - Remove product from inventory
- `POST /shops/me/images/upload` - Upload shop images to S3

**Data Models**:
- Shop (id, user_id, name, description, whatsapp_number, address, latitude, longitude, image_url, banner_url, created_at, updated_at)
- ShopInventory (id, shop_id, catalog_item_id, price, stock, created_at, updated_at)

### 3. Customer Service
**Responsibilities**:
- Shop discovery based on geo-location
- Product browsing
- Shop details viewing

**Endpoints**:
- `GET /shops/nearby` - Get shops near customer location
- `GET /shops/{shop_id}` - Get shop details
- `GET /shops/{shop_id}/products` - Get products from a shop
- `GET /shops/search` - Search shops by name or products

**Data Models**:
- CustomerPreference (id, user_id, default_latitude, default_longitude, search_radius, created_at, updated_at)

### 4. Product Catalog Service
**Responsibilities**:
- Manage master catalog of electronics items
- Provide search functionality for catalog items
- Seed and maintain product data

**Endpoints**:
- `GET /catalog` - List all catalog items (paginated)
- `GET /catalog/search` - Search catalog items
- `GET /catalog/{item_id}` - Get catalog item details
- `POST /catalog` - Add new catalog item (admin only)
- `PUT /catalog/{item_id}` - Update catalog item (admin only)
- `DELETE /catalog/{item_id}` - Delete catalog item (admin only)

**Data Models**:
- CatalogItem (id, name, description, category, brand, model, image_url, specifications, created_at, updated_at)
- Category (id, name, description, created_at, updated_at)

### 5. Admin Panel Backend
**Responsibilities**:
- User management
- Shop management
- Product catalog management
- System monitoring and logging

**Endpoints**:
- `GET /admin/users` - List all users
- `PUT /admin/users/{user_id}` - Update user details
- `DELETE /admin/users/{user_id}` - Delete user
- `GET /admin/shops` - List all shops
- `PUT /admin/shops/{shop_id}` - Update shop details
- `DELETE /admin/shops/{shop_id}` - Delete shop
- `GET /admin/logs` - View system logs
- `GET /admin/stats` - Get system statistics

**Data Models**:
- AdminLog (id, admin_id, action, entity_type, entity_id, details, created_at)

## Cross-Cutting Concerns

### Authentication & Authorization
- Firebase Auth integration for user authentication
- JWT token-based session management
- Role-based access control (RBAC)

### Database
- MySQL with async SQLAlchemy ORM
- Alembic for database migrations
- Connection pooling for performance

### API Documentation
- OpenAPI/Swagger documentation
- Postman collection

### Error Handling
- Standardized error responses
- Comprehensive logging
- Exception middleware

### Deployment
- Docker containers for each microservice
- Docker Compose for local development
- Environment variables for configuration

### Media Storage
- AWS S3 integration for image storage
- Presigned URLs for secure access

### Geo-Location
- Efficient geo-spatial queries
- Distance calculation and sorting

## Data Flow

1. **User Registration/Login**:
   - User authenticates via Firebase
   - Backend verifies Firebase token
   - JWT token issued for subsequent requests

2. **Seller Flow**:
   - Seller registers shop with location
   - Seller searches catalog for products
   - Seller adds products to inventory with custom price/stock
   - Images uploaded to S3

3. **Customer Flow**:
   - Customer shares location
   - Backend finds nearby shops
   - Customer views shop details and products
   - Distance calculated and displayed

4. **Admin Flow**:
   - Admin logs in with admin credentials
   - Admin manages users, shops, and catalog
   - Admin views system logs and statistics
