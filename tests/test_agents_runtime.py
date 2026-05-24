from pathlib import Path

from tiny_llm.agents_runtime import (
    discover_agent_files,
    discover_agents,
    ensure_agents_in_state,
    expected_agent_files,
    missing_expected_agents,
    set_agent_status,
    status_counts,
    sync_missing_agents,
)


def test_discover_agent_files_finds_markdown_agents() -> None:
    files = discover_agent_files()
    assert any(path.name == "qa-evaluation-engineer.md" for path in files)


def test_discover_agents_parses_name_and_description() -> None:
    agents = discover_agents()
    agent = next(a for a in agents if a["name"] == "qa-evaluation-engineer")
    assert "question-answer behavior" in str(agent["description"])


def test_agent_state_status_counts_and_updates() -> None:
    state: dict[str, object] = {"agents": {}, "events": []}
    agents = [{"name": "qa-evaluation-engineer", "description": "", "path": str(Path("x.md"))}]
    state = ensure_agents_in_state(state, agents)
    state = set_agent_status(state, "qa-evaluation-engineer", "running", note="Investigating QA behavior")

    counts = status_counts(state)
    assert counts["running"] == 1


def test_expected_agent_files_parse_required_agents_block() -> None:
    files = expected_agent_files()
    assert "qa-evaluation-engineer.md" in files


def test_missing_expected_agents_and_sync_event() -> None:
    agents = [
        {"name": "qa-evaluation-engineer", "description": "", "path": "Codex/agents/qa-evaluation-engineer.md"},
    ]
    expected = ["qa-evaluation-engineer.md", "school-demo-release-gatekeeper.md"]
    missing = missing_expected_agents(agents, expected)
    assert missing == ["school-demo-release-gatekeeper"]

    state: dict[str, object] = {"agents": {}, "events": [], "missing_agents": []}
    state = sync_missing_agents(state, missing)
    assert state["missing_agents"] == ["school-demo-release-gatekeeper"]
    events = state["events"]
    assert isinstance(events, list)
    assert any(isinstance(evt, dict) and evt.get("event") == "missing-agents-detected" for evt in events)
