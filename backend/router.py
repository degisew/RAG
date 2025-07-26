from typing import Any
from fastapi import BackgroundTasks, UploadFile
from fastapi.routing import APIRouter
from sqlalchemy import select
from backend.chat import process_query
from backend.core.db import DbSession
from backend.core.models import Chat, Document, Message
from backend.ingest import ingest_embeddings
from backend.utils import buffer_message, flush_user_messages_to_db, generate_chat_name, save_document, validate_message_timestamp
from backend.account.dependencies import CurrentUser
from backend.core.schemas import (
    BaseMessageSchema,
    ChatSessionResponseSchema,
    ChatSchema,
    ChatSessionSchema,
    DocumentResponseSchema,
    MessageResponseSchema
)

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

    # background_tasks.add_task(ingest_embeddings, file_path, metadata)

    return file_info


@router.post("/chat")
def chat(request_body: ChatSchema, current_user: CurrentUser):
    user_id = current_user.id
    result = process_query(request_body, user_id)

    return result


@router.get("/documents")
def get_user_documents(db: DbSession, current_user: CurrentUser):
    user_id = current_user.id
    docs = db.scalars(select(
        Document
    ).where(
        Document.user_id == user_id
    ))

    return [DocumentResponseSchema.model_validate(doc) for doc in docs]


@router.get("/{chat_id}/messages")
def get_chat_messages(db: DbSession, chat_id, current_user: CurrentUser):
    # TODO: check how/where to get user_id if we write it in async way
    # TODO: (we might not have current logged in user here in the route)
    user_id = current_user.id
    chat_messages = db.scalars(select(Message).where(
        Message.chat_id == chat_id,
        Message.user_id == user_id
    ))

    return [MessageResponseSchema.model_validate(message) for message in chat_messages]


@router.post("/messages")
def store_chat_messages(
    db: DbSession,
    chat_message: BaseMessageSchema,
    current_user: CurrentUser,
    background_tasks: BackgroundTasks
):
    user_id = current_user.id
    serialized_data = chat_message.model_dump(exclude_unset=True)
    client_timestamp = serialized_data["timestamp"]

    if not client_timestamp:
        raise

    validated_timestamp = validate_message_timestamp(client_timestamp)

    serialized_data.update(timestamp=validated_timestamp)

    number_of_messages_per_user = buffer_message(user_id, serialized_data)

    if number_of_messages_per_user >= 3:
        background_tasks.add_task(flush_user_messages_to_db, db, user_id)

    return {"status": "message received"}


@router.post("/chat-session")
def create_chat_session(db: DbSession, chat_session: ChatSessionSchema, current_user: CurrentUser):
    serialized_data = chat_session.model_dump(exclude_unset=True)
    chat_name = generate_chat_name(serialized_data["file_name"])
    print("CHAT_NAME", chat_name)
    instance = Chat(chat_name=chat_name, user_id=current_user.id)

    db.add(instance)

    db.commit()

    db.refresh(instance)

    return ChatSessionResponseSchema.model_validate(instance)


# TODO: We might have a separate model for storing chat_id, and name
# TODO: to avoid loading much data here on messages DB
@router.get("/chat-histories")
def get_chat_history(db: DbSession, current_user: CurrentUser):
    user_id = current_user.id
    histories = db.scalars(select(Chat).where(
        Chat.user_id == user_id
    ))

    return [ChatSessionResponseSchema.model_validate(his) for his in histories]
