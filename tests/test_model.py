import pytest
import torch

from tiny_llm.model import TinyGPT


def test_model_forward_shape() -> None:
    model = TinyGPT(vocab_size=256, seq_len=16, d_model=32, n_heads=4, n_layers=2, dropout=0.1)
    x = torch.randint(0, 256, (2, 16))
    logits = model(x)
    assert logits.shape == (2, 16, 256)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"vocab_size": 0, "seq_len": 16, "d_model": 32, "n_heads": 4, "n_layers": 2, "dropout": 0.1},
        {"vocab_size": 256, "seq_len": 0, "d_model": 32, "n_heads": 4, "n_layers": 2, "dropout": 0.1},
        {"vocab_size": 256, "seq_len": 16, "d_model": 0, "n_heads": 4, "n_layers": 2, "dropout": 0.1},
        {"vocab_size": 256, "seq_len": 16, "d_model": 32, "n_heads": 0, "n_layers": 2, "dropout": 0.1},
        {"vocab_size": 256, "seq_len": 16, "d_model": 32, "n_heads": 4, "n_layers": 0, "dropout": 0.1},
        {"vocab_size": 256, "seq_len": 16, "d_model": 30, "n_heads": 8, "n_layers": 2, "dropout": 0.1},
        {"vocab_size": 256, "seq_len": 16, "d_model": 32, "n_heads": 4, "n_layers": 2, "dropout": 1.0},
    ],
)
def test_invalid_model_config(kwargs: dict[str, float | int]) -> None:
    with pytest.raises(ValueError):
        TinyGPT(**kwargs)
