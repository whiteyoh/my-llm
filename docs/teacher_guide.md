# Kairo Teacher Guide

## Lesson overview
Kairo is a tiny educational language-model lab for demonstrating next-token prediction.

## Learning objectives
- Understand tokens.
- Understand training data.
- Understand next-token prediction.
- Understand loss.
- Understand why small models produce limited results.
- Understand why LLMs are not magic.

## Suggested age range
Secondary school (roughly ages 12-18), with teacher facilitation.

## 45-minute lesson plan
1. 10 min: Introduce tokens and byte-level text.
2. 10 min: Show dataset examples and discuss quality.
3. 15 min: Run a tiny training job and watch loss.
4. 10 min: Prompt the model and discuss outputs.

## 90-minute workshop plan
1. 15 min: Intro and safety context.
2. 20 min: Build a dataset from safe samples.
3. 25 min: Train model and inspect loss trends.
4. 20 min: Compare prompts and sampling settings.
5. 10 min: Reflection and misconceptions.

## Discussion questions
- Why does better training data usually help output quality?
- Why can low loss still produce strange text?
- What is missing from this tiny educational setup compared with modern LLM products?

## Safe dataset guidance
Use short, school-safe texts. Start with files in `data/samples/`.
Avoid personal data, harmful content, or copyrighted materials.

## What pupils should observe
- Loss usually decreases during training.
- Tiny models copy local patterns.
- Outputs can be repetitive or nonsensical.

## Common misconceptions
- "The model understands like a person" (it predicts tokens statistically).
- "One good output means the model is reliable" (it is not).

## Extension tasks
- Try different prompts and compare outputs.
- Train on mixed datasets and discuss bias.
- Explore top-k and top-p sampling effects.
