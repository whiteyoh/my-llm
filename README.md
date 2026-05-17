# Kairo

An educational byte-level GPT lab built with PyTorch.

## 1. What Kairo is

Kairo is a small, readable, beginner-friendly GPT-style project for learning how byte-level language modeling works end-to-end.

## 2. What Kairo is not

- Not a production LLM.
- Not instruction-tuned.
- No safety/alignment layer.
- Not designed for untrusted checkpoint execution.

## 3. Features

- Decoder-only transformer (causal self-attention)
- Byte-level tokenizer (UTF-8 bytes, vocab size 256)
- Training with validation split, gradient clipping, and checkpointing
- Resume support from `last.pt`
- Generation with temperature + top-k + top-p sampling
- Perplexity evaluation script
- Simple terminal chat demo

## 4. Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

Package note: distribution name is `kairo-llm`, while Python imports stay `tiny_llm` for compatibility.

## 5. Quick start

```bash
python src/train.py --input_file data/sample.txt --out_dir runs/demo --epochs 1 --batch_size 4 --seq_len 32
python src/generate.py --checkpoint runs/demo/best.pt --prompt "Once upon a time" --max_new_tokens 10
```

## 6. Train

```bash
python src/train.py \
  --input_file data/sample.txt \
  --out_dir runs/demo \
  --epochs 1 \
  --batch_size 4 \
  --seq_len 32 \
  --device auto
```

## 7. Resume training

```bash
python src/train.py \
  --input_file data/sample.txt \
  --out_dir runs/demo \
  --epochs 3 \
  --resume runs/demo/last.pt \
  --device auto
```

## 8. Generate text

```bash
python src/generate.py \
  --checkpoint runs/demo/best.pt \
  --prompt "Once upon a time" \
  --max_new_tokens 50 \
  --temperature 0.9 \
  --top_k 40 \
  --top_p 0.95 \
  --device auto
```

## 9. Evaluate checkpoints

```bash
python src/evaluate.py \
  --checkpoint runs/demo/best.pt \
  --input_file data/sample.txt \
  --batch_size 4 \
  --device auto
```

## 10. Chat demo

```bash
python src/chat.py --checkpoint runs/demo/best.pt --max_new_tokens 80
```

Type `/exit` or `/quit` to stop.

## 11. Checkpoint compatibility and safety

Kairo loads checkpoints through `tiny_llm.utils.load_checkpoint`, which first tries `torch.load(..., weights_only=True)` and falls back only for older torch versions.

Only load trusted local checkpoint files. External checkpoints can execute unsafe code paths in fallback mode.

## 12. Byte-level tokenizer limitations

The byte tokenizer is intentionally simple and dependency-free. It is easy to study, but usually less token-efficient than BPE/SentencePiece tokenizers.

## 13. Quality checks

```bash
ruff check .
python -m compileall src tests
pytest -q
```

## 14. Roadmap

- Keep examples small and educational
- Add clearer dataset preparation notes
- Add optional tiny eval metrics beyond perplexity
- Add minimal instruction fine-tuning example as a separate educational step

---

Output quality depends heavily on dataset size and dataset quality.
