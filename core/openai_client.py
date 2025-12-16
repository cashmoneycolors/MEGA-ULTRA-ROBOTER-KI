"""Zentrale OpenAI-Client Utilities (SDK 1.x).

Ziele:
- Einheitliche Client-Erzeugung
- Kein Hardcoding von Secrets
- Kleine Helfer für Chat/Vision zur Wiederverwendung
"""

from __future__ import annotations

import os
from typing import Any, Optional

from dotenv import load_dotenv

load_dotenv()


def get_openai_api_key() -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY fehlt in .env/Umgebung")
    return api_key


def get_openai_client(api_key: Optional[str] = None) -> Any:
    """Erzeugt einen OpenAI Client. Unterstützt SDK 1.x Importvarianten."""

    api_key = api_key or get_openai_api_key()

    try:
        from openai import OpenAI

        return OpenAI(api_key=api_key)
    except Exception:
        import openai

        return openai.OpenAI(api_key=api_key)


def chat_completion_text(
    prompt: str,
    *,
    model: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 1000,
) -> str:
    client = get_openai_client()
    model = model or os.getenv("OPENAI_CHAT_MODEL") or "gpt-4o-mini"

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=max_tokens,
    )

    return response.choices[0].message.content


def vision_completion_text(
    image_url: str,
    *,
    question: str = "Beschreibe dieses Bild detailliert.",
    model: Optional[str] = None,
    max_tokens: int = 500,
) -> str:
    client = get_openai_client()
    model = model or os.getenv("OPENAI_VISION_MODEL") or "gpt-4o-mini"

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": question},
                    {"type": "image_url", "image_url": {"url": image_url}},
                ],
            }
        ],
        max_tokens=max_tokens,
    )

    return response.choices[0].message.content
