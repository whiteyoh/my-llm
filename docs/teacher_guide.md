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

# Teacher Guide

## Lesson goal

Students should leave understanding that language models are next-token prediction systems whose behavior changes when training data changes.

---

## Quick-reference classroom flow

| Section | Suggested timing | Teacher moves | Student outcome |
|---|---:|---|---|
| 1. Build it | 10 min | Choose dataset and ask for predictions | Students form hypotheses |
| 2. Train it | 15 min | Run short training and track loss | Students connect loss to prediction error |
| 3. Talk to it | 10 min | Prompt and evaluate outputs | Students see uncertainty and repetition |
| 4. Retrain it | 15 min | Swap dataset and retrain | Students observe style shift |
| 5. Reflect | 10 min | Guide discussion and worksheet reflection | Students explain what changed and why |

---

## Setup checklist (5–10 min before class)

- Python environment installed
- Repo cloned
- Dependencies installed:

```bash
pip install -e .
```

- Optional Learn Mode dependencies:

```bash
pip install -e ".[learn]"
```

- Confirm sample files in `data/samples/`

---

## Suggested classroom pacing

### 45-minute version

1. Build and predict (10 min)
2. Train model (15 min)
3. Generate text (10 min)
4. Reflection and misconceptions (10 min)

### 90-minute version

1. Build and predict (10 min)
2. Train model (20 min)
3. Generate text (15 min)
4. Retrain comparison (20 min)
5. Attention + probabilities (15 min)
6. Reflection and Q&A (10 min)

---

## Facilitation tips

- Ask students to predict outputs *before* running commands.
- Reuse the exact same prompt before and after retraining.
- Project at least two outputs side-by-side for evidence-based discussion.
- Praise uncertainty language ("I think", "I notice") during reflection.
- Normalize "weird" model behavior as expected in tiny models.

---

## Common misconceptions and Q&A guidance

### Misconception: "Lower loss means understanding"

**Teacher response:** Loss means prediction error went down; it does not prove understanding.

### Misconception: "Attention shows thinking"

**Teacher response:** Attention is token weighting, not reasoning or consciousness.

### Misconception: "If it sounds fluent, it must be true"

**Teacher response:** Fluency is pattern generation; always verify claims externally.

### Misconception: "Retraining adds knowledge like a fact database"

**Teacher response:** Retraining shifts learned token patterns and style distributions.

---

## Classroom Q&A prompts

- What changed between output before retrain and output after retrain?
- Which words or style markers suggest the dataset influenced behavior?
- Why can generated text feel intelligent even when it is incorrect?
- What does attention help us inspect, and what does it *not* prove?

---

## Troubleshooting quick guide

### Training is too slow

Use smaller settings (fewer epochs, shorter sequence length).

### Outputs look repetitive

This is expected for tiny models and is a useful teaching moment.

### Checkpoint load fails

Verify `metadata.json` and `model.pt` were saved in the run directory.

---

## Reflection close-out (5–10 min)

Ask students to complete worksheet sections:

- Output Before Retrain
- Output After Retrain
- What Changed and Why?
- Reflection
- Extension exercises

---

<p align="center">
  <a href="../README.md">Home</a> •
  <a href="first_lesson_walkthrough.md">First Lesson Walkthrough</a> •
  <a href="teacher_guide.md">Teacher Guide</a> •
  <a href="student_worksheet.md">Student Worksheet</a> •
  <a href="architecture.md">Architecture</a> •
  <a href="how_llms_work.md">How LLMs Work</a>
</p>
