"""Seul fichier qui parle à Apertus. Le reste du projet appelle call_llm()."""
import os
import time

import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("APERTUS_BASE_URL", "").rstrip("/")
API_KEY = os.getenv("APERTUS_API_KEY", "")
MODELS = {
    "8b": os.getenv("APERTUS_MODEL_8B") or os.getenv("APERTUS_MODEL", ""),
    "70b": os.getenv("APERTUS_MODEL_70B", ""),
}


class LLMError(Exception):
    """Erreur lors de l'appel au modèle."""


def call_llm(
    prompt: str,
    model: str = "8b",
    system: str | None = None,
    temperature: float = 0.2,
    max_tokens: int = 800,
    retries: int = 2,
) -> str:
    if not BASE_URL or not API_KEY:
        raise LLMError("APERTUS_BASE_URL ou APERTUS_API_KEY manquant dans .env")

    model_name = MODELS.get(model)
    if not model_name:
        raise LLMError(f"Nom de modèle manquant dans .env pour '{model}'")

    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": model_name,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    last_error = None
    for attempt in range(retries + 1):
        try:
            r = requests.post(
                f"{BASE_URL}/chat/completions",
                json=payload,
                headers=headers,
                timeout=120,
            )
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"].strip()
        except (requests.RequestException, KeyError, IndexError, ValueError) as e:
            last_error = e
            time.sleep(2 * (attempt + 1))

    raise LLMError(f"Échec de l'appel au modèle : {last_error}")