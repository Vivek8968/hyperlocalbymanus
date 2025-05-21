from sqlalchemy import MetaData

# Create a metadata object for Alembic
metadata = MetaData()

# Import all models to include them in migrations
from services.user_service.models.user import *
from services.seller_service.models.shop import *
from services.seller_service.models.inventory import *
from services.customer_service.models.preference import *
from services.catalog_service.models.category import *
from services.catalog_service.models.catalog import *
from services.admin_service.models.admin_log import *
