from tiny_llm.data import ByteTokenizer


def test_encode_decode_round_trip_ascii() -> None:
    tok = ByteTokenizer()
    text = "Hello, Kairo!"
    assert tok.decode(tok.encode(text)) == text


def test_encode_decode_round_trip_non_ascii() -> None:
    tok = ByteTokenizer()
    text = "Café 🚀 こんにちは"
    assert tok.decode(tok.encode(text)) == text


def test_vocab_size_is_256() -> None:
    assert ByteTokenizer().vocab_size == 256
