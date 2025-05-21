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
COPY services/admin_service/ /app/services/admin_service/

# Set environment variables
ENV PYTHONPATH=/app
ENV MODULE_NAME=services.admin_service.main
ENV PORT=8005

# Expose port
EXPOSE ${PORT}

# Run the application
CMD uvicorn ${MODULE_NAME}:app --host 0.0.0.0 --port ${PORT}
