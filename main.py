from typing import Any
from backend.chat import process_query
from backend.ingest import ingest_embeddings
from fastapi import BackgroundTasks, FastAPI, UploadFile
from backend.utils import save_document


app = FastAPI()


@app.post("/upload")
def upload_document(file: UploadFile, background_tasks: BackgroundTasks) -> dict[str, Any]:
    file_name = file.filename
    user_id = "1234"

    metadata = {
        "file_name": file_name,
        "user_id": user_id
    }

    file_path = save_document(file, metadata)

    background_tasks.add_task(ingest_embeddings, file_path, metadata)

    return {
        "status_code": 202,
        "message": "Uploading your file..."
    }


@app.post("/chat")
def chat(query: str):
    result = process_query(query)

    return result
