from __future__ import annotations

import importlib
from pathlib import Path
import sys


def _run_main(module_name: str) -> None:
    module = importlib.import_module(module_name)
    module.main()


def train() -> None:
    _run_main("tiny_llm.train")


def generate() -> None:
    _run_main("tiny_llm.generate")


def evaluate() -> None:
    _run_main("tiny_llm.evaluate")


def chat() -> None:
    _run_main("tiny_llm.chat")


def learn() -> None:
    try:
        from streamlit.web import cli as streamlit_cli
    except ImportError as exc:
        raise SystemExit('Learn Mode requires Streamlit. Install it with: pip install -e ".[learn]"') from exc

    script_path = Path(__file__).resolve().with_name("kairo_learn.py")
    sys.argv = ["streamlit", "run", str(script_path), *sys.argv[1:]]
    streamlit_cli.main()
