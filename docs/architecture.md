# Architecture

## Why `tiny_llm` inside Kairo?
Kairo is the product and learning experience; `tiny_llm` is the internal reusable engine package.

## ASCII diagram
```
CLI/Streamlit UI -> tiny_llm helpers -> model/data/safety/attention -> artifacts (runs/*)
```

## Learn Mode flow
Build text -> configure -> train -> generate -> compare retrain -> inspect attention -> save metadata/checkpoint.

## Model flow
Text -> byte tokenizer -> sequence dataset -> TinyGPT -> logits -> sampling output.

## Safety flow
Prompt/output -> safety checks (blocked terms/masking) -> classroom-safe display.

## Experiment persistence flow
save_experiment -> metadata.json + model.pt; load_experiment_metadata/load_experiment_checkpoint/restore_experiment_model.

## Attention visualisation flow
Prompt -> forward with `return_attn=True` -> layer/head select -> matrix/table for UI.
