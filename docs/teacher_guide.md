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

## Quick-reference classroom flow

| Step | Suggested timing | Teacher action | Student outcome |
|---|---:|---|---|
| 1. Build it | 10 min | Select dataset and preview tokenisation | Learners predict model behaviour |
| 2. Train it | 15 min | Run 1 short epoch and watch loss | Learners connect training to pattern learning |
| 3. Talk to it | 10 min | Prompt model and inspect output | Learners observe uncertainty and repetition |
| 4. Retrain it | 15 min | Swap dataset and rerun train | Learners compare style shift before/after |
| 5. Reflect | 10 min | Lead discussion using prompts below | Learners explain what changed and why |

---

## Before-lesson checklist (5–10 min setup)

- Python installed
- Repo cloned
- `pip install -e .` completed
- Sample data available in `data/samples/`
- Optional Learn Mode extras installed with:

```bash
pip install -e ".[learn]"
```

### Pacing tips by learner age/experience

- **Ages 11–13 / beginners:** Use only one dataset and one fixed prompt.
- **Ages 14–16 / mixed experience:** Add retrain comparison and one misconception check.
- **Advanced learners:** Add temperature experiments and multiple prompt evaluations.

---

## Hardware expectations (2 min)

- CPU-only works well
- 8GB RAM recommended
- No GPU required
- Classroom demo preset recommended for slower laptops

---

## Setup options (3–5 min)

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

1. Build it (token viewer) — **10 min**
2. Train it (1 epoch) — **15 min**
3. Talk to it — **10 min**
4. Inspect probabilities — **5 min**
5. Reflection and discussion — **5 min**

---

## 90-minute workshop script

Add:
- retraining (**15 min**)
- attention inspection (**10 min**)
- experiment save/restore (**10 min**)
- comparing datasets (**10 min**)
- changing prompts and temperatures (**10 min**)

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

## Common misconceptions to watch for

- **"Lower loss means the model understands."**
- **"Attention maps show what the model is thinking."**
- **"If text sounds fluent, it must be true."**
- **"Retraining adds facts rather than shifting pattern probabilities."**

Coaching move: ask students to point to evidence in output before accepting a claim.

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

## Experiment save/restore workflow (10 min)

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
