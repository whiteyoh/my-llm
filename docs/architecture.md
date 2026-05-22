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

## Normal to pirate retrain flow

```text
Normal story data
-> train TinyGPT
-> generate normal-style output
-> pirate dialogue data
-> retrain TinyGPT
-> generate pirate-style output
-> compare behavior
```

The architecture stays the same; the training data changes the model behavior.

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
