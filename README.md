# Kairo

Build it. Train it. Talk to it. Retrain it. Understand it.

Kairo is a hands-on educational GPT lab that helps learners inspect how language models actually work.

Logo: docs/assets/kairo-logo.svg

## Navigation

- Home: README.md
- First Lesson: docs/first_lesson_walkthrough.md
- Teacher Guide: docs/teacher_guide.md
- Student Worksheet: docs/student_worksheet.md
- Architecture: docs/architecture.md
- How LLMs Work: docs/how_llms_work.md

## The idea

Kairo makes model behaviour visible:

- tokenisation
- next-token prediction
- probabilities
- attention
- retraining effects

Instead of treating AI like magic, Kairo exposes the mechanics directly.

## Why it exists

Many learners meet AI through polished products that hide the mechanics.

Kairo exists to make those mechanics:

- concrete
- testable
- discussable
- visible in a classroom

## The learning loop

| Step          | Learner action                      | Concept learned              |
| ------------- | ----------------------------------- | ---------------------------- |
| Build it      | Pick training text                  | Tokens and dataset shape     |
| Train it      | Run a tiny transformer              | Loss and pattern learning    |
| Talk to it    | Prompt the model                    | Sampling and uncertainty     |
| Retrain it    | Change the data                     | Distribution shift           |
| Understand it | Inspect probabilities and attention | Influence, not understanding |

## Simple architecture

Training text  
↓  
Byte tokenizer  
↓  
Sequence dataset  
↓  
TinyGPT  
↓  
Loss and updates  
↓  
Generation and inspection

## Installation

Run:

python -m venv .venv
source .venv/bin/activate
pip install -e .

Optional Learn Mode:

pip install -e ".[learn]"

## Try it in 3 minutes

Train:

python src/train.py --input_file data/samples/space_adventure.txt --out_dir runs/demo --epochs 1 --batch_size 4 --seq_len 32 --d_model 64 --n_heads 4 --n_layers 2 --device cpu

Generate:

python src/generate.py --checkpoint runs/demo/best.pt --prompt "The robot opened the door" --max_new_tokens 20 --device cpu

Evaluate:

python src/evaluate.py --checkpoint runs/demo/best.pt --input_file data/samples/space_adventure.txt --device cpu

Chat:

python src/chat.py --checkpoint runs/demo/best.pt --device cpu

## What you should see

With tiny datasets and tiny models, you should expect:

- short repetitive phrases
- unstable grammar
- occasional nonsense
- noticeable style shifts after retraining

That weirdness is the point: it reveals the mechanism.

## Learn Mode

Launch interactive Learn Mode:

streamlit run src/kairo_learn.py

You can walk students through:

- token previews
- training curves
- next-token probabilities
- attention maps
- retrain-and-compare experiments

## Why byte-level tokens?

Byte-level tokenisation is:

- simple
- deterministic
- easy to visualise
- suitable for any text

Production models often use more advanced tokenisers, but byte-level tokens make the mechanics easier to inspect.

## Expected weirdness

Tiny models frequently:

- copy chunks from training text
- overfit quickly
- drift off-topic
- contradict themselves
- repeat phrases

These are valuable teaching moments, not failures.

## Common misconceptions

- Low loss means intelligence: No, it means lower prediction error.
- Attention is reasoning: No, it is weighting over previous tokens.
- The model knows facts: No, it predicts plausible continuations.
- Generated text means understanding: No, it means the model learned patterns.

## Classroom use

Kairo works for:

- teacher-led demos
- pair labs
- short workshops
- independent experiments
- STEM clubs

Start with:

- First Lesson Walkthrough: docs/first_lesson_walkthrough.md
- Teacher Guide: docs/teacher_guide.md

## Safety and supervision

Kairo includes lightweight classroom-safe checks, but it is not fully moderated.
Teacher supervision is required.
Kairo is not suitable for unsupervised public deployment.

## What Kairo is not

Kairo is not:

- a production chatbot
- a benchmark-leading model
- an autonomous agent
- a replacement for critical thinking
- a fully moderated child-safety system

It is a learning tool for inspecting core LLM mechanics.

## Developer quickstart

ruff check .
python -m compileall src tests
pytest -q

## Documentation map

- First Lesson Walkthrough: docs/first_lesson_walkthrough.md
- Teacher Guide: docs/teacher_guide.md
- Student Worksheet: docs/student_worksheet.md
- Architecture: docs/architecture.md
- How LLMs Work: docs/how_llms_work.md

## Roadmap

Future educational improvements:

- richer attention visuals
- clearer experiment comparison UI
- more classroom-ready sample datasets
- additional explainability activities
- printable lesson packs
- screenshots and walkthrough images
