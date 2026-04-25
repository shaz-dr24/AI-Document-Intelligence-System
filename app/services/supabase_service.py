from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)


def save_to_department(file_name, doc_type, extracted_data, decision):

    try:
        # 🔒 Safety
        if not isinstance(extracted_data, dict):
            extracted_data = {}

        if not isinstance(doc_type, str):
            doc_type = "unknown"

        doc_type_lower = doc_type.lower()

        # 🔥 Routing logic
        if "invoice" in doc_type_lower or "bill" in doc_type_lower:
            table = "finance_docs"

        elif "resume" in doc_type_lower:
            table = "hr_docs"

        elif "contract" in doc_type_lower or "agreement" in doc_type_lower:
            table = "legal_docs"

        else:
            table = "general_docs"

        # ✅ Common payload (IMPORTANT)
        payload = {
            "file_name": file_name,
            "document_type": doc_type,
            "extracted_data": extracted_data,
            "decision": decision
        }

        print("📦 Payload:", payload)

        # ✅ 1. MASTER TABLE
        supabase.table("documents").insert(payload).execute()
        print("📁 Stored in documents")

        # ✅ 2. DEPARTMENT TABLE
        supabase.table(table).insert(payload).execute()
        print(f"💾 Stored in {table}")

        return True

    except Exception as e:
        print(f"❌ DB Error: {str(e)}")
        return None

def get_all_documents():
    try:
        response = supabase.table("documents").select("*").execute()
        return response.data
    except Exception as e:
        print(f"❌ DB Error: {str(e)}")
        return []

def get_document_by_name(file_name):
    try:
        response = supabase.table("documents").select("*").eq("file_name", file_name).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"❌ DB Error: {str(e)}")
        return None