## Custom RAG
RAG using ollama on local machine with Llama 3.2 1B model and contents from web pages scraped on the fly.
### Using this repo
* Clone the repo
```
git clone https://github.com/turinaf/rag_ollama.git
``` 
Just add links of website from where you want to get the knowledge base to `flask_api/embed_data.py` and it will load page content from the link using langchain's `WebBaseLoader` .
* Then start docker app and build docker container to run it
```
docker compose up --build
```
After building successfully visit [http://localhost:8080/](http://localhost:8080/) to chat with your custom RAG
