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

# Student Worksheet

## Can you train a tiny AI?

In this activity you will build, train, test, retrain, and analyze a tiny
language model named Kairo.

Name: ________________________________________________

Date: ________________________________________________

---

## Challenge 1 — Build it

### My dataset

Dataset name or file:

__________________________________________________

What kind of text is in the dataset?

__________________________________________________

### Prediction (before training)

What kind of text do you think the model will generate?

__________________________________________________

Which words or style do you expect to appear?

__________________________________________________

---

## Challenge 2 — Train it

### Loss notes

Starting train loss:

__________________________________________________

Ending train loss:

__________________________________________________

What happened to the loss value while training?

__________________________________________________

### Reflection

Why do you think the loss changed?

__________________________________________________

Does lower loss mean the model understands like a person?

__________________________________________________

---

## Challenge 3 — Talk to it

### My prompt

__________________________________________________

### Top predicted next token

__________________________________________________

### Generated output

__________________________________________________

__________________________________________________

### Reflection

Did the generated text make sense? Why or why not?

__________________________________________________

Which parts sounded fluent but might not be true?

__________________________________________________

---

## Challenge 4 — Retrain it

### Output Before Retrain

Prompt used:

__________________________________________________

Output recorded:

__________________________________________________

Example prompt:

`Captain Rowan looked at the stars`

Example observation before retrain:

`The output sounds like a space story.`

---

### Output After Retrain

Prompt used (same prompt recommended):

__________________________________________________

Output recorded:

__________________________________________________

Example observation after pirate retrain:

`The output includes pirate-style words such as "matey", "sail", or "tide".`

---

### What Changed and Why?

Compare the two outputs. Note style, vocabulary, repetition, and topic shifts.

| Evidence | Before | After |
|---|---|---|
| Vocabulary | | |
| Tone | | |
| Repetition | | |
| Topic | | |

Why do you think retraining changed the output?

__________________________________________________

---

### Reflection

How did this change your understanding of how AI models learn?

__________________________________________________

---

### Extension exercises

- Try two different datasets with the same prompt and compare outputs.
- Run one additional retrain round and record whether style shifts become stronger.
- Change `max_new_tokens`, `temperature`, or `top_k` and describe the effect.
- Write one prediction about what might happen with a much larger dataset.

Notes:

__________________________________________________

---

## Challenge 5 — Inspect attention

### Token with strongest attention

Prompt:

__________________________________________________

Token inspected:

__________________________________________________

Strongest attended token:

__________________________________________________

### Reflection

Does attention mean understanding? Explain your answer.

__________________________________________________

What can attention help you inspect?

__________________________________________________

---

## Challenge 6 — Save experiment

### Experiment folder name

__________________________________________________

What would you need to record so someone else could repeat your experiment?

__________________________________________________

---

## Challenge 7 — Understand it

### What surprised you most?

__________________________________________________

### What did you learn about AI?

__________________________________________________

One sentence I can now explain:

```text
Language models learn...
```

__________________________________________________

---

---

## Before/after retrain prompt ideas

```text
Captain Rowan:
The station woke
Rain taps softly
The robot opened the door
Raise the black sail
```

---

## New sample datasets

Use one starter file from `data/samples/`:

- `space_adventure.txt`
- `pirate_dialogue.txt`
- `sci_fi_micro_story.txt`
- `short_poems.txt`
- `nature_notes.txt`
- `robot_helper.txt`

---

## Final reflection

- What did Kairo help you understand about language models?
- What changed when the training data changed?
- Why does this show that AI output depends on data?

---

<p align="center">
  <a href="../README.md">Home</a> •
  <a href="first_lesson_walkthrough.md">First Lesson Walkthrough</a> •
  <a href="teacher_guide.md">Teacher Guide</a> •
  <a href="student_worksheet.md">Student Worksheet</a> •
  <a href="architecture.md">Architecture</a> •
  <a href="how_llms_work.md">How LLMs Work</a>
</p>
