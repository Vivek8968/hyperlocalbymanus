FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy common modules
COPY common/ /app/common/

# Copy migrations
COPY migrations/ /app/migrations/
COPY alembic.ini /app/

# Copy service code
COPY services/seller_service/ /app/services/seller_service/

# Set environment variables
ENV PYTHONPATH=/app
ENV MODULE_NAME=services.seller_service.main
ENV PORT=8002

# Expose port
EXPOSE ${PORT}

# Run the application
CMD uvicorn ${MODULE_NAME}:app --host 0.0.0.0 --port ${PORT}
