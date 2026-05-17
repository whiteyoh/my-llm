import pytest
import torch

from tiny_llm.data import SequenceDataset


def test_dataset_length_and_shapes() -> None:
    ds = SequenceDataset(list(range(20)), seq_len=8)
    assert len(ds) == 12
    x, y = ds[0]
    assert x.shape == (8,)
    assert y.shape == (8,)
    assert x.dtype == torch.long
    assert y.dtype == torch.long


def test_dataset_sequence_shift() -> None:
    ds = SequenceDataset([10, 11, 12, 13, 14], seq_len=3)
    x, y = ds[0]
    assert x.tolist() == [10, 11, 12]
    assert y.tolist() == [11, 12, 13]


def test_dataset_invalid_inputs() -> None:
    with pytest.raises(ValueError):
        SequenceDataset([], seq_len=4)
    with pytest.raises(ValueError):
        SequenceDataset([1, 2, 3], seq_len=0)
    with pytest.raises(ValueError):
        SequenceDataset([1, 2, 3], seq_len=3)
