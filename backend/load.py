from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.documents.base import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter


def pdf_loader(file_path: str, metadata: dict) -> list[Document]:
    loader = PyMuPDFLoader(file_path)

    docs: list[Document] = loader.load()

    file_name = metadata["file_name"].split(".")[0]
    metadata.update({"file_name": file_name})
    # TODO: Add all necessary fields
    for doc in docs:
        doc.metadata.update(metadata)

    return docs


def get_chunks(file_path: str, metadata: dict) -> list[Document]:
    documents: list[Document] = pdf_loader(file_path, metadata)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500)

    chunks: list[Document] = text_splitter.split_documents(documents)

    return chunks
