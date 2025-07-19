from langchain_community.document_loaders import (
    PyMuPDFLoader,
    UnstructuredWordDocumentLoader,
    TextLoader,
    UnstructuredMarkdownLoader
)
from langchain_core.documents.base import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter


def document_loader(file_path: str, metadata: dict) -> list[Document]:
    file_name = metadata["file_name"]
    extension = file_name.split(".")[-1].lower()
    base_name = ".".join(file_name.split(".")[:-1])

    if extension == "pdf":
        loader = PyMuPDFLoader(file_path)
    elif extension in {"docx", "doc"}:
        loader = UnstructuredWordDocumentLoader(file_path)
    elif extension == "txt":
        loader = TextLoader(file_path)
    elif extension == "md":
        loader = UnstructuredMarkdownLoader(file_path)
    else:
        raise ValueError(f"Unsupported file type: {extension}")

    print("DDD", extension)

    docs: list[Document] = loader.load()

    metadata.update({"file_name": base_name})

    for doc in docs:
        doc.metadata.update(metadata)

    return docs


def get_chunks(file_path: str, metadata: dict) -> list[Document]:
    documents: list[Document] = document_loader(file_path, metadata)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500)

    chunks: list[Document] = text_splitter.split_documents(documents)

    return chunks
