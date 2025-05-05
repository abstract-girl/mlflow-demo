FROM python:3.9-slim

WORKDIR /app

# Install system dependencies for building packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY train.py .
COPY predict.py .

# Create directory for models
RUN mkdir -p /app/models

# Set environment variables
ENV MLFLOW_TRACKING_URI=http://mlflow:5000

# Default command - can be overridden
CMD ["python", "train.py"] 