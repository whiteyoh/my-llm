from __future__ import annotations


def validate_training_token_count(token_count: int, seq_len: int) -> None:
    if token_count <= seq_len + 1:
        needed = seq_len + 2
        raise ValueError(
            "Training text is too short for this sequence length. "
            f"Need at least {needed} byte tokens for seq_len={seq_len}; got {token_count}. "
            "Add more text or lower seq_len."
        )


def train_val_split_sizes(sequence_count: int, val_ratio: float) -> tuple[int, int]:
    if sequence_count < 2:
        raise ValueError(
            "Training data does not create enough sequence windows. "
            "Add more text or lower seq_len."
        )
    if not (0.0 < val_ratio < 1.0):
        raise ValueError("val_ratio must be in (0, 1)")

    val_size = max(1, int(sequence_count * val_ratio))
    if val_size >= sequence_count:
        val_size = sequence_count - 1
    train_size = sequence_count - val_size
    if train_size <= 0:
        raise ValueError(
            "Training data leaves no examples for training after validation split. "
            "Add more text, lower seq_len, or lower val_ratio."
        )
    return train_size, val_size
