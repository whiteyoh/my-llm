# Kairo Step-by-Step Guide

**Build it. Train it. Talk to it. Retrain it. Understand it.**

This guide is the shortest complete path through Kairo. It uses the sample
datasets already included in the repository, so learners can focus on what
changes in the model rather than on setup work.

---

## 1. Set up Kairo

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

For the interactive classroom app:

```bash
pip install -e ".[learn]"
```

Commands in this guide use the installed `kairo-*` aliases. The older
`python src/...` script paths still work when you are developing inside the
repository.

---

## 2. Train on normal story text

Use the space-adventure sample as the "normal" baseline.

```bash
kairo-train --input_file data/samples/space_adventure.txt --out_dir runs/normal_demo --epochs 1 --batch_size 4 --seq_len 32 --d_model 64 --n_heads 4 --n_layers 2 --device cpu
```

Watch for:

- the device used for training
- the number of model parameters
- train and validation loss
- the saved `best.pt` checkpoint

---

## 3. Generate from the baseline model

```bash
kairo-generate --checkpoint runs/normal_demo/best.pt --prompt "Captain Rowan looked at the stars" --max_new_tokens 40 --temperature 0.9 --top_k 20 --device cpu
```

Record the output before changing the dataset. It may be repetitive or strange;
that is expected for a tiny model.

---

## 4. Train the same architecture on pirate text

Use the same model size and training settings, but change the data.

```bash
kairo-train --input_file data/samples/pirate_dialogue.txt --out_dir runs/pirate_demo --epochs 1 --batch_size 4 --seq_len 32 --d_model 64 --n_heads 4 --n_layers 2 --device cpu
```

This classroom comparison trains a fresh tiny model with the same architecture.
The learning question is: what changes when the data changes?

---

## 5. Generate with the same prompt

```bash
kairo-generate --checkpoint runs/pirate_demo/best.pt --prompt "Captain Rowan looked at the stars" --max_new_tokens 40 --temperature 0.9 --top_k 20 --device cpu
```

Compare the before and after outputs:

| Evidence to compare | What to look for |
|---|---|
| Vocabulary | New words, repeated words, style markers |
| Tone | Story-like, pirate-like, poetic, technical |
| Structure | Sentence length, punctuation, repetition |
| Reliability | Fluent text vs true statements |

---

## 6. Evaluate a checkpoint

```bash
kairo-evaluate --checkpoint runs/normal_demo/best.pt --input_file data/samples/space_adventure.txt --device cpu
```

Lower loss and perplexity usually mean the model predicts this dataset better.
They do not mean the model understands the text like a person.

---

## 7. Open Learn Mode

```bash
kairo-learn
```

Use Learn Mode to:

- preview byte tokens
- train and retrain interactively
- compare before and after outputs
- inspect top next-token probabilities
- inspect attention patterns
- save and restore local experiments

---

## 8. Print classroom materials

```bash
pip install -e ".[pdf]"
python tools/pdf/generate_printables.py
python tools/pdf/generate_tech_i_can_book.py
```

Generated PDFs are written to `docs/printable/`.
Use `python tools/pdf/generate_printables.py letter` if your class needs US
Letter instead of A4.

The generator writes both simple filenames, such as `teacher_guide.pdf`, and
title-cased aliases, such as `Kairo_Teacher_Guide.pdf`, so older links keep
working.

---

## 9. Optional: Turn it into QA behavior

Create QA training text from JSONL:

```bash
kairo-build-qa-corpus --input_jsonl qa_space_facts.jsonl --output_file runs/qa_space_facts.txt
```

`--input_jsonl` accepts either a full path or a bundled sample name.

Train and ask a question with context:

```bash
kairo-train --input_file runs/qa_space_facts.txt --out_dir runs/qa_demo --epochs 1 --batch_size 4 --seq_len 32 --d_model 64 --n_heads 4 --n_layers 2 --device cpu
kairo-qa --checkpoint runs/qa_demo/best.pt --question "Who pilots the Aurora?" --context "Captain Rowan is the pilot of the starship Aurora."
```

Tip for classrooms: always provide `--context` or `--context_file`. If tiny-model
generation quality is weak, Kairo QA now falls back to the best matching
sentence from the supplied context.

---

## Reflection questions

- What changed after switching datasets?
- Which output details are evidence of the training data?
- Why can tiny models sound fluent but still be wrong?
- What does attention help inspect?
- What does attention not prove?

---

## Next experiments

- Compare `space_adventure.txt` with `short_poems.txt`.
- Compare `robot_helper.txt` with `pirate_dialogue.txt`.
- Change only `epochs` and observe loss and output changes.
- Keep the same prompt across every run for a fair comparison.
