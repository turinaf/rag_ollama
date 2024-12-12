#!/bin/sh

# Wait for Ollama to be ready
echo "Waiting for Ollama service..."

echo "Running initial embedding..."
python3 embed_data.py

echo "Starting Flask application..."
python3 app.py