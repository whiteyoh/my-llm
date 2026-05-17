# Kairo

**Build it. Train it. Talk to it. Understand it.**

Kairo is a beginner-friendly educational AI lab where you train and inspect a tiny byte-level GPT model on your own text. Instead of treating language models like magic, Kairo helps learners and teachers see the mechanics directly: tokenization, next-token prediction, training loss, sampling choices, and how retraining changes behavior. The goal is demystification through hands-on practice.

---

## A) What Kairo Is

Kairo is an **educational byte-level GPT lab** designed for transparent learning.

It gives you a small transformer you can actually inspect, run on CPU, and discuss in class.

Kairo is built to teach:
- how text becomes tokens,
- how a model predicts the next token,
- how training changes probabilities,
- how model behavior depends on data.

It is designed for:
- classrooms,
- workshops,
- STEM clubs,
- self-learning,
- beginner developer exploration.

---

## B) What Kairo Is NOT

Kairo is intentionally small and honest about limits.

It is **not**:
- production-ready,
- instruction-tuned,
- a chatbot replacement,
- fully moderated,
- a large-scale foundation model.

Important reality check:
- Outputs depend entirely on training data.
- If data is narrow, noisy, or biased, outputs will be too.

---

## C) Why Kairo Exists

Most people can *use* AI tools but cannot explain what is happening under the hood.

Kairo exists to make key ideas visible:
- **tokens** (how text is represented),
- **probabilities** (how choices are ranked),
- **training loss** (how prediction error changes),
- **retraining effects** (how behavior shifts),
- **sampling behavior** (why outputs vary).

Kairo’s purpose is education, not hype.

---

## D) Core Learning Journey

Kairo uses a repeatable five-step workflow:

### 1) Build it
**What happens:** you choose or paste training text and inspect tokenized bytes.  
**Observe:** token count, token boundaries, repeated patterns.  
**Why it matters:** learners connect raw text to model inputs.

### 2) Train it
**What happens:** a tiny GPT trains on your data and saves checkpoints.  
**Observe:** train/validation loss trends over time.  
**Why it matters:** learners see prediction quality improve numerically.

### 3) Talk to it
**What happens:** you prompt the model and generate text.  
**Observe:** style, repetition, uncertainty, and sampling effects.  
**Why it matters:** learners see generation as probability-based token selection.

### 4) Retrain it
**What happens:** you change the dataset and train again.  
**Observe:** before/after output differences for the same prompt.  
**Why it matters:** learners see that behavior comes from data, not hidden understanding.

### 5) Understand it
**What happens:** you interpret charts, outputs, and failure cases.  
**Observe:** where the model succeeds, where it fails, and why.  
**Why it matters:** learners build accurate mental models of LLMs.

---

## E) Features

- Byte-level tokenizer
- Tiny GPT model (inspectable, CPU-friendly)
- Training loop with checkpoints
- Text generation CLI
- Evaluation with loss/perplexity metrics
- Chat mode
- Learn Mode Streamlit UI
- Token visualization
- Next-token probability viewer
- Retrain comparison workflow
- Classroom safety mode
- Tests + CI support

---

## F) Installation

### Requirements
- Python **3.11+**
- pip

### Clone + install

```bash
git clone https://github.com/whiteyoh/my-llm.git
cd my-llm
pip install -e .
```

### Optional: Learn Mode dependencies

```bash
pip install -e ".[learn]"
```

---

## G) Quick Start

### 1) Train a tiny model

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

### 2) Generate text

```bash
python src/generate.py \
  --checkpoint runs/demo/best.pt \
  --prompt "The robot opened the door" \
  --max_new_tokens 20 \
  --device cpu
```

### 3) Evaluate loss/perplexity

```bash
python src/evaluate.py \
  --checkpoint runs/demo/best.pt \
  --input_file data/samples/space_adventure.txt \
  --device cpu
```

### 4) Chat with the model

```bash
python src/chat.py \
  --checkpoint runs/demo/best.pt \
  --device cpu
```

---

## H) Learn Mode

Learn Mode is a guided **Streamlit classroom and self-learning interface**.

Run it:

```bash
streamlit run src/kairo_learn.py
```

What Learn Mode supports:
- guided step-by-step workflow,
- token viewer,
- live training/loss chart inspection,
- next-token prediction and probability inspection,
- retrain comparison on the same prompt.

Screenshot idea: Learn Mode home  
Screenshot idea: token viewer  
Screenshot idea: loss chart  
Screenshot idea: retrain comparison

---

## I) Classroom Safety

Kairo includes lightweight classroom guardrails, but it is not a full safety system.

Included guardrails:
- safe mode toggle,
- prompt filtering,
- output filtering,
- training text warnings,
- personal-data warnings.

Important limits:
- Not full moderation.
- Not safeguarding-complete.
- Not suitable for unsupervised public deployment.
- Teacher supervision is required.

---

## J) Educational Concepts (Plain English)

| Concept | Simple meaning |
|---|---|
| Token | A chunk of text the model processes (in Kairo, bytes). |
| Next-token prediction | The model guesses what comes next, one token at a time. |
| Loss | A score for prediction error (lower usually means better fit to data). |
| Perplexity | A readability-style uncertainty score derived from loss (lower is usually better). |
| Top-k sampling | Choose from the top *k* likely tokens only. |
| Top-p sampling | Choose from the smallest set of tokens whose probabilities add to *p*. |
| Retraining effects | Model outputs change when you train on different text. |

---

## K) Suggested Classroom Usage

Suggested teaching contexts:
- **Secondary school computing** (ages ~13–18)
- **STEM clubs** (ages ~12+)
- **AI workshops** (ages ~14+)
- **University intro labs** (first-year undergrad)
- **Teacher-led demos** (mixed ability groups)

Tip: start with short, safe, theme-based datasets (space, nature, sports, robots).

---

## L) Example Experiments

Try these practical activities:

1. **Space baseline**
   - Train on `data/samples/space_adventure.txt`.
   - Prompt with: `The astronaut looked out the window`.

2. **Pirate retrain**
   - Retrain on pirate-themed text.
   - Re-run the same prompt and compare style shifts.

3. **Temperature comparison**
   - Generate at low vs high temperature.
   - Observe stability vs creativity.

4. **Probability inspection**
   - Inspect top next-token candidates before generation.
   - Discuss why token #1 was selected.

5. **Dataset size comparison**
   - Train with very short text, then larger text.
   - Compare coherence, repetition, and loss.

---

## M) Roadmap

Planned improvements:
- attention visualization,
- save/load Learn Mode sessions,
- classroom lesson packs,
- printable worksheets,
- richer token inspection,
- better retraining comparisons,
- optional lightweight web deployment.

---

## N) Contributing

Beginner contributions are welcome (docs, tests, bug fixes, teaching activities).

### Local quality checks

```bash
ruff check .
python -m compileall src tests
pytest -q
```

### Smoke checks used in docs

```bash
python src/train.py --input_file data/samples/space_adventure.txt --out_dir runs/demo --epochs 1 --batch_size 4 --seq_len 32 --d_model 64 --n_heads 4 --n_layers 2 --device cpu
python src/generate.py --checkpoint runs/demo/best.pt --prompt "The robot opened the door" --max_new_tokens 20 --device cpu
python src/evaluate.py --checkpoint runs/demo/best.pt --input_file data/samples/space_adventure.txt --device cpu
```

Optional Learn Mode run:

```bash
streamlit run src/kairo_learn.py
```

---

## O) License

This project is available under the terms of the repository license. See `LICENSE` for details.
