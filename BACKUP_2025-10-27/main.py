from fastapi import FastAPI, Header, HTTPException, status, Depends, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import openai
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Secure API with Authentication",
    description="A FastAPI application with API key authentication and OpenAI integration",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load API keys
API_KEY = os.getenv("API_KEY")
APP_ID = os.getenv("APP_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Validate required environment variables
if not API_KEY or not APP_ID:
    raise ValueError("API_KEY and APP_ID must be set in environment variables")

# Pydantic models
class AuthResponse(BaseModel):
    message: str

class OpenAIRequest(BaseModel):
    prompt: str
    model: str = "gpt-3.5-turbo"

class OpenAIResponse(BaseModel):
    response: str

# Dependency for authentication
def verify_keys(
    x_api_key: str = Header(..., alias="X-API-KEY"),
    x_app_id: str = Header(..., alias="X-APP-ID")
):
    if x_api_key != API_KEY or x_app_id != APP_ID:
        logger.warning(f"Unauthorized access attempt with API_KEY: {x_api_key[:10]}... and APP_ID: {x_app_id[:10]}...")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is missing or invalid",
            headers={"WWW-Authenticate": "API-Key"},
        )
    logger.info("Authentication successful")

# Health check endpoint
@app.get("/health", summary="Health Check", description="Check if the API is running")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

# Authenticated endpoint
@app.get("/something", dependencies=[Depends(verify_keys)], response_model=AuthResponse)
async def something():
    return AuthResponse(message="OK (successfully authenticated)")

@app.post("/set-openai-key", dependencies=[Depends(verify_keys)])
def set_openai_key(key: str = Form(...)):
    global OPENAI_API_KEY
    OPENAI_API_KEY = key
    # Update .env file
    with open('.env', 'r') as f:
        lines = f.readlines()
    with open('.env', 'w') as f:
        for line in lines:
            if line.startswith('OPENAI_API_KEY='):
                f.write(f'OPENAI_API_KEY={key}\n')
            else:
                f.write(line)
    return {"message": "OpenAI API key updated successfully"}

@app.get("/openai/status", dependencies=[Depends(verify_keys)])
def openai_status():
    return {"openai_key_set": bool(OPENAI_API_KEY)}

@app.post("/openai/generate", dependencies=[Depends(verify_keys)], response_model=OpenAIResponse)
def generate_openai(request: OpenAIRequest):
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=400, detail="OpenAI API key not set")

    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model=request.model,
            messages=[{"role": "user", "content": request.prompt}]
        )
        return OpenAIResponse(response=response.choices[0].message.content)
    except Exception as e:
        logger.error(f"OpenAI API error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
