from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Final, Iterable

"""Lightweight classroom-safety helpers for Kairo demos."""

DEFAULT_BANNED_TERMS: Final[tuple[str, ...]] = ("kill", "suicide", "self-harm", "bomb", "weapon", "drugs")
EMAIL_RE: Final[re.Pattern[str]] = re.compile(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b", re.IGNORECASE)
PHONE_RE: Final[re.Pattern[str]] = re.compile(
    r"\b(?:\+?\d{1,2}[\s.-]?)?(?:\(?\d{3}\)?[\s.-]?)\d{3}[\s.-]?\d{4}\b"
)


@dataclass(frozen=True)
class SafetyConfig:
    enabled: bool = True
    banned_terms: tuple[str, ...] = DEFAULT_BANNED_TERMS
    mask: str = "[filtered]"


def normalise_text(text: str) -> str:
    return " ".join(text.split()).lower().replace("_", "-")


def _term_pattern(term: str) -> re.Pattern[str]:
    escaped = re.escape(term.strip().lower()).replace(r"\-", r"[-\s]?")
    return re.compile(rf"\b{escaped}\b", re.IGNORECASE)


def contains_blocked_term(text: str, banned_terms: Iterable[str] | None = None) -> bool:
    terms = tuple(banned_terms) if banned_terms is not None else DEFAULT_BANNED_TERMS
    norm = normalise_text(text)
    return bool(norm) and any(_term_pattern(term).search(norm) for term in terms if term.strip())


def is_prompt_allowed(text: str, banned_terms: Iterable[str] | None = None) -> bool:
    return bool(normalise_text(text)) and not contains_blocked_term(text, banned_terms=banned_terms)


def filter_output(text: str, banned_terms: Iterable[str] | None = None, mask: str = "[filtered]") -> str:
    terms = tuple(banned_terms) if banned_terms is not None else DEFAULT_BANNED_TERMS
    masked = text
    for term in terms:
        if term.strip():
            masked = _term_pattern(term).sub(mask, masked)
    return masked


def validate_training_text(text: str, min_chars: int = 80, banned_terms: Iterable[str] | None = None) -> list[str]:
    warnings: list[str] = []
    norm = normalise_text(text)
    if not norm:
        return ["Training text is empty. Add classroom-safe sample text before training."]
    if len(norm) < min_chars:
        warnings.append("Training text is very short; outputs may be unstable or repetitive.")
    if contains_blocked_term(text, banned_terms=banned_terms):
        warnings.append("Training text contains blocked classroom safety terms.")
    if EMAIL_RE.search(text):
        warnings.append("Possible personal data detected: email-like text.")
    if PHONE_RE.search(text):
        warnings.append("Possible personal data detected: phone-number-like text.")
    warnings.append("Use only text you are allowed to use; avoid personal, sensitive, or copyrighted content.")
    return warnings


def safety_notice() -> str:
    return "Kairo uses lightweight classroom guardrails. A teacher should supervise use. This is not full moderation."
