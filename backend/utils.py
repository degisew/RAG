from datetime import datetime, timezone, timedelta
import os
import shutil
from typing import Any
from fastapi import UploadFile

from backend.core.db import DbSession
from backend.core.models import Document


def validate_message_timestamp(client_timestamp) -> datetime:
    MAX_CLOCK_SKEW = timedelta(minutes=1)

    try:
        sent_at = datetime.fromisoformat(client_timestamp)
        now = datetime.now(timezone.utc)
        if abs(now - sent_at) < MAX_CLOCK_SKEW:
            return sent_at
    except Exception:
        pass

    return datetime.now(timezone.utc)


def save_document(
    db: DbSession,
    uploaded_file: UploadFile,
    metadata: dict[str, Any]
) -> dict[str, Any]:
    file_path = store_document_on_disk(uploaded_file, metadata)

    saved_file_metadata = {
        "file_name": metadata["file_name"],
        "user_id": metadata["user_id"],
        "file_location": file_path
    }

    document = store_document_metadata_on_db(db, data=saved_file_metadata)

    return {
        "file_name": metadata["file_name"],
        "id": document.id,
        "file_path": file_path
    }


def store_document_on_disk(uploaded_file: UploadFile, metadata: dict[str, Any]) -> str:
    directory: str = f"./documents/{metadata["user_id"]}"
    file_path = os.path.join(directory, metadata["file_name"])
    os.makedirs(directory, exist_ok=True)
    with open(file_path, 'wb+') as file:
        shutil.copyfileobj(uploaded_file.file, file)

    return file_path


def store_document_metadata_on_db(db: DbSession, data: dict[str, Any]):
    instance = Document(**data)

    db.add(instance)

    db.commit()

    db.refresh(instance)

    return instance
