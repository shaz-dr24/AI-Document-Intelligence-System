

# 📄 AI Document Processing & Automation System

An advanced **AI-powered document intelligence platform** that automates document ingestion, extraction, classification, and decision-making using OCR, LLMs, and automation pipelines.

---

## 📌 Overview

This system processes documents using **OCR + LLM + automation workflows** to:

* Identify document type
* Extract structured data
* Detect and mask sensitive information
* Automatically route documents to relevant departments

---

## 🚀 Key Features

### 📥 Multi-Source Document Input

* Upload documents via API
* Email attachment ingestion using IMAP

---

### 🔍 OCR Processing

* Supports:

  * Images (JPG, PNG)
  * PDFs
* Powered by **Tesseract OCR**

---

### 🔐 PII Masking

* Detects and anonymizes:

  * Names
  * Emails
  * Phone numbers
* Uses **Microsoft Presidio** for privacy protection

---

### 🧠 AI Document Understanding

* Uses LLM (**Groq – LLaMA 3.1**)
* Automatically extracts structured information from documents

---

### ⚙️ Smart Decision Engine

* Automatically classifies documents into:

  * ✅ `AUTO_APPROVED`
  * ⚠️ `REVIEW_REQUIRED`

---

### 🗂️ Intelligent Routing

Documents are automatically categorized and stored:

* 💰 Finance → Invoices
* 👨‍💼 HR → Resumes
* ⚖️ Legal → Contracts
* 📁 General Documents

---

### ⚡ Background Processing

* Powered by **Celery + Redis**
* Enables scalable asynchronous processing

---

### 📊 Dashboard APIs

* View all processed documents
* Fetch individual document details

---

## 🏗️ System Architecture

```id="arch2"
User / Email Input
        ↓
FastAPI Backend
        ↓
Celery Queue (Redis)
        ↓
Worker Processing
   ├── OCR (Tesseract)
   ├── PII Masking (Presidio)
   ├── LLM Extraction (Groq)
   └── Decision Engine
        ↓
Supabase Database
        ↓
Dashboard APIs
```

---

## ⚙️ Tech Stack

| Category      | Technology       |
| ------------- | ---------------- |
| Backend       | FastAPI          |
| Queue System  | Celery + Redis   |
| OCR           | Tesseract        |
| LLM           | Groq (LLaMA 3.1) |
| PII Detection | Presidio         |
| Database      | Supabase         |
| Email         | IMAP             |

---

## 📁 Project Structure

```id="proj2"
app/
│
├── routes/
│   ├── upload.py
│   ├── email.py
│   └── documents.py
│
├── services/
│   ├── email_service.py
│   ├── llm_service.py
│   ├── pii_service.py
│   └── supabase_service.py
│
├── workers/
│   ├── celery_app.py
│   ├── tasks.py
│   └── email_tasks.py
│
└── main.py

data/
└── uploads/
```

---

## 📡 API Endpoints

### 📥 Document APIs

| Endpoint                       | Description         |
| ------------------------------ | ------------------- |
| POST `/upload`                 | Upload document     |
| GET `/api/documents`           | Get all documents   |
| GET `/api/document/{filename}` | Get single document |

---

### 📧 Email Integration

| Endpoint                | Description             |
| ----------------------- | ----------------------- |
| POST `/api/email/fetch` | Fetch email attachments |

---

## 🧠 Processing Pipeline

1. Upload / Email Fetch
2. OCR Text Extraction
3. PII Masking
4. LLM Data Extraction
5. Decision Engine
6. Supabase Storage

---

## 📊 Example Output

```json id="ex2"
{
  "document_type": "invoice",
  "extracted_data": {
    "invoice_number": "12345",
    "total_amount": "₹10,000",
    "vendor": "ABC Pvt Ltd"
  },
  "decision": "AUTO_APPROVED"
}
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository

```bash id="c2"
git clone https://github.com/your-username/ai-document-system.git
cd ai-document-system
```

---

### 2️⃣ Install Dependencies

```bash id="i2"
pip install -r requirements.txt
```

---

### 3️⃣ Environment Variables

Create a `.env` file:

```env id="env2"
GROQ_API_KEY=your_groq_key
SUPABASE_URL=your_url
SUPABASE_KEY=your_key
EMAIL_USER=your_email
EMAIL_PASS=your_password
```

---

### 4️⃣ Install External Tools

* Install **Tesseract OCR**

  ```python
  pytesseract.pytesseract.tesseract_cmd = "YOUR_PATH"
  ```
* Install **Poppler** (required for PDFs)

---

### 5️⃣ Start Redis

```bash id="r2"
redis-server
```

---

### 6️⃣ Run Celery Worker

```bash id="cw2"
celery -A app.workers.celery_app worker --loglevel=info
```

---

### 7️⃣ Run Celery Beat (Scheduler)

```bash id="cb2"
celery -A app.workers.celery_app beat --loglevel=info
```

---

### 8️⃣ Run FastAPI Server

```bash id="f2"
uvicorn app.main:app --reload
```

---

## 🔐 Security Features

* PII masking before AI processing
* Safe JSON parsing
* Input size validation
* Robust error handling & fallback mechanisms

---

## 📈 Future Enhancements

* 📊 React-based dashboard
* 🔍 Advanced document search & filtering
* 🌍 Multi-language OCR support
* 🤖 Fine-tuned LLM models
* ☁️ Cloud deployment

---

## 👨‍💻 Author

Developed as part of an **AI Automation & Document Intelligence System**

---

## 📜 License

MIT License

---

## ⭐ Support

If you found this project useful:

* ⭐ Star the repository
* 🍴 Fork it
* 🚀 Contribute

