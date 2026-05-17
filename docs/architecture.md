# Architecture

## Why Kairo + `tiny_llm`
Kairo is the product/learning experience name. `tiny_llm` is the internal Python package containing reusable model and learning logic.

## Learn Mode flow
UI (`src/kairo_learn.py`) orchestrates sections; helper logic lives in `src/tiny_llm/learn.py`.

## Attention visualisation flow
Prompt -> tokenize -> model forward with `return_attn=True` -> select layer/head -> matrix/table output for heatmap-style rendering.

## Experiment persistence flow
Save writes `metadata.json` + `model.pt`. Load supports metadata and model restoration from config + checkpoint.

## Safety flow
Safe mode checks prompts, filters outputs, and supports custom banned terms.
