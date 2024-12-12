FROM python:3.10-slim

WORKDIR /app

# Install system dependencies and curl
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY flask_api/ /app/
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy all application code
COPY flask_api/start.sh /app/start.sh

# Make start script executable
RUN chmod +x /app/start.sh

# Expose port for Flask API
EXPOSE 8080
# Set environment variables
ENV FLASK_PORT=8080

# Run the startup script
CMD ["/app/start.sh"]