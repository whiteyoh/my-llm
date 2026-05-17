# Kairo

Build it. Train it. Talk to it. Understand it.

**An educational byte-level GPT lab that helps learners build, train, talk to, and understand a tiny language model.**

## What Kairo is
Kairo is a small, readable, beginner-friendly project for learning how language models work.

## Learn Mode walkthrough
Run Learn Mode:
```bash
pip install -e ".[learn]"
streamlit run src/kairo_learn.py
```

Learners follow a guided workflow:
1. **Build it**: paste/select training text, inspect token count, and preview first 20 byte tokens.
2. **Train it**: train a tiny GPT on CPU, watch train/validation loss, and learn that loss = prediction error.
3. **Talk to it**: enter a prompt, tune sampling, generate output, and inspect top next-token probabilities.
4. **Retrain it**: change text, retrain, and compare before/after outputs for the same prompt.
5. **Understand it**: discuss why low loss is not human understanding and why tiny models can be strange.

Screenshot idea: token viewer
Screenshot idea: loss chart
Screenshot idea: before/after retrain comparison

## Why this demystifies LLMs
- You can see raw byte tokens, not hidden magic.
- You can watch the model improve during training.
- You can inspect next-token probabilities directly.
- You can retrain and immediately observe behavior changes.
- You can discuss limitations with classroom-safe guardrails and teacher supervision.

## Safety in Kairo (lightweight classroom guardrails)
Kairo uses lightweight classroom guardrails. A teacher should supervise use. It is not full moderation or safeguarding.
