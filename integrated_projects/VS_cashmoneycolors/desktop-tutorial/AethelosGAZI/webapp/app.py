from flask import Flask, render_template, request, jsonify
import requests
from payment import payment_bp
from monitoring import monitoring_bp
from local_storage import local_storage_bp

app = Flask(__name__)

PYTHON_API = "http://127.0.0.1:8081"
C_SHARP_API = "http://127.0.0.1:5000"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/status")
def status():
    py_status = requests.get(f"{PYTHON_API}/status").json()
    try:
        cs_status = requests.get(f"{C_SHARP_API}/status").json()
    except Exception:
        cs_status = {"error": "C#-API nicht erreichbar"}
    return jsonify({"python": py_status, "csharp": cs_status})

@app.route("/optimize", methods=["POST"])
def optimize():
    py_result = requests.post(f"{PYTHON_API}/optimize").json()
    try:
        cs_result = requests.post(f"{C_SHARP_API}/optimize").json()
    except Exception:
        cs_result = {"error": "C#-API nicht erreichbar"}
    return jsonify({"python": py_result, "csharp": cs_result})

# Payment-, Monitoring- und Local-Storage-Blueprints einbinden
app.register_blueprint(payment_bp)
app.register_blueprint(monitoring_bp)
app.register_blueprint(local_storage_bp)

if __name__ == "__main__":
    app.run(debug=True, port=3000)
