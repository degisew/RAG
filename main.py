from typing import List
from dotenv import load_dotenv
from langchain import hub
from langchain.chains.combine_documents.stuff import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.documents.base import Document
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_pinecone.vectorstores import PineconeVectorStore
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_groq.chat_models import ChatGroq

from config import Config


load_dotenv()


def document_loader() -> list[Document]:
    file_path: str = "/home/dag/Desktop/projects/RAG/documents/medium_blog1.txt"

    loader = TextLoader(file_path)

    documents: list[Document] = loader.load()
    print("loading docs...")
    return documents


def text_splitter(documents: list[Document]) -> List[Document]:
    spliter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)

    chunks = spliter.split_documents(documents)

    print("preparing chunks...")
    return chunks


def generate_embeddings() -> HuggingFaceEmbeddings:

    print("Initializing Embedding...")
    embedding_model = HuggingFaceEmbeddings(
        model_name=Config.embedding_model,
    )

    return embedding_model


def store_embeddings(
    chunks: list[Document],
    embedding: HuggingFaceEmbeddings
):
    print("Storing...")
    PineconeVectorStore.from_documents(
        chunks,
        embedding,
        index_name=Config.pinecone_index_name
    )
    print("Done!")


def retrieval():
    llm = ChatGroq(
        model=Config.model,
        temperature=0.0
    )

    embedding = generate_embeddings()

    query = "WWhy caching?"

    retrieval_qa_prompt = hub.pull("langchain-ai/retrieval-qa-chat")

    vector_store = PineconeVectorStore(index_name=Config.pinecone_index_name, embedding=embedding)

    combine_docs_chain = create_stuff_documents_chain(llm, retrieval_qa_prompt)

    retrieval_chain = create_retrieval_chain(
        vector_store.as_retriever(),
        combine_docs_chain
    )

    res = retrieval_chain.invoke({"input": query})

    return res


def main():
    # docs = document_loader()
    # chunks = text_splitter(docs)
    # embedding = generate_embeddings()

    # store_embeddings(chunks, embedding)
    print(retrieval())


if __name__ == "__main__":
    main()
