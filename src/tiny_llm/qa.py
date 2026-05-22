from __future__ import annotations

import argparse
from pathlib import Path
import re

import torch

from tiny_llm.data import ByteTokenizer
from tiny_llm.generation import generate_tokens, resolve_device, set_seed, validate_sampling_args
from tiny_llm.model import TinyGPT
from tiny_llm.safety import SafetyConfig, filter_output, is_prompt_allowed, safety_notice
from tiny_llm.utils import load_checkpoint

NO_ANSWER_FALLBACK = "I don't know based on the provided context."
STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "how",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "this",
    "to",
    "was",
    "what",
    "when",
    "where",
    "which",
    "who",
    "why",
    "with",
}


def build_qa_prompt(question: str, context: str | None = None) -> str:
    cleaned_question = question.strip()
    if context is None:
        return (
            "You are Kairo QA.\n"
            "Answer the question in 1-3 sentences.\n"
            f"If you cannot answer reliably, say exactly: {NO_ANSWER_FALLBACK}\n\n"
            f"Question: {cleaned_question}\n"
            "Answer:"
        )

    cleaned_context = context.strip()
    return (
        "You are Kairo QA.\n"
        "Use only the context to answer in 1-3 sentences.\n"
        f"If the answer is not in the context, say exactly: {NO_ANSWER_FALLBACK}\n\n"
        f"Context:\n{cleaned_context}\n\n"
        f"Question: {cleaned_question}\n"
        "Answer:"
    )


def extract_answer(decoded_text: str, prompt: str) -> str:
    if decoded_text.startswith(prompt):
        answer = decoded_text[len(prompt) :]
    else:
        marker = "Answer:"
        if marker in decoded_text:
            answer = decoded_text.split(marker, 1)[1]
        else:
            answer = decoded_text

    answer = answer.strip()
    if "\nQuestion:" in answer:
        answer = answer.split("\nQuestion:", 1)[0].strip()
    return answer


def _word_tokens(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z]+", text.lower())


def _question_keywords(question: str) -> set[str]:
    return {token for token in _word_tokens(question) if token not in STOPWORDS}


def needs_context_fallback(answer: str) -> bool:
    words = _word_tokens(answer)
    if not words:
        return True
    if len(words) < 3:
        return True
    short_ratio = sum(1 for word in words if len(word) <= 2) / len(words)
    unique_ratio = len(set(words)) / len(words)
    if short_ratio > 0.65:
        return True
    if len(words) >= 8 and unique_ratio < 0.45:
        return True
    return False


def select_context_answer(question: str, context: str) -> str | None:
    question_terms = _question_keywords(question)
    if not question_terms:
        return None

    sentence_candidates = [s.strip() for s in re.split(r"(?<=[.!?])\s+", context.strip()) if s.strip()]
    if not sentence_candidates:
        return None

    best_sentence: str | None = None
    best_score = 0
    for sentence in sentence_candidates:
        sentence_terms = set(_word_tokens(sentence))
        overlap = len(question_terms & sentence_terms)
        if overlap > best_score:
            best_score = overlap
            best_sentence = sentence

    if best_score == 0:
        return None
    return best_sentence


def _read_context(args: argparse.Namespace, parser: argparse.ArgumentParser) -> str | None:
    if args.context and args.context_file:
        parser.error("Use either --context or --context_file, not both.")

    if args.context_file:
        context_path = Path(args.context_file)
        if not context_path.exists():
            parser.exit(2, f"Context file not found: {context_path}\n")
        return context_path.read_text(encoding="utf-8")
    return args.context


def main() -> None:
    parser = argparse.ArgumentParser(description="Answer a question with a trained Kairo checkpoint.")
    parser.add_argument("--checkpoint", type=str, required=True)
    parser.add_argument("--question", type=str, required=True)
    parser.add_argument("--context", type=str, default="")
    parser.add_argument("--context_file", type=str, default="")
    parser.add_argument("--max_new_tokens", type=int, default=80)
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--top_k", type=int, default=40)
    parser.add_argument("--top_p", type=float, default=1.0)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--device", type=str, default="auto", choices=["auto", "cpu", "cuda"])
    parser.add_argument("--unsafe-disable-filter", action="store_true")
    args = parser.parse_args()

    if not args.question.strip():
        parser.error("question must not be empty")
    validate_sampling_args(args.max_new_tokens, args.temperature, args.top_k, args.top_p)

    context_text = _read_context(args, parser)
    cfg = SafetyConfig(enabled=not args.unsafe_disable_filter)
    print(safety_notice())
    if not cfg.enabled:
        print("Safety filtering disabled. Use only with trusted local datasets and supervised contexts.")

    qa_prompt = build_qa_prompt(args.question, context=context_text if context_text else None)
    if cfg.enabled and not is_prompt_allowed(qa_prompt, banned_terms=cfg.banned_terms):
        parser.exit(2, "Question or context blocked by classroom safety mode. Please try safer text.\n")

    if args.seed is not None:
        set_seed(args.seed)

    device = resolve_device(args.device)
    try:
        ckpt = load_checkpoint(args.checkpoint, map_location=device)
    except FileNotFoundError as exc:
        parser.exit(2, f"{exc}\n")
    config = ckpt["config"]

    model = TinyGPT(
        vocab_size=config["vocab_size"],
        seq_len=config["seq_len"],
        d_model=config["d_model"],
        n_heads=config["n_heads"],
        n_layers=config["n_layers"],
        dropout=config["dropout"],
    ).to(device)
    model.load_state_dict(ckpt["model_state"])
    model.eval()

    tokenizer = ByteTokenizer()
    with torch.no_grad():
        out_ids = generate_tokens(
            model,
            qa_prompt,
            tokenizer,
            seq_len=config["seq_len"],
            max_new_tokens=args.max_new_tokens,
            temperature=args.temperature,
            top_k=args.top_k,
            top_p=args.top_p,
            device=device,
        )

    decoded = tokenizer.decode(out_ids)
    answer = extract_answer(decoded, qa_prompt)
    filtered = filter_output(answer, banned_terms=cfg.banned_terms, mask=cfg.mask) if cfg.enabled else answer
    final_answer = filtered.strip()
    if not final_answer or needs_context_fallback(final_answer):
        if context_text:
            grounded = select_context_answer(args.question, context_text)
            final_answer = grounded if grounded else NO_ANSWER_FALLBACK
        else:
            final_answer = NO_ANSWER_FALLBACK

    print("=== Kairo QA ===")
    print(f"Device: {device}")
    print(f"Question: {args.question}")
    if context_text:
        print("Context: provided")
    else:
        print("Context: none")
    print("Answer:")
    print(final_answer)


if __name__ == "__main__":
    main()
