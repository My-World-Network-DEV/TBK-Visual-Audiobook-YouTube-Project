# Karamazov Visual Audiobook — Pipeline

## Project vision
- Narration and character performances with distinct AI-generated voices.
- High-quality, photo-realistic visuals in a consistent style.
- Narrative flow that preserves Dostoevsky's text.
- Emotional immersion through voice, pacing, and visuals.
- Cohesive episodes for platforms like YouTube.

## Quick start
0. **Git LFS**: `git lfs install`
1. **Python** 3.10+ recommended. Install FFmpeg on your system.
2. Copy `.env.example` → `.env` and fill keys.
3. `pip install -r requirements.txt`
4. Place your excerpt at `book/book1_ch2.txt` (or change `E` value).
5. Run: `make episode E=book1_ch2`

Outputs in `build/book1_ch2/`:
- `book1_ch2.mp4` (h264/aac)
- `book1_ch2.srt` (captions)
- `thumb_book1_ch2.png`

### Make targets
- `make plan E=...` → generate `shots/{E}.yaml`
- `make tts E=...` → synth narration (and/or character stems)
- `make images E=...` → generate stills from prompts
- `make edit E=...` → assemble timeline
- `make export E=...` → finalize (loudness, mux captions)
- `make episode E=...` → all of the above
- `make clean` → remove builds and images

## Notes
- Voices default to **ElevenLabs**; fallback to **OpenAI TTS** if a voice is missing (see `bible/characters.json`).
- Images default to **OpenAI gpt-image-1**.
- Character-by-character stems are supported; default is a single narration stem for POC.
- For rock-solid visual identity, add reference images to `assets/refs/` and expand prompts.
- Secrets do not flow to PRs from forks; maintainers must rerun CI.
