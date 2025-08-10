import argparse, re, json
from pathlib import Path
from src.config import Paths

def sentences(text: str):
    # naive split; replace with WhisperX or timestamps later
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--episode", required=True)
    args = ap.parse_args()
    ep = args.episode
    outdir = Paths.build / ep
    outdir.mkdir(parents=True, exist_ok=True)
    raw = (Paths.book / f"{ep}.txt").read_text(encoding="utf-8")
    timing = json.loads((outdir / f"{ep}_timing.json").read_text())
    total = timing.get("total_seconds", 60)
    sents = sentences(raw)
    per = max(1.5, total / max(1, len(sents)))

    def ts(sec):
        ms = int((sec - int(sec)) * 1000)
        h = int(sec // 3600); sec %= 3600
        m = int(sec // 60); s = int(sec % 60)
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

    t = 0.0
    lines = []
    for i, s in enumerate(sents, 1):
        start = t; end = min(t + per, total)
        lines.append(f"{i}\n{ts(start)} --> {ts(end)}\n{s}\n")
        t = end
    (outdir / f"{ep}.srt").write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {outdir / (ep + '.srt')}")
