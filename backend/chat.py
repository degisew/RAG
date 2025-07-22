from langchain_groq import ChatGroq
from langchain_pinecone import PineconeVectorStore
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain

from backend.embedding_model import embedding_model
from backend.prompts import RETRIEVAL_QA_CHAT_PROMPT
from backend.core.schemas import ChatSchema
from config import Config


def process_query(request_body: ChatSchema, user_id):
    request_data = request_body.model_dump(exclude_unset=True)
    query = request_data["query"]
    file_name = request_data["file_name"]

    llm = ChatGroq(
        model=Config.model,
        temperature=0.0
    )

    embedding = embedding_model()
    retriever = PineconeVectorStore(
        index_name=Config.pinecone_index_name,
        embedding=embedding
    ).as_retriever(
        search_kwargs={
            "k": 5,
            "filter": {
                # TODO: get this from the request
                "file_name": file_name,
                "user_id": str(user_id)
            }
        }
    )

    combine_docs_chain = create_stuff_documents_chain(
        llm,
        RETRIEVAL_QA_CHAT_PROMPT
    )

    # retriever
    retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)

    res = retrieval_chain.invoke({"input": query})

    return res['answer']
