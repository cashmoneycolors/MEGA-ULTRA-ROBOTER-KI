"""FastAPI KI-Sideboard - REST API für KI-Services & Modulsteuerung"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import sys
import importlib
import traceback
from typing import List
from dotenv import load_dotenv

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir)
)
MODULES_PATH = os.path.abspath(os.path.join(PROJECT_ROOT, "modules"))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
if MODULES_PATH not in sys.path:
    sys.path.insert(0, MODULES_PATH)

from core.key_check import check_all_keys

load_dotenv()
app = FastAPI(title="KI-Sideboard", version="2.0")


class VisionRequest(BaseModel):
    image_url: str


class RunRequest(BaseModel):
    module: str
    action: str = "run"
    params: List[str] = []


def discover_modules():
    modules = []
    if not os.path.isdir(MODULES_PATH):
        return modules
    for fname in os.listdir(MODULES_PATH):
        if fname.endswith(".py") and not fname.startswith("__"):
            modules.append(fname[:-3])
    return sorted(modules)


def get_capabilities(mod):
    caps = []
    for cap in ["run", "install", "to_svg", "to_word", "describe"]:
        if hasattr(mod, cap):
            caps.append(cap)
    return caps


def read_team_log(max_lines: int = 400):
    log_path = os.path.join(PROJECT_ROOT, "team_log.txt")
    if not os.path.exists(log_path):
        return {"entries": [], "lastRun": None}
    with open(log_path, "r", encoding="utf-8") as f:
        lines = f.readlines()[-max_lines:]
    last_run = None
    for line in reversed(lines):
        line = line.strip()
        if line.startswith("[TEAM-MODUS] Autostart"):
            last_run = line.replace("[TEAM-MODUS] Autostart am", "").strip()
            break
    return {
        "entries": [line.rstrip("\n") for line in lines],
        "lastRun": last_run,
    }


@app.get("/health")
async def health():
    return {"status": "ok", "service": "ki_sideboard"}


@app.get("/modules")
async def list_modules():
    result = []
    for module_name in discover_modules():
        try:
            mod = importlib.import_module(module_name)
            caps = get_capabilities(mod)
            result.append({"name": module_name, "capabilities": caps})
        except Exception as exc:
            result.append(
                {"name": module_name, "capabilities": [], "error": str(exc)}
            )
    return {"modules": result}


@app.post("/module/run")
async def run_module(request: RunRequest):
    check_all_keys()
    module_name = request.module.strip()
    if module_name not in discover_modules():
        raise HTTPException(
            status_code=404,
            detail=f"Modul '{module_name}' nicht gefunden",
        )
    try:
        mod = importlib.import_module(module_name)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Import-Fehler: {exc}")

    if not hasattr(mod, request.action):
        raise HTTPException(
            status_code=400,
            detail=f"Aktion '{request.action}' nicht verfügbar",
        )

    func = getattr(mod, request.action)
    try:
        result = func(*request.params)
    except Exception as exc:
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Modulausführung fehlgeschlagen: {exc}",
        )

    return {
        "status": "success",
        "module": module_name,
        "action": request.action,
        "result": result,
    }


@app.get("/status")
async def get_status():
    snapshot = read_team_log()
    return {
        "status": "ok",
        "lastRun": snapshot["lastRun"],
        "entries": snapshot["entries"],
    }


@app.post("/openai_vision")
async def openai_vision(request: VisionRequest):
    """OpenAI Vision API - Bildanalyse mit GPT-4 Vision"""
    try:
        check_all_keys()
        from modules import openai_integration

        result = openai_integration.analyze_image(
            request.image_url,
            question="Beschreibe dieses Bild detailliert.",
        )

        if result.get("status") != "success":
            raise HTTPException(
                status_code=500,
                detail=(
                    "OpenAI Vision Fehler: "
                    f"{result.get('message')}"
                ),
            )

        return {
            "status": "success",
            "image_url": request.image_url,
            "description": result.get("analysis"),
            "model": result.get("model"),
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"OpenAI Vision Fehler: {str(e)}",
        )


@app.post("/openai_chat")
async def openai_chat(prompt: str):
    """OpenAI Chat Completion API"""
    try:
        check_all_keys()
        from modules import openai_integration

        result = openai_integration.chat(prompt)
        if result.get("status") != "success":
            raise HTTPException(
                status_code=500,
                detail=(
                    "OpenAI Chat Fehler: "
                    f"{result.get('message')}"
                ),
            )

        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"OpenAI Chat Fehler: {str(e)}",
        )


@app.post("/mathpix")
async def mathpix(request: VisionRequest):
    """Mathpix OCR für mathematische Formeln"""
    return {
        "status": "success",
        "formula": "x = y",
        "note": "Mathpix Integration ausstehend",
    }


@app.get("/api_status")
async def api_status():
    """Zeigt Status aller konfigurierten APIs"""
    keys_status = {}

    required_keys = [
        "OPENAI_API_KEY", "STRIPE_API_KEY", "PAYPAL_CLIENT_ID",
        "PAYPAL_CLIENT_SECRET", "AWS_ACCESS_KEY_ID", "NFT_API_KEY"
    ]

    for key in required_keys:
        value = os.getenv(key)
        keys_status[key] = {
            "configured": bool(
                value
                and not value.startswith("test_")
                and not value.startswith("sk-test")
            ),
            "value_preview": value[:10] + "..." if value else None
        }

    return {
        "status": "ok",
        "keys": keys_status,
        "total_configured": sum(
            1 for k in keys_status.values() if k["configured"]
        )
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
