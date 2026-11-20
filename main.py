from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="LexCheck API")

# CORS sozlamalari (frontend bilan ulanish uchun kerak)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "LexCheck API ishlayapti!"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Hozircha AI limiti tugaganligi uchun, demo ma'lumotlarini qaytaramiz
    
    demo_citations = [
        {
            "page": 12,
            "old_text": "Mehnat kodeksining 97-moddasiga ko'ra ta'til 15 kun.",
            "status": "ESKIRGAN",
            "new_text": "2024-yil holatiga ko'ra, ta'til muddati 21 kun etib belgilangan.",
            "law_name": "Mehnat kodeksi, 97-modda"
        },
        {
            "page": 25,
            "old_text": "Soliq stavkasi 12 foizni tashkil qiladi.",
            "status": "O'ZGARGAN",
            "new_text": "Yangi tahrirda soliq stavkasi 15 foiz qilib belgilandi.",
            "law_name": "Soliq kodeksi, 53-modda"
        }
    ]

    return {
        "filename": file.filename,
        "pages": 38,
        "citations": demo_citations
    }
