import pytest

from tiny_llm.training import train_val_split_sizes, validate_training_token_count


def test_validate_training_token_count_rejects_too_short_text() -> None:
    with pytest.raises(ValueError, match="Training text is too short"):
        validate_training_token_count(token_count=9, seq_len=8)


def test_validate_training_token_count_accepts_minimum_for_train_and_validation() -> None:
    validate_training_token_count(token_count=10, seq_len=8)


def test_train_val_split_sizes_keeps_one_training_and_one_validation_example() -> None:
    assert train_val_split_sizes(sequence_count=2, val_ratio=0.1) == (1, 1)


def test_train_val_split_sizes_rejects_single_sequence() -> None:
    with pytest.raises(ValueError, match="enough sequence windows"):
        train_val_split_sizes(sequence_count=1, val_ratio=0.1)
