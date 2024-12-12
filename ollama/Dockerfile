FROM python:3.10-slim

WORKDIR /app

# Install system dependencies and curl
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Copy all application code
COPY ollama/start.sh /app/start.sh

# Make start script executable
RUN chmod +x /app/start.sh

# Expose port for Ollama
EXPOSE 11434

# Set environment variables
ENV OLLAMA_HOST=0.0.0.0
ENV OLLAMA_PORT=11434

# Run the startup script
CMD ["/app/start.sh"]