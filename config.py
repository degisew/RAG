import os
from dotenv import load_dotenv


load_dotenv()


class Config:
    pinecone_index_name = os.environ["INDEX_NAME"]
    model = os.environ["MODEL"]
