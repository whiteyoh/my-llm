# Kairo

**Build it. Train it. Talk to it. Retrain it. Understand it.**

## The idea
Kairo is a tiny language-model lab for classrooms.
You pick text and turn it into tokens.
You train a small CPU-friendly model and watch loss change.
You prompt it, inspect probabilities, and compare retrains.
You inspect attention to see pattern use, not human-like understanding.

## Why it exists
Most people use AI systems without seeing what is happening inside them. Kairo makes hidden mechanics visible so learners can experiment, ask better questions, and build intuition.

## The learning loop

| Step | Learner does | Kairo shows | Concept learned |
|---|---|---|---|
| Build it | choose text | byte tokens | tokenisation |
| Train it | train tiny model | loss chart | prediction error |
| Talk to it | prompt model | output + probabilities | sampling |
| Retrain it | change data | before/after output | data changes behaviour |
| Understand it | inspect attention | attention table/heatmap | pattern use, not human understanding |

## Installation
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

### Optional Learn Mode extras
```bash
pip install -e ".[learn]"
```

### Quality checks
```bash
pytest -q
```

## Try it in 3 minutes
```bash
python src/train.py --input_file data/samples/space_adventure.txt --out_dir runs/demo --epochs 1 --batch_size 4 --seq_len 32 --d_model 64 --n_heads 4 --n_layers 2 --device cpu
python src/generate.py --checkpoint runs/demo/best.pt --prompt "The robot opened the door" --max_new_tokens 20 --device cpu
python src/evaluate.py --checkpoint runs/demo/best.pt --input_file data/samples/space_adventure.txt --device cpu
```

## Learn Mode
```bash
streamlit run src/kairo_learn.py
```
Includes token viewer, loss chart, probability table, attention view, retrain comparison, and experiment save/restore.

## Classroom use
Designed for teacher-led demos, secondary school lessons, STEM clubs, and workshops.

## Safety and supervision
Kairo includes lightweight guardrails, not full moderation. Teacher supervision is required.

## What Kairo is not
- not a production LLM
- not instruction-tuned
- not fully moderated
- not a chatbot replacement

## Developer quickstart
Install deps, run train/generate/evaluate/chat scripts, then run tests:
```bash
pip install -e .
pytest -q
```

## Documentation map
- `docs/teacher_guide.md`
- `docs/student_worksheet.md`
- `docs/architecture.md`
- `docs/how_llms_work.md`

## Roadmap
- better attention visuals
- save/load Learn Mode sessions
- lesson packs
- printable worksheets
- richer experiment comparison
