import torch

from tiny_llm.model import TinyGPT


def test_model_forward_shape() -> None:
    model = TinyGPT(vocab_size=256, seq_len=16, d_model=32, n_heads=4, n_layers=2, dropout=0.1)
    x = torch.randint(0, 256, (2, 16))
    logits = model(x)
    assert logits.shape == (2, 16, 256)
