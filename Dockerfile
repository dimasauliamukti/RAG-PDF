FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/
COPY datasets/documents/ ./documents/


# Create directory for vector database
RUN mkdir -p /app/qdrant_data

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "src.api:api", "--host", "0.0.0.0", "--port", "8000"]