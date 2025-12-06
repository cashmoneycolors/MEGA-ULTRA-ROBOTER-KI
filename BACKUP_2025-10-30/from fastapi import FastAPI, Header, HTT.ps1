from fastapi import FastAPI, Header, HTTPException, status, Depends
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

API_KEY = os.getenv("API_KEY")
APP_ID = os.getenv("APP_ID")

def verify_keys(
    x_api_key: str = Header(..., alias="X-API-KEY"),
    x_app_id: str = Header(..., alias="X-APP-ID")
):
    if x_api_key != API_KEY or x_app_id != APP_ID:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is missing or invalid",
            headers={"WWW-Authenticate": "API-Key"},
        )

@app.get("/something", dependencies=[Depends(verify_keys)])
def something():
    return {"message": "OK (successfully authenticated)"}