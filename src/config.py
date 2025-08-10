from dataclasses import dataclass
from pathlib import Path
import os

ROOT = Path(__file__).resolve().parents[1]

@dataclass
class Paths:
    book = ROOT / "book"
    shots = ROOT / "shots"
    img = ROOT / "img"
    build = ROOT / "build"
    bible = ROOT / "bible" / "characters.json"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
OPENAI_PLANNER_MODEL = os.getenv("OPENAI_PLANNER_MODEL", "gpt-5")
OPENAI_IMAGE_MODEL = os.getenv("OPENAI_IMAGE_MODEL", "gpt-image-1")
ELEVENLABS_MODEL_ID = os.getenv("ELEVENLABS_MODEL_ID", "eleven_multilingual_v2")
NARRATOR_VOICE_ID = os.getenv("ELEVENLABS_NARRATOR_VOICE_ID", "")

Paths.build.mkdir(exist_ok=True)
Paths.img.mkdir(exist_ok=True)
Paths.shots.mkdir(exist_ok=True)
