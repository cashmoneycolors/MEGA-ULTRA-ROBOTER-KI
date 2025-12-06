from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# StaticFiles für Frontend (index.html, CSS, JS, etc.)
frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../frontend"))
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")

@app.get("/api")
async def read_root():
    return {"Hello": "World"}
chmod +x install_ai_converter.sh
sudo ./install_ai_converter.shcp -r ./app /opt/ai_converter/
cp -r ./frontend /opt/ai_converter/cd /opt/ai_converter
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000cd /opt/ai_converter
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000