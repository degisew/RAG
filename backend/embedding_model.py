from langchain_huggingface import HuggingFaceEmbeddings

from config import Config


def embedding_model() -> HuggingFaceEmbeddings:

    print("Initializing Embedding...")
    embedding_model = HuggingFaceEmbeddings(
        model_name=Config.embedding_model,
    )

    return embedding_model
