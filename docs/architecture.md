# Kairo Architecture (Beginner-Friendly)

This document explains how Kairo is organized so learners can connect code to concepts.

---

## High-level flow

```text
Training text
   │
   ▼
ByteTokenizer ──> token IDs
   │
   ▼
SequenceDataset ──> (input tokens, target next tokens)
   │
   ▼
TinyGPT
   │
   ├─ training loop (optimize loss, save checkpoints)
   ├─ generation pipeline (sample next tokens)
   └─ evaluation (loss + perplexity)
```

---

## 1) ByteTokenizer

What it does:
- converts raw text into byte-level token IDs,
- converts token IDs back into readable text.

Why it matters:
- learners can see tokenization directly,
- no hidden large vocabulary files are required.

---

## 2) SequenceDataset

What it does:
- creates short token windows from a long token stream,
- returns `(x, y)` pairs where:
  - `x` = input sequence,
  - `y` = same sequence shifted by one token (the learning target).

Why it matters:
- this is the core of next-token prediction training.

---

## 3) TinyGPT

What it includes:
- token embeddings,
- positional information,
- transformer blocks (attention + MLP),
- output head over vocabulary.

Why it matters:
- it is small enough to inspect,
- still large enough to show real LLM behavior patterns.

---

## 4) Training Loop

```text
for each batch:
  model predicts next-token logits
  compute cross-entropy loss
  backpropagate gradients
  update weights
  track train/validation metrics
  save best checkpoint
```

Educational focus:
- watch loss change,
- discuss overfitting vs generalization,
- compare different hyperparameters.

---

## 5) Generation Pipeline

What happens during generation:
1. Encode prompt into tokens.
2. Run model to get next-token probabilities.
3. Apply sampling controls (temperature/top-k/top-p).
4. Sample one token.
5. Append token and repeat.

Why it matters:
- shows that output is iterative probability sampling, not full-sentence planning.

---

## 6) Evaluation

Kairo evaluation focuses on:
- **loss** (prediction error),
- **perplexity** (uncertainty-like measure derived from loss).

Why this helps:
- learners can compare checkpoints quantitatively,
- teachers can anchor discussion in metrics, not vibes.

---

## 7) Learn Mode (Streamlit UI)

Learn Mode wraps the pipeline into guided steps:
- Build it,
- Train it,
- Talk to it,
- Retrain it,
- Understand it.

It exposes:
- token previews,
- loss charts,
- next-token probability views,
- before/after retrain comparisons.

---

## 8) Safety Layer

Kairo includes lightweight guardrails for classroom use:
- prompt filtering,
- output filtering,
- warnings on risky training text and personal data.

Important limitation:
- This is not full moderation and does not replace teacher supervision.

---

## 9) Explainability Layer

Kairo’s explainability tools emphasize:
- token visibility,
- top next-token probabilities,
- training metric trends,
- retraining comparisons.

These are the “windows” learners use to understand model behavior.
