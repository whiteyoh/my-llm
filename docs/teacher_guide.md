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

Students should leave understanding that language models are next-token
prediction systems whose behavior changes when training data changes.

---

## Before-lesson checklist

- Python 3.11 or newer is available.
- The repository is cloned locally.
- Core dependencies are installed with `pip install -e .`.
- Optional Learn Mode dependencies are installed with `pip install -e ".[learn]"`.
- Sample files are present in `data/samples/`.
- The first training command has been tested once on the classroom machine.
- Projector or screen-sharing is ready for side-by-side output comparison.

Quick preflight:

```bash
python -m compileall src tests
kairo-train --input_file data/samples/space_adventure.txt --out_dir runs/preflight --epochs 1 --batch_size 4 --seq_len 32 --d_model 64 --n_heads 4 --n_layers 2 --device cpu
```

---

## Quick-reference classroom flow

| Section | Suggested timing | Teacher moves | Student outcome |
|---|---:|---|---|
| 1. Build it | 10 min | Show byte tokens and ask for next-token predictions | Students form hypotheses |
| 2. Train it | 15 min | Run short training and track loss | Students connect loss to prediction error |
| 3. Talk to it | 10 min | Prompt and evaluate outputs | Students see uncertainty and repetition |
| 4. Retrain it | 15 min | Swap dataset and compare the same prompt | Students observe style shift |
| 5. Reflect | 10 min | Guide worksheet reflection | Students explain what changed and why |

---

## Suggested classroom pacing

### 45-minute version

1. Prediction warm-up (5 min)
2. Token viewer or short explanation (5 min)
3. Train the baseline model (12 min)
4. Generate and record output (8 min)
5. Retrain or show prepared comparison (10 min)
6. Exit ticket (5 min)

### 90-minute version

1. Prediction warm-up (10 min)
2. Tokenization and byte-token discussion (10 min)
3. Baseline training (15 min)
4. Prompt experiments (15 min)
5. Retrain comparison (20 min)
6. Attention and probability inspection (10 min)
7. Reflection and Q&A (10 min)

---

## Facilitation tips

- Ask students to predict outputs before running commands.
- Reuse the exact same prompt before and after changing datasets.
- Project at least two outputs side-by-side for evidence-based discussion.
- Encourage precise uncertainty language: "I think", "I notice", "the output suggests".
- Normalize weird model behavior as expected in tiny models.
- Keep one prepared checkpoint ready in case live training is slow.

---

## Common misconceptions and Q&A guidance

### Misconception: "Lower loss means understanding"

**Teacher response:** Loss means prediction error went down; it does not prove
understanding.

### Misconception: "Attention shows thinking"

**Teacher response:** Attention is token weighting, not reasoning,
consciousness, or intent.

### Misconception: "If it sounds fluent, it must be true"

**Teacher response:** Fluency is pattern generation; factual claims still need
external verification.

### Misconception: "Retraining stores facts like a database"

**Teacher response:** Training shifts model weights so token patterns become
more or less likely. It is not the same as saving a fact in a table.

---

## Classroom Q&A prompts

- What changed between output before retrain and output after retrain?
- Which words or style markers suggest the dataset influenced behavior?
- Which parts of the output are fluent but not necessarily reliable?
- What does attention help us inspect?
- What does attention not prove?

---

## Assessment ideas

| Evidence | Emerging | Secure |
|---|---|---|
| Explains next-token prediction | Says the model "guesses words" | Connects previous tokens to next-token probabilities |
| Interprets loss | Says lower is better | Explains loss as prediction error, not understanding |
| Compares retrain outputs | Notices style changed | Uses vocabulary and tone evidence from both outputs |
| Explains attention | Says it shows important words | States attention is weighting, not consciousness |

---


## Teacher gotchas

| Gotcha | What it means | What to do |
|---|---|---|
| Training is slow | CPU training can take longer than expected with larger settings. | Use shorter runs (`epochs 1`, smaller `seq_len`) and frame waiting time as part of experimentation. |
| Output repeats | Tiny models often loop or reuse phrases. | Treat repetition as evidence of model limits and ask students why it happens. |
| Students think attention means thinking | Learners may interpret attention maps as human reasoning. | Repeat that attention is a weighting mechanism over tokens, not consciousness. |
| Students think low loss means intelligence | Lower loss can be mistaken for true understanding. | Explain loss as prediction error only; compare fluent text with incorrect claims. |
| Pirate style does not appear strongly enough | One short retrain may not produce dramatic style shift. | Retrain briefly again or use stronger pirate prompts and compare vocabulary changes. |

---

## Example teacher script

- “A language model predicts the next token.”
- “Retraining changes the patterns the model has seen.”
- “Attention is not thinking; it is a weighting mechanism.”
- “Strange output is useful because it shows the limits of small models.”

---

## Troubleshooting quick guide

### Training is too slow

Use fewer epochs, shorter sequence length, or the "Classroom demo" preset in
Learn Mode.

### Training text is too short

Use a longer sample file or lower `--seq_len`. The text must contain more tokens
than the sequence length.

### Outputs look repetitive

This is expected for tiny models and is a useful teaching moment.

### CLI checkpoint load fails

Verify the training run saved `best.pt` or `last.pt` in the run directory.

### Learn Mode experiment restore fails

Verify the experiment folder contains both `metadata.json` and `model.pt`.

---

## Printable materials

Markdown sources live in `docs/`. Printable PDFs live in `docs/printable/`.

To regenerate the printables:

```bash
pip install -e ".[pdf]"
python tools/pdf/generate_printables.py
```

The default output is A4. For US Letter, run:

```bash
python tools/pdf/generate_printables.py letter
```

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
