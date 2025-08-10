# Contributing to TBK Visual Audiobook
Thanks for helping build a faithful, cinematic adaptation of *The Brothers Karamazov*.

## Getting started
1. **Requirements**: Python 3.11, FFmpeg, Git LFS.
2. **Clone & setup**:
```bash
git lfs install
pip install -r requirements.txt
cp .env.example .env # add keys
```
Secrets (local): add to `.env` — `OPENAI_API_KEY`, `ELEVENLABS_API_KEY`, `ELEVENLABS_NARRATOR_VOICE_ID`.
Test a build:
```bash
make episode E=book1_ch2
```

## Branching & commits
- Create feature branches from main (`feat/...`, `fix/...`).
- Use Conventional Commits style (e.g., `feat(tts): add OpenAI fallback`).

## Pull requests
- Ensure CI passes (Episode Build).
- Include a short demo artifact or screenshots.
- Request at least 1 review.

## Style & quality
- Python: keep functions small; prefer pure functions for planners and builders.
- Media: commit pointers only via Git LFS; do not commit generated files under `build/`.

## Security & keys
- Never commit `.env` or raw keys. CI uses repository secrets.
- Secrets do not flow to PRs from forks; maintainers must rerun CI from branches in the main repo.

## Voice routing policy
Primary: ElevenLabs per-character voices.
Fallback: OpenAI TTS for characters missing an ElevenLabs voice, using the `openai_voice` field in `bible/characters.json`.

## Reporting issues
Use GitHub Issues; attach `build/*/log.txt` if the assembler prints errors.
