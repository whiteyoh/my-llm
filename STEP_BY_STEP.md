# Kairo – Hands-On LLM Learning Lab

**Build it. Train it. Talk to it. Retrain it. Understand it.**

---

## Overview

Kairo is an educational platform that lets learners train, experiment with, and understand small language models (LLMs). It is designed for schools, STEM clubs, workshops, and independent learners to explore how models learn from text and change their behavior after retraining.

## Quick Start (CPU-Friendly)

### 1. Clone the repository
```bash
git clone https://github.com/whiteyoh/my-llm.git
cd my-llm
```

### 2. Set up virtual environment
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Mac/Linux
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```
Optional for Learn Mode:
```bash
pip install -e ".[learn]"
```

## Step-by-Step Learning Flow

### Step 1 – Train on normal stories
Create `data/samples/normal.txt` with normal story text.

Train:
```bash
python src/train.py --input_file data/samples/normal.txt --out_dir runs/normal_demo --epochs 2 --batch_size 4 --seq_len 32 --d_model 64 --n_heads 4 --n_layers 2 --device cpu
```

### Step 2 – Ask a question
```bash
python src/generate.py --checkpoint runs/normal_demo/best.pt --prompt "Tell me a story about the child and the magical stone" --max_new_tokens 50 --temperature 0.9 --top_k 20 --device cpu
```

### Step 3 – Retrain with additional normal data
Add `data/samples/normal_extra.txt` with extra normal story phrases and retrain using the same command.

### Step 4 – Ask another question
```bash
python src/generate.py --checkpoint runs/normal_demo/best.pt --prompt "What happens next in the village?" --max_new_tokens 50 --temperature 0.9 --top_k 20 --device cpu
```

### Step 5 – Train on pirate text
Create `data/samples/pirate.txt` with pirate phrases.
```bash
python src/train.py --input_file data/samples/pirate.txt --out_dir runs/pirate_demo --epochs 2 --batch_size 4 --seq_len 32 --d_model 64 --n_heads 4 --n_layers 2 --device cpu
```

### Step 6 – Ask a pirate question
```bash
python src/generate.py --checkpoint runs/pirate_demo/best.pt --prompt "Raise the anchor," --max_new_tokens 50 --temperature 0.9 --top_k 20 --device cpu
```

### Step 7 – Explore Learn Mode
```bash
streamlit run src/kairo_learn.py
```
- Visualize token predictions
- Inspect attention maps
- See probability changes after retraining
- Experiment interactively

## Key Concepts Learners Will Explore
- Tokens and tokenization
- Next-token prediction
- Attention patterns
- Model retraining effects
- How dataset changes impact output style

## Classroom Use
- Designed for schools, STEM clubs, and workshops
- Worksheets, Teacher Guide, and First Lesson Walkthrough available
- Easy to run on normal laptops (CPU only)
- Students can experiment with text, retraining, and prompts

## Documentation Map
- [First Lesson Walkthrough](docs/first_lesson_walkthrough.md)
- [Teacher Guide](docs/teacher_guide.md)
- [Student Worksheet](docs/student_worksheet.md)
- [Architecture](docs/architecture.md)
- [How LLMs Work](docs/how_llms_work.md)

## Roadmap
- Richer visuals (attention maps, token previews, retraining comparisons)
- Printable lesson packs
- More sample datasets (pirate, sci-fi, poems)
- Improved Learn Mode walkthroughs
- Classroom-ready exercises

## Safety & Scope
- Kairo is a learning tool, not a production chatbot
- Supervision recommended for younger learners
- Designed to demystify LLMs, not provide factual guarantees
