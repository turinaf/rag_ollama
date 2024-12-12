#!/bin/bash

# Start Ollama service in the background
ollama serve &

# Wait for Ollama to be ready
echo "Waiting for Ollama to start..."
sleep 2
echo "Ollama is ready!"

# Pull models
echo "Pulling nomic-embed-text model..."
if ! ollama pull nomic-embed-text; then
       echo "Failed to pull nomic-embed-text model"
       exit 1  # Exit the script if the pull fails
   fi

echo "Pulling llama3.2:1b model..."
if ! ollama pull llama3.2:1b; then
    echo "Failed to pull llama3.2:1b model"
       exit 1  # Exit the script if the pull fails
   fi

# Keep container running
wait