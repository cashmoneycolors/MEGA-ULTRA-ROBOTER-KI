"""OpenAI Integration - Chat, Vision, Images, Whisper."""

import os

from core.key_check import require_keys
from core.openai_client import get_openai_client

try:
    import openai as _openai  # noqa: F401

    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("⚠️ openai package nicht installiert. Run: pip install openai")


@require_keys
def run(*args):
    """Testet OpenAI API Verbindung"""
    if not OPENAI_AVAILABLE:
        return {"status": "error", "message": "openai package fehlt"}

    try:
        client = get_openai_client()

        # Test API mit einfachem Request
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_SMOKE_MODEL") or "gpt-4o-mini",
            messages=[{"role": "user", "content": "Say 'API Connected!'"}],
            max_tokens=10
        )

        return {
            "status": "success",
            "message": "OpenAI API verbunden",
            "response": response.choices[0].message.content,
            "models_available": [
                "gpt-4o",
                "gpt-4o-mini",
                "dall-e-3",
                "whisper-1",
            ],
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@require_keys
def chat(prompt, model="gpt-4", max_tokens=1000, temperature=0.7):
    """Chat Completion mit GPT-4 oder GPT-3.5"""
    if not OPENAI_AVAILABLE:
        raise RuntimeError("openai package nicht installiert")

    try:
        client = get_openai_client()
        model = model or os.getenv("OPENAI_CHAT_MODEL") or "gpt-4o-mini"

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


@require_keys
def generate_image(prompt, size="1024x1024", quality="standard"):
    """DALL-E 3 Bildgenerierung"""
    if not OPENAI_AVAILABLE:
        raise RuntimeError("openai package nicht installiert")

    try:
        client = get_openai_client()

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
            "revised_prompt": (
                response.data[0].revised_prompt
                if hasattr(response.data[0], "revised_prompt")
                else None
            ),
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@require_keys
def transcribe_audio(audio_file_path, language="de"):
    """Whisper Audio Transkription"""
    if not OPENAI_AVAILABLE:
        raise RuntimeError("openai package nicht installiert")

    try:
        client = get_openai_client()

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


@require_keys
def analyze_image(image_url, question="Was siehst du auf diesem Bild?"):
    """GPT-4 Vision - Bildanalyse"""
    if not OPENAI_AVAILABLE:
        raise RuntimeError("openai package nicht installiert")

    try:
        client = get_openai_client()
        vision_model = os.getenv("OPENAI_VISION_MODEL") or "gpt-4o-mini"

        response = client.chat.completions.create(
            model=vision_model,
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
            "image_url": image_url,
            "model": vision_model,
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@require_keys
def get_embeddings(text, model="text-embedding-ada-002"):
    """Text Embeddings für Vektordatenbanken"""
    if not OPENAI_AVAILABLE:
        raise RuntimeError("openai package nicht installiert")

    try:
        client = get_openai_client()
        model = (
            model
            or os.getenv("OPENAI_EMBEDDING_MODEL")
            or "text-embedding-3-small"
        )

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


@require_keys
def install():
    """Installiert OpenAI Dependencies"""
    import subprocess

    print("📦 Installiere openai...")
    subprocess.run(["pip", "install", "-U", "openai"], check=True)
    return {"status": "success", "message": "openai installiert"}


def describe():
    return "OpenAI Integration - Chat, Vision, DALL-E 3, Whisper, Embeddings"
