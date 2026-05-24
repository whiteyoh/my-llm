from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
import json
import re


STATUS_VALUES = ("idle", "queued", "running", "blocked", "completed")


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def discover_agent_files(root: Path | None = None) -> list[Path]:
    base = root or project_root()
    candidates = [base / ".Codex" / "agents", base / "Codex" / "agents"]
    files: list[Path] = []
    for directory in candidates:
        if directory.exists():
            files.extend(sorted(directory.glob("*.md")))
    return files


def _parse_frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"^---\n(.*?)\n---\n", text, flags=re.DOTALL)
    if not match:
        return {}
    fields: dict[str, str] = {}
    for raw in match.group(1).splitlines():
        if ":" not in raw:
            continue
        key, value = raw.split(":", 1)
        fields[key.strip()] = value.strip()
    return fields


def _parse_tag_block(text: str, tag: str) -> list[str]:
    match = re.search(rf"<{tag}>\n(.*?)\n</{tag}>", text, flags=re.DOTALL)
    if not match:
        return []
    lines = []
    for line in match.group(1).splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            lines.append(stripped[2:])
    return lines


def parse_agent_markdown(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    frontmatter = _parse_frontmatter(text)

    file_name = path.stem
    name = frontmatter.get("name", file_name)
    description = frontmatter.get("description", "")
    use_when = _parse_tag_block(text, "use-when")
    responsibilities = _parse_tag_block(text, "responsibilities")

    return {
        "name": name,
        "description": description,
        "path": str(path),
        "use_when": use_when,
        "responsibilities": responsibilities,
    }


def discover_agents(root: Path | None = None) -> list[dict[str, object]]:
    return [parse_agent_markdown(path) for path in discover_agent_files(root=root)]


def default_state() -> dict[str, object]:
    return {"agents": {}, "events": [], "phase": "Discovery", "missing_agents": []}


def load_state(path: Path) -> dict[str, object]:
    if not path.exists():
        return default_state()
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return default_state()
    if not isinstance(raw, dict):
        return default_state()
    raw.setdefault("agents", {})
    raw.setdefault("events", [])
    raw.setdefault("phase", "Discovery")
    raw.setdefault("missing_agents", [])
    return raw


def save_state(path: Path, state: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2), encoding="utf-8")


def ensure_agents_in_state(state: dict[str, object], agents: list[dict[str, object]]) -> dict[str, object]:
    agent_state = state.setdefault("agents", {})
    assert isinstance(agent_state, dict)
    for agent in agents:
        name = str(agent["name"])
        existing = agent_state.get(name)
        if not isinstance(existing, dict):
            agent_state[name] = {"status": "idle", "notes": "", "updated_at": ""}
            continue
        existing.setdefault("status", "idle")
        existing.setdefault("notes", "")
        existing.setdefault("updated_at", "")
    state.setdefault("missing_agents", [])
    return state


def _now_iso() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat()


def set_agent_status(state: dict[str, object], agent_name: str, status: str, note: str = "") -> dict[str, object]:
    if status not in STATUS_VALUES:
        raise ValueError(f"Invalid status: {status}")
    agent_state = state.setdefault("agents", {})
    assert isinstance(agent_state, dict)
    info = agent_state.setdefault(agent_name, {"status": "idle", "notes": "", "updated_at": ""})
    assert isinstance(info, dict)
    info["status"] = status
    info["notes"] = note
    info["updated_at"] = _now_iso()

    append_event(state, agent_name, f"status->{status}", note=note)
    return state


def set_phase(state: dict[str, object], phase: str) -> dict[str, object]:
    state["phase"] = phase
    return state


def status_counts(state: dict[str, object]) -> dict[str, int]:
    counts = {status: 0 for status in STATUS_VALUES}
    agent_state = state.get("agents", {})
    if not isinstance(agent_state, dict):
        return counts
    for info in agent_state.values():
        if isinstance(info, dict):
            status = str(info.get("status", "idle"))
            if status in counts:
                counts[status] += 1
    return counts


def append_event(state: dict[str, object], agent: str, event: str, note: str = "") -> dict[str, object]:
    events = state.setdefault("events", [])
    assert isinstance(events, list)
    events.append(
        {
            "timestamp": _now_iso(),
            "agent": agent,
            "event": event,
            "note": note,
        }
    )
    if len(events) > 200:
        del events[:-200]
    return state


def expected_agent_files(root: Path | None = None) -> list[str]:
    base = root or project_root()
    agents_md = base / "AGENTS.md"
    if not agents_md.exists():
        return []
    text = agents_md.read_text(encoding="utf-8")
    # `examples` are illustrative. Missing-agent alerts should only use explicit
    # required lists to avoid false-positive warnings in the dashboard.
    block = _parse_tag_block(text, "required-agents")
    if not block:
        return []
    files: list[str] = []
    for item in block:
        stripped = item.strip()
        if stripped.endswith(".md"):
            files.append(Path(stripped).name)
    return sorted(set(files))


def missing_expected_agents(agents: list[dict[str, object]], expected_files: list[str]) -> list[str]:
    if not expected_files:
        return []
    discovered = {Path(str(agent.get("path", ""))).name for agent in agents}
    missing_files = sorted(file_name for file_name in expected_files if file_name not in discovered)
    return [Path(file_name).stem for file_name in missing_files]


def sync_missing_agents(state: dict[str, object], missing_agent_names: list[str]) -> dict[str, object]:
    previous = state.get("missing_agents", [])
    previous_list = previous if isinstance(previous, list) else []
    previous_set = {str(item) for item in previous_list}
    current = sorted(set(missing_agent_names))
    current_set = set(current)

    if current_set != previous_set:
        state["missing_agents"] = current
        if current:
            append_event(
                state,
                "orchestrator",
                "missing-agents-detected",
                note=", ".join(current),
            )
        else:
            append_event(state, "orchestrator", "missing-agents-resolved")
    return state
