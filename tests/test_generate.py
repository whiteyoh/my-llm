import torch

from generate import sample_next_token


def test_sample_next_token_valid_id() -> None:
    logits = torch.randn(1, 256)
    token = sample_next_token(logits, temperature=1.0, top_k=20, top_p=0.9)
    assert 0 <= token < 256


def test_sample_next_token_with_top_p_top_k() -> None:
    logits = torch.linspace(-1.0, 1.0, 256).unsqueeze(0)
    token = sample_next_token(logits, temperature=0.8, top_k=10, top_p=0.8)
    assert isinstance(token, int)
    assert 0 <= token < 256
