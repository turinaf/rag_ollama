import argparse
import os
import shutil
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from langchain_community.document_loaders import WebBaseLoader
from langchain_ollama import OllamaLLM
import bs4

CHROMA_PATH = "chroma"
embedding_func = OllamaEmbeddings(model="nomic-embed-text")

def load_document():
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    loader = WebBaseLoader(
        web_paths =("https://www.chinahighlights.com/beijing/how-to-get-to-great-wall.htm",),
        bs_kwargs = dict(
            parse_only = bs4.SoupStrainer(
                class_=("main_content")
                )
        ),
        requests_kwargs={"headers": {"User-Agent": USER_AGENT}} 
    )
    docs = loader.load()
    return docs

def split_documents(documents: list[Document]):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    return splitter.split_documents(documents)

def store_vectors(chunks: list[Document]):
    db = Chroma(
        persist_directory=CHROMA_PATH, embedding_function=embedding_func
    )
    
    # get chunk ids
    chuncks_with_ids = calculate_chunk_ids(chunks)
    
    # add or update the vector
    existing_items = db.get(include=[])
    existing_ids = set(existing_items['ids'])
    print(f"Existing Documents in DB: {len(existing_ids)}")
    
    # only add documents that don't exist in the DB
    new_chunks = []
    for chunk in chuncks_with_ids:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)
    if len(new_chunks):
        print(f"Adding {len(new_chunks)} new documents to the DB")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids)
    else:
        print("No new documents to add to the DB")
    
def calculate_chunk_ids(chunks):

    # This will create IDs like "data/monopoly.pdf:6:2"
    # Page Source : Page Number : Chunk Index

    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        # If the page ID is the same as the last one, increment the index.
        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        # Calculate the chunk ID.
        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        # Add it to the page meta-data.
        chunk.metadata["id"] = chunk_id

    return chunks

def clear_database():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
        print("Cleared the database")
    else:
        print("No database to clear")
        
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Clear the database")
    args = parser.parse_args()
    if args.reset:
        clear_database()
    # create or update the databse
    documents =load_document()
    chunks = split_documents(documents)
    store_vectors(chunks)
    
if __name__ == "__main__":
    main()