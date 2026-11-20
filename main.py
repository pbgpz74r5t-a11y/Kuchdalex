"""LexCheck backend, 1-2 bosqich: fayl yuklash, matn ajratish, qonun havolalarini topish."""
import io
import re

import fitz  # PyMuPDF
from docx import Document
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="LexCheck")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# "Fuqarolik kodeksining 234-moddasi", "FK 234-modda", "MK 77-m." kabi yozuvlar
CITE_RE = re.compile(
    r"(Fuqarolik kodeksi(?:ning)?|Mehnat kodeksi(?:ning)?|"
    r"Ma.muriy javobgarlik to.g.risidagi kodeksi(?:ning)?|FK|MK|MJTK)"
    r"\s*,?\s*(\d+)\s*-\s*(?:moddasi|modda|m\.)",
    re.IGNORECASE,
)


def code_of(name: str) -> str:
    n = name.lower()
    if n.startswith("fuq") or n == "fk":
        return "FK"
    if n.startswith("meh") or n == "mk
