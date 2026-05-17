# Teacher Guide

## Before-lesson checklist
- Python installed
- Repo cloned
- `pip install -e .` done
- Sample data available in `data/samples/`

## Hardware expectations
- CPU-only works
- 8GB RAM recommended
- No GPU required

## Setup options
- CLI-only lesson
- Learn Mode with Streamlit (`pip install -e ".[learn]"`)

## 45-minute lesson script
1. Build it (token viewer)
2. Train it (1 epoch)
3. Talk to it
4. Inspect probabilities
5. Reflection

## 90-minute workshop script
Add retraining, attention inspection, and experiment save/restore.

## Teacher controls
Use presets to clamp model/training/generation sizes. If exceeded, Kairo warns: “Teacher controls are keeping this demo CPU-friendly.”

## Attention visualisation teaching notes
Attention shows which prior tokens influenced a prediction. It does **not** mean human-like understanding.

## Experiment save/restore workflow
1. Train model
2. Save experiment
3. Load metadata
4. Restore model checkpoint

## Safeguarding notes
Safe mode is on by default. Custom banned terms apply to prompt checks and output filtering. Supervision is still required.

## Troubleshooting
- Short text errors: reduce `seq_len` or add more text.
- Slow run: pick Classroom demo preset.
- Load error: verify `metadata.json` and `model.pt` exist.

## Reflection questions
- What changed after retraining?
- Which token had strongest attention?
- Why can attention be useful but limited?
