# How LLMs Work (Using Kairo)

This guide explains language models in plain English, without hype.

---

## 1) What a token is

A language model does not read text exactly like we do. It reads **tokens**.

In Kairo, tokens are bytes, so every character sequence becomes numeric IDs.
That means the model sees numbers and patterns, not ideas or intentions.

---

## 2) What prediction means

At each step, the model answers one question:

> “Given these previous tokens, which token is most likely next?”

It does this repeatedly. One token at a time becomes a sentence.

---

## 3) How training works

During training, Kairo shows the model many token sequences.
For each sequence, the model predicts the next token and compares that guess with the true next token.
Then it adjusts internal weights to reduce future mistakes.

This loop repeats thousands of times in larger systems, fewer times in tiny educational models.

---

## 4) Why loss matters

**Loss** is a numeric summary of prediction error.
- High loss = many wrong/uncertain predictions.
- Lower loss = predictions are matching training patterns better.

Loss does not mean “understanding.”
It only means better pattern prediction for the training objective.

---

## 5) Why models hallucinate

Models can produce incorrect statements because they are optimizing for likely token sequences, not truth checking.
If training data is incomplete, mixed, or misleading, the model can sound confident and still be wrong.

---

## 6) Why tiny models fail often

Tiny models (like Kairo’s educational GPT) have limited capacity:
- fewer parameters,
- less memory of long context,
- less ability to represent complex patterns.

So they may repeat, contradict themselves, or produce unstable text more often.

---

## 7) Why larger models feel smarter

Larger models usually train on much more data with much larger networks.
They can capture richer statistical patterns, which often makes responses feel more coherent.

But even large models still predict tokens; they are not human minds.

---

## 8) Why training data matters

Training data strongly shapes model behavior:
- writing style,
- common vocabulary,
- topic knowledge,
- common errors and biases.

If you change data, you change what the model is likely to produce.

---

## 9) What retraining changes

In Kairo, retraining is one of the clearest demonstrations.
Use the same prompt before and after retraining on a new dataset.
If outputs shift in style or topic, you are seeing data influence in action.

That is the key lesson: model behavior is learned pattern behavior.


## Attention in plain English
Attention is a weighting mechanism over earlier tokens for next-token prediction. It is useful evidence about pattern use, not proof of human-like understanding.
