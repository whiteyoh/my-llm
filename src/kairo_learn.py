from __future__ import annotations

import streamlit as st

from tiny_llm.data import ByteTokenizer
from tiny_llm.experiments import load_experiment_metadata, make_experiment_metadata, restore_experiment_model, save_experiment
from tiny_llm.learn import build_attention_labels, build_attention_matrix_rows, build_attention_preview, build_probability_preview, build_restored_learning_state, build_token_preview, build_training_config, create_model_status, enforce_teacher_limits, generate_learning_output, prepare_retrain_comparison, train_tiny_model, validate_learn_training_text
from tiny_llm.paths import read_sample_text
from tiny_llm.safety import SafetyConfig, safety_notice

DEFAULTS = {"seq_len": 32, "d_model": 64, "n_heads": 4, "n_layers": 2, "epochs": 1, "batch_size": 4, "seed": 42}
MAX_CLASSROOM_NEW_TOKENS = 40
PRESETS = {
    "Very small / classroom demo": DEFAULTS,
    "Small / better output": {"seq_len": 48, "d_model": 96, "n_heads": 4, "n_layers": 3, "epochs": 2, "batch_size": 4, "seed": 42},
    "Custom": DEFAULTS,
}


st.set_page_config(page_title="Kairo Learn Mode", layout="centered")
st.title("Kairo Learn Mode: Build it. Train it. Talk to it. Retrain it. Understand it.")
st.info("Kairo uses lightweight classroom guardrails with teacher control and human review.")
st.caption(safety_notice())

st.sidebar.header("Guided lesson")
lesson_steps = [
    ("1) Predict the next token yourself", "Student action: Guess what byte/token comes next.", "Reflection: What clue in the prompt helped you?") ,
    ("2) Inspect Kairo predictions", "Student action: Check top-token probability table.", "Reflection: Did Kairo match your guess?") ,
    ("3) Train the model", "Student action: Train with classroom text.", "Reflection: Did loss go down?") ,
    ("4) Generate from a prompt", "Student action: Try a new prompt.", "Reflection: What pattern is repeated?") ,
    ("5) Retrain on different text", "Student action: Switch domain and retrain.", "Reflection: Which tokens changed most?") ,
    ("6) Compare before/after", "Student action: Use comparison panel.", "Reflection: What changed and why?") ,
    ("7) Reflect", "Student action: Write one misconception corrected today.", "Reflection: Does attention imply understanding?") ,
]
for title, action, reflection in lesson_steps:
    with st.sidebar.expander(title):
        st.write(action)
        st.caption(reflection)

st.sidebar.header("Teacher controls")
show_advanced = st.sidebar.toggle("Show advanced hyperparameters", value=False)
safe_mode = st.sidebar.toggle("Classroom Safe Mode", value=True)
max_new_tokens_cap = int(st.sidebar.number_input("Allowed max_new_tokens", min_value=5, max_value=80, value=40))
model_size_preset = st.sidebar.selectbox("Max model size preset", ["Classroom demo", "Moderate"], index=0)
custom_banned = st.sidebar.text_area("Custom banned terms (comma-separated)", value="")
def reset_session_state(keys: list[str] | None = None) -> None:
    session_keys = keys or ["kairo_state", "before_output", "last_prompt", "last_output", "restored_meta", "restored_model"]
    for key in session_keys:
        st.session_state.pop(key, None)


if st.sidebar.button("Reset session"):
    reset_session_state()
    st.sidebar.success("Session reset.")

banned_terms = tuple(t.strip() for t in custom_banned.split(",") if t.strip()) or None
safety_cfg = SafetyConfig(enabled=safe_mode, banned_terms=banned_terms or SafetyConfig().banned_terms)

default_text = read_sample_text("space_adventure.txt")
training_text = st.text_area("Build it: choose or paste training text", value=default_text, height=170)

st.subheader("Training configuration")
preset = st.selectbox("Preset", list(PRESETS.keys()))
base = PRESETS[preset]
col1, col2, col3 = st.columns(3)
seq_len = col1.number_input("seq_len", min_value=8, max_value=128, value=base["seq_len"])
d_model = col2.number_input("d_model", min_value=32, max_value=256, value=base["d_model"], step=32)
n_heads = col3.number_input("n_heads", min_value=1, max_value=8, value=base["n_heads"])
col4, col5, col6 = st.columns(3)
if show_advanced:
    n_layers = col4.number_input("n_layers", min_value=1, max_value=8, value=base["n_layers"])
    epochs = col5.number_input("epochs", min_value=1, max_value=20, value=base["epochs"])
    batch_size = col6.number_input("batch_size", min_value=1, max_value=32, value=base["batch_size"])
