from fastapi import FastAPI
from core.echo import Echo
from agents.oracle import Oracle
from meta.gazi import GAZI
import uvicorn

app = FastAPI()
echo = Echo()
oracle = Oracle(echo)
gazi = GAZI(oracle)

@app.get("/status")
def get_status():
    status = echo.get_instantaneous_status()
    decision = oracle.anticipate()
    return {"echo": status, "oracle": decision, "gazi": gazi.tuning}

@app.post("/optimize")
def optimize():
    gazi.audit_and_optimize()
    return {"message": "GAZI optimization triggered.", "gazi": gazi.tuning}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
