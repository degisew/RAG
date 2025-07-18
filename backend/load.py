import os
from typing import List
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.documents.base import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter


def pdf_loader() -> list[Document]:
    file_path = "/home/dag/Desktop/projects/RAG/documents/Intch_user_agreement.pdf"

    loader = PyMuPDFLoader(file_path)

    docs: List[Document] = loader.load()

    file_name = os.path.basename(file_path).split(".")[0]
    # TODO: Add all necessary fields
    for doc in docs:
        doc.metadata.update({
            "file_name": file_name,
            "user_id": "1234"
        })

    return docs


def get_chunks() -> List[Document]:
    documents: List[Document] = pdf_loader()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500)

    chunks: List[Document] = text_splitter.split_documents(documents)

    return chunks
