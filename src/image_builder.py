import argparse, base64, os
from pathlib import Path
import yaml, requests
from dotenv import load_dotenv
from tqdm import tqdm
from src.config import Paths, OPENAI_API_KEY, OPENAI_IMAGE_MODEL
load_dotenv()
URL = "https://api.openai.com/v1/images"
HDR = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}

def gen_image(prompt: str) -> bytes:
    data = {
        "model": OPENAI_IMAGE_MODEL,
        "prompt": prompt,
        "size": "1792x1024"
    }
    r = requests.post(URL, headers=HDR, json=data, timeout=120)
    r.raise_for_status()
    b64 = r.json()["data"][0].get("b64_json")
    return base64.b64decode(b64)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--episode", required=True)
    args = ap.parse_args()
    ep = args.episode
    shots = yaml.safe_load((Paths.shots / f"{ep}.yaml").read_text(encoding="utf-8"))
    outdir = Paths.img / ep
    outdir.mkdir(parents=True, exist_ok=True)
    style = shots.get("style_paragraph", "")
    beats = [b for s in shots.get("scenes", []) for b in s.get("beats", [])]
    n = shots.get("n_images") or max(1, len(beats))
    prompts = [(b.get("image_prompt") or "scene still") for b in beats][:n]
    for i, p in enumerate(tqdm(prompts, desc="Images"), start=1):
        full = f"{style}\n{p}"
        img = gen_image(full)
        (outdir / f"still_{i:02d}.png").write_bytes(img)
    print(f"Wrote {len(prompts)} images to img/{ep}")
