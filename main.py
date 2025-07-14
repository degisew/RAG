from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_core.documents.base import Document
from langchain_text_splitters import CharacterTextSplitter
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_pinecone.vectorstores import PineconeVectorStore

from config import Config


load_dotenv()


def document_loader() -> list[Document]:
    file_path: str = "/home/dag/Desktop/projects/RAG/documents/medium_blog1.txt"

    loader = TextLoader(file_path)

    documents: list[Document] = loader.load()
    print("loading docs...")
    return documents


def text_splitter(documents: list[Document]):
    spliter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)

    chunks = spliter.split_documents(documents)

    print("preparing chunks...")
    return chunks


def generate_embeddings() -> HuggingFaceEmbeddings:

    print("Initializing Embedding...")
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
    )

    return embedding_model


def store_embeddings(
    chunks: list[Document],
    embedding_model: HuggingFaceEmbeddings
):
    print("Storing...")
    PineconeVectorStore.from_documents(chunks, embedding_model)
    print("Done!")


if __name__ == "__main__":
    docs = document_loader()
    chunks = text_splitter(docs)
    embedding_model = generate_embeddings()

    store_embeddings(chunks, embedding_model)