else:
    n_layers, epochs, batch_size = base["n_layers"], base["epochs"], base["batch_size"]

for warning in validate_learn_training_text(training_text, banned_terms=safety_cfg.banned_terms):
    st.warning(warning)

preview = build_token_preview(training_text, limit=20)
st.subheader("1) Build it: token viewer")
st.write(f"Token count: **{len(ByteTokenizer().encode(training_text))}**")
st.write("First 20 byte tokens:")
st.table(preview)
st.caption("Kairo uses byte-level tokens so every text can be encoded without a separate tokenizer file.")
if preview:
    snippet = training_text[:120]
    tok = ByteTokenizer()
    ids = [int(row["token_id"]) for row in preview]
    st.code(f"Original snippet: {snippet}\nEncoded bytes: {ids}\nDecoded round trip: {tok.decode(ids)}")

cfg, cfg_warnings = build_training_config({"seq_len": int(seq_len), "d_model": int(d_model), "n_heads": int(n_heads), "n_layers": int(n_layers), "epochs": int(epochs), "batch_size": int(batch_size), "seed": int(base.get("seed", 42))}, preset=model_size_preset)
max_new_tokens_cap, cap_warn = enforce_teacher_limits({"max_new_tokens": max_new_tokens_cap}, model_size_preset)
max_new_tokens_cap = max_new_tokens_cap["max_new_tokens"]
cfg_warnings.extend(cap_warn)
for warning in cfg_warnings:
    st.warning(warning)

train_col, retrain_col, reset_col = st.columns(3)
train_clicked = train_col.button("Train")
retrain_clicked = retrain_col.button("Retrain")
if reset_col.button("Reset session"):
    reset_session_state(keys=["kairo_state", "before_output", "last_prompt", "last_output", "restored_meta", "restored_model"])
    st.success("Session reset.")

if train_clicked or retrain_clicked:
    if len(ByteTokenizer().encode(training_text)) <= cfg["seq_len"] + 1:
        st.error("Training text is too short for these settings. Add more text or lower seq_len.")
    else:
        if retrain_clicked and "last_output" in st.session_state:
            st.session_state["before_output"] = st.session_state.get("last_output")
        progress = st.progress(0.0, text="Starting training...")
        st.session_state["kairo_state"] = train_tiny_model(training_text, cfg, progress_callback=lambda p: progress.progress(p))
        st.success("You have trained your own tiny language model.")

st.subheader("Model status")
status = create_model_status(st.session_state.get("kairo_state"))
if status["trained"]:
    st.success(status["label"])
    st.write(f"Token count: {status['token_count']}")
    st.write(f"Sequence count: {status['sequence_count']}")
    st.write(f"Parameter count: {status['param_count']}")
    st.write(f"Latest train loss: {status['train_loss']:.4f}")
    st.write(f"Latest validation loss: {status['val_loss']:.4f}")
else:
    st.warning(status["label"])

st.subheader("2) Train it: loss chart")
if "kairo_state" in st.session_state:
    state = st.session_state["kairo_state"]
    st.line_chart({"train_loss": state["train_losses"], "validation_loss": state["val_losses"]})
    st.caption("Loss measures how wrong the model is when predicting the next token. Lower is better.")
    if state["val_losses"][-1] > state["train_losses"][-1]:
        st.warning("Validation loss is higher than training loss. The model may not generalize well yet.")

st.subheader("3) Talk to it")
prompt = st.text_input("Prompt", value=st.session_state.get("last_prompt", "The robot opened the door"))
colt1, colt2, colt3 = st.columns(3)
max_new_tokens = int(colt1.number_input("max_new_tokens", min_value=1, max_value=max_new_tokens_cap, value=min(20, max_new_tokens_cap)))
temperature = float(colt2.number_input("temperature", min_value=0.1, max_value=2.0, value=0.9, step=0.1))
top_k = int(colt3.number_input("top_k", min_value=0, max_value=100, value=40))

