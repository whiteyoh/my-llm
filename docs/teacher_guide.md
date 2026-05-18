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

## Before-lesson checklist

- Python installed
- Repo cloned
- `pip install -e .` completed
- Sample data available in `data/samples/`
- Optional Learn Mode extras installed with:

```bash
pip install -e ".[learn]"
```

---

## Hardware expectations

- CPU-only works well
- 8GB RAM recommended
- No GPU required
- Classroom demo preset recommended for slower laptops

---

## Setup options

### Teacher-led demo
One machine projected to the class.

### Pair activity
Two learners work together on one laptop.

### Individual exploration
Each learner trains and experiments independently.

---

## Suggested classroom pacing

| Time | Activity |
|---|---|
| 0–10 mins | Introduce AI prediction concepts |
| 10–20 mins | Tokenisation + Build it |
| 20–35 mins | Train a tiny model |
| 35–45 mins | Generate text + reflection |
| 45–90 mins | Retraining, attention inspection, experiment save/restore |

---

## 45-minute lesson script

1. Build it (token viewer)
2. Train it (1 epoch)
3. Talk to it
4. Inspect probabilities
5. Reflection and discussion

---

## 90-minute workshop script

Add:
- retraining
- attention inspection
- experiment save/restore
- comparing datasets
- changing prompts and temperatures

---

## What students usually find surprising

Learners are often surprised that:
- the model repeats itself
- changing small amounts of training data changes outputs
- low loss does not mean understanding
- attention is not human reasoning
- tiny models can still feel convincing

These moments create strong discussion opportunities.

---

## Suggested classroom discussion prompts

- Does prediction equal understanding?
- Why might training data create bias?
- Why can generated text feel intelligent?
- What happens when training data changes?
- Why do tiny models sometimes repeat themselves?

---

## Teacher controls

Use presets to clamp model, training, and generation sizes.

If limits are exceeded, Kairo warns:

> “Teacher controls are keeping this demo CPU-friendly.”

Safe mode is enabled by default.

---

## Attention visualisation teaching notes

Attention shows which earlier tokens influenced a prediction.

It does **not** mean:
- understanding
- beliefs
- reasoning like a human

A useful explanation for learners:

> “Attention is a weighting mechanism, not a mind.”

---

## Experiment save/restore workflow

1. Train model
2. Save experiment
3. Load metadata
4. Restore model checkpoint
5. Compare before/after outputs

---

## Safeguarding notes

Safe mode is enabled by default.

Custom banned terms apply to:
- prompt checks
- output filtering

Teacher supervision is still required.

Kairo is not fully moderated.

---

## Troubleshooting

### Short text errors
Reduce `seq_len` or add more training text.

### Slow training
Pick the Classroom demo preset.

### Load error
Verify `metadata.json` and `model.pt` exist.

### Strange output
Tiny models often:
- repeat text
- drift off-topic
- memorise phrases
- generate inconsistent grammar

This is normal and educationally useful.

---

## Reflection questions

- What changed after retraining?
- Which token had strongest attention?
- Why can attention be useful but limited?
- Why does data quality matter?
- Did the model appear intelligent? Why?

---

<p align="center">
  <a href="../README.md">Home</a> •
  <a href="first_lesson_walkthrough.md">First Lesson Walkthrough</a> •
  <a href="teacher_guide.md">Teacher Guide</a> •
  <a href="student_worksheet.md">Student Worksheet</a> •
  <a href="architecture.md">Architecture</a> •
  <a href="how_llms_work.md">How LLMs Work</a>
</p>
