import argparse, json, yaml
from pathlib import Path
from dotenv import load_dotenv
from src.config import Paths, OPENAI_API_KEY, OPENAI_PLANNER_MODEL, ROOT
load_dotenv()
# Uses OpenAI Responses API via HTTP (SDK optional). Minimal requests version below.
import requests
SYSTEM = (
"You are a disciplined scene/beat planner. Output compact JSON with keys: "
"scenes, dialogue, n_images, style_paragraph."
)

def call_openai_plan(prompt: str) -> dict:
    url = "https://api.openai.com/v1/responses"
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": OPENAI_PLANNER_MODEL,
        "input": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": prompt}
        ],
        "response_format": {"type": "json_object"}
    }
    r = requests.post(url, headers=headers, json=data, timeout=120)
    r.raise_for_status()
    out = r.json()
    # Responses API returns consolidated text in output_text or the first content part
    text = None
    if "output_text" in out:
        text = out["output_text"]
    else:
        parts = out.get("output", [{}])[0].get("content", [])
        text = "".join(p.get("text", "") for p in parts)
    return json.loads(text)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--episode", required=True)
    args = ap.parse_args()
    ep = args.episode
    txt_path = Paths.book / f"{ep}.txt"
    prompt_path = ROOT / "prompts" / "scene_planner.md"
    if not txt_path.exists():
        raise SystemExit(f"Excerpt not found: {txt_path}")
    excerpt = txt_path.read_text(encoding="utf-8")
    instr = prompt_path.read_text(encoding="utf-8")
    plan = call_openai_plan(instr + "\n\nEXCERPT:\n" + excerpt[:12000])
    plan["meta"] = {"episode": ep}
    out = {k: plan.get(k) for k in ["meta", "style_paragraph", "scenes", "dialogue", "n_images"]}
    (Paths.shots / f"{ep}.yaml").write_text(yaml.safe_dump(out, sort_keys=False), encoding="utf-8")
    print(f"Wrote shots/{ep}.yaml")
