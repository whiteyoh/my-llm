# Build and Train Your Own Mini-LLM

This repository gives you a **from-scratch, educational pipeline** for creating and training a small GPT-style language model.

It is designed for people who want to:

- understand how a decoder-only transformer works,
- train on their own text data,
- generate text with the trained model,
- and extend the project into a larger/custom LLM system.

---

## What You Get

- A lightweight GPT-style model implemented in PyTorch.
- A simple byte-level tokenizer (no external tokenizer dependency).
- A training script with checkpointing and validation loss reporting.
- A text generation script for inference/sampling.
- Clear configuration flags so you can scale model/data settings.

---

## Project Structure

```text
.
├── README.md
├── requirements.txt
├── data
│   └── sample.txt
└── src
    ├── tiny_llm
    │   ├── __init__.py
    │   ├── data.py
    │   ├── model.py
    │   └── utils.py
    ├── train.py
    └── generate.py
```

---

## Quick Start

### 1) Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

### 3) Train a model

```bash
python src/train.py \
  --input_file data/sample.txt \
  --out_dir runs/demo \
  --epochs 8 \
  --batch_size 32 \
  --seq_len 128
```

### 4) Generate text

```bash
python src/generate.py \
  --checkpoint runs/demo/best.pt \
  --prompt "Once upon a time" \
  --max_new_tokens 120 \
  --temperature 0.9 \
  --top_k 40
```

---

## How It Works

### Data pipeline

1. Read your input text file.
2. Convert text into UTF-8 bytes (`0-255` vocabulary size).
3. Create overlapping sequences of length `seq_len` for next-token prediction.
4. Split into train/validation sets.

### Model architecture

A decoder-only transformer made of:

- Token embeddings
- Learned positional embeddings
- Stacked causal self-attention blocks
- Feed-forward MLP layers
- Final layer norm + linear head

### Training objective

Standard autoregressive language modeling:

- Input tokens: `x[0...n-1]`
- Targets: `x[1...n]`
- Loss: cross-entropy over next token prediction

---

## Using Your Own Dataset

1. Put your corpus in a plain text file (UTF-8), e.g. `data/my_corpus.txt`.
2. Train:

```bash
python src/train.py --input_file data/my_corpus.txt --out_dir runs/my_model
```

### Dataset tips

- More text = better fluency/generalization.
- Clean, consistent formatting helps.
- Start small (a few MB) to verify pipeline, then scale.

---

## Key Training Arguments

- `--d_model`: embedding/hidden size (default: `256`)
- `--n_heads`: attention heads (default: `8`)
- `--n_layers`: transformer blocks (default: `6`)
- `--seq_len`: context window (default: `128`)
- `--batch_size`: samples per step (default: `32`)
- `--lr`: learning rate (default: `3e-4`)
- `--epochs`: passes over data (default: `8`)
- `--dropout`: dropout rate (default: `0.1`)

Example bigger run:

```bash
python src/train.py \
  --input_file data/my_corpus.txt \
  --out_dir runs/bigger \
  --d_model 384 \
  --n_heads 8 \
  --n_layers 8 \
  --seq_len 256 \
  --batch_size 24 \
  --epochs 12
```

---

## Checkpoints and Outputs

Training writes to `--out_dir`:

- `best.pt`: best validation checkpoint
- `last.pt`: most recent checkpoint
- `metrics.json`: per-epoch losses
- `config.json`: training/model config

---

## Extending Toward a “Real” LLM

This starter is educational and small. To grow into a production-grade LLM workflow, consider:

- Subword tokenizer (BPE/SentencePiece)
- Mixed precision + gradient accumulation
- Multi-GPU distributed training (DDP/FSDP)
- Better datasets and streaming loaders
- Evaluation suites (perplexity, benchmarks)
- Fine-tuning (LoRA/QLoRA, instruction tuning)
- Safety filters and inference serving stack

---

## Troubleshooting

### CUDA out of memory

- Reduce `--batch_size`
- Reduce `--seq_len`
- Reduce model size (`--d_model`, `--n_layers`)

### Loss does not improve

- Train longer
- Lower learning rate (`--lr 1e-4`)
- Increase dataset size/quality

### Generated text is repetitive

- Increase `--temperature` (e.g. `1.0`)
- Use smaller `--top_k` or add top-p sampling (future extension)

---

## License

Use this repo as a learning baseline and adapt it freely.
