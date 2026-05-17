# Kairo Teacher Guide

## Before class checklist
- Install: `pip install -e .` (and optionally `pip install -e ".[learn]"`).
- Verify smoke commands run once on your machine.
- Open safe sample data from `data/samples/`.
- Confirm classroom safe mode is ON in Learn Mode.

## Safe dataset checklist
- No personal data (emails, phone numbers, addresses).
- No violent/self-harm/weapon instructions.
- No copyrighted text you cannot use.
- Age-appropriate language for your pupils.
- Short, focused themes (space, nature, robots) work best.

## Prompt rules for pupils
- Keep prompts classroom-safe and respectful.
- No requests for harm, weapons, or illegal advice.
- Use short prompts first, then iterate.
- Report unsuitable output to teacher immediately.

## 45-minute lesson script
1. **0-5 min**: Intro to next-token prediction and lesson goals.
2. **5-12 min**: Build it (paste dataset, inspect byte tokens).
3. **12-20 min**: Train it (run tiny CPU training, watch loss chart).
4. **20-30 min**: Talk to it (prompt and generation settings).
5. **30-38 min**: Retrain it (change dataset and compare outputs).
6. **38-45 min**: Understand it discussion and reflection.

## 90-minute workshop script
1. **0-15 min**: Concepts + safety framing.
2. **15-30 min**: Build it activity with token-table worksheet.
3. **30-45 min**: Train and read train/validation loss.
4. **45-60 min**: Prompt design and next-token probability view.
5. **60-75 min**: Retrain comparison groups (different datasets).
6. **75-90 min**: Debrief: pattern learning vs understanding.

## Learn Mode workflow (teacher explanation)
- **Build it**: show that text becomes byte tokens.
- **Train it**: explain loss as "how wrong next-token guesses are".
- **Talk to it**: show sampling controls and output variability.
- **Retrain it**: prove behavior changes when training text changes.
- **Understand it**: reinforce limits (pattern matching, no human understanding).

## Discussion prompts after retraining
- What changed in tone/words/style?
- Which dataset phrases appeared in outputs?
- Did the model reason, or mirror patterns?
- Why did odd repetitions happen?

## If output is unsuitable
1. Pause pupil interaction and do not continue generating.
2. Remind class that guardrails are lightweight, not perfect.
3. Switch to reviewed safe sample text and safer prompt.
4. Keep safe mode ON and re-run with teacher supervision.
5. Use the incident as a discussion on AI limitations and safety.
