#!/bin/bash

# Pull required models
ollama pull nomic-embed-text
ollama pull llama3.2:1b

# Start Ollama in background
ollama serve &

# Wait for Ollama to start
sleep 10
# Run initial embedding
python3 embed_data.py
# Start the Flask application
python3 app.py