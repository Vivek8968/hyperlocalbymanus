import os
import sys
import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx
from dotenv import load_dotenv

# Add the project root to the Python path
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

# Load environment variables
load_dotenv()

# Import settings
from common.config.settings import get_settings
settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title=f"{settings.APP_NAME} - API Gateway",
    description="API Gateway for the Hyperlocal Marketplace",
    version=settings.APP_VERSION,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Service URL mapping
SERVICE_URLS = {
    "user": settings.USER_SERVICE_URL,
    "seller": settings.SELLER_SERVICE_URL,
    "customer": settings.CUSTOMER_SERVICE_URL,
    "catalog": settings.CATALOG_SERVICE_URL,
    "admin": settings.ADMIN_SERVICE_URL
}

# API route mapping
API_ROUTES = {
    # Auth routes
    "auth": "user",
    
    # User routes
    "users": "user",
    
    # Shop routes
    "shops": "seller",
    
    # Product routes
    "products": "seller",
    
    # Catalog routes
    "catalog": "catalog",
    
    # Admin routes
    "admin": "admin"
}

@app.api_route("/api/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def gateway(request: Request, path: str):
    """
    API Gateway to route requests to appropriate microservices
    """
    # Extract the first part of the path to determine the service
    path_parts = path.split("/")
    service_key = path_parts[0] if path_parts else ""
    
    # Determine which service to route to
    target_service = API_ROUTES.get(service_key, "user")
    target_url = SERVICE_URLS.get(target_service)
    
    if not target_url:
        raise HTTPException(status_code=404, detail=f"Service not found for path: {path}")
    
    # Construct the full URL
    full_url = f"{target_url}/{path}"
    
    # Get request body if any
    body = await request.body()
    
    # Get request headers
    headers = dict(request.headers)
    # Remove host header to avoid conflicts
    headers.pop("host", None)
    
    # Get query parameters
    params = dict(request.query_params)
    
    try:
        # Create httpx client
        async with httpx.AsyncClient() as client:
            # Forward the request to the appropriate service
            response = await client.request(
                method=request.method,
                url=full_url,
                headers=headers,
                params=params,
                content=body,
                timeout=30.0
            )
            
            # Return the response from the service
            return JSONResponse(
                content=response.json() if response.content else {},
                status_code=response.status_code,
                headers=dict(response.headers)
            )
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Service unavailable: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Hyperlocal Marketplace API Gateway"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(
        "gateway:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )