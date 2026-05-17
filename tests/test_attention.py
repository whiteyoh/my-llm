import torch

from tiny_llm.attention import attention_to_table, get_attention_map
from tiny_llm.data import ByteTokenizer
from tiny_llm.model import TinyGPT


def test_default_forward_returns_logits_only() -> None:
    model = TinyGPT(256, 16, 32, 4, 1, 0.0)
    x = torch.randint(0, 256, (1, 8))
    out = model(x)
    assert isinstance(out, torch.Tensor)


def test_attention_output_shape() -> None:
    model = TinyGPT(256, 16, 32, 4, 2, 0.0)
    x = torch.randint(0, 256, (1, 8))
    logits, maps = model(x, return_attn=True)
    assert logits.shape == (1, 8, 256)
    assert len(maps) == 2
    assert maps[-1].shape == (1, 4, 8, 8)


def test_attention_helper_table_structure() -> None:
    model = TinyGPT(256, 16, 32, 4, 1, 0.0)
    tok = ByteTokenizer()
    out = get_attention_map(model, tok, "hello", seq_len=16, device=torch.device("cpu"))
    assert "table" in out and out["table"]
    row = out["table"][0]
    assert {"query_index", "query_token", "top_attended"}.issubset(row)
    manual = attention_to_table(out["attention"], out["token_ids"])
    assert isinstance(manual, list)