if st.button("Generate output"):
    if "kairo_state" not in st.session_state:
        st.warning("Train a model first.")
    else:
        state = st.session_state["kairo_state"]
        generated = generate_learning_output(state, prompt, max_new_tokens=max_new_tokens, temperature=temperature, top_k=top_k, safe_cfg=safety_cfg)
        raw_out = generated["raw_output"]
        out = generated["output"]
        st.session_state["last_output"] = out
        st.session_state["last_prompt"] = prompt
        if out != raw_out and safety_cfg.enabled:
            st.caption("Output filtered by Classroom Safe Mode.")
        st.code(out)

        st.write("Top next-token predictions (demystification view):")
        probs = build_probability_preview(state, prompt, top_n=5)
        st.table(probs)

st.subheader("4) Retrain it: compare before/after")
comparison = prepare_retrain_comparison(st.session_state.get("before_output"), st.session_state.get("last_output"))
if comparison:
    c1, c2 = st.columns(2)
    c1.write("Before retrain")
    c1.code(comparison["before"])
    c2.write("After retrain")
    c2.code(comparison["after"])
    st.caption("Changing the training text changes the patterns the model learns.")

st.subheader("5) Understand it")
st.markdown(
    """
- Kairo predicts the **next byte/token** based on earlier tokens.
- It learns **patterns in training text**; it does not think like a person.
- Lower loss means better prediction on this task, not human understanding.
- Tiny models often repeat, drift, or produce strange text.
"""
)


st.subheader("6) Attention visualisation")
if "kairo_state" in st.session_state:
    state = st.session_state["kairo_state"]
    attn_prompt = st.text_input("Attention prompt", value=prompt, key="attn_prompt")
    if st.button("Show attention map"):
        amap = build_attention_preview(state, attn_prompt)
        st.write("Attention shows which earlier tokens the model looked at most when making a prediction.")
        st.table(amap["tokens"])
        st.table([{"query": r["query_token"], "top_attended": ", ".join(f"{x['token']} ({x['weight']:.2f})" for x in r["top_attended"])} for r in amap["table"]])
        matrix = amap.get("attention_matrix")
        if matrix:
            token_labels = build_attention_labels(amap.get("tokens", []))
            st.caption("Rows are the token currently looking back. Columns are earlier tokens it can attend to.")
            st.dataframe(build_attention_matrix_rows(matrix, token_labels), use_container_width=True)
            if token_labels:
                st.caption("Token order: " + " | ".join(token_labels))

st.subheader("7) Save / load experiment")
exp_path = st.text_input("Experiment folder", value="runs/experiments/latest")
if st.button("Save experiment") and "kairo_state" in st.session_state:
    state = st.session_state["kairo_state"]
    meta = make_experiment_metadata(training_text_length=len(training_text), token_count=state["token_count"], sequence_count=state["sequence_count"], config=state["cfg"], train_loss=state["train_losses"][-1], validation_loss=state["val_losses"][-1], prompt=st.session_state.get("last_prompt", ""), generated_output=st.session_state.get("last_output", ""), safe_mode=safety_cfg.enabled)
    save_experiment(exp_path, state["model"], meta)
    st.success("Experiment saved locally.")
if st.button("Load experiment metadata"):
    try:
        loaded = load_experiment_metadata(exp_path)
        st.json(loaded)
    except FileNotFoundError as exc:
        st.error(str(exc))


if st.button("Restore experiment model"):
    try:
        model, metadata = restore_experiment_model(exp_path)
        restored_state, cfg_missing = build_restored_learning_state(
            model,
            metadata,
            defaults={"seq_len": DEFAULTS["seq_len"], "d_model": DEFAULTS["d_model"], "n_heads": DEFAULTS["n_heads"], "n_layers": DEFAULTS["n_layers"]},
        )
        st.session_state["kairo_state"] = restored_state
        st.session_state["restored_model"] = str(model.__class__.__name__)
        st.session_state["restored_meta"] = metadata
        if metadata.get("prompt"):
            st.session_state["last_prompt"] = metadata.get("prompt")
        if metadata.get("generated_output"):
            st.session_state["last_output"] = metadata.get("generated_output")
        st.success("Experiment restored. You can now generate, inspect probabilities, and view attention.")
        if st.session_state.get("last_prompt"):
            st.write("Restored prompt")
            st.code(st.session_state["last_prompt"])
        if st.session_state.get("last_output"):
            st.write("Restored output")
            st.code(st.session_state["last_output"])
        if cfg_missing:
            st.warning("Some saved metadata was missing, so Kairo used safe defaults for parts of the restore.")
    except (FileNotFoundError, ValueError, KeyError, RuntimeError) as exc:
        st.error(str(exc))
if "restored_meta" in st.session_state:
    st.write("Restored model status:")
    st.json(st.session_state["restored_meta"])
