from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
import uvicorn
import sys
import os

# Add parent directory to path to import common modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import common modules
from common.config.settings import get_settings
from common.exceptions.http_exceptions import AppException, exception_handler
from common.utils.logging import setup_logger

# Import routers
from services.admin_service.routers import users, shops, catalog, logs

# Get settings
settings = get_settings()

# Setup logger
logger = setup_logger(
    "admin_service", 
    log_file="logs/admin_service.log"
)

# Create FastAPI app
app = FastAPI(
    title=f"{settings.APP_NAME} - Admin Panel Backend",
    description="Admin panel backend for system management and monitoring",
    version=settings.APP_VERSION,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add exception handler
app.add_exception_handler(AppException, exception_handler)

# Include routers
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(shops.router, prefix="/shops", tags=["Shops"])
app.include_router(catalog.router, prefix="/catalog", tags=["Catalog"])
app.include_router(logs.router, prefix="/logs", tags=["Logs"])

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Admin Panel Backend API"}

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Custom OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    
    # Add custom schema components here if needed
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8004,
        reload=True
    )
