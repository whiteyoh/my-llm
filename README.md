# Kairo

Build it. Train it. Talk to it. Understand it.

**An educational byte-level GPT lab that helps learners build, train, talk to, and understand a tiny language model.**

## What Kairo is
Kairo is a small, readable, beginner-friendly project for learning how language models work.

## What Kairo is not
- Kairo is **not** a production LLM.
- Kairo is **not** instruction-tuned.
- Kairo is **not** a full moderation, alignment, or safeguarding platform.
- Kairo outputs may be poor, strange, biased, or unsuitable depending on training data.

## Safety in Kairo (lightweight classroom guardrails)
### What safety does
- Screens prompts for a small set of clearly unsafe classroom terms.
- Filters generated output for the same blocked terms by default.
- Shows clear safety notices in CLI and Learn Mode.
- Provides dataset safety warnings (short text, blocked terms, and possible personal data markers).

### What safety does not do
- It does not provide full moderation.
- It does not guarantee child-safety compliance.
- It does not replace teacher supervision.
- It can miss context, coded language, spelling changes, and implied meaning.

### Teacher guidance
- Prefer safe sample files in `data/samples/`.
- Review any custom dataset before pupils use it.
- Keep use supervised and discuss limitations openly.

### Disabling filtering for trusted local experiments
You can disable filtering in CLI tools with:
- `python src/generate.py ... --unsafe-disable-filter`
- `python src/chat.py ... --unsafe-disable-filter`

When disabled, Kairo prints a warning. This setting is not suitable for unsupervised learners.

## Quick start
```bash
pip install -e .
python src/train.py --input_file data/samples/space_adventure.txt --out_dir runs/demo --epochs 1 --batch_size 4 --seq_len 32 --d_model 64 --n_heads 4 --n_layers 2
python src/generate.py --checkpoint runs/demo/best.pt --prompt "The robot opened the door" --max_new_tokens 20
```

## Learn Mode
Optional Streamlit UI:
```bash
pip install -e ".[learn]"
streamlit run src/kairo_learn.py
```
