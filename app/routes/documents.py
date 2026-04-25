from fastapi import APIRouter, HTTPException
from app.services.supabase_service import get_all_documents, get_document_by_name

router = APIRouter()

@router.get("/api/documents")
def get_documents_dashboard():
    docs = get_all_documents()
    return {"documents": docs}

@router.get("/api/document/{filename}")
def get_single_document(filename: str):
    doc = get_document_by_name(filename)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found or not processed yet")
    return {"document": doc}
