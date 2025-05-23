import os
import sys
import argparse
import uvicorn
import importlib.util
import importlib

# Add the project root to the Python path
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

def run_service(service_name):
    """
    Run a specific service using uvicorn
    """
    service_dir = f"services/{service_name}_service"
    service_path = f"{service_dir}/main.py"
    
    if not os.path.exists(service_path):
        print(f"Error: Service '{service_name}' not found at {service_path}")
        return False
    
    # Get the port from settings
    from common.config.settings import get_settings
    settings = get_settings()
    port_map = {
        "user": settings.USER_SERVICE_PORT,
        "seller": settings.SELLER_SERVICE_PORT,
        "customer": settings.CUSTOMER_SERVICE_PORT,
        "catalog": settings.CATALOG_SERVICE_PORT,
        "admin": settings.ADMIN_SERVICE_PORT
    }
    
    port = port_map.get(service_name, 8000)
    
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    # Import the main module directly
    module_name = f"services.{service_name}_service.main"
    try:
        module = importlib.import_module(module_name)
        app = module.app
        
        # Run the service with uvicorn
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=port,
            reload=False  # Can't use reload with app instance
        )
        return True
    except Exception as e:
        print(f"Error running service: {str(e)}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a microservice")
    parser.add_argument("service", choices=["user", "seller", "customer", "catalog", "admin"], 
                        help="The service to run")
    args = parser.parse_args()
    
    run_service(args.service)