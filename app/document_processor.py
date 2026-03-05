from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

def load_and_split_pdf(file_path: str):
    loader = PyPDFLoader(file_path)
    documents = load_documents(loader)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = splitter.split_documents(documents)
    return chunks

def load_documents(loader):
    return loader.load()