<p align="center">
  <img src="docs/assets/kairo-logo.svg" alt="Kairo logo" width="760"/>
</p>
<p align="center">
  <strong>Build it. Train it. Talk to it. Retrain it. Understand it.</strong>
</p>
<p align="center">
  <a href="README.md">Home</a> • <a href="STEP_BY_STEP.md">Step-by-Step</a> • <a href="docs/first_lesson_walkthrough.md">First Lesson</a> • <a href="docs/teacher_guide.md">Teacher Guide</a> • <a href="docs/student_worksheet.md">Student Worksheet</a> • <a href="docs/architecture.md">Architecture</a> • <a href="docs/how_llms_work.md">How LLMs Work</a>
</p>

---

# Kairo

Kairo is a classroom-ready mini LLM lab for making AI behavior visible. Learners
train a tiny transformer, compare outputs before and after changing the training
data, and inspect token probabilities and attention so LLMs feel understandable
rather than magical.

---

## Why Kairo?

Kairo helps learners understand how language models learn from text by making the hidden steps visible and discussable. Students can inspect tokenization, next-token prediction, loss trends, retraining effects, probability distributions, and attention patterns.

It is designed for classrooms, STEM clubs, workshops, and self-learning where people need a clear, hands-on model of how LLM behavior changes with data.

---

## What you will see

- Normal story-style output before retraining.
- A changed style after pirate retraining with different vocabulary and rhythm.
- A realistic reminder that tiny models may repeat themselves or produce strange text, which is useful for learning.

---

## Who This Is For

- Teachers running AI literacy lessons
- Middle/high school students learning ML basics
- Clubs and workshops wanting hands-on LLM demos
- Developers who want a tiny transparent transformer example

---

## What You Can Do

- Train a small byte-level GPT model on local text.
- Generate text from saved checkpoints.
- Compare the same prompt across different datasets.
- Evaluate loss and perplexity on a dataset.
- Use Learn Mode to inspect tokens, probabilities, attention, and retrain effects.
- Print classroom-ready teacher and student materials.

## Why it exists

Many AI tools hide how models behave. Kairo surfaces the mechanism so students
can observe, test, and discuss model behavior with evidence.

## The magic moment

Train on normal stories, then retrain on pirate text and watch style shift immediately.

Same model architecture. Different data. Different behavior.

---

## Project layout

| Path | Purpose |
|---|---|
| `src/train.py` | Train a checkpoint (`best.pt`, `last.pt`, metrics, config). |
| `src/generate.py` | Generate text from a checkpoint. |
| `src/evaluate.py` | Report loss and perplexity for a checkpoint and dataset. |
| `src/chat.py` | Run a small terminal chat loop from a checkpoint. |
| `src/qa.py` | Ask question/answer prompts from a checkpoint (optional context). |
| `src/build_qa_corpus.py` | Convert JSONL Q/A records into training text. |
| `src/kairo_learn.py` | Streamlit Learn Mode for classroom exploration. |
| `src/tiny_llm/` | Tokenizer, model, generation, attention, safety, and Learn Mode helpers. |
| `data/samples/` | Starter datasets for lessons and demos. |
| `data/samples/README.md` | Intro + insight guide for each training text file. |
| `docs/` | Lesson guides, architecture notes, and printable sources. |
| `tools/pdf/` | Printable PDF generation tooling. |
| `tests/` | Smoke, model, dataset, safety, docs, and helper tests. |

---

## Step-by-step learning flow

1. **Normal stories:** train on a neutral dataset (for example `space_adventure.txt`).
2. **Compare:** generate from a fixed prompt and record the output.
3. **Pirate style:** retrain on `pirate_dialogue.txt` and compare tone/word choices.
4. **Questions:** ask what changed and why, using output evidence.
5. **Learn Mode:** inspect token probabilities and attention maps.

---

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

Optional extras:

```bash
pip install -e ".[learn]"
pip install -e ".[pdf]"
pip install -e ".[dev]"
```

Contributor setup (installs everything needed for checks, tests, and printables):

```bash
pip install -e ".[dev,learn,pdf]"
```

---

## Quickstart commands

After `pip install -e .`, you can use either the `kairo-*` commands or the
script paths shown in older examples.

Train:

