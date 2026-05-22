<p align="center">
  <img src="assets/kairo-logo.svg" alt="Kairo logo" width="640"/>
</p>

<p align="center">
  <a href="../README.md">Home</a> •
  <a href="first_lesson_walkthrough.md">First Lesson Walkthrough</a> •
  <a href="teacher_guide.md">Teacher Guide</a> •
  <a href="student_worksheet.md">Student Worksheet</a> •
  <a href="architecture.md">Architecture</a> •
  <a href="how_llms_work.md">How LLMs Work</a>
</p>

---

# Architecture

## System diagram

![Simple architecture flowchart](assets/simple-architecture-flowchart.svg)

```text
Text data
  -> byte tokenizer
  -> fixed-length sequence windows
  -> TinyGPT forward pass
  -> next-token logits
  -> loss
  -> optimizer update
  -> saved checkpoint
```

---

## Code map

| Area | Files | Responsibility |
|---|---|---|
| Training CLI | `src/train.py` | Load text, build dataset, train, save checkpoints and metrics |
| Generation CLI | `src/generate.py`, `src/chat.py` | Load checkpoint, sample tokens, apply classroom safety filter |
| Evaluation CLI | `src/evaluate.py` | Report loss and perplexity for a saved checkpoint |
| Learn Mode | `src/kairo_learn.py`, `src/tiny_llm/learn.py` | Interactive classroom training, comparison, and inspection |
| Model core | `src/tiny_llm/model.py` | Tiny GPT-style transformer blocks and causal self-attention |
| Data | `src/tiny_llm/data.py` | Byte tokenizer and sequence dataset |
| Explanation | `src/tiny_llm/explain.py`, `src/tiny_llm/attention.py` | Token previews, top-token probabilities, attention maps |
| Safety | `src/tiny_llm/safety.py` | Lightweight prompt/output guardrails for classroom demos |
| Experiments | `src/tiny_llm/experiments.py` | Save and restore Learn Mode experiment folders |

---

## What happens during training?

```text
input:          "Captain Rowan looked"
shifted target: "Rowan looked at"
model output:   probability scores for each next token
loss:           prediction error between output and target
optimizer:      small weight updates to reduce future error
```

The CLI writes:

- `best.pt` for the checkpoint with the best validation loss
- `last.pt` for the most recent checkpoint
- `config.json` for training settings
- `metrics.json` for loss history

Small example output after a short training run:

```text
Prompt: Captain Rowan
Output: Captain Rowan crossed the bridge and checked the star map
```

---

## Generation flow

```text
Prompt text
  -> byte tokens
  -> model predicts next-token distribution
  -> sampling chooses one token
  -> token is appended to the prompt
  -> repeat until max_new_tokens is reached
```

Sampling controls:

- `temperature` changes how sharp or random the distribution feels
- `top_k` limits sampling to the strongest candidate tokens
- `top_p` limits sampling to a probability mass cutoff

---

## Learn Mode architecture flow

```text
Learner selects or pastes dataset
  -> teacher limits keep settings CPU-friendly
  -> train/evaluate model
  -> generate output
  -> inspect probabilities
  -> inspect attention
  -> retrain and compare
  -> optionally save experiment
```

Learn Mode experiment folders contain:

- `metadata.json`
- `model.pt`

That format is separate from CLI training runs, which use `best.pt` and `last.pt`.

---

## Attention visualization flow

```text
Prompt
  -> tokenize
  -> forward pass with attention weights
  -> pick layer/head
  -> render token table and attention matrix
```

Attention is a diagnostic view into token weighting. It should not be presented
as a view into thoughts, beliefs, or intent.

---

## Design constraints

- CPU-friendly defaults for classrooms.
- Byte-level tokens so every text can be encoded without an external tokenizer.
- Small model sizes so failures remain visible and discussable.
- Local files only; no hosted model or external API is required.
- Tests cover core model behavior, helpers, safety, docs, and CLI smoke paths.

---

<p align="center">
  <a href="../README.md">Home</a> •
  <a href="first_lesson_walkthrough.md">First Lesson Walkthrough</a> •
  <a href="teacher_guide.md">Teacher Guide</a> •
  <a href="student_worksheet.md">Student Worksheet</a> •
  <a href="architecture.md">Architecture</a> •
  <a href="how_llms_work.md">How LLMs Work</a>
</p>
