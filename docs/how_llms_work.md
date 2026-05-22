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

Generation repeats that step:

```text
predict -> sample -> append -> predict again
```

The model is not looking up a finished answer. It is repeatedly choosing likely
next tokens.

---

## What is a token?

A token is a unit of text the model processes.

Token illustration:

```text
"matey!" -> [m][a][t][e][y][!]
```

Kairo uses byte-level tokenization. That means every piece of text can be turned
into numbers without downloading a separate tokenizer.

Trade-off:

- byte tokens are simple and visible
- byte tokens can be less efficient than larger word-piece tokens

---

## What is loss?

Loss measures prediction error.

```text
Higher loss  -> poorer predictions
Lower loss   -> better predictions
```

During training, Kairo compares predicted next-token probabilities with the real
next token in the dataset. The optimizer updates model weights to reduce that
error.

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

In a causal language model, each token can only attend to earlier tokens and
itself, not future tokens.

---

## Attention is not understanding

Attention does not prove thoughts, beliefs, intent, or consciousness. It is a
mathematical weighting mechanism that can help us inspect one part of the model.

Useful statement:

```text
Attention can show which earlier tokens were weighted strongly.
```

Unsafe statement:

```text
Attention proves what the model was thinking.
```

---

## Why retraining changes behavior

Changing datasets changes token statistics and style patterns.

Example retrain effect:

```text
Before retrain: "The station door opened quietly"
After retrain:  "Arrr, the hatch swung wide, matey"
```

The model architecture can stay the same while the learned weights change. That
is why the same prompt can lead to different vocabulary and tone after training
on different text.

---

## What sampling changes

Sampling controls how the next token is chosen from the probability list.

| Setting | Classroom explanation |
|---|---|
| `temperature` | Higher values make choices more surprising; lower values make them safer. |
| `top_k` | Only sample from the strongest K token candidates. |
| `top_p` | Only sample from candidates that fit inside a probability mass cutoff. |

Changing sampling can change output style even when the model checkpoint stays
the same.

---

## Why tiny models can fail

Tiny models often repeat, drift, or contradict themselves because capacity and
training data are limited. That visible failure is useful for classroom
learning: students can see the difference between pattern generation and
reliable knowledge.


---

## FAQ

### Why does the model repeat itself?
Tiny models have limited capacity, so they may fall into repeating patterns instead of producing varied text.

### Why did pirate training change the style?
Retraining changed the token patterns the model sees most often, so pirate-like words and rhythm become more likely.

### Does attention mean understanding?
No. Attention shows which tokens are weighted more during prediction, not human-like understanding.

### Does lower loss mean the model is smart?
Not by itself. Lower loss means prediction error is lower on the training pattern, not that the model is generally intelligent.

### Can tiny models be wrong?
Yes. They can be fluent and still incorrect, repetitive, or off-topic.

---

<p align="center">
  <a href="../README.md">Home</a> •
  <a href="first_lesson_walkthrough.md">First Lesson Walkthrough</a> •
  <a href="teacher_guide.md">Teacher Guide</a> •
  <a href="student_worksheet.md">Student Worksheet</a> •
  <a href="architecture.md">Architecture</a> •
  <a href="how_llms_work.md">How LLMs Work</a>
</p>
