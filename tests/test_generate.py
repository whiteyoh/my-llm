import torch

from src.generate import sample_next_token


def test_sample_next_token_valid_id() -> None:
    logits = torch.randn(1, 256)
    token = sample_next_token(logits, temperature=1.0, top_k=20, top_p=0.9)
    assert 0 <= token < 256
