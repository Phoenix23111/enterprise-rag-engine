# 1. Use an official lightweight Python image
FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Install system dependencies
RUN apt-get update && apt-get install -y \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# 4. Copy your dependency list
COPY requirements.txt .

# 5. Upgrade pip and install the lightweight CPU-only version of PyTorch FIRST
RUN pip install --upgrade pip && \
    pip install torch --index-url https://download.pytorch.org/whl/cpu

# 6. Install the rest of the RAG engine libraries
RUN pip install --no-cache-dir --default-timeout=100 -r requirements.txt

# 7. Copy your application code
COPY . .

# 8. Expose the port (FastAPI)
EXPOSE 8000

# 9. Start the service
CMD ["python3", "app.py"]