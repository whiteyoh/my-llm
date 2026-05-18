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

## Why Kairo + `tiny_llm`

Kairo is the product and learning experience name.

`tiny_llm` is the internal Python package containing reusable:
- model logic
- learning helpers
- explainability tools
- safety logic
- experiment persistence

This separation keeps the educational experience clean while keeping the code modular.

---

## High-level flow

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
 Weight updates
      ↓
 Text generation
```

---

## What happens during training?

```text
Input text
→ tokens
→ sequences
→ predictions
→ prediction error
→ weight updates
→ improved predictions
```

The model slowly improves by reducing prediction error.

---

## Learn Mode flow

```text
Learner input
      ↓
 Build it
      ↓
 Train it
      ↓
 Generate text
      ↓
 Inspect probabilities
      ↓
 Inspect attention
      ↓
 Retrain and compare
```

UI rendering lives in:
- `src/kairo_learn.py`

Reusable educational helpers live in:
- `src/tiny_llm/learn.py`

---

## Attention visualisation flow

```text
Prompt
→ tokenize
→ model forward with return_attn=True
→ select layer/head
→ attention matrix
→ heatmap/table rendering
```

Attention shows which previous tokens influenced a prediction.

It does not mean:
- understanding
- beliefs
- consciousness

---

## Experiment persistence flow

```text
Train model
→ save metadata.json
→ save model.pt
→ restore config
→ load checkpoint
→ continue experimenting
```

Experiments allow learners to compare outputs before and after retraining.

---

## Safety flow

```text
Prompt
→ safe-mode checks
→ optional filtering
→ generation
→ output filtering
```

Safe mode is lightweight and classroom-focused.

Teacher supervision is still required.

---

<p align="center">
  <a href="../README.md">Home</a> •
  <a href="first_lesson_walkthrough.md">First Lesson Walkthrough</a> •
  <a href="teacher_guide.md">Teacher Guide</a> •
  <a href="student_worksheet.md">Student Worksheet</a> •
  <a href="architecture.md">Architecture</a> •
  <a href="how_llms_work.md">How LLMs Work</a>
</p>
