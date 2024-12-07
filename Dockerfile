FROM python:3.10-slim

WORKDIR /app

# Install system dependencies and curl
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy all application code
COPY . /app/

# Make start script executable
RUN chmod +x /app/start.sh

# Expose port for both Ollama and Flask API
EXPOSE 11434 8080

# Set environment variables
ENV OLLAMA_HOST=0.0.0.0
ENV OLLAMA_PORT=11434
ENV FLASK_PORT=8080

# Run the startup script
CMD ["/app/start.sh"]