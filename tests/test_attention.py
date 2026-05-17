import pytest
import torch

from tiny_llm.attention import get_attention_map
from tiny_llm.data import ByteTokenizer
from tiny_llm.model import TinyGPT


def test_default_forward_returns_logits_only() -> None:
    model = TinyGPT(256, 16, 32, 4, 1, 0.0)
    x = torch.randint(0, 256, (1, 8))
    out = model(x)
    assert isinstance(out, torch.Tensor)


def test_attention_valid_output_contains_matrix_list() -> None:
    model = TinyGPT(256, 16, 32, 4, 2, 0.0)
    tok = ByteTokenizer()
    out = get_attention_map(model, tok, "hello", seq_len=16, device=torch.device("cpu"))
    assert isinstance(out["attention_matrix"], list)
    assert out["note"] == "Attention is a model mechanism, not human understanding."
    assert out["token_count"] == len(out["token_ids"])


def test_attention_invalid_layer_head_topk_limit_prompt() -> None:
    model = TinyGPT(256, 16, 32, 4, 1, 0.0)
    tok = ByteTokenizer()
    with pytest.raises(ValueError):
        get_attention_map(model, tok, "hello", seq_len=16, device=torch.device("cpu"), layer=5)
    with pytest.raises(ValueError):
        get_attention_map(model, tok, "hello", seq_len=16, device=torch.device("cpu"), head=99)
    with pytest.raises(ValueError):
        get_attention_map(model, tok, "hello", seq_len=16, device=torch.device("cpu"), top_k=0)
    with pytest.raises(ValueError):
        get_attention_map(model, tok, "hello", seq_len=16, device=torch.device("cpu"), limit=0)
    with pytest.raises(ValueError):
        get_attention_map(model, tok, "  ", seq_len=16, device=torch.device("cpu"))
