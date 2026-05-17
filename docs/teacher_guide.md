# Kairo Teacher Guide

Kairo is designed for supervised educational use. Its core message for learners is:

> **LLMs predict patterns; they do not think like humans.**

---

## 1) Classroom Setup Checklist

### Before the lesson
- [ ] Install Python 3.11+.
- [ ] Install project dependencies: `pip install -e .`.
- [ ] (Optional) Install Learn Mode UI: `pip install -e ".[learn]"`.
- [ ] Run smoke training once on teacher machine.
- [ ] Run smoke generation once from saved checkpoint.
- [ ] Prepare 2–3 safe datasets (short, theme-based).
- [ ] Review classroom safety expectations with staff.

### In the room
- [ ] Confirm internet policy (Kairo can run offline after setup).
- [ ] Confirm student device access and power.
- [ ] Pair students if hardware is limited.
- [ ] Keep teacher demo screen visible.
- [ ] Keep safe mode ON.

---

## 2) Timing Plans

## 45-minute lesson (intro)
- **0–5 min**: Explain goals and safety.
- **5–12 min**: Build it (tokens).
- **12–22 min**: Train it (loss chart).
- **22–32 min**: Talk to it (prompt + generate).
- **32–40 min**: Retrain it (dataset change).
- **40–45 min**: Reflection and wrap-up.

## 90-minute workshop (deeper)
- **0–15 min**: Concepts + safeguards.
- **15–30 min**: Token exploration activity.
- **30–50 min**: Training and metric reading.
- **50–65 min**: Sampling controls and probabilities.
- **65–80 min**: Retrain comparison groups.
- **80–90 min**: Debrief + extension options.

---

## 3) Hardware Expectations

Minimum practical setup:
- CPU-only laptops/desktops are acceptable.
- 8 GB RAM recommended (4 GB may work with smaller runs).
- Python 3.11+.

Classroom recommendations:
- 1 device per 1–2 students.
- Run tiny settings (small `d_model`, fewer epochs) for predictable lesson pacing.
- If time is tight, pre-train one checkpoint for demonstration.

---

## 4) Safe Dataset Suggestions

Good starter topics:
- space travel logs,
- weather reports,
- nature descriptions,
- robotics diary entries,
- sports commentary.

Avoid datasets containing:
- personal data (emails, phone numbers, addresses),
- instructions for harm or illegal activity,
- explicit or age-inappropriate content,
- copyrighted text you do not have permission to use.

---

## 5) Teacher Moderation Workflow

1. **Pre-screen** all training text.
2. **Enable safe mode** before student generation.
3. **Set classroom prompt rules** (respectful, safe, on-topic).
4. **Monitor outputs live** during exercises.
5. **Pause and review** if an output seems unsafe or inappropriate.
6. **Switch to known-safe dataset** if needed.
7. **Debrief** why the output happened (pattern learning, not reasoning intent).

---

## 6) Classroom Rules for Students

- Use only teacher-approved datasets.
- Keep prompts school-appropriate and respectful.
- Do not enter personal information.
- If an output looks strange or unsafe, stop and tell the teacher.
- Treat model output as a prediction experiment, not as truth.

---

## 7) What to Say When Outputs Look Strange

Use lines like:
- “This model is predicting likely patterns, not checking facts.”
- “It can sound confident and still be wrong.”
- “Strange repetition often means limited data or unstable sampling.”
- “Let’s inspect probabilities and training data to explain this result.”

This keeps discussion scientific instead of sensational.

---

## 8) Troubleshooting Tips

- **Training is too slow**: reduce epochs, sequence length, layers, or model dimension.
- **Loss not improving**: use cleaner/repetitive training text and verify tokenization input.
- **Output is repetitive**: adjust temperature/top-k/top-p; expand dataset variety.
- **Checkpoint missing**: confirm `--out_dir` path and that training finished.
- **Streamlit won’t launch**: ensure `pip install -e ".[learn]"` completed.

---

## 9) Extension Challenges

- Compare two groups using different datasets and report style differences.
- Keep dataset fixed and compare sampling settings.
- Predict next token before generating, then compare with model top choice.
- Create a “bias check” by analyzing repeated stereotypes in small datasets.
- Design a short class report: “What retraining changed and why.”

---

## 10) Learning Outcomes

By the end of a Kairo lesson, students should be able to:
- explain that an LLM predicts next tokens from patterns,
- describe tokenization at a basic level,
- interpret loss as prediction error,
- compare outputs before and after retraining,
- identify why outputs can be wrong, repetitive, or odd,
- apply basic safety thinking when using generative AI.


## Guided lesson script additions
- Run seven-step guided lesson (predict, inspect, train, generate, retrain, compare, reflect).
- Use attention map as a discussion prompt: "Attention shows which earlier tokens the model looked at most when making a prediction."
- Save classroom experiments and review metadata later for comparison.
