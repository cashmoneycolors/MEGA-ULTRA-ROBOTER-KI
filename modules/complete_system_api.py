"""Complete System API Endpoints"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
from complete_system_modul import converter, business, dashboard, marketplace

app = FastAPI(title="Complete System API")

# ===== MODELS =====
class FileConversionRequest(BaseModel):
    file_input: str
    file_type: str = "auto"
    output_format: str = "text"

class UserRegistration(BaseModel):
    username: str
    email: str
    password: str

class PaymentRequest(BaseModel):
    user_id: str
    amount: float
    plan: str

class FileUploadRequest(BaseModel):
    user_id: str
    filename: str
    file_data: str
    file_type: str = "auto"

class ArtProductRequest(BaseModel):
    artist_id: str
    title: str
    category: str
    price: float

class CustomOrderRequest(BaseModel):
    customer_id: str
    order_type: str
    description: str = ""

# ===== CONVERTER ENDPOINTS =====
@app.post("/api/convert")
async def convert_file(request: FileConversionRequest):
    """Convert any file format"""
    result = converter.convert_any_file(request.file_input, request.file_type, request.output_format)
    return result

@app.get("/api/converter/formats")
async def get_supported_formats():
    """Get all supported formats"""
    return {
        "success": True,
        "total_formats": len(converter.supported_formats),
        "formats": converter.supported_formats
    }

# ===== BUSINESS SYSTEM ENDPOINTS =====
@app.post("/api/user/register")
async def register_user(request: UserRegistration):
    """Register new user"""
    result = business.register_user(request.username, request.email, request.password)
    return result

@app.post("/api/payment/create")
async def create_payment(request: PaymentRequest):
    """Create PayPal payment"""
    result = business.create_paypal_payment(request.user_id, request.amount, request.plan)
    return result

@app.post("/api/file/upload")
async def upload_file(request: FileUploadRequest):
    """Upload file"""
    result = business.upload_file(request.user_id, request.filename, request.file_data, request.file_type)
    return result

# ===== DASHBOARD ENDPOINTS =====
@app.get("/api/dashboard/earnings/{user_id}")
async def get_earnings(user_id: str):
    """Get live earnings"""
    result = dashboard.get_live_earnings(user_id)
    return result

@app.get("/api/dashboard/articles/{user_id}")
async def get_articles(user_id: str):
    """Get articles overview"""
    result = dashboard.get_articles_overview(user_id)
    return result

# ===== MARKETPLACE ENDPOINTS =====
@app.post("/api/art/create")
async def create_art_product(request: ArtProductRequest):
    """Create art product"""
    product_data = {
        "title": request.title,
        "category": request.category,
        "price": request.price
    }
    result = marketplace.create_art_product(request.artist_id, product_data)
    return result

@app.get("/api/art/catalog/{category}")
async def get_catalog(category: str = "all"):
    """Get art catalog"""
    result = marketplace.get_art_catalog(category)
    return result

@app.post("/api/art/order")
async def create_order(request: CustomOrderRequest):
    """Create custom order"""
    order_data = {
        "type": request.order_type,
        "description": request.description
    }
    result = marketplace.create_custom_order(request.customer_id, order_data)
    return result

# ===== HEALTH CHECK =====
@app.get("/api/health")
async def health_check():
    """Health check"""
    return {
        "status": "healthy",
        "systems": {
            "converter": "active",
            "business": "active",
            "dashboard": "active",
            "marketplace": "active"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
