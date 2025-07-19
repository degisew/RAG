from config import Config
from .load import get_chunks
from .embedding_model import embedding_model
from langchain_pinecone import PineconeVectorStore


def ingest_embeddings(file_path: str, metadata: dict):
    chunks = get_chunks(file_path, metadata)
    embedding = embedding_model()
    PineconeVectorStore.from_documents(
        chunks,
        embedding,
        index_name=Config.pinecone_index_name
    )

    print("Done!")
