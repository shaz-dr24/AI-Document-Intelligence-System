from app.workers.celery_app import celery_app
from app.services.pii_service import mask_pii
from app.services.supabase_service import save_to_department
from app.services.llm_service import extract_document_data

import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import os

# 🔥 Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# 🔥 Poppler path
POPPLER_PATH = r"C:\Users\HP\Downloads\Release-25.12.0-0\poppler-25.12.0\Library\bin"

UPLOAD_DIR = "data/uploads"


def decision_engine(data):
    """
    Decide whether output is reliable
    """

    if not isinstance(data, dict) or "error" in data:
        return "REVIEW_REQUIRED"

    extracted = data.get("extracted_data", {})

    if not isinstance(extracted, dict):
        return "REVIEW_REQUIRED"

    filled_fields = sum(1 for v in extracted.values() if v)

    return "AUTO_APPROVED" if filled_fields >= 3 else "REVIEW_REQUIRED"


@celery_app.task
def process_document(filename):
    file_path = os.path.join(UPLOAD_DIR, filename)

    print(f"🚀 Processing {filename}...")

    try:
        extracted_text = ""

        # ✅ PDF
        if filename.lower().endswith(".pdf"):
            images = convert_from_path(file_path, poppler_path=POPPLER_PATH)

            for img in images:
                extracted_text += pytesseract.image_to_string(img) + "\n"

        # ✅ Image
        else:
            image = Image.open(file_path)
            extracted_text = pytesseract.image_to_string(image)

        print("📄 Extracted Text:")
        print(extracted_text)

        # 🔐 STEP 1: PII Masking
        masked_text = mask_pii(extracted_text)

        print("🔐 Masked Text:")
        print(masked_text)

        # 🔥 STEP 2: Limit input size
        clean_text = masked_text[:3000]

        # 🧠 STEP 3: LLM Processing
        structured_data = extract_document_data(clean_text)

        print("🧠 Structured Data:")
        print(structured_data)

        # ⚠️ Safety fallback
        if not isinstance(structured_data, dict):
            structured_data = {
                "document_type": "unknown",
                "extracted_data": {}
            }

        # ⚙️ STEP 4: Decision Engine
        decision = decision_engine(structured_data)

        print("⚙️ Decision:", decision)

        # 📦 Extract values safely
        doc_type = structured_data.get("document_type", "unknown")
        extracted = structured_data.get("extracted_data", {})

        # 🔥 STEP 5: ROUTING TO DEPARTMENT TABLE
        save_to_department(
            file_name=filename,
            doc_type=doc_type,
            extracted_data=extracted,
            decision=decision
        )

        # ✅ FINAL RETURN
        return {
            "status": "processed",
            "file": filename,
            "document_type": doc_type,
            "decision": decision
        }

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return {"error": str(e)}