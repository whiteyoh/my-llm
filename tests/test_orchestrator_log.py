from pathlib import Path

from tiny_llm import orchestrator_log


def test_start_run_reads_agents_and_writes_events(tmp_path: Path, monkeypatch) -> None:
    state_path = tmp_path / "state.json"
    monkeypatch.setattr(
        orchestrator_log,
        "discover_agents",
        lambda: [{"name": "qa-evaluation-engineer", "description": "", "path": "Codex/agents/qa-evaluation-engineer.md"}],
    )
    monkeypatch.setattr(
        orchestrator_log,
        "expected_agent_files",
        lambda: ["qa-evaluation-engineer.md", "school-demo-release-gatekeeper.md"],
    )

    agents_md = tmp_path / "AGENTS.md"
    agents_md.write_text("# AGENTS\\n<role>orchestrator</role>\\n", encoding="utf-8")
    monkeypatch.setattr(orchestrator_log, "AGENTS_POLICY_PATH", agents_md)

    state = orchestrator_log.start_run("Review repository quality", state_path=state_path)
    assert state["status"] == "running"
    assert state["current_agent"] == "orchestrator"
    assert "run_id" in state
    assert state["missing_agents"] == ["school-demo-release-gatekeeper"]
    assert isinstance(state.get("agents_policy"), dict)
    assert state["agents_policy"]["path"].endswith("AGENTS.md")
    assert state["agents_policy"]["sha256_12"] != "missing"

    events = state.get("events", [])
    assert isinstance(events, list)
    event_names = [str(evt.get("event")) for evt in events if isinstance(evt, dict)]
    assert "task-received" in event_names
    assert "agents-md-read" in event_names
    assert "missing-agents-detected" in event_names


def test_start_run_logs_missing_agents_policy_file(tmp_path: Path, monkeypatch) -> None:
    state_path = tmp_path / "state.json"
    missing_agents_md = tmp_path / "NOPE_AGENTS.md"
    monkeypatch.setattr(orchestrator_log, "AGENTS_POLICY_PATH", missing_agents_md)
    monkeypatch.setattr(
        orchestrator_log,
        "discover_agents",
        lambda: [{"name": "qa-evaluation-engineer", "description": "", "path": "Codex/agents/qa-evaluation-engineer.md"}],
    )
    monkeypatch.setattr(orchestrator_log, "expected_agent_files", lambda: ["qa-evaluation-engineer.md"])

    state = orchestrator_log.start_run("Task without policy", state_path=state_path)
    assert state["agents_policy"]["sha256_12"] == "missing"
    events = state.get("events", [])
    assert isinstance(events, list)
    event_names = [str(evt.get("event")) for evt in events if isinstance(evt, dict)]
    assert "agents-md-missing" in event_names


def test_log_step_and_complete_update_state(tmp_path: Path, monkeypatch) -> None:
    state_path = tmp_path / "state.json"
    monkeypatch.setattr(
        orchestrator_log,
        "discover_agents",
        lambda: [{"name": "qa-evaluation-engineer", "description": "", "path": "Codex/agents/qa-evaluation-engineer.md"}],
    )
    monkeypatch.setattr(orchestrator_log, "expected_agent_files", lambda: ["qa-evaluation-engineer.md"])

    orchestrator_log.start_run("Run checks", state_path=state_path)
    step = orchestrator_log.log_step(
        status="running",
        message="Running tests",
        agent="qa-evaluation-engineer",
        next_action="Summarise results",
        state_path=state_path,
    )
    assert step["status"] == "running"
    assert step["current_agent"] == "qa-evaluation-engineer"
    assert step["next_action"] == "Summarise results"

    final = orchestrator_log.complete_run("Checks complete", state_path=state_path)
    assert final["status"] == "completed"
    assert final["message"] == "Checks complete"
    assert final["current_agent"] == "orchestrator"
