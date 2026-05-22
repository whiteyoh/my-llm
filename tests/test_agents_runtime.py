from pathlib import Path

from tiny_llm.agents_runtime import discover_agent_files, discover_agents, ensure_agents_in_state, set_agent_status, status_counts


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
