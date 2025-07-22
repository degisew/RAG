from typing import Any
from fastapi import BackgroundTasks, UploadFile
from fastapi.routing import APIRouter
from sqlalchemy import select
from backend.chat import process_query
from backend.core.db import DbSession
from backend.core.models import Document
from backend.core.schemas import ChatSchema, DocumentResponseSchema
from backend.ingest import ingest_embeddings
from backend.utils import save_document
from backend.account.dependencies import CurrentUser

router = APIRouter(tags=["RAG"])


@router.post("/upload")
def upload_document(
    db: DbSession,
    file: UploadFile,
    background_tasks: BackgroundTasks,
    current_user: CurrentUser
) -> dict[str, Any]:
    file_name = file.filename
    user_id = current_user.id

    metadata = {
        "file_name": file_name,
        "user_id": str(user_id)
    }

    # TODO: Here do a get_or_create operation to avoid saving the same file to DB
    file_info = save_document(db, file, metadata)

    file_path = file_info.pop('file_path')

    background_tasks.add_task(ingest_embeddings, file_path, metadata)

    return file_info


@router.post("/chat")
def chat(request_body: ChatSchema, current_user: CurrentUser):
    user_id = current_user.id
    result = process_query(request_body, user_id)

    return result


@router.get("/documents")
def get_user_documents(db: DbSession, current_user: CurrentUser):
    user_id = current_user.id
    docs = db.scalars(select(Document).where(
        Document.user_id == user_id
    ))

    return [DocumentResponseSchema.model_validate(doc) for doc in docs]
