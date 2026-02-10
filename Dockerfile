# 🪼 Jelly V6 - Docker Image
# Multi-purpose: runs both brain (FastAPI) and body (Streamlit)

FROM python:3.11-slim

# System dependencies for psutil
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    iproute2 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Default: run the brain (override in docker-compose for body)
EXPOSE 8000
CMD ["uvicorn", "core.nervenet:app", "--host", "0.0.0.0", "--port", "8000"]
