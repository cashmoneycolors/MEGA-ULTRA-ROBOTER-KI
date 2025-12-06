"""OpenAI Integration - Vollständige GPT-4, DALL-E, Whisper Unterstützung"""
from core.key_check import require_keys
import os
from dotenv import load_dotenv

load_dotenv()

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("⚠️ openai package nicht installiert. Run: pip install openai")

@require_keys
def run(*args):
    """Testet OpenAI API Verbindung"""
    api_key = os.getenv("OPENAI_API_KEY")

    if not OPENAI_AVAILABLE:
        return {"status": "error", "message": "openai package fehlt"}

    if not api_key or api_key.startswith("sk-test"):
        return {"status": "error", "message": "OPENAI_API_KEY nicht konfiguriert"}

    try:
        client = OpenAI(api_key=api_key)

        # Test API mit einfachem Request
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say 'API Connected!'"}],
            max_tokens=10
        )

        return {
            "status": "success",
            "message": "OpenAI API verbunden",
            "response": response.choices[0].message.content,
            "models_available": ["gpt-4", "gpt-3.5-turbo", "dall-e-3", "whisper-1"]
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def chat(prompt, model="gpt-4", max_tokens=1000, temperature=0.7):
    """Chat Completion mit GPT-4 oder GPT-3.5"""
    api_key = os.getenv("OPENAI_API_KEY")

    if not OPENAI_AVAILABLE:
        raise RuntimeError("openai package nicht installiert")

    if not api_key:
        raise RuntimeError("OPENAI_API_KEY fehlt in .env")

    try:
        client = OpenAI(api_key=api_key)

        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature
        )

        return {
            "status": "success",
            "response": response.choices[0].message.content,
            "model": model,
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def generate_image(prompt, size="1024x1024", quality="standard"):
    """DALL-E 3 Bildgenerierung"""
    api_key = os.getenv("OPENAI_API_KEY")

    if not OPENAI_AVAILABLE:
        raise RuntimeError("openai package nicht installiert")

    if not api_key:
        raise RuntimeError("OPENAI_API_KEY fehlt in .env")

    try:
        client = OpenAI(api_key=api_key)

        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=size,
            quality=quality,
            n=1
        )

        return {
            "status": "success",
            "image_url": response.data[0].url,
            "prompt": prompt,
            "revised_prompt": response.data[0].revised_prompt if hasattr(response.data[0], 'revised_prompt') else None
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def transcribe_audio(audio_file_path, language="de"):
    """Whisper Audio Transkription"""
    api_key = os.getenv("OPENAI_API_KEY")

    if not OPENAI_AVAILABLE:
        raise RuntimeError("openai package nicht installiert")

    if not api_key:
        raise RuntimeError("OPENAI_API_KEY fehlt in .env")

    try:
        client = OpenAI(api_key=api_key)

        with open(audio_file_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language=language
            )

        return {
            "status": "success",
            "transcript": transcript.text,
            "language": language
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def analyze_image(image_url, question="Was siehst du auf diesem Bild?"):
    """GPT-4 Vision - Bildanalyse"""
    api_key = os.getenv("OPENAI_API_KEY")

    if not OPENAI_AVAILABLE:
        raise RuntimeError("openai package nicht installiert")

    if not api_key:
        raise RuntimeError("OPENAI_API_KEY fehlt in .env")

    try:
        client = OpenAI(api_key=api_key)

        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": question},
                    {"type": "image_url", "image_url": {"url": image_url}}
                ]
            }],
            max_tokens=500
        )

        return {
            "status": "success",
            "analysis": response.choices[0].message.content,
            "image_url": image_url
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_embeddings(text, model="text-embedding-ada-002"):
    """Text Embeddings für Vektordatenbanken"""
    api_key = os.getenv("OPENAI_API_KEY")

    if not OPENAI_AVAILABLE:
        raise RuntimeError("openai package nicht installiert")

    if not api_key:
        raise RuntimeError("OPENAI_API_KEY fehlt in .env")

    try:
        client = OpenAI(api_key=api_key)

        response = client.embeddings.create(
            model=model,
            input=text
        )

        return {
            "status": "success",
            "embeddings": response.data[0].embedding,
            "model": model,
            "dimensions": len(response.data[0].embedding)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def install():
    """Installiert OpenAI Dependencies"""
    import subprocess
    print("📦 Installiere openai...")
    subprocess.run(["pip", "install", "-U", "openai"], check=True)
    return {"status": "success", "message": "openai installiert"}

def describe():
    return "OpenAI Integration - GPT-4, DALL-E 3, Whisper, Vision, Embeddings"
