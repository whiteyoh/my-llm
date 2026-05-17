from __future__ import annotations

from pathlib import Path

import streamlit as st
import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader, random_split

from tiny_llm.attention import get_attention_map
from tiny_llm.data import ByteTokenizer, SequenceDataset
from tiny_llm.experiments import load_experiment, make_experiment_metadata, save_experiment
from tiny_llm.explain import tokens_preview, top_next_token_predictions
from tiny_llm.generation import generate_tokens, resolve_device, validate_sampling_args
from tiny_llm.model import TinyGPT
from tiny_llm.safety import SafetyConfig, filter_output, is_prompt_allowed, safety_notice, validate_training_text

DEFAULTS = {"seq_len": 32, "d_model": 64, "n_heads": 4, "n_layers": 2, "epochs": 1, "batch_size": 4}
MAX_CLASSROOM_NEW_TOKENS = 40
PRESETS = {
    "Very small / classroom demo": DEFAULTS,
    "Small / better output": {"seq_len": 48, "d_model": 96, "n_heads": 4, "n_layers": 3, "epochs": 2, "batch_size": 4},
    "Custom": DEFAULTS,
}


def _train_model(training_text: str, cfg: dict[str, int], progress: st.delta_generator.DeltaGenerator) -> dict:
    tok = ByteTokenizer()
    token_ids = tok.encode(training_text)
    ds = SequenceDataset(token_ids, seq_len=cfg["seq_len"])
    val_size = max(1, int(len(ds) * 0.1))
    train_size = len(ds) - val_size
    train_ds, val_ds = random_split(ds, [train_size, val_size])

    train_loader = DataLoader(train_ds, batch_size=cfg["batch_size"], shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=cfg["batch_size"])
    device = resolve_device("cpu")
    model = TinyGPT(tok.vocab_size, cfg["seq_len"], cfg["d_model"], cfg["n_heads"], cfg["n_layers"], 0.1).to(device)
    opt = torch.optim.AdamW(model.parameters(), lr=3e-4)

    train_losses, val_losses = [], []
    total_steps = max(1, cfg["epochs"] * len(train_loader))
    step_count = 0

    for epoch in range(cfg["epochs"]):
        model.train()
        running = 0.0
        for x, y in train_loader:
            x, y = x.to(device), y.to(device)
            opt.zero_grad(set_to_none=True)
            logits = model(x)
            loss = F.cross_entropy(logits.view(-1, logits.size(-1)), y.view(-1))
            loss.backward()
            opt.step()
            running += loss.item()

            step_count += 1
            progress.progress(min(step_count / total_steps, 1.0), text=f"Training... epoch {epoch + 1}/{cfg['epochs']}")

        train_losses.append(running / max(1, len(train_loader)))

        model.eval()
        v_running = 0.0
        with torch.no_grad():
            for x, y in val_loader:
                x, y = x.to(device), y.to(device)
                logits = model(x)
                v_running += F.cross_entropy(logits.view(-1, logits.size(-1)), y.view(-1)).item()
        val_losses.append(v_running / max(1, len(val_loader)))

    progress.progress(1.0, text="Training complete")
    return {
        "model": model,
        "tokenizer": tok,
        "token_count": len(token_ids),
        "sequence_count": len(ds),
        "param_count": sum(p.numel() for p in model.parameters()),
        "train_losses": train_losses,
        "val_losses": val_losses,
        "cfg": cfg,
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
max_new_tokens_cap = int(st.sidebar.number_input("Allowed max_new_tokens", min_value=5, max_value=80, value=20))
model_size_preset = st.sidebar.selectbox("Max model size preset", ["Classroom demo", "Moderate"], index=0)
custom_banned = st.sidebar.text_area("Custom banned terms (comma-separated)", value="")
if st.sidebar.button("Reset session"):
    for key in ["kairo_state", "before_output", "last_prompt", "last_output"]:
        st.session_state.pop(key, None)
    st.sidebar.success("Session reset.")

banned_terms = tuple(t.strip() for t in custom_banned.split(",") if t.strip()) or None
safety_cfg = SafetyConfig(enabled=safe_mode, banned_terms=banned_terms or SafetyConfig().banned_terms)

default_text = Path("data/samples/space_adventure.txt").read_text(encoding="utf-8")
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

for warning in validate_training_text(training_text):
    st.warning(warning)

preview = tokens_preview(training_text, limit=20)
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

cfg = {"seq_len": int(seq_len), "d_model": int(d_model), "n_heads": int(n_heads), "n_layers": int(n_layers), "epochs": int(epochs), "batch_size": int(batch_size)}

train_col, retrain_col, reset_col = st.columns(3)
train_clicked = train_col.button("Train")
retrain_clicked = retrain_col.button("Retrain")
if reset_col.button("Reset session"):
    for key in ["kairo_state", "before_output", "last_prompt"]:
        st.session_state.pop(key, None)
    st.success("Session reset.")

if train_clicked or retrain_clicked:
    if len(ByteTokenizer().encode(training_text)) <= cfg["seq_len"] + 1:
        st.error("Training text is too short for these settings. Add more text or lower seq_len.")
    else:
        if retrain_clicked and "last_output" in st.session_state:
            st.session_state["before_output"] = st.session_state.get("last_output")
        progress = st.progress(0.0, text="Starting training...")
        st.session_state["kairo_state"] = _train_model(training_text, cfg, progress)
        st.success("Model trained.")

st.subheader("Model status")
if "kairo_state" in st.session_state:
    state = st.session_state["kairo_state"]
    st.success("Status: Trained")
    st.write(f"Token count: {state['token_count']}")
    st.write(f"Sequence count: {state['sequence_count']}")
    st.write(f"Parameter count: {state['param_count']}")
    st.write(f"Latest train loss: {state['train_losses'][-1]:.4f}")
    st.write(f"Latest validation loss: {state['val_losses'][-1]:.4f}")
else:
    st.warning("Status: Not trained")

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
max_new_tokens = int(colt1.number_input("max_new_tokens", min_value=1, max_value=min(MAX_CLASSROOM_NEW_TOKENS, max_new_tokens_cap), value=min(20, max_new_tokens_cap)))
temperature = float(colt2.number_input("temperature", min_value=0.1, max_value=2.0, value=0.9, step=0.1))
top_k = int(colt3.number_input("top_k", min_value=0, max_value=100, value=40))

if st.button("Generate output"):
    validate_sampling_args(max_new_tokens, temperature, top_k, 1.0)
    if safety_cfg.enabled and not is_prompt_allowed(prompt, banned_terms=safety_cfg.banned_terms):
        st.warning("Prompt blocked by Classroom Safe Mode. Try a safer prompt.")
    elif "kairo_state" not in st.session_state:
        st.warning("Train a model first.")
    else:
        state = st.session_state["kairo_state"]
        ids = generate_tokens(state["model"], prompt, state["tokenizer"], seq_len=state["cfg"]["seq_len"], max_new_tokens=max_new_tokens, temperature=temperature, top_k=top_k, top_p=1.0, device=torch.device("cpu"))
        raw_out = state["tokenizer"].decode(ids)
        out = filter_output(raw_out, banned_terms=safety_cfg.banned_terms, mask=safety_cfg.mask) if safety_cfg.enabled else raw_out
        st.session_state["last_output"] = out
        st.session_state["last_prompt"] = prompt
        if out != raw_out and safety_cfg.enabled:
            st.caption("Output filtered by Classroom Safe Mode.")
        st.code(out)

        st.write("Top next-token predictions (demystification view):")
        probs = top_next_token_predictions(state["model"], state["tokenizer"], prompt, seq_len=state["cfg"]["seq_len"], device=torch.device("cpu"), top_n=5)
        st.table(probs)

st.subheader("4) Retrain it: compare before/after")
if st.session_state.get("before_output") and st.session_state.get("last_output"):
    c1, c2 = st.columns(2)
    c1.write("Before retrain")
    c1.code(st.session_state["before_output"])
    c2.write("After retrain")
    c2.code(st.session_state["last_output"])
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
        amap = get_attention_map(state["model"], state["tokenizer"], attn_prompt, seq_len=state["cfg"]["seq_len"], device=torch.device("cpu"))
        st.write("Attention shows which earlier tokens the model looked at most when making a prediction.")
        st.table(amap["tokens"])
        st.table([{"query": r["query_token"], "top_attended": ", ".join(f"{x['token']} ({x['weight']:.2f})" for x in r["top_attended"])} for r in amap["table"]])

st.subheader("7) Save / load experiment")
exp_path = st.text_input("Experiment folder", value="runs/experiments/latest")
if st.button("Save experiment") and "kairo_state" in st.session_state:
    state = st.session_state["kairo_state"]
    meta = make_experiment_metadata(training_text_length=len(training_text), token_count=state["token_count"], sequence_count=state["sequence_count"], config=state["cfg"], train_loss=state["train_losses"][-1], validation_loss=state["val_losses"][-1], prompt=st.session_state.get("last_prompt", ""), generated_output=st.session_state.get("last_output", ""), safe_mode=safety_cfg.enabled)
    save_experiment(exp_path, state["model"], meta)
    st.success("Experiment saved locally.")
if st.button("Load experiment metadata"):
    try:
        loaded = load_experiment(exp_path)
        st.json(loaded)
    except FileNotFoundError as exc:
        st.error(str(exc))
