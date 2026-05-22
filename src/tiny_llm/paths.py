from __future__ import annotations

from contextlib import ExitStack
from importlib import resources
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SAMPLE_DIR = PROJECT_ROOT / "data" / "samples"
PACKAGE_SAMPLE_DIR = resources.files("tiny_llm").joinpath("samples")
_RESOURCE_STACK = ExitStack()
_RESOURCE_PATHS: dict[str, Path] = {}


def _validate_sample_filename(filename: str) -> None:
    if Path(filename).name != filename:
        raise ValueError("Sample filename must not include path separators")


def sample_path(filename: str) -> Path:
    _validate_sample_filename(filename)
    source_path = SAMPLE_DIR / filename
    if source_path.exists():
        return source_path

    cached_path = _RESOURCE_PATHS.get(filename)
    if cached_path is not None and cached_path.exists():
        return cached_path

    resource = PACKAGE_SAMPLE_DIR.joinpath(filename)
    if not resource.is_file():
        raise FileNotFoundError(f"Sample dataset not found: {filename}")

    package_path = Path(_RESOURCE_STACK.enter_context(resources.as_file(resource)))
    _RESOURCE_PATHS[filename] = package_path
    return package_path


def read_sample_text(filename: str) -> str:
    _validate_sample_filename(filename)
    source_path = SAMPLE_DIR / filename
    if source_path.exists():
        return source_path.read_text(encoding="utf-8")

    resource = PACKAGE_SAMPLE_DIR.joinpath(filename)
    if not resource.is_file():
        raise FileNotFoundError(f"Sample dataset not found: {filename}")
    return resource.read_text(encoding="utf-8")
