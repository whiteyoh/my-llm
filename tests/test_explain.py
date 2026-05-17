import torch

from tiny_llm.data import ByteTokenizer
from tiny_llm.explain import tokens_preview, top_next_token_predictions
from tiny_llm.model import TinyGPT


def test_tokens_preview_basic() -> None:
    rows = tokens_preview("A B\n", limit=4)
    assert rows[0]["token_id"] == 65
    assert rows[1]["display"] == "<space>"
    assert any(r["display"] == "<newline>" for r in rows)


def test_top_next_token_predictions_shape() -> None:
    tok = ByteTokenizer()
    model = TinyGPT(tok.vocab_size, 32, 64, 4, 2, 0.1)
    preds = top_next_token_predictions(model, tok, "Hello", seq_len=32, device=torch.device("cpu"), top_n=5)
    assert len(preds) == 5
    assert all("probability" in p for p in preds)
    assert all(p["probability"] >= 0 for p in preds)
