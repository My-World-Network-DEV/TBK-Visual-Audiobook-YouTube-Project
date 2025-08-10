.ONESHELL:
E ?= book1_ch2
PY := python
export PYTHONPATH := $(PWD)

plan:
$(PY) -m src.scene_planner --episode $(E)

tts:
$(PY) -m src.tts_builder --episode $(E)

images:
$(PY) -m src.image_builder --episode $(E)

captions:
$(PY) -m src.captions --episode $(E)

edit:
$(PY) -m src.assembler --episode $(E)

export: edit
bash scripts/ffmpeg_presets.sh $(E)

episode: plan tts images captions export

clean:
rm -rf build/* img/*/

.PHONY: plan tts images captions edit export episode clean
