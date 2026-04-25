from fastapi import APIRouter
from app.services.email_service import fetch_email_attachments
from app.workers.tasks import process_document

router = APIRouter()

@router.post("/api/email/fetch")
def fetch_emails():
    # Fetch attachments from real IMAP
    downloaded = fetch_email_attachments()
    
    response_data = []
    
    for item in downloaded:
        filename = item["filename"]
        # Enqueue processing in background
        process_document.delay(filename)
        
        response_data.append({
            "id": filename, 
            "subject": item.get("subject", "Automated Document"),
            "from": item.get("from", "system@mail.com"),
            "date": item.get("date", ""),
            "attachmentType": filename.split(".")[-1].upper(),
            "status": "pending",
            "priority": "normal"
        })
        
    return {"message": "Emails fetched", "emails": response_data}
