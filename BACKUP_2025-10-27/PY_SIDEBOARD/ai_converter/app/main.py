from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
import os
import io
from docx import Document
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import tempfile
import trimesh

app = FastAPI(title="AI Converter - Screenshot/Text -> Word/PDF/JPG/3D")

# StaticFiles für Frontend (index.html, CSS, JS, etc.)
frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../frontend"))
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")

@app.get("/api")
async def read_root():
    return {"Hello": "World"}

# (Hier können die Konverter-Endpunkte wie im Beispiel oben ergänzt werden)
