import torch

from tiny_llm.data import ByteTokenizer
from tiny_llm.generation import generate_tokens, sample_next_token, validate_sampling_args
from tiny_llm.model import TinyGPT


def test_sample_next_token_valid_id() -> None:
    logits = torch.randn(1, 256)
    token = sample_next_token(logits, temperature=1.0, top_k=20, top_p=0.9)
    assert 0 <= token < 256


def test_sample_next_token_with_top_k() -> None:
    logits = torch.linspace(-1.0, 1.0, 256).unsqueeze(0)
    token = sample_next_token(logits, temperature=1.0, top_k=10, top_p=1.0)
    assert isinstance(token, int)


def test_sample_next_token_with_top_p() -> None:
    logits = torch.linspace(-1.0, 1.0, 256).unsqueeze(0)
    token = sample_next_token(logits, temperature=0.8, top_k=0, top_p=0.8)
    assert 0 <= token < 256


def test_generate_tokens_smoke() -> None:
    model = TinyGPT(vocab_size=256, seq_len=8, d_model=16, n_heads=4, n_layers=1, dropout=0.0)
    tokenizer = ByteTokenizer()
    ids = generate_tokens(model, "hi", tokenizer, 8, 3, 1.0, 0, 1.0, torch.device("cpu"))
    assert len(ids) >= 3


def test_invalid_sampling_args() -> None:
    import pytest

    with pytest.raises(ValueError):
        validate_sampling_args(0, 1.0, 0, 1.0)
    with pytest.raises(ValueError):
        validate_sampling_args(1, 0.0, 0, 1.0)
    with pytest.raises(ValueError):
        validate_sampling_args(1, 1.0, -1, 1.0)
    with pytest.raises(ValueError):
        validate_sampling_args(1, 1.0, 0, 0.0)
