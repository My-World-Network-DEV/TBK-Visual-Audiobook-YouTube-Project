import argparse, json, os
from pathlib import Path
from dotenv import load_dotenv
from pydub import AudioSegment
from src.config import Paths, ELEVENLABS_API_KEY, ELEVENLABS_MODEL_ID
import requests
from src.voice_router import get_character_voices, tts_openai
load_dotenv()
BASE = "https://api.elevenlabs.io/v1"
HDR = {"xi-api-key": ELEVENLABS_API_KEY, "accept": "audio/mpeg", "Content-Type": "application/json"}

def tts(voice_id: str, text: str) -> bytes:
    url = f"{BASE}/text-to-speech/{voice_id}"
    data = {
        "model_id": ELEVENLABS_MODEL_ID,
        "text": text,
        "voice_settings": {"stability": 0.6, "similarity_boost": 0.8}
    }
    r = requests.post(url, headers=HDR, json=data, timeout=120)
    r.raise_for_status()
    return r.content

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--episode", required=True)
    ap.add_argument("--mode", choices=["narration", "dialogue"], default="narration")
    args = ap.parse_args()
    ep = args.episode
    outdir = Paths.build / ep
    outdir.mkdir(parents=True, exist_ok=True)
    if args.mode == "narration":
        text = (Paths.book / f"{ep}.txt").read_text(encoding="utf-8")
        el_voice, oa_voice = get_character_voices("narrator")
        if el_voice:
            mp3_bytes = tts(el_voice, text)
        else:
            if not oa_voice:
                oa_voice = "alloy"
            mp3_bytes = tts_openai(text, voice=oa_voice)
        audio_path = outdir / f"{ep}_narration.mp3"
        audio_path.write_bytes(mp3_bytes)
        seg = AudioSegment.from_file(audio_path)
        seg.export(outdir / f"{ep}_narration.wav", format="wav")
        dur = len(seg) / 1000.0
        (outdir / f"{ep}_timing.json").write_text(json.dumps({"total_seconds": dur}, indent=2))
        print(f"Wrote {audio_path}")
    else:
        raise SystemExit("Dialogue mode scaffold to be expanded later.")
