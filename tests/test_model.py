import pytest
import torch

from tiny_llm.model import TinyGPT


def _valid_config() -> dict[str, int | float]:
    return {"vocab_size": 256, "seq_len": 16, "d_model": 32, "n_heads": 4, "n_layers": 1, "dropout": 0.1}


def test_tinygpt_forward_output_shape() -> None:
    model = TinyGPT(**_valid_config())
    x = torch.randint(0, 256, (2, 16))
    logits = model(x)
    assert logits.shape == (2, 16, 256)


def test_sequence_longer_than_seq_len_raises() -> None:
    model = TinyGPT(**_valid_config())
    x = torch.randint(0, 256, (1, 17))
    with pytest.raises(ValueError):
        model(x)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"vocab_size": 0},
        {"seq_len": 0},
        {"d_model": 0},
        {"n_heads": 0},
        {"n_layers": 0},
        {"d_model": 30, "n_heads": 8},
        {"dropout": -0.1},
        {"dropout": 1.0},
    ],
)
def test_invalid_model_values_raise(kwargs: dict[str, int | float]) -> None:
    config = _valid_config() | kwargs
    with pytest.raises(ValueError):
        TinyGPT(**config)
