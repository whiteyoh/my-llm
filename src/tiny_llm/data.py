from __future__ import annotations

import numpy as np
import torch
from torch.utils.data import Dataset


class ByteTokenizer:
    """Byte-level tokenizer using UTF-8 bytes as tokens."""

    vocab_size = 256

    def encode(self, text: str) -> list[int]:
        return list(text.encode("utf-8", errors="replace"))

    def decode(self, token_ids: list[int]) -> str:
        return bytes(token_ids).decode("utf-8", errors="replace")


class SequenceDataset(Dataset):
    def __init__(self, token_ids: list[int], seq_len: int) -> None:
        if len(token_ids) <= seq_len:
            raise ValueError("Input text is too short for selected seq_len.")
        self.data = np.asarray(token_ids, dtype=np.int64)
        self.seq_len = seq_len

    def __len__(self) -> int:
        return len(self.data) - self.seq_len

    def __getitem__(self, idx: int) -> tuple[torch.Tensor, torch.Tensor]:
        chunk = self.data[idx : idx + self.seq_len + 1]
        x = torch.tensor(chunk[:-1], dtype=torch.long)
        y = torch.tensor(chunk[1:], dtype=torch.long)
        return x, y
