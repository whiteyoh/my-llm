# Kairo Student Worksheet

Name: ____________________   Date: ____________________   Group: ____________________

## Big idea
**LLMs predict patterns in text. They do not think like humans.**

---

## Activity 1: Build it (tokens)

1. What training text did your group use?
2. How many tokens were shown?
3. Copy at least 8 tokens from the token viewer.

| Index | Token ID | Display / character |
|---|---:|---|
| 0 |  |  |
| 1 |  |  |
| 2 |  |  |
| 3 |  |  |
| 4 |  |  |
| 5 |  |  |
| 6 |  |  |
| 7 |  |  |

**Quick thought:** Did any token patterns repeat? Which ones?

---

## Activity 2: Train it (loss)

Record your settings:
- Epochs:
- Batch size:
- Sequence length:

Record metrics:
- Latest training loss:
- Latest validation loss:

Reflection:
- Did loss go down during training?
- Was validation loss higher or lower than training loss?
- What might that mean about generalization?

---

## Activity 3: Guess the next token

Prompt: ___________________________________________

Before generating, predict what comes next.
- **My guess:**
- **Model top prediction:**
- **Top 3 token predictions:**
  1.
  2.
  3.

Were you close? Why or why not?

---

## Activity 4: Talk to it (generation)

Write one prompt and output:
- Prompt:
- Output:

Change one sampling control (temperature, top-k, or top-p) and try again.
- What changed?
- Did output become safer, stranger, or more repetitive?

---

## Activity 5: Retrain comparison (before vs after)

Use the **same prompt** before and after retraining.

| Same prompt | Before retrain | After retrain |
|---|---|---|
|  |  |  |

Questions:
1. What changed in style, topic, or vocabulary?
2. Which words seem copied from the new dataset?
3. What does this show about training data influence?

---

## Activity 6: Probability prediction challenge

Choose a short prompt and inspect next-token probabilities.
- Prompt:
- Highest-probability token:
- Second token:
- Third token:

Why do you think token #1 was most likely?

---

## Reflection Prompts

- One thing I understand better about LLMs now:
- One way LLMs can fail:
- One safety rule that matters in class:
- One question I still have:

---

## Glossary

- **Token**: A piece of text the model reads (in Kairo, bytes).
- **Loss**: A number showing prediction error; lower usually means better fit.
- **Probability**: How likely the model thinks each next token is.
- **Retraining**: Training again on new text to change model behavior.
- **Dataset**: The text collection used for training.
