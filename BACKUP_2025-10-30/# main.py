# main.py
from fastapi import FastAPI, Header, HTTPException, status, Depends
from pydantic import BaseModel
from typing import List
import os

app = FastAPI(title="Beispiel-API mit API-Key-Authentifizierung", version="1.0.0")
API_KEY = os.getenv("API_KEY", "abcdef12345")
APP_ID = os.getenv("APP_ID", "myappid98765")

def verify_keys(x_api_key: str = Header(..., alias="X-API-KEY"), x_app_id: str = Header(..., alias="X-APP-ID")):
    if x_api_key != API_KEY or x_app_id != APP_ID:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is missing or invalid",
            headers={"WWW-Authenticate": "API-Key"},
        )

class Item(BaseModel):
    id: int
    name: str
    value: float

db: List[Item] = []

@app.get("/items", dependencies=[Depends(verify_keys)])
def get_items():
    return db

@app.post("/items", dependencies=[Depends(verify_keys)])
def create_item(item: Item):
    db.append(item)
    return {"message": "Item created", "item": item}

@app.put("/items/{item_id}", dependencies=[Depends(verify_keys)])
def update_item(item_id: int, item: Item):
    for idx, db_item in enumerate(db):
        if db_item.id == item_id:
            db[idx] = item
            return {"message": "Item updated", "item": item}
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/items/{item_id}", dependencies=[Depends(verify_keys)])
def delete_item(item_id: int):
    for idx, db_item in enumerate(db):
        if db_item.id == item_id:
            del db[idx]
            return {"message": "Item deleted"}
    raise HTTPException(status_code=404, detail="Item not found")