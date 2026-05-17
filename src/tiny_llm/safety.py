from __future__ import annotations

from typing import Final

"""Lightweight school-safety helpers for demos.

Important: this is only a minimal educational filter and NOT a full moderation,
alignment, or safety system.
"""

BANNED_WORDS: Final[list[str]] = [
    "kill",
    "suicide",
    "self-harm",
    "bomb",
    "weapon",
    "drugs",
]


def is_prompt_allowed(text: str) -> bool:
    """Return False when obvious banned keywords are present."""
    lowered = text.lower()
    return all(word not in lowered for word in BANNED_WORDS)


def filter_output(text: str) -> str:
    """Mask banned keywords in generated text.

    This simple replacement can miss context and should not be treated as robust safety.
    """
    masked = text
    for word in BANNED_WORDS:
        masked = masked.replace(word, "[filtered]")
        masked = masked.replace(word.capitalize(), "[filtered]")
        masked = masked.replace(word.upper(), "[filtered]")
    return masked
