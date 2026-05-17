<p align="center">
  <img src="docs/assets/kairo-logo.svg" alt="Kairo logo" width="760"/>
</p>

<p align="center">
  <strong>Build it. Train it. Talk to it. Retrain it. Understand it.</strong>
</p>

<p align="center">
  <a href="README.md">Home</a> •
  <a href="docs/teacher_guide.md">Teacher Guide</a> •
  <a href="docs/student_worksheet.md">Student Worksheet</a> •
  <a href="docs/architecture.md">Architecture</a> •
  <a href="docs/how_llms_work.md">How LLMs Work</a>
</p>

---

# Kairo

Kairo is a hands-on educational GPT lab for demystifying how language models learn.

## The idea

Kairo is designed to help learners understand:
- tokenisation
- prediction
- probabilities
- attention
- retraining effects

Instead of treating AI like magic, Kairo exposes the mechanics directly.

## The learning loop

| Step | Learner does | Concept learned |
|---|---|---|
| Build it | Choose training text | Tokenisation |
| Train it | Train a tiny transformer | Prediction and loss |
| Talk to it | Prompt the model | Sampling |
| Retrain it | Change the data | Behaviour shifts |
| Understand it | Inspect attention/probabilities | Pattern learning |

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

Optional Learn Mode:

```bash
pip install -e ".[learn]"
```

## Try it in 3 minutes

Train:

```bash
python src/train.py --input_file data/samples/space_adventure.txt --out_dir runs/demo --epochs 1 --batch_size 4 --seq_len 32 --d_model 64 --n_heads 4 --n_layers 2 --device cpu
```

Generate:

```bash
python src/generate.py --checkpoint runs/demo/best.pt --prompt "The robot opened the door" --max_new_tokens 20 --device cpu
```

Learn Mode:

```bash
streamlit run src/kairo_learn.py
```

## What you should expect

Tiny language models often:
- repeat text
- produce strange grammar
- drift off-topic
- overfit tiny datasets

This is normal and educationally useful.

## Common misconceptions

- Attention is not human reasoning.
- Lower loss does not mean intelligence.
- Outputs depend heavily on training data.
- Tiny models are prediction systems, not minds.

## Documentation

- `docs/teacher_guide.md`
- `docs/student_worksheet.md`
- `docs/architecture.md`
- `docs/how_llms_work.md`
