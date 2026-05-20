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
  -> sequence windows
  -> TinyGPT forward pass
  -> next-token logits
  -> loss
  -> optimizer update
  -> improved weights
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
input: "Captain Rowan looked"
shifted target: "Rowan looked at"
model predicts token probabilities at each position
loss compares predictions vs targets
optimizer nudges weights to lower error
```

Small example output after a short training run:

```text
Prompt: Captain Rowan
Output: Captain Rowan crossed the bridge and checked the star map
```

---

## Generation flow

```text
Prompt tokens
  -> model predicts next-token distribution
  -> sample one token
  -> append token
  -> repeat until max tokens reached
```

---

## Learn Mode architecture flow

```text
Learner selects dataset
  -> training controls
  -> train/evaluate model
  -> generate output
  -> inspect probabilities
  -> inspect attention
  -> retrain and compare
```

---

## Attention visualization flow

```text
Prompt
  -> tokenize
  -> forward pass with attention weights
  -> pick layer/head
  -> render attention table or heatmap
```

---

<p align="center">
  <a href="../README.md">Home</a> •
  <a href="first_lesson_walkthrough.md">First Lesson Walkthrough</a> •
  <a href="teacher_guide.md">Teacher Guide</a> •
  <a href="student_worksheet.md">Student Worksheet</a> •
  <a href="architecture.md">Architecture</a> •
  <a href="how_llms_work.md">How LLMs Work</a>
</p>
