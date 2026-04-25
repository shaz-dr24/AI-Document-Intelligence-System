from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import upload, email, documents

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router)
app.include_router(email.router)
app.include_router(documents.router)

@app.get("/")
def root():
    return {"message": "AI Document System Backend Running 🚀"}