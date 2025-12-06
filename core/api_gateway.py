"""API Gateway + Load Balancer + Monitoring"""
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
import time
import psutil
import sqlite3
from datetime import datetime
from typing import Dict, Any
import jwt
import os
from functools import wraps
import asyncio

app = FastAPI(title="Kontrollzentrum Gateway")

# ===== METRICS =====
class Metrics:
    def __init__(self):
        self.requests = 0
        self.errors = 0
        self.total_time = 0
        self.start_time = time.time()
    
    def get_stats(self) -> Dict:
        uptime = time.time() - self.start_time
        cpu = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory().percent
        return {
            "uptime_seconds": uptime,
            "requests": self.requests,
            "errors": self.errors,
            "avg_response_time": self.total_time / max(self.requests, 1),
            "cpu_percent": cpu,
            "memory_percent": memory
        }

metrics = Metrics()

# ===== DATABASE =====
def init_db():
    conn = sqlite3.connect("kontrollzentrum.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS requests (
        id INTEGER PRIMARY KEY,
        timestamp TEXT,
        module TEXT,
        status TEXT,
        response_time REAL,
        error TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS cache (
        key TEXT PRIMARY KEY,
        value TEXT,
        expires_at REAL
    )""")
    conn.commit()
    conn.close()

init_db()

def log_request(module: str, status: str, response_time: float, error: str = None):
    conn = sqlite3.connect("kontrollzentrum.db")
    c = conn.cursor()
    c.execute("INSERT INTO requests VALUES (NULL, ?, ?, ?, ?, ?)",
              (datetime.now().isoformat(), module, status, response_time, error))
    conn.commit()
    conn.close()

# ===== AUTH =====
SECRET_KEY = os.getenv("JWT_SECRET", "dev-secret-key-change-in-production")

def verify_token(token: str) -> Dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

async def get_token(request: Request):
    auth = request.headers.get("Authorization")
    if not auth:
        raise HTTPException(status_code=401, detail="Missing token")
    token = auth.replace("Bearer ", "")
    return verify_token(token)

# ===== CIRCUIT BREAKER =====
class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.last_failure = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
    
    def call(self, func, *args, **kwargs):
        if self.state == "OPEN":
            if time.time() - self.last_failure > self.timeout:
                self.state = "HALF_OPEN"
            else:
                raise Exception(f"Circuit breaker OPEN for {self.timeout}s")
        
        try:
            result = func(*args, **kwargs)
            if self.state == "HALF_OPEN":
                self.state = "CLOSED"
                self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure = time.time()
            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"
            raise e

breakers = {}

def get_breaker(module_name: str) -> CircuitBreaker:
    if module_name not in breakers:
        breakers[module_name] = CircuitBreaker()
    return breakers[module_name]

# ===== MIDDLEWARE =====
@app.middleware("http")
async def monitoring_middleware(request: Request, call_next):
    start = time.time()
    metrics.requests += 1
    
    try:
        response = await call_next(request)
        response_time = time.time() - start
        metrics.total_time += response_time
        
        module = request.url.path.split("/")[-1]
        log_request(module, "success", response_time)
        
        response.headers["X-Response-Time"] = str(response_time)
        return response
    except Exception as e:
        response_time = time.time() - start
        metrics.errors += 1
        metrics.total_time += response_time
        
        module = request.url.path.split("/")[-1]
        log_request(module, "error", response_time, str(e))
        
        return JSONResponse({"error": str(e)}, status_code=500)

# ===== ENDPOINTS =====
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/metrics")
async def get_metrics():
    return metrics.get_stats()

@app.post("/execute/{module_name}")
async def execute_module(module_name: str, request: Request, token: Dict = Depends(get_token)):
    """Execute module with circuit breaker protection"""
    try:
        breaker = get_breaker(module_name)
        
        # Import and execute module
        import importlib
        mod = importlib.import_module(f"modules.{module_name}")
        
        def execute():
            return mod.run()
        
        result = breaker.call(execute)
        return {"module": module_name, "result": result, "status": "success"}
    
    except Exception as e:
        metrics.errors += 1
        return JSONResponse({"error": str(e), "module": module_name}, status_code=500)

@app.get("/status/{module_name}")
async def module_status(module_name: str):
    """Get module status and circuit breaker state"""
    breaker = get_breaker(module_name)
    return {
        "module": module_name,
        "circuit_breaker": breaker.state,
        "failures": breaker.failure_count
    }

@app.get("/logs")
async def get_logs(limit: int = 100, token: Dict = Depends(get_token)):
    """Get request logs"""
    conn = sqlite3.connect("kontrollzentrum.db")
    c = conn.cursor()
    c.execute("SELECT * FROM requests ORDER BY id DESC LIMIT ?", (limit,))
    logs = [{"id": row[0], "timestamp": row[1], "module": row[2], "status": row[3], 
             "response_time": row[4], "error": row[5]} for row in c.fetchall()]
    conn.close()
    return logs

# ===== GRACEFUL SHUTDOWN =====
@app.on_event("shutdown")
async def shutdown():
    print("🛑 Graceful shutdown initiated...")
    await asyncio.sleep(1)
    print("✅ All connections closed")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
