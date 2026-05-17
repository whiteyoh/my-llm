# Kairo

**Build it. Train it. Talk to it. Retrain it. Understand it.**

Kairo is a hands-on educational GPT lab for demystifying how language models learn.

## The idea
Kairo helps learners build and train a tiny model on CPU.
It makes tokens, probabilities, loss, and attention visible.
It supports a guided classroom learning loop.
It is intentionally small and transparent.
It is designed for curiosity, not production deployment.

## Why it exists
Most people use AI without understanding it. Kairo makes the invisible parts visible.

## The learning loop
| Step | Learner does | Kairo shows | Concept learned |
|---|---|---|---|
| Build it | choose text | byte tokens | tokenisation |
| Train it | run training | loss chart | prediction error |
| Talk to it | prompt model | generated output | sampling |
| Retrain it | change data | before/after output | data changes behaviour |
| Understand it | inspect probabilities/attention | tables/charts | models predict patterns |

## Try it in 3 minutes
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
python src/train.py --input_file data/samples/space_adventure.txt --out_dir runs/demo --epochs 1 --batch_size 4 --seq_len 32 --d_model 64 --n_heads 4 --n_layers 2 --device cpu
python src/generate.py --checkpoint runs/demo/best.pt --prompt "The robot opened the door" --max_new_tokens 20 --device cpu
```

## Learn Mode
Run `pip install -e ".[learn]"` and `streamlit run src/kairo_learn.py`.

Screenshot idea placeholders:
- guided workflow
- token viewer
- probability table
- attention view
- retrain comparison

## Classroom use
Teacher-led demos, secondary school lessons, STEM clubs, and workshops.

## Safety and supervision
Kairo includes lightweight classroom guardrails and teacher controls, but it is not full moderation.

## What Kairo is not
Not a production LLM. Not instruction-tuned. Not fully moderated. Not a chatbot replacement.

## Developer quickstart
Install, train, generate, evaluate, chat, test.

## Documentation map
- [Teacher guide](docs/teacher_guide.md)
- [Student worksheet](docs/student_worksheet.md)
- [Architecture](docs/architecture.md)
- [How LLMs work](docs/how_llms_work.md)

## Roadmap
Prioritise learning UX, attention visuals, experiment comparison, and lesson packs.
