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

Language models work by predicting what token is most likely to come next.

Example:

```text
The robot opened the _____
```

The model might predict:
- door
- gate
- hatch
- window

Generation happens by repeating this prediction process many times.

---

## What is a token?

A token is a chunk of text the model works with.

Kairo uses byte-level tokens because they are:
- simple
- universal
- easy to inspect
- useful for learning the raw mechanics

Production models often use more advanced tokenisation systems.

---

## What is loss?

Loss measures prediction error.

High loss:
- poor predictions
- weak pattern learning

Lower loss:
- better predictions
- stronger pattern learning

Lower loss does not mean human-like intelligence.

---

## What is attention?

Attention is a weighting mechanism over earlier tokens.

It helps the model decide:
- which earlier words matter most
- which patterns are useful for prediction

---

## Attention is not understanding

Attention does not mean:
- thoughts
- beliefs
- emotions
- consciousness
- human reasoning

Attention is a mathematical mechanism, not a mind.

---

## Why retraining changes behaviour

Changing training text changes token statistics and patterns.

That means the model starts predicting differently.

This is why:
- datasets matter
- tone changes
- style changes
- biases can appear

---

## Why small models fail

Tiny models have:
- limited memory
- limited capacity
- short context windows

They often:
- repeat themselves
- drift off-topic
- produce strange grammar
- memorise text

This behaviour is useful for learning because the mechanics are easier to observe.

---

## Why AI hallucinations happen

Language models predict plausible patterns.

They do not:
- verify truth
- understand facts like humans
- know when they are wrong

This is why models can confidently generate incorrect information.

---

## Why tiny models can still feel intelligent

Even small models can produce surprisingly convincing text.

This can create the illusion of understanding.

But language models are still fundamentally:
- prediction systems
- pattern learners
- probability engines

Kairo is designed to help learners inspect these mechanics directly.

---

## Why data quality matters

Cleaner and more focused training data usually produces:
- more coherent outputs
- fewer random errors
- more stable style

Poor or mixed data often creates:
- inconsistency
- repetition
- unstable behaviour

---

<p align="center">
  <a href="../README.md">Home</a> •
  <a href="first_lesson_walkthrough.md">First Lesson Walkthrough</a> •
  <a href="teacher_guide.md">Teacher Guide</a> •
  <a href="student_worksheet.md">Student Worksheet</a> •
  <a href="architecture.md">Architecture</a> •
  <a href="how_llms_work.md">How LLMs Work</a>
</p>
