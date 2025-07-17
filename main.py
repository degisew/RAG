# from backend.ingest import ingest_embeddings

#     llm = ChatGroq(
#         model=Config.model,
#         temperature=0.0
#     )

#     embedding = generate_embeddings()

#     query = "WWhy caching?"

#     retrieval_qa_prompt = hub.pull("langchain-ai/retrieval-qa-chat")

#     vector_store = PineconeVectorStore(index_name=Config.pinecone_index_name, embedding=embedding)

#     combine_docs_chain = create_stuff_documents_chain(llm, retrieval_qa_prompt)

#     retrieval_chain = create_retrieval_chain(
#         vector_store.as_retriever(),
#         combine_docs_chain
#     )

#     res = retrieval_chain.invoke({"input": query})

#     return res
from backend.chat import chat


def main():
    print(chat())
    # print(ingest_embeddings())


if __name__ == "__main__":
    main()
