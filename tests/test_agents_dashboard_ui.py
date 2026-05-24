from __future__ import annotations

import importlib.util

import pytest


class _FakeContext:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class _FakeSidebar:
    def header(self, _label: str) -> None:
        return None

    def selectbox(self, _label: str, options, index: int = 0):
        return options[index]

    def button(self, _label: str) -> bool:
        return False


class _FakeStreamlit:
    def __init__(self) -> None:
        self.markdowns: list[str] = []
        self.sidebar = _FakeSidebar()

    def set_page_config(self, **_kwargs) -> None:
        return None

    def markdown(self, text: str, unsafe_allow_html: bool = False) -> None:
        del unsafe_allow_html
        self.markdowns.append(text)

    def columns(self, count: int):
        return [_FakeContext() for _ in range(count)]

    def error(self, text: str) -> None:
        self.markdowns.append(text)

    def expander(self, _label: str, expanded: bool = False):
        del expanded
        return _FakeContext()


def test_dashboard_renders_running_and_missing_agent_signals(monkeypatch) -> None:
    if importlib.util.find_spec("streamlit") is None:
        pytest.skip('streamlit not installed; install with: pip install -e ".[learn]"')

    import tiny_llm.agents_dashboard as dashboard

    agents = [
        {"name": "qa-evaluation-engineer", "description": "QA checks", "path": ".Codex/agents/qa-evaluation-engineer.md"},
        {"name": "ci-pipeline-maintainer", "description": "CI checks", "path": ".Codex/agents/ci-pipeline-maintainer.md"},
    ]
    state = {
        "agents": {
            "qa-evaluation-engineer": {"status": "running", "notes": "Reviewing chapter QA", "updated_at": "2026-05-24T10:00:00+00:00"},
            "ci-pipeline-maintainer": {"status": "idle", "notes": "", "updated_at": ""},
        },
        "events": [],
        "phase": "Discovery",
        "missing_agents": [],
    }

    monkeypatch.setattr(dashboard, "discover_agents", lambda: agents)
    monkeypatch.setattr(dashboard, "load_state", lambda _path: state)
    monkeypatch.setattr(dashboard, "save_state", lambda _path, _state: None)
    monkeypatch.setattr(dashboard, "expected_agent_files", lambda: ["qa-evaluation-engineer.md", "release-manager.md"])
    fake_streamlit = _FakeStreamlit()
    monkeypatch.setattr(dashboard, "st", fake_streamlit)

    dashboard.main()
    assert any("http-equiv='refresh'" in value for value in fake_streamlit.markdowns)
    assert any("qa-evaluation-engineer" in value for value in fake_streamlit.markdowns)
    assert any("missing: release-manager" in value for value in fake_streamlit.markdowns)
    assert any("pulse" in value for value in fake_streamlit.markdowns)
