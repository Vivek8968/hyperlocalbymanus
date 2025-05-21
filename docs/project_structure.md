# Hyperlocal Marketplace Backend - Project Structure

## Overview

The project follows a microservices architecture with each service having its own directory. Each microservice is designed to be independently deployable while sharing common utilities and configurations.

## Directory Structure

```
hyperlocal-marketplace/
│
├── docker-compose.yml           # Docker Compose configuration for all services
├── .env.example                 # Example environment variables
├── README.md                    # Project documentation
│
├── common/                      # Shared code across microservices
│   ├── auth/                    # Authentication utilities
│   │   ├── __init__.py
│   │   ├── firebase.py          # Firebase authentication
│   │   └── jwt.py               # JWT token handling
│   │
│   ├── database/                # Database utilities
│   │   ├── __init__.py
│   │   ├── session.py           # Async SQLAlchemy session
│   │   └── base.py              # Base model class
│   │
│   ├── config/                  # Configuration management
│   │   ├── __init__.py
│   │   └── settings.py          # Environment settings
│   │
│   ├── exceptions/              # Custom exceptions
│   │   ├── __init__.py
│   │   └── http_exceptions.py   # HTTP error handling
│   │
│   └── utils/                   # Utility functions
│       ├── __init__.py
│       ├── s3.py                # S3 integration
│       ├── geo.py               # Geolocation utilities
│       └── logging.py           # Logging configuration
│
├── services/                    # Microservices
│   │
│   ├── user_service/            # User Service
│   │   ├── Dockerfile           # Docker configuration
│   │   ├── requirements.txt     # Service-specific dependencies
│   │   ├── alembic/             # Database migrations
│   │   ├── alembic.ini          # Alembic configuration
│   │   ├── main.py              # FastAPI application entry point
│   │   ├── models/              # SQLAlchemy models
│   │   │   ├── __init__.py
│   │   │   └── user.py          # User model
│   │   ├── schemas/             # Pydantic schemas
│   │   │   ├── __init__.py
│   │   │   └── user.py          # User schemas
│   │   ├── routers/             # API routes
│   │   │   ├── __init__.py
│   │   │   └── auth.py          # Authentication routes
│   │   └── services/            # Business logic
│   │       ├── __init__.py
│   │       └── user_service.py  # User service logic
│   │
│   ├── seller_service/          # Seller Service
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── alembic/
│   │   ├── alembic.ini
│   │   ├── main.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── shop.py          # Shop model
│   │   │   └── inventory.py     # Inventory model
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── shop.py          # Shop schemas
│   │   │   └── inventory.py     # Inventory schemas
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── shops.py         # Shop routes
│   │   │   └── inventory.py     # Inventory routes
│   │   └── services/
│   │       ├── __init__.py
│   │       ├── shop_service.py  # Shop service logic
│   │       └── s3_service.py    # S3 integration logic
│   │
│   ├── customer_service/        # Customer Service
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── alembic/
│   │   ├── alembic.ini
│   │   ├── main.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── preference.py    # Customer preference model
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── shop.py          # Shop schemas (for viewing)
│   │   │   └── preference.py    # Preference schemas
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── shops.py         # Shop discovery routes
│   │   │   └── preferences.py   # Customer preference routes
│   │   └── services/
│   │       ├── __init__.py
│   │       ├── discovery_service.py  # Shop discovery logic
│   │       └── geo_service.py   # Geolocation service
│   │
│   ├── catalog_service/         # Product Catalog Service
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── alembic/
│   │   ├── alembic.ini
│   │   ├── main.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── catalog.py       # Catalog item model
│   │   │   └── category.py      # Category model
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── catalog.py       # Catalog schemas
│   │   │   └── category.py      # Category schemas
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── catalog.py       # Catalog routes
│   │   │   └── categories.py    # Category routes
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   └── catalog_service.py  # Catalog service logic
│   │   └── seed/
│   │       ├── __init__.py
│   │       └── seed_data.py     # Seed data for electronics catalog
│   │
│   └── admin_service/           # Admin Panel Backend
│       ├── Dockerfile
│       ├── requirements.txt
│       ├── alembic/
│       ├── alembic.ini
│       ├── main.py
│       ├── models/
│       │   ├── __init__.py
│       │   └── admin_log.py     # Admin log model
│       ├── schemas/
│       │   ├── __init__.py
│       │   ├── admin.py         # Admin schemas
│       │   └── log.py           # Log schemas
│       ├── routers/
│       │   ├── __init__.py
│       │   ├── users.py         # User management routes
│       │   ├── shops.py         # Shop management routes
│       │   ├── catalog.py       # Catalog management routes
│       │   └── logs.py          # Log viewing routes
│       └── services/
│           ├── __init__.py
│           ├── admin_service.py # Admin service logic
│           └── log_service.py   # Logging service
│
├── api_gateway/                 # API Gateway (Optional)
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py                  # FastAPI application for API Gateway
│   └── routes/                  # Route definitions for services
│
└── docs/                        # Documentation
    ├── requirements_analysis.md # Requirements analysis
    ├── api_docs.md              # API documentation
    ├── setup_guide.md           # Setup guide
    └── project_structure.md     # This file
```

## Service Communication

Each microservice will have its own database schema but will be able to communicate with other services when needed. Communication between services can be done through:

1. **Direct HTTP calls** - For synchronous operations
2. **Message queue** (future enhancement) - For asynchronous operations

## Docker Configuration

Each service will have its own Dockerfile, and a docker-compose.yml file will orchestrate all services together. This allows for:

1. Independent deployment of services
2. Scaling individual services as needed
3. Isolated development environments

## Environment Configuration

Environment variables will be used for configuration, with a `.env.example` file provided as a template. Each service will load its required environment variables from the `.env` file.

## Database Design

Each service will have its own database schema, but all will connect to the same MySQL instance. Alembic will be used for database migrations, with each service having its own migration scripts.

## API Documentation

Swagger/OpenAPI documentation will be automatically generated for each service, providing a comprehensive API reference.

## Deployment Strategy

The project will be deployable using Docker Compose for development and testing. For production, the same Docker images can be deployed to a container orchestration platform like Kubernetes.

## Security Considerations

1. **Authentication** - Firebase Auth for user authentication
2. **Authorization** - JWT tokens for API access
3. **Data Protection** - HTTPS for all API endpoints
4. **Environment Variables** - Sensitive information stored in environment variables
5. **Input Validation** - Pydantic schemas for request validation
