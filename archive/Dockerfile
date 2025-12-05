FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
COPY pyproject.toml .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY gen_ai_utils/ ./gen_ai_utils/
COPY . .

# Install package
RUN pip install -e .

# Expose port for FastAPI
EXPOSE 8000

# Default command
CMD ["uvicorn", "gen_ai_utils.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
