# Kairo

**Build it. Train it. Talk to it. Retrain it. Understand it.**

Kairo is a hands-on educational GPT lab for demystifying how language models learn.

---

## The idea

Kairo is a tiny transformer lab built for learning, not hype.

It uses a byte-level tokenizer so learners can see exactly what text becomes before it reaches the model.

Kairo is designed for:
- classrooms
- workshops
- STEM clubs
- self-learning
- developers curious about transformers

You learn by experimenting:
- train a tiny model
- prompt it
- inspect probabilities
- inspect attention
- retrain on new text
- observe how behaviour changes

---

## Why it exists

Most people use AI every day without seeing how it works underneath.

Kairo makes invisible concepts visible:
- tokens
- next-token prediction
- loss
- probabilities
- attention
- retraining effects

Instead of treating models like magic, learners build intuition by watching these mechanics change in real time.

---

## The learning loop

| Step | Learner does | Kairo shows | Concept learned |
|---|---|---|---|
| Build it | Choose text and tokenize it | Byte-level token stream | How text becomes model input |
| Train it | Train a tiny transformer | Loss over time | Prediction and error minimisation |
| Talk to it | Prompt the model | Generated text + token probabilities | Sampling and uncertainty |
| Retrain it | Swap or extend training text | Before/after output shifts | Data changes behaviour |
| Understand it | Inspect attention patterns | Attention table/heatmap | Pattern use, not human understanding |

---

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
 Prediction loss
      ↓
 Text generation
```

---

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

Supported:
- Python 3.11+
- CPU-first workflows
- Optional CUDA acceleration

---

## Try it in 3 minutes

### Train

```bash
python src/train.py \
  --input_file data/samples/space_adventure.txt \
  --out_dir runs/demo \
  --epochs 1 \
  --batch_size 4 \
  --seq_len 32 \
  --d_model 64 \
  --n_heads 4 \
  --n_layers 2 \
  --device cpu
```

### Generate

```bash
python src/generate.py \
  --checkpoint runs/demo/best.pt \
  --prompt "The robot opened the door" \
  --max_new_tokens 20 \
  --device cpu
```

### Evaluate

```bash
python src/evaluate.py \
  --checkpoint runs/demo/best.pt \
  --input_file data/samples/space_adventure.txt \
  --device cpu
```

### Chat

```bash
python src/chat.py \
  --checkpoint runs/demo/best.pt \
  --device cpu
```

If `runs/demo/best.pt` is created and generation prints continuation text, your setup is working.

---

## What you should see

Exact values and generated text will vary depending on randomness and training data.

### Training example

```text
Kairo training
Device: cpu
Parameter count: 123,456

Epoch 1
train_loss=3.21
val_loss=3.05

Saved best checkpoint:
runs/demo/best.pt
```

### Generation example

```text
Kairo Generation

Prompt:
The robot opened the door

Generated output:
The robot opened the door and saw a flicker of blue lights...
```

### Evaluation example

```text
Evaluation results
loss=3.02
perplexity=20.49
tokens=987
sequences=955
```

---

## Learn Mode

```bash
streamlit run src/kairo_learn.py
```

Learn Mode includes:
- guided workflow
- token viewer
- probability viewer
- attention visualisation
- retrain comparison
- experiment save/restore
- classroom safe mode

Screenshot ideas:
- guided workflow
- token viewer
- attention matrix
- retrain comparison

---

## Why byte-level tokens?

Kairo uses byte-level tokenisation because it is:
- simple to teach
- easy to inspect
- language agnostic
- useful for understanding raw mechanics

Production LLMs often use more advanced tokenisers, but byte-level tokens make the learning process much easier to observe.

---

## Expected weirdness

Tiny language models often produce:
- repetition
- strange grammar
- looping outputs
- overfitting
- memorised phrases
- inconsistent text

This is normal.

Kairo is intentionally small so learners can inspect and understand the mechanics behind these behaviours.

---

## Common misconceptions

- Kairo does not “understand” language like a human.
- Low loss does not mean intelligence.
- Attention is not human reasoning.
- Generated text quality depends heavily on training data.
- Tiny models often repeat patterns rather than reasoning.

---

## Classroom use

Kairo is designed for:
- secondary school computing
- STEM clubs
- workshops
- university intro labs
- teacher-led demonstrations

---

## Safety and supervision

Kairo includes lightweight classroom guardrails, not full moderation.

Teacher supervision is required.

Kairo is:
- not fully moderated
- not safeguarding-complete
- not suitable for unsupervised public deployment

---

## What Kairo is not

Kairo is:
- not a production LLM
- not instruction-tuned
- not a chatbot replacement
- not a frontier model
- not fully moderated

Outputs depend entirely on training data.

---

## Developer quickstart

Run quality checks:

```bash
ruff check .
python -m compileall src tests
pytest -q
```

CI also runs:
- smoke train
- smoke generate
- smoke evaluate

---

## Documentation map

- `docs/teacher_guide.md`
- `docs/student_worksheet.md`
- `docs/architecture.md`
- `docs/how_llms_work.md`

---

## Roadmap

Future educational improvements include:
- richer attention visuals
- guided lesson flows
- printable worksheets
- lesson packs
- stronger experiment comparison
- improved Learn Mode UX
