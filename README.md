# Kairo

**Kairo is an educational byte-level GPT lab that helps learners build, train, and understand a tiny language model from first principles.**

## What Kairo is
Kairo is a small, readable, beginner-friendly project for learning how language models work.

## What Kairo is not
- Kairo is **not** a production LLM.
- Kairo is **not** instruction-tuned.
- Kairo has **no** safety/alignment layer.
- Kairo outputs may be poor, strange, biased, or unsuitable depending on training data.

## Who it is for
- Students learning core ML/LLM ideas.
- Teachers running short classroom demos.
- Beginners who want transparent code.

## Suggested classroom use
- Use short, safe datasets from `data/samples/`.
- Train tiny configs on CPU.
- Discuss prediction, loss, and limitations.

## Safety notes for teachers
Kairo includes only lightweight prompt/output filtering for obvious cases.
It is not full moderation and should always be supervised.

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

## CLI usage
- Train: `python src/train.py --help`
- Generate: `python src/generate.py --help`
- Evaluate: `python src/evaluate.py --help`
- Chat: `python src/chat.py --help`

## Roadmap
- Keep educational defaults tiny and fast.
- Expand classroom activities.
- Add more explainers and visualizations.
