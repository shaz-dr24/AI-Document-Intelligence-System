import os
from groq import Groq
from dotenv import load_dotenv
import json
import re

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def extract_document_data(text):
    """
    Dynamically understand document type and extract structured data
    """

    prompt = f"""
You are an intelligent document processing AI.

Step 1: Identify the document type (invoice, resume, contract, report, etc.)

Step 2: Extract important structured fields based on document type.

Examples:

If Invoice:
- invoice_number
- date
- total_amount
- vendor
- customer

If Resume:
- name
- phone
- education
- skills

If General Document:
- title
- key_points
- summary

IMPORTANT RULES:
- Return ONLY valid JSON
- No explanation
- No markdown
- No extra text
IMPORTANT:
- Extract ALL possible fields
- Do not miss any key information
- Ensure complete output
- Return full structured JSON

FORMAT:
{{
  "document_type": "...",
  "extracted_data": {{
    ...
  }}
}}

TEXT:
{text}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            max_tokens=1024   # 🔥 VERY IMPORTANT
        )

        result = response.choices[0].message.content.strip()

        try:
            return json.loads(result)
        except:
            json_match = re.search(r"\{.*\}", result, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group())
                except:
                    return {"raw_output": result}
            else:
                return {"raw_output": result}

    except Exception as e:
        print(f"❌ LLM Error: {str(e)}")
        return {"error": str(e)}