# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port
EXPOSE 8000

# Run command
CMD ["python", "run.py"]

# Set environment variable for Redis connection
ENV REDIS_URL=redis://redis-service:6379
