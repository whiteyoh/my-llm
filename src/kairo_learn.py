from __future__ import annotations

from pathlib import Path

import streamlit as st
import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader, random_split

from tiny_llm.data import ByteTokenizer, SequenceDataset
from tiny_llm.generation import generate_tokens, resolve_device, validate_sampling_args
from tiny_llm.model import TinyGPT
from tiny_llm.safety import SafetyConfig, filter_output, is_prompt_allowed, safety_notice, validate_training_text

st.set_page_config(page_title="Kairo Learn Mode", layout="centered")
st.title("Kairo Learn Mode")

st.info("Kairo uses lightweight classroom guardrails. Teachers should supervise use.")

st.header("1. What is Kairo?")
st.write("Kairo is an educational tiny GPT lab. It predicts the next byte-level token.")

safe_mode = st.toggle("Classroom Safe Mode", value=True)
safety_cfg = SafetyConfig(enabled=safe_mode)

st.header("2. Add training text")
default_text = Path("data/samples/space_adventure.txt").read_text(encoding="utf-8")
training_text = st.text_area("Paste a short, school-safe text sample:", value=default_text, height=160)
for warning in validate_training_text(training_text):
    st.warning(warning)

st.header("3. Train tiny model")
seq_len = 32
d_model = 64
n_heads = 4
n_layers = 2
epochs = 1
batch_size = 4

if st.button("Train tiny model"):
    if len(" ".join(training_text.split())) < 80:
        st.error("Training text is too short for a useful demo. Add a longer classroom-safe sample first.")
    else:
        tok = ByteTokenizer()
        ds = SequenceDataset(tok.encode(training_text), seq_len=seq_len)
        val_size = max(1, int(len(ds) * 0.1))
        train_size = len(ds) - val_size
        train_ds, val_ds = random_split(ds, [train_size, val_size])

        train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True)
        val_loader = DataLoader(val_ds, batch_size=batch_size)
        device = resolve_device("cpu")
        model = TinyGPT(tok.vocab_size, seq_len, d_model, n_heads, n_layers, 0.1).to(device)
        opt = torch.optim.AdamW(model.parameters(), lr=3e-4)

        train_losses, val_losses = [], []
        for _ in range(epochs):
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
            train_losses.append(running / max(1, len(train_loader)))

            model.eval()
            v_running = 0.0
            with torch.no_grad():
                for x, y in val_loader:
                    x, y = x.to(device), y.to(device)
                    logits = model(x)
                    v_running += F.cross_entropy(logits.view(-1, logits.size(-1)), y.view(-1)).item()
            val_losses.append(v_running / max(1, len(val_loader)))

        st.session_state["kairo_model"] = model
        st.session_state["kairo_tok"] = tok
        st.session_state["train_losses"] = train_losses
        st.session_state["val_losses"] = val_losses

st.header("4. Watch it learn")
if "train_losses" in st.session_state:
    st.line_chart({"train_loss": st.session_state["train_losses"], "val_loss": st.session_state["val_losses"]})

st.header("5. Try a prompt")
prompt = st.text_input("Prompt", value="The robot opened the door")
if st.button("Generate"):
    validate_sampling_args(20, 0.9, 40, 1.0)
    if safety_cfg.enabled and not is_prompt_allowed(prompt, banned_terms=safety_cfg.banned_terms):
        st.warning("Prompt blocked by Classroom Safe Mode. Try a safer prompt.")
    elif "kairo_model" in st.session_state:
        ids = generate_tokens(
            st.session_state["kairo_model"],
            prompt,
            st.session_state["kairo_tok"],
            seq_len=seq_len,
            max_new_tokens=20,
            temperature=0.9,
            top_k=40,
            top_p=1.0,
            device=torch.device("cpu"),
        )
        raw_out = st.session_state["kairo_tok"].decode(ids)
        out = (
            filter_output(raw_out, banned_terms=safety_cfg.banned_terms, mask=safety_cfg.mask)
            if safety_cfg.enabled
            else raw_out
        )
        if out != raw_out and safety_cfg.enabled:
            st.caption("Safety filtering applied to generated output.")
        st.code(out)

st.header("6. What did the model learn?")
st.write(
    "It learned local token patterns from your text. Lower loss means better next-token prediction on this small data. "
    "It does not understand like a human, and outputs depend on training data."
)
st.caption(safety_notice())
