from typing_extensions import List, TypedDict
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM,OllamaEmbeddings
import argparse

CHROMA_PATH = "chroma"
PROMPT_TEMPLATE = """
Answer the following question based the given context:\n
{context}
\n
Question: {question}
"""
def query(query_text):
    embedding_func = OllamaEmbeddings(model="nomic-embed-text")
    db = Chroma(
        persist_directory=CHROMA_PATH, embedding_function=embedding_func
    )
    # search the DB for the most similar document
    results = db.similarity_search_with_score(query_text, k=3)
    context_text = "\n".join(doc.page_content for doc, _score in results)
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    
    model = OllamaLLM(model="llama3.2:1b")
    response = model.invoke(prompt)
    
    return response

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The text to query")
    args = parser.parse_args()
    query_text = args.query_text
    print(query(query_text))
    
if __name__ == "__main__":
    main()
