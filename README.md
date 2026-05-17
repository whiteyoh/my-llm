# tiny-llm

A small, educational GPT-style language model built with PyTorch and a byte-level tokenizer.

## Features

- Decoder-only transformer (causal self-attention)
- Byte-level tokenizer (UTF-8 bytes, vocab size 256)
- Training with validation split, reproducible seeding, gradient clipping
- Checkpoint save/resume (`best.pt`, `last.pt`)
- Text generation with temperature + top-k + top-p sampling
- Evaluation script (loss + perplexity)
- Simple terminal chat demo
- Tests + lint + CI quality workflow

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Train

```bash
python src/train.py \
  --input_file data/sample.txt \
  --out_dir runs/demo \
  --epochs 1 \
  --batch_size 4 \
  --seq_len 32
```

## Resume training

```bash
python src/train.py \
  --input_file data/sample.txt \
  --out_dir runs/demo \
  --epochs 3 \
  --resume runs/demo/last.pt
```

## Generate (top-k + top-p)

```bash
python src/generate.py \
  --checkpoint runs/demo/best.pt \
  --prompt "Once upon a time" \
  --max_new_tokens 50 \
  --temperature 0.9 \
  --top_k 40 \
  --top_p 0.95
```

## Evaluate

```bash
python src/evaluate.py \
  --checkpoint runs/demo/best.pt \
  --input_file data/sample.txt
```

## Chat demo

```bash
python src/chat.py --checkpoint runs/demo/best.pt
```

Type `/exit` or `/quit` to stop.

## Quality checks

```bash
ruff check .
python -m compileall src tests
pytest -q
```

## Byte-level tokenizer limitations

The byte tokenizer is intentionally simple and has no external tokenizer dependency. This makes the code easy to understand, but is generally less token-efficient than BPE/SentencePiece.

## Roadmap

- richer evaluation metrics
- optional mixed precision training
- larger dataset tooling
- configurable learning-rate schedules
- instruction-style fine-tuning examples
