import argparse
from pathlib import Path
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
from src.config import Paths

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--episode", required=True)
    args = ap.parse_args()
    ep = args.episode
    outdir = Paths.build / ep
    outdir.mkdir(parents=True, exist_ok=True)
    audio = AudioFileClip(str(outdir / f"{ep}_narration.wav"))
    total = audio.duration
    stills = sorted((Paths.img / ep).glob("still_*.png"))
    if not stills:
        raise SystemExit("No images found. Run image_builder.")
    per = total / len(stills)
    clips = []
    for i, s in enumerate(stills):
        clip = ImageClip(str(s)).set_duration(per)
        # simple Ken Burns (zoom in/out alternate)
        if i % 2 == 0:
            clip = clip.resize(lambda t: 1 + 0.05 * (t / per))
        else:
            clip = clip.resize(lambda t: 1.05 - 0.05 * (t / per))
        clips.append(clip)
    video = concatenate_videoclips(clips, method="compose").set_audio(audio)
    raw = outdir / f"{ep}_raw.mp4"
    video.write_videofile(str(raw), fps=24, codec="libx264", audio_codec="aac")
    print(f"Wrote {raw}")
