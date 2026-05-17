from __future__ import annotations

from typing import Any

import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader, random_split

from tiny_llm.attention import get_attention_map
from tiny_llm.data import ByteTokenizer, SequenceDataset
from tiny_llm.explain import tokens_preview, top_next_token_predictions
from tiny_llm.generation import generate_tokens, resolve_device, validate_sampling_args
from tiny_llm.model import TinyGPT
from tiny_llm.safety import SafetyConfig, filter_output, is_prompt_allowed, validate_training_text

DEFAULTS = {"seq_len": 32, "d_model": 64, "n_heads": 4, "n_layers": 2, "epochs": 1, "batch_size": 4, "max_new_tokens": 40}
TEACHER_LIMITS = {
    "Classroom demo": {"seq_len": 32, "d_model": 64, "n_layers": 2, "epochs": 1, "max_new_tokens": 40},
    "Moderate": {"seq_len": 64, "d_model": 128, "n_layers": 4, "epochs": 3, "max_new_tokens": 80},
}


def enforce_teacher_limits(cfg: dict[str, int], preset: str = "Classroom demo") -> tuple[dict[str, int], list[str]]:
    limits = TEACHER_LIMITS.get(preset, TEACHER_LIMITS["Classroom demo"])
    out = dict(cfg)
    warnings: list[str] = []
    for key, max_value in limits.items():
        if key in out and int(out[key]) > max_value:
            out[key] = max_value
            warnings.append("Teacher controls are keeping this demo CPU-friendly.")
    return out, sorted(set(warnings))


def build_training_config(raw: dict[str, int], preset: str = "Classroom demo") -> tuple[dict[str, int], list[str]]:
    cfg = {k: int(v) for k, v in raw.items()}
    return enforce_teacher_limits(cfg, preset=preset)


def validate_learn_training_text(text: str, banned_terms: tuple[str, ...] | None = None) -> list[str]:
    return validate_training_text(text, banned_terms=banned_terms)


def train_tiny_model(training_text: str, cfg: dict[str, int], progress_callback: Any | None = None) -> dict[str, Any]:
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

    for _epoch in range(cfg["epochs"]):
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
            if progress_callback:
                progress_callback(min(step_count / total_steps, 1.0))
        train_losses.append(running / max(1, len(train_loader)))

        model.eval()
        v_running = 0.0
        with torch.no_grad():
            for x, y in val_loader:
                x, y = x.to(device), y.to(device)
                logits = model(x)
                v_running += F.cross_entropy(logits.view(-1, logits.size(-1)), y.view(-1)).item()
        val_losses.append(v_running / max(1, len(val_loader)))

    if progress_callback:
        progress_callback(1.0)
    return {"model": model, "tokenizer": tok, "token_count": len(token_ids), "sequence_count": len(ds), "param_count": sum(p.numel() for p in model.parameters()), "train_losses": train_losses, "val_losses": val_losses, "cfg": cfg}


def create_model_status(state: dict[str, Any] | None) -> dict[str, Any]:
    if not state:
        return {"trained": False, "label": "🔴 Not trained yet"}
    return {"trained": True, "label": "🟢 Trained", "token_count": state["token_count"], "sequence_count": state["sequence_count"], "param_count": state["param_count"], "train_loss": state["train_losses"][-1], "val_loss": state["val_losses"][-1]}


def generate_learning_output(state: dict[str, Any], prompt: str, *, max_new_tokens: int, temperature: float, top_k: int, safe_cfg: SafetyConfig) -> dict[str, str]:
    validate_sampling_args(max_new_tokens, temperature, top_k, 1.0)
    if safe_cfg.enabled and not is_prompt_allowed(prompt, banned_terms=safe_cfg.banned_terms):
        raise ValueError("Prompt blocked by Classroom Safe Mode. Try a safer prompt.")
    ids = generate_tokens(state["model"], prompt, state["tokenizer"], seq_len=state["cfg"]["seq_len"], max_new_tokens=max_new_tokens, temperature=temperature, top_k=top_k, top_p=1.0, device=torch.device("cpu"))
    raw_out = state["tokenizer"].decode(ids)
    out = filter_output(raw_out, banned_terms=safe_cfg.banned_terms, mask=safe_cfg.mask) if safe_cfg.enabled else raw_out
    return {"raw_output": raw_out, "output": out}


def prepare_retrain_comparison(before_output: str | None, after_output: str | None) -> dict[str, str] | None:
    if before_output and after_output:
        return {"before": before_output, "after": after_output}
    return None


def build_token_preview(training_text: str, limit: int = 20) -> list[dict[str, Any]]:
    return tokens_preview(training_text, limit=limit)


def build_probability_preview(state: dict[str, Any], prompt: str, top_n: int = 5) -> list[dict[str, Any]]:
    return top_next_token_predictions(state["model"], state["tokenizer"], prompt, seq_len=state["cfg"]["seq_len"], device=torch.device("cpu"), top_n=top_n)


def build_attention_preview(state: dict[str, Any], prompt: str, *, layer: int = -1, head: int = 0, limit: int = 24, top_k: int = 3) -> dict[str, Any]:
    return get_attention_map(state["model"], state["tokenizer"], prompt, seq_len=state["cfg"]["seq_len"], device=torch.device("cpu"), layer=layer, head=head, limit=limit, top_k=top_k)
