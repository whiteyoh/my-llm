from tiny_llm.data import ByteTokenizer


def test_encode_decode_round_trip() -> None:
    tok = ByteTokenizer()
    text = "Hello, Kairo! 👋"
    assert tok.decode(tok.encode(text)) == text
