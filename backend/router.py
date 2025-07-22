from typing import Any
from fastapi import BackgroundTasks, UploadFile
from backend.chat import process_query
from backend.core.schemas import ChatSchema
from backend.ingest import ingest_embeddings
from backend.utils import save_document
from fastapi.routing import APIRouter


router = APIRouter(tags=["RAG"])


@router.post("/upload")
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


@router.post("/chat")
def chat(request_body: ChatSchema):
    user_id = "1234"
    result = process_query(request_body, user_id)

    return result


@router.get("/documents")
def get_user_documents():
    pass
