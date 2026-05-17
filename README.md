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

Kairo is a hands-on educational GPT lab that helps learners inspect how language models actually work.

## The idea

Kairo makes model behavior visible:
- tokenization
- next-token prediction
- probabilities
- attention
- retraining effects

## Why it exists

Many learners meet AI through polished products that hide the mechanics.
Kairo exists to make those mechanics concrete, testable, and discussable in class.

## Learning loop

| Step | Learner action | Concept |
|---|---|---|
| Build it | Pick training text | Tokens and dataset shape |
| Train it | Run a tiny transformer | Loss and pattern learning |
| Generate | Prompt completions | Sampling and uncertainty |
| Evaluate | Inspect predictions | Confidence vs correctness |
| Chat | Iterate prompts | Behavior under interaction |
| Retrain | Change data | Distribution shift |
| Understand | Inspect attention | Influence, not understanding |

## Simple architecture

```text
Training text
   ↓
Byte tokenizer
   ↓
Sequence dataset
   ↓
TinyGPT
   ↓
Loss + updates
   ↓
Generation + inspection
```

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

```bash
python src/train.py --input_file data/samples/space_adventure.txt --out_dir runs/demo --epochs 1 --batch_size 4 --seq_len 32 --d_model 64 --n_heads 4 --n_layers 2 --device cpu
python src/generate.py --checkpoint runs/demo/best.pt --prompt "The robot opened the door" --max_new_tokens 20 --device cpu
python src/evaluate.py --checkpoint runs/demo/best.pt --input_file data/samples/space_adventure.txt --device cpu
python src/chat.py --checkpoint runs/demo/best.pt --device cpu
```

## Train / Generate / Evaluate / Chat examples

Train:

```bash
python src/train.py --input_file data/samples/space_adventure.txt --out_dir runs/demo --epochs 1 --batch_size 4 --seq_len 32 --d_model 64 --n_heads 4 --n_layers 2 --device cpu
```

Generate:

```bash
python src/generate.py --checkpoint runs/demo/best.pt --prompt "Mission log:" --max_new_tokens 40 --temperature 0.9 --top_k 20 --device cpu
```

Evaluate:

```bash
python src/evaluate.py --checkpoint runs/demo/best.pt --input_file data/samples/space_adventure.txt --batch_size 8 --seq_len 32 --device cpu
```

Chat:

```bash
python src/chat.py --checkpoint runs/demo/best.pt --temperature 0.9 --top_k 25 --max_new_tokens 64 --device cpu
```

## What you should see

With tiny datasets and tiny models, you should expect:
- short repetitive phrases
- unstable grammar
- occasional nonsense
- noticeable style shifts after retraining

That "weirdness" is the point: it reveals the mechanism.

## Learn Mode

Launch interactive Learn Mode:

```bash
streamlit run src/kairo_learn.py
```

You can walk students through:
- token previews
- training curves
- next-token probabilities
- attention maps
- retrain-and-compare experiments

## Why byte-level tokens?

Byte-level tokenization is simple, deterministic, and easy to visualize.
It avoids hidden preprocessing complexity and works on any text.

## Expected weirdness

Tiny models frequently:
- copy chunks from training text
- overfit quickly
- drift off-topic
- contradict themselves

These are valuable teaching moments, not failures.

## Common misconceptions

- "Low loss means intelligence." → No, it means lower prediction error.
- "Attention is reasoning." → No, it is weighting over previous tokens.
- "The model knows facts." → No, it predicts plausible continuations.

## Classroom use

Kairo works for:
- teacher-led demos
- pair labs
- short workshops
- independent experiments

See full pacing and facilitation in the Teacher Guide.

## Safety and supervision

Kairo includes lightweight classroom-safe checks, but it is not fully moderated.
Teacher supervision is required.

## What Kairo is not

Kairo is not:
- a production chatbot
- a benchmark-leading model
- an autonomous agent
- a replacement for critical thinking

It is a learning tool for inspecting core LLM mechanics.

## Developer quickstart

```bash
ruff check .
python -m compileall src tests
pytest -q
```

## Documentation map

- [Teacher Guide](docs/teacher_guide.md)
- [Student Worksheet](docs/student_worksheet.md)
- [Architecture](docs/architecture.md)
- [How LLMs Work](docs/how_llms_work.md)

## Roadmap

- richer evaluation visuals
- clearer experiment comparison UI
- more classroom-ready sample datasets
- additional explainability activities
