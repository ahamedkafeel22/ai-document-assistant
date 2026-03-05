from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import os

CHROMA_DIR = "chroma_db"

def get_embeddings():
    return OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

def create_vector_store(chunks):
    embeddings = get_embeddings()
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DIR
    )
    return vector_store

def load_vector_store():
    embeddings = get_embeddings()
    vector_store = Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings
    )
    return vector_store 