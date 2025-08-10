from __future__ import annotations
import os, json
from pathlib import Path
from typing import Tuple
from src.config import Paths, OPENAI_API_KEY
# OpenAI TTS endpoint (simple):
OPENAI_TTS_URL = "https://api.openai.com/v1/audio/speech"
import requests

def get_character_voices(name: str) -> Tuple[str | None, str | None]:
    data = json.loads(Path(Paths.bible).read_text(encoding="utf-8"))
    entry = data.get(name) or {}
    return entry.get("voice_id"), entry.get("openai_voice")

def tts_openai(text: str, voice: str = "alloy") -> bytes:
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
    payload = {"model": "tts-1", "voice": voice, "input": text, "format": "mp3"}
    r = requests.post(OPENAI_TTS_URL, headers=headers, json=payload, timeout=120)
    r.raise_for_status()
    return r.content
