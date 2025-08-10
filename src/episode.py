import argparse
import subprocess
from src.config import ROOT

STEPS = ["scene_planner", "tts_builder", "image_builder", "captions", "assembler"]

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--episode", required=True)
    args = ap.parse_args()
    for step in STEPS:
        print(f"\n=== Running {step} ===")
        subprocess.check_call([
            "python", "-m", f"src.{step}", "--episode", args.episode
        ], cwd=ROOT)
    # finalize via scripts/ffmpeg_presets.sh (Makefile handles this)
