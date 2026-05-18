<p align="center">
  <img src="assets/kairo-logo.svg" alt="Kairo logo" width="640"/>
</p>

<p align="center">
  <a href="../README.md">Home</a> •
  <a href="teacher_guide.md">Teacher Guide</a> •
  <a href="student_worksheet.md">Student Worksheet</a> •
  <a href="architecture.md">Architecture</a> •
  <a href="how_llms_work.md">How LLMs Work</a>
</p>

---

# First Lesson Walkthrough

## Goal

By the end of this session, learners should understand:
- language models predict tokens
- training data changes behaviour
- low loss is not intelligence
- attention is not human reasoning

---

# Suggested lesson length

45–60 minutes.

---

# Lesson flow

| Time | Activity |
|---|---|
| 0–5 mins | Introduce AI prediction |
| 5–15 mins | Tokenisation + Build it |
| 15–30 mins | Train a tiny model |
| 30–40 mins | Generate outputs |
| 40–50 mins | Inspect attention + probabilities |
| 50–60 mins | Reflection and discussion |

---

# Step 1 — Introduce the idea

Explain:

> Kairo is not trying to be a smart chatbot.

It is trying to make AI mechanics visible.

Useful explanation:

> “Language models predict what token comes next.”

---

# Step 2 — Build it

Open Learn Mode:

```bash
streamlit run src/kairo_learn.py
```

Choose a small training dataset.

Good starter datasets:
- sci-fi stories
- pirate text
- fantasy dialogue
- tiny poems

Ask learners:

> “What patterns do you think the model will learn?”

---

# Step 3 — Train it

Use the Classroom demo preset.

Explain:
- loss = prediction error
- lower loss = better prediction
- lower loss does not mean understanding

Expected learner reactions:
- surprise at how fast tiny models train
- confusion about repetitive outputs
- curiosity about strange grammar

These are useful teaching moments.

---

# Step 4 — Generate text

Use prompts like:

```text
The robot opened the door
```

or:

```text
Captain Mira looked across the stars
```

Ask learners:
- What patterns appeared?
- Did the style match the dataset?
- Did the model repeat itself?

---

# Step 5 — Inspect probabilities

Show learners:
- top predicted tokens
- confidence differences
- uncertainty

Key insight:

> Models choose from probabilities, not certainty.

---

# Step 6 — Inspect attention

Explain:

> Attention shows which earlier tokens influenced the prediction.

Important clarification:

> Attention is not human understanding.

Ask:

> “Which earlier words mattered most?”

---

# Step 7 — Retrain and compare

Retrain on different text.

Example:
- fantasy → pirate dataset
- sci-fi → poems

Ask learners:

> “What changed?”

This is often the biggest educational moment.

---

# Suggested discussion questions

- Does prediction equal intelligence?
- Why does training data matter?
- Why can generated text feel convincing?
- Why do tiny models fail in strange ways?
- What surprised you most?

---

# Common learner misconceptions

| Misconception | Clarification |
|---|---|
| “The model understands.” | It predicts patterns. |
| “Low loss means smart.” | It means lower prediction error. |
| “Attention means reasoning.” | It is token weighting. |
| “The model knows facts.” | It predicts plausible continuations. |

---

# Expected weirdness

Tiny models often:
- repeat phrases
- contradict themselves
- drift off-topic
- overfit quickly
- generate nonsense

This is educationally valuable.

---

# Success criteria

Learners should leave understanding:
- AI prediction
- probabilities
- training data influence
- attention basics
- why models can appear intelligent

---

<p align="center">
  <a href="../README.md">← Home</a> •
  <a href="teacher_guide.md">Teacher Guide</a> •
  <a href="student_worksheet.md">Student Worksheet</a>
</p>
