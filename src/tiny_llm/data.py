from __future__ import annotations

import torch
from torch.utils.data import Dataset


class ByteTokenizer:
    """Byte-level tokenizer using UTF-8 bytes as tokens.

    Trade-off: this is simple and has no external tokenizer dependency,
    but is usually less token-efficient than BPE/SentencePiece tokenizers.
    """

    vocab_size = 256

    def encode(self, text: str) -> list[int]:
        return list(text.encode("utf-8", errors="replace"))

    def decode(self, token_ids: list[int]) -> str:
        return bytes(token_ids).decode("utf-8", errors="replace")


class SequenceDataset(Dataset[tuple[torch.Tensor, torch.Tensor]]):
    def __init__(self, token_ids: list[int], seq_len: int) -> None:
        if not token_ids:
            raise ValueError("token_ids must not be empty")
        if seq_len <= 0:
            raise ValueError("seq_len must be > 0")
        if len(token_ids) <= seq_len:
            raise ValueError("len(token_ids) must be greater than seq_len")

        self.data = torch.tensor(token_ids, dtype=torch.long)
        self.seq_len = seq_len

    def __len__(self) -> int:
        return self.data.size(0) - self.seq_len

    def __getitem__(self, idx: int) -> tuple[torch.Tensor, torch.Tensor]:
        x = self.data[idx : idx + self.seq_len]
        y = self.data[idx + 1 : idx + self.seq_len + 1]
        return x, y
