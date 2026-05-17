import pytest
import torch

from tiny_llm.data import SequenceDataset


def test_sequence_dataset_length() -> None:
    ds = SequenceDataset(list(range(20)), seq_len=8)
    assert len(ds) == 12


def test_sequence_dataset_x_y_shapes() -> None:
    ds = SequenceDataset(list(range(20)), seq_len=8)
    x, y = ds[0]
    assert x.shape == (8,)
    assert y.shape == (8,)
    assert x.dtype == torch.long
    assert y.dtype == torch.long


def test_next_token_shift_correctness() -> None:
    ds = SequenceDataset([10, 11, 12, 13, 14], seq_len=3)
    x, y = ds[0]
    assert x.tolist() == [10, 11, 12]
    assert y.tolist() == [11, 12, 13]


def test_empty_token_list_raises_value_error() -> None:
    with pytest.raises(ValueError):
        SequenceDataset([], seq_len=4)


def test_seq_len_less_or_equal_zero_raises_value_error() -> None:
    with pytest.raises(ValueError):
        SequenceDataset([1, 2, 3], seq_len=0)


def test_token_count_less_or_equal_seq_len_raises_value_error() -> None:
    with pytest.raises(ValueError):
        SequenceDataset([1, 2, 3], seq_len=3)
