# --- JARVIS NEURAL BACKEND DOCKER ---
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libespeak1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source
COPY . .

# Expose neural port
EXPOSE 5000

# Launch server
CMD ["python", "server.py"]
