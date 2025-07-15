import os
from dotenv import load_dotenv


load_dotenv()


class Config:
    model = os.environ["MODEL"]
    pinecone_index_name = os.environ["INDEX_NAME"]
    embedding_model = os.environ["EMBEDDING_MODEL"]
