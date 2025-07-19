import os
import shutil
from typing import Any

from fastapi import UploadFile



def save_document(uploaded_file: UploadFile, metadata: dict[str, Any]):
    directory: str = f"./documents/{metadata["user_id"]}"
    file_path = os.path.join(directory, metadata["file_name"])
    os.makedirs(directory, exist_ok=True)
    with open(file_path, 'wb+') as file:
        shutil.copyfileobj(uploaded_file.file, file)

    return file_path
