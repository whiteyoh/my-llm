import pytest
import torch

from tiny_llm.data import ByteTokenizer
from tiny_llm.generation import (
    generate_tokens,
    resolve_device,
    sample_next_token,
    validate_sampling_args,
)
from tiny_llm.model import TinyGPT


def _tiny_model() -> TinyGPT:
    return TinyGPT(vocab_size=256, seq_len=8, d_model=32, n_heads=4, n_layers=1, dropout=0.0)


def test_validate_sampling_args_accepts_valid_values() -> None:
    validate_sampling_args(max_new_tokens=5, temperature=0.8, top_k=0, top_p=1.0)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"max_new_tokens": 0, "temperature": 1.0, "top_k": 0, "top_p": 1.0},
        {"max_new_tokens": 1, "temperature": 0.0, "top_k": 0, "top_p": 1.0},
        {"max_new_tokens": 1, "temperature": 1.0, "top_k": -1, "top_p": 1.0},
        {"max_new_tokens": 1, "temperature": 1.0, "top_k": 0, "top_p": 0.0},
    ],
)
def test_validate_sampling_args_rejects_bad_values(kwargs: dict[str, int | float]) -> None:
    with pytest.raises(ValueError):
        validate_sampling_args(**kwargs)


def test_sample_next_token_returns_valid_vocab_id() -> None:
    logits = torch.randn(1, 256)
    token = sample_next_token(logits, temperature=1.0, top_k=0, top_p=1.0)
    assert isinstance(token, int)
    assert 0 <= token < 256


def test_sample_next_token_top_k_path_works() -> None:
    logits = torch.linspace(-1.0, 1.0, 256).unsqueeze(0)
    token = sample_next_token(logits, temperature=1.0, top_k=10, top_p=1.0)
    assert 0 <= token < 256


def test_sample_next_token_top_p_path_works() -> None:
    logits = torch.linspace(-1.0, 1.0, 256).unsqueeze(0)
    token = sample_next_token(logits, temperature=1.0, top_k=0, top_p=0.9)
    assert 0 <= token < 256


def test_generate_tokens_returns_prompt_plus_new_tokens() -> None:
    model = _tiny_model()
    tok = ByteTokenizer()
    prompt = "The robot"
    prompt_ids = tok.encode(prompt)
    max_new_tokens = 5

    out_ids = generate_tokens(model, prompt, tok, seq_len=8, max_new_tokens=max_new_tokens, temperature=1.0, top_k=0, top_p=1.0, device=torch.device("cpu"))
    assert out_ids[: len(prompt_ids)] == prompt_ids
    assert len(out_ids) == len(prompt_ids) + max_new_tokens


def test_resolve_device_cpu() -> None:
    assert resolve_device("cpu").type == "cpu"


def test_resolve_device_auto_returns_usable_device() -> None:
    assert resolve_device("auto").type in {"cpu", "cuda"}


def test_resolve_device_cuda_raises_when_unavailable() -> None:
    if torch.cuda.is_available():
        pytest.skip("CUDA is available in this environment; this test targets CPU-only runners")
    with pytest.raises(ValueError):
        resolve_device("cuda")