```bash
kairo-train --input_file data/samples/space_adventure.txt --out_dir runs/demo --epochs 1 --batch_size 4 --seq_len 32 --d_model 64 --n_heads 4 --n_layers 2 --device cpu
```

Generate:

```bash
kairo-generate --checkpoint runs/demo/best.pt --prompt "The robot opened the door" --max_new_tokens 20 --device cpu
```

Evaluate:

```bash
kairo-evaluate --checkpoint runs/demo/best.pt --input_file data/samples/space_adventure.txt --device cpu
```

Chat:

```bash
kairo-chat --checkpoint runs/demo/best.pt --device cpu
```

Build a QA training corpus from JSONL records:

```bash
kairo-build-qa-corpus --input_jsonl qa_space_facts.jsonl --output_file runs/qa_space_facts.txt
```

The QA sample JSONL is included in both `data/samples/` (repo use) and
`src/tiny_llm/samples/` (packaged installs).
You can pass either a full path or just the bundled sample name.

Train and ask QA with context:

```bash
kairo-train --input_file runs/qa_space_facts.txt --out_dir runs/qa_demo --epochs 1 --batch_size 4 --seq_len 32 --d_model 64 --n_heads 4 --n_layers 2 --device cpu
kairo-qa --checkpoint runs/qa_demo/best.pt --question "Who pilots the Aurora?" --context "Captain Rowan is the pilot of the starship Aurora."
```

`kairo-qa` now includes a classroom-safe grounding fallback: if the generated
answer looks low-quality and a context is supplied, it returns the best matching
context sentence instead of random token noise.

Learn Mode (after installing the `learn` extra):

```bash
kairo-learn
```

Agent operations dashboard (after installing the `learn` extra):

```bash
kairo-agents-dashboard
```

The dashboard reads agent definitions from `.Codex/agents/` and `Codex/agents/`,
shows live status by agent, and stores session state in `runs/agent_dashboard/state.json`.

Regenerate classroom PDFs:

```bash
python tools/pdf/generate_printables.py
python tools/pdf/generate_tech_i_can_book.py
```

Use `python tools/pdf/generate_printables.py letter` for US Letter output.

Run quality checks:

```bash
ruff check .
python -m compileall src tests tools
pytest -q
```

---

## Documentation map

- [Step-by-Step Guide](STEP_BY_STEP.md)
- [First Lesson Walkthrough](docs/first_lesson_walkthrough.md)
- [Teacher Guide](docs/teacher_guide.md)
- [Student Worksheet](docs/student_worksheet.md)
- [Architecture](docs/architecture.md)
- [How LLMs Work](docs/how_llms_work.md)
- [Sample Training Text Guide](data/samples/README.md)

### Printable lesson packs

- [Teacher Guide (PDF)](docs/printable/teacher_guide.pdf)
- [Student Worksheet (PDF)](docs/printable/student_worksheet.pdf)
- [First Lesson Walkthrough (PDF)](docs/printable/first_lesson_walkthrough.pdf)
- [Tech I Can: Kairo Book (PDF)](docs/printable/Tech_I_Can_Kairo_Book.pdf)

### Assets and diagrams

- [Kairo logo](docs/assets/kairo-logo.svg)
- [Simple architecture flowchart](docs/assets/simple-architecture-flowchart.svg)
- [Learn Mode token preview](docs/assets/learn-mode-token-preview.svg)
- [Learn Mode attention map](docs/assets/learn-mode-attention-map.svg)
- [Learn Mode probability table](docs/assets/learn-mode-probability-table.svg)
- [Learn Mode retrain compare](docs/assets/learn-mode-retrain-compare.svg)

---

## Classroom safety and scope

Kairo is a local learning tool, not a production chatbot. It includes lightweight
classroom safety checks, but teachers should still supervise prompts, training
data, and generated outputs. The model can repeat, drift, or sound confident
while being wrong; those limitations are part of the lesson.

---

<p align="center">
  <a href="README.md">Home</a> • <a href="STEP_BY_STEP.md">Step-by-Step</a> • <a href="docs/first_lesson_walkthrough.md">First Lesson</a> • <a href="docs/teacher_guide.md">Teacher Guide</a> • <a href="docs/student_worksheet.md">Student Worksheet</a> • <a href="docs/architecture.md">Architecture</a> • <a href="docs/how_llms_work.md">How LLMs Work</a>
</p>
