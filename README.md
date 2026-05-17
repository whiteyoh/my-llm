# Kairo

**Build it. Train it. Talk to it. Retrain it. Understand it.**

Kairo is a hands-on educational GPT lab for demystifying how language models learn.

## The idea
Kairo is a tiny transformer lab built for learning, not hype.
It uses a byte-level tokenizer so learners can see exactly what text becomes.
It is classroom and workshop friendly, and runs on modest hardware.
You learn by experimenting: train, prompt, inspect probabilities, and inspect attention.
Then retrain on new text and observe how behavior changes.

## Why it exists
Most people use AI every day without seeing how it works underneath.
Kairo makes invisible concepts visible: tokens, next-token prediction, loss, probabilities, attention, and retraining effects.
Instead of treating models like magic, learners build intuition by watching these mechanics change in real time.

## The learning loop

| Step | Learner does | Kairo shows | Concept learned |
|---|---|---|---|
| Build it | Choose text and tokenize it | Byte-level token stream | How text becomes model input |
| Train it | Train a tiny transformer | Loss over time | Prediction and error minimization |
| Talk to it | Prompt the model | Generated text + token probabilities | Sampling and uncertainty |
| Retrain it | Swap or extend training text | Before/after output shifts | Data changes behavior |
| Understand it | Inspect attention patterns | Attention table/heatmap | Pattern use, not human understanding |

## Installation
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## First successful run
Start with one tiny training run, then generate, then evaluate:

```bash
python src/train.py --input_file data/samples/space_adventure.txt --out_dir runs/demo --epochs 1 --batch_size 4 --seq_len 32 --d_model 64 --n_heads 4 --n_layers 2 --device cpu
python src/generate.py --checkpoint runs/demo/best.pt --prompt "The robot opened the door" --max_new_tokens 20 --device cpu
python src/evaluate.py --checkpoint runs/demo/best.pt --input_file data/samples/space_adventure.txt --device cpu
```

If `runs/demo/best.pt` is created and generation prints continuation text, your setup is working.

### Optional Learn Mode extras
```bash
pip install -e ".[learn]"
```

### Quality checks
```bash
pytest -q
```

## What you should see

Your exact numbers and generated text will vary run-to-run, but a successful first run should look roughly like this:

**Training (`src/train.py`)**
```text
Kairo training
Device: cpu
Parameter count: 123,456
Epoch 1: train_loss=3.21 val_loss=3.05
Saved best checkpoint: runs/demo/best.pt
```

**Generation (`src/generate.py`)**
```text
Kairo Generation
Prompt: The robot opened the door
Sampling: max_new_tokens=20 temperature=1.0 top_k=40 top_p=1.0
Output: The robot opened the door and saw a flicker of blue lights...
```

**Evaluation (`src/evaluate.py`)**
```text
loss: 3.02
perplexity: 20.49
token_count: 987
sequence_count: 955
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
