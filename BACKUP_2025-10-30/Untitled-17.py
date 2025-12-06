FROM node:20-alpine as build
WORKDIR /app
COPY . .
RUN npm install && npm run build
FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html

import os
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Vectra All-in-One KI-Umwandler")

# Healthcheck
@app.get("/healthz")
def health():
    return {"status": "ok"}

# Beispiel-Endpunkt: Screenshot zu Text (OCR)
@app.post("/api/ocr")
async def ocr(file: UploadFile = File(...)):
    # Hier: Tesseract-OCR aufrufen, Text extrahieren
    return {"text": "Demo-OCR-Text"}

# Beispiel-Endpunkt: Text zu PDF/Word/JPG/3D
@app.post("/api/convert")
async def convert(text: str):
    # Hier: PDF, Word, JPG, 3D generieren (Demo)
    return {"pdf": "demo.pdf", "word": "demo.docx", "jpg": "demo.jpg", "stl": "demo.stl"}

# API-Key-Check (Demo)
@app.middleware("http")
    api_key = os.getenv("API_KEY", "DEMO-KEY")
    if api_key == "DEMO-KEY":KEY", "DEMO-KEY")
        print("WARNUNG: Demo-API-Key aktiv!")
    response = await call_next(request)tiv!")
    return responset call_next(request)
    return response
# StaticFiles für Frontend
frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../frontend/build"))
if os.path.exists(frontend_path):s.path.join(os.path.dirname(__file__), "../frontend/build"))
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")

version: "3.9"
services:"3.9"
  backend:
    build: ./backend
    env_file: .envnd
    volumes:: .env
      - ./sample_art:/app/sample_art
    ports:sample_art:/app/sample_art
      - "8000:8000"
  frontend:00:8000"
    build: ./frontend
    ports: ./frontend
      - "3000:80"
  nginx:"3000:80"
    image: nginx:alpine
    volumes:ginx:alpine
      - ./nginx.conf:/etc/nginx/nginx.conf
    ports:nginx.conf:/etc/nginx/nginx.conf
      - "8080:80"
    depends_on:0"
      - backend
      - frontend
      - frontend
import React, { useState } from "react";
function App() {useState } from "react";
  const [file, setFile] = useState(null);
  const [result, setResult] = useState("");
  return (esult, setResult] = useState("");
    <div className="p-8">
      <h1 className="text-2xl font-bold">Vectra KI-Umwandler</h1>
      <input type="file" onChange={e => setFile(e.target.files[0])} />
      <button onClick={async () => { => setFile(e.target.files[0])} />
        const form = new FormData();
        form.append("file", file););
        const res = await fetch("/api/ocr", { method: "POST", body: form });
        const data = await res.json();ocr", { method: "POST", body: form });
        setResult(data.text);s.json();
      }}>OCR starten</button>
      <div className="mt-4">Ergebnis: {result}</div>
    </div> className="mt-4">Ergebnis: {result}</div>
  );</div>
} );
export default App;
export default App;
events {}
http { {}
  server {
    listen 80;
    location /api/ {
      proxy_pass http://backend:8000/api/;
    } proxy_pass http://backend:8000/api/;
    location / {
      proxy_pass http://frontend:80/;
    } proxy_pass http://frontend:80/;
    location /healthz {
      proxy_pass http://backend:8000/healthz;
    }
  }
}

[Unit]
Description=Vectra Backend
After=network.target

[Service]
User=www-data
WorkingDirectory=/pfad/zum/backend
ExecStart=/usr/local/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target

GPT_API_KEY=DEMO-GPT-KEYSHOPIFY_SHOP=deinshop.myshopify.comSHOPIFY_API_KEY=DEMO-SHOPIFY-KEYAPI_KEY=DEMO-KEY-1234567890
}  }    }      proxy_pass http://backend:8000/healthz;    }
  }
}