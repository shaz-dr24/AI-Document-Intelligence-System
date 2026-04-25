from fastapi import APIRouter, UploadFile, File
import os
import shutil
from app.workers.tasks import process_document

router = APIRouter()

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 🔥 send to background worker
    process_document.delay(file.filename)

    return {
        "filename": file.filename,
        "status": "uploaded & processing started"
    }