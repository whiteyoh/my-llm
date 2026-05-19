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

# How LLMs Work (Simple)

## What is next-token prediction?

LLMs predict one token at a time based on previous tokens.

```text
Prompt: The robot opened the
Top candidates: door (0.31), gate (0.18), hatch (0.14)
```

---

## What is a token?

A token is a unit of text the model processes.

Token illustration:

```text
"matey!" -> [m][a][t][e][y][!]
```

Kairo uses byte-level tokenization to make this easy to inspect.

---

## What is loss?

Loss measures prediction error.

```text
Higher loss  -> poorer predictions
Lower loss   -> better predictions
```

Lower loss does **not** mean human-like understanding.

---

## What is attention?

Attention weights earlier tokens when predicting the next token.

```text
Prompt tokens: [Captain] [Rowan] [raised] [the]
Predict next: "sail"
Attention weights to next token:
Captain: 0.08
Rowan:   0.12
raised:  0.46
the:     0.34
```

---

## Attention is not understanding

Attention does not prove thoughts, beliefs, or consciousness.
It is a mathematical weighting mechanism.

---

## Why retraining changes behavior

Changing datasets changes token statistics and style patterns.

Example retrain effect:

```text
Before retrain: "The station door opened quietly"
After retrain:  "Arrr, the hatch swung wide, matey"
```

---

## Why tiny models can fail

Tiny models often repeat, drift, or contradict themselves because capacity is limited.
That visible failure is useful for classroom learning.

---

<p align="center">
  <a href="../README.md">Home</a> •
  <a href="first_lesson_walkthrough.md">First Lesson Walkthrough</a> •
  <a href="teacher_guide.md">Teacher Guide</a> •
  <a href="student_worksheet.md">Student Worksheet</a> •
  <a href="architecture.md">Architecture</a> •
  <a href="how_llms_work.md">How LLMs Work</a>
</p>
