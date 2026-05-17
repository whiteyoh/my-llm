from __future__ import annotations

import argparse

import torch

from tiny_llm.data import ByteTokenizer
from tiny_llm.generation import generate_tokens, resolve_device, set_seed, validate_sampling_args
from tiny_llm.model import TinyGPT
from tiny_llm.safety import SafetyConfig, filter_output, is_prompt_allowed, safety_notice
from tiny_llm.utils import load_checkpoint


def main() -> None:
    parser = argparse.ArgumentParser(description="Simple terminal chat demo for Kairo checkpoints.")
    parser.add_argument("--checkpoint", type=str, required=True)
    parser.add_argument("--max_new_tokens", type=int, default=120)
    parser.add_argument("--temperature", type=float, default=0.9)
    parser.add_argument("--top_k", type=int, default=40)
    parser.add_argument("--top_p", type=float, default=1.0)
    parser.add_argument("--device", type=str, default="auto", choices=["auto", "cpu", "cuda"])
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--unsafe-disable-filter", action="store_true")
    args = parser.parse_args()

    validate_sampling_args(args.max_new_tokens, args.temperature, args.top_k, args.top_p)
    cfg = SafetyConfig(enabled=not args.unsafe_disable_filter)

    if args.seed is not None:
        set_seed(args.seed)

    device = resolve_device(args.device)
    ckpt = load_checkpoint(args.checkpoint, map_location=device)
    config = ckpt["config"]
    tokenizer = ByteTokenizer()

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

    print("Kairo chat ready. Type /exit or /quit to stop.")
    print(safety_notice())
    if not cfg.enabled:
        print("Safety filtering disabled. Use only with trusted local datasets and supervised contexts.")
    with torch.no_grad():
        while True:
            prompt = input("you> ").strip()
            if prompt in {"/exit", "/quit"}:
                break
            if cfg.enabled and not is_prompt_allowed(prompt, banned_terms=cfg.banned_terms):
                print("bot> Prompt blocked by classroom safe mode. Try a kind, school-appropriate prompt.")
                continue
            out_ids = generate_tokens(
                model,
                prompt,
                tokenizer,
                seq_len=config["seq_len"],
                max_new_tokens=args.max_new_tokens,
                temperature=args.temperature,
                top_k=args.top_k,
                top_p=args.top_p,
                device=device,
            )
            decoded = tokenizer.decode(out_ids)
            out_text = filter_output(decoded, banned_terms=cfg.banned_terms, mask=cfg.mask) if cfg.enabled else decoded
            print("bot>", out_text)


if __name__ == "__main__":
    main()
