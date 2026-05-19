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

# First Lesson Walkthrough

## Goal

Run one complete learning loop: normal story training → retrain on pirate style → compare outputs.

---

## Sample datasets for this lesson

- Normal style dataset: `data/samples/space_adventure.txt`
- Retrain style dataset: `data/samples/pirate_dialogue.txt`

---

## Step 1 — Train on normal story data

```bash
python src/train.py --input_file data/samples/space_adventure.txt --out_dir runs/lesson_normal --epochs 1 --batch_size 4 --seq_len 32 --d_model 64 --n_heads 4 --n_layers 2 --device cpu
```

## Step 2 — Generate output before retrain

```bash
python src/generate.py --checkpoint runs/lesson_normal/best.pt --prompt "Captain Rowan looked at the stars" --max_new_tokens 30 --device cpu
```

### Example output (before retrain)

```text
Captain Rowan looked at the stars and the station lights flickered in the dark hall
```

---

## Step 3 — Retrain on pirate dataset

```bash
python src/train.py --input_file data/samples/pirate_dialogue.txt --out_dir runs/lesson_pirate --epochs 1 --batch_size 4 --seq_len 32 --d_model 64 --n_heads 4 --n_layers 2 --device cpu
```

## Step 4 — Generate output after retrain

```bash
python src/generate.py --checkpoint runs/lesson_pirate/best.pt --prompt "Captain Rowan looked at the stars" --max_new_tokens 30 --device cpu
```

### Example output (after retrain)

```text
Captain Rowan looked at the stars, matey, and swore by the tide to raise the black sail
```

---

## Step 5 — Ask comparison questions

- Which vocabulary changed?
- Did sentence rhythm or tone change?
- Which output better matches pirate style?

---

## Step 6 — Optional Learn Mode inspection

```bash
streamlit run src/kairo_learn.py
```

Use Learn Mode to inspect token probabilities and attention maps for the same prompt.

---

## Before/after retrain exercise prompts

```text
Captain Rowan:
The station woke as
Raise the black sail
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
