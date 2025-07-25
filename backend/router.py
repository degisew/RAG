from collections import defaultdict
from typing import Any
from fastapi import BackgroundTasks, UploadFile
from fastapi.routing import APIRouter
from sqlalchemy import select
from backend.chat import process_query
from backend.core.db import DbSession
from backend.core.models import Document, Message
from backend.ingest import ingest_embeddings
from backend.utils import save_document, validate_message_timestamp
from backend.account.dependencies import CurrentUser
from backend.core.schemas import (
    BaseMessageSchema,
    ChatHistorySchema,
    ChatSchema,
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


# ! GLOBAL MESSAGE BUFFER
message_buffer = defaultdict(list)


@router.post("/messages")
def store_chat_messages(chat_message: BaseMessageSchema, current_user: CurrentUser):
    user_id = current_user.id
    serialized_data = chat_message.model_dump(exclude_unset=True)
    chat_info = serialized_data.pop("chatInfo")
    chat_id = chat_info["chatId"]
    chat_name = chat_info["chatName"]
    client_timestamp = serialized_data["timestamp"]

    if not client_timestamp:
        raise

    validated_timestamp = validate_message_timestamp(client_timestamp)

    serialized_data.update(timestamp=validated_timestamp,
                           chat_name=chat_name, chat_id=chat_id)

    message_buffer[user_id].append(serialized_data)

    print(f"{message_buffer}")

    return "Ok"


# TODO: We might have a separate model for storing chat_id, and name
# TODO: to avoid loading much data here on messages DB
@router.get("/chat-histories")
def get_chat_history(db: DbSession, current_user: CurrentUser):
    user_id = current_user.id
    histories = db.scalars(select(Message).where(
        Message.user_id == user_id
    ))

    return [ChatHistorySchema.model_validate(history) for history in histories]
