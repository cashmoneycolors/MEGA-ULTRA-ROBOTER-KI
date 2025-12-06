from flask import Blueprint, jsonify
import requests

monitoring_bp = Blueprint('monitoring', __name__)
PYTHON_API = "http://127.0.0.1:8000"
C_SHARP_API = "http://127.0.0.1:5000"

@monitoring_bp.route('/monitor/status')
def monitor_status():
    py = requests.get(f"{PYTHON_API}/status").json()
    try:
        cs = requests.get(f"{C_SHARP_API}/status").json()
    except Exception:
        cs = {"error": "C#-API nicht erreichbar"}
    return jsonify({"python": py, "csharp": cs})

@monitoring_bp.route('/monitor/selfheal', methods=['POST'])
def monitor_selfheal():
    # Beispiel: Triggert Self-Healing über beide APIs
    py = requests.post(f"{PYTHON_API}/optimize").json()
    try:
        cs = requests.post(f"{C_SHARP_API}/optimize").json()
    except Exception:
        cs = {"error": "C#-API nicht erreichbar"}
    return jsonify({"python": py, "csharp": cs})
