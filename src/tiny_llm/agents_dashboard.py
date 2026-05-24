from __future__ import annotations

from pathlib import Path

import streamlit as st

from tiny_llm.agents_runtime import (
    STATUS_VALUES,
    append_event,
    discover_agents,
    ensure_agents_in_state,
    expected_agent_files,
    load_state,
    missing_expected_agents,
    save_state,
    set_agent_status,
    set_phase,
    status_counts,
    sync_missing_agents,
)


STATE_PATH = Path("runs/agent_dashboard/state.json")
PHASES = ("Discovery", "Planning", "Implementation", "Testing", "Documentation", "Release")
STATUS_LABELS = {
    "idle": "Idle",
    "queued": "Queued",
    "running": "Running",
    "blocked": "Blocked",
    "completed": "Completed",
}
STATUS_COLORS = {
    "idle": "#94a3b8",
    "queued": "#3b82f6",
    "running": "#06b6d4",
    "blocked": "#ef4444",
    "completed": "#22c55e",
}
STATUS_ICONS = {
    "idle": "◯",
    "queued": "⏳",
    "running": "▶",
    "blocked": "⛔",
    "completed": "✓",
}


def _enable_auto_refresh(interval_ms: int = 2000) -> str:
    auto_refresh_fn = getattr(st, "autorefresh", None)
    if callable(auto_refresh_fn):
        auto_refresh_fn(interval=interval_ms, key="agents-dashboard-autorefresh-2s")
        return "native"

    seconds = max(1.0, interval_ms / 1000.0)
    st.markdown(
        f"<meta http-equiv='refresh' content='{seconds:.1f}'>",
        unsafe_allow_html=True,
    )
    return "meta"


def _inject_style() -> None:
    st.markdown(
        """
<style>
.stApp { background: #0b1220; color: #dbe4f0; }
.wrap { margin-bottom: 0.35rem; }
.title { font-weight: 700; color: #e5edff; font-size: 1.1rem; margin-bottom: 0.1rem; }
.sub { color: #7f93b5; font-size: 0.8rem; }
.kpi {
  background: linear-gradient(180deg,#121d31 0%,#0d1628 100%);
  border: 1px solid #263652; border-radius: 10px; min-height: 76px;
  display:flex; align-items:center; justify-content:center; flex-direction:column; gap:2px;
}
.kpi-ico { font-size: 1.2rem; line-height:1; }
.kpi-val { color:#ecf4ff; font-weight:700; font-size: 1rem; line-height:1.1; }
.lane {
  background:#0f1728; border:1px solid #26354f; border-radius:10px; padding:8px; min-height:200px;
}
.lane-head { color:#dce7fb; font-size:0.82rem; margin-bottom:6px; display:flex; align-items:center; gap:6px; }
.agent {
  background:#14223a; border:1px solid #2f456b; border-radius:8px; padding:6px 8px; margin-bottom:6px;
  color:#dce7fb; font-size:0.78rem; display:flex; align-items:center; gap:7px;
}
.tiny { color:#91a7c9; font-size:0.72rem; }
.pulse {
  width: 8px; height: 8px; border-radius: 999px; background: #06b6d4; display: inline-block;
  box-shadow: 0 0 0 rgba(6,182,212,0.5); animation: pulse 1.3s infinite;
}
@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(6,182,212,0.55); transform: scale(1); }
  70% { box-shadow: 0 0 0 10px rgba(6,182,212,0.0); transform: scale(1.1); }
  100% { box-shadow: 0 0 0 0 rgba(6,182,212,0.0); transform: scale(1); }
}
.alert {
  border:1px solid #7f1d1d; background:#2a1214; color:#fecaca; border-radius:10px; padding:8px 10px;
  font-size:0.8rem;
}
.ok {
  border:1px solid #14532d; background:#0f2417; color:#bbf7d0; border-radius:10px; padding:8px 10px;
  font-size:0.8rem;
}
</style>
        """,
        unsafe_allow_html=True,
    )


def _sort_for_board(agent: dict[str, object], state: dict[str, object]) -> tuple[int, str]:
    name = str(agent["name"])
    agent_info = state.get("agents", {}).get(name, {}) if isinstance(state.get("agents"), dict) else {}
    updated = ""
    if isinstance(agent_info, dict):
        updated = str(agent_info.get("updated_at", ""))
    return (0 if updated else 1, updated)


def _icon_kpi(icon: str, value: str, color: str) -> None:
    st.markdown(
        f"<div class='kpi'><div class='kpi-ico' style='color:{color}'>{icon}</div><div class='kpi-val'>{value}</div></div>",
        unsafe_allow_html=True,
    )


def _lane_header(status: str, count: int) -> str:
    icon = STATUS_ICONS[status]
    color = STATUS_COLORS[status]
    return f"<div class='lane-head'><span style='color:{color}'>{icon}</span><span>{count}</span></div>"


def main() -> None:
    st.set_page_config(page_title="Kairo Agent Ops", layout="wide")
    _inject_style()
    _enable_auto_refresh(interval_ms=2000)

    st.markdown(
        "<div class='wrap'><div class='title'>Agent Ops</div><div class='sub'>live / 2s</div></div>",
        unsafe_allow_html=True,
    )

    agents = discover_agents()
    if not agents:
        st.error("No agent files found in .Codex/agents or Codex/agents.")
        return

    state = ensure_agents_in_state(load_state(STATE_PATH), agents)
    missing_agents = missing_expected_agents(agents, expected_agent_files())
    state = sync_missing_agents(state, missing_agents)

    sidebar = st.sidebar
    sidebar.header("Ops")
    phase = sidebar.selectbox("Phase", PHASES, index=PHASES.index(str(state.get("phase", "Discovery"))))
    state = set_phase(state, phase)

    if sidebar.button("Reset"):
        for agent in agents:
            state = set_agent_status(state, str(agent["name"]), "idle", note="Board reset")
        state["events"] = []
        state["missing_agents"] = []
        state = set_phase(state, "Discovery")
        append_event(state, "orchestrator", "board-reset")

    counts = status_counts(state)
    running_agents = [
        str(agent["name"])
        for agent in agents
        if isinstance(state.get("agents", {}).get(str(agent["name"]), {}), dict)
        and state["agents"][str(agent["name"])].get("status") == "running"
    ]

    k1, k2, k3, k4, k5, k6 = st.columns(6)
    with k1:
        _icon_kpi("🧩", str(len(agents)), "#9ca3af")
    with k2:
        _icon_kpi("▶", str(counts["running"]), STATUS_COLORS["running"])
    with k3:
        _icon_kpi("⏳", str(counts["queued"]), STATUS_COLORS["queued"])
    with k4:
        _icon_kpi("⛔", str(counts["blocked"]), STATUS_COLORS["blocked"])
    with k5:
        _icon_kpi("✓", str(counts["completed"]), STATUS_COLORS["completed"])
    with k6:
        _icon_kpi("⚠" if missing_agents else "✔", str(len(missing_agents)), "#f59e0b" if missing_agents else "#22c55e")

    if running_agents:
        st.markdown(
            f"<div class='ok'><span class='pulse'></span>&nbsp; {', '.join(running_agents)}</div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown("<div class='ok'>✓ idle</div>", unsafe_allow_html=True)

    if missing_agents:
        st.markdown(
            f"<div class='alert'>⚠ missing: {', '.join(missing_agents)}</div>",
            unsafe_allow_html=True,
        )

    board_cols = st.columns(5)
    for i, status in enumerate(STATUS_VALUES):
        with board_cols[i]:
            st.markdown(_lane_header(status, counts[status]), unsafe_allow_html=True)
            st.markdown("<div class='lane'>", unsafe_allow_html=True)
            members = []
            for agent in sorted(agents, key=lambda a: _sort_for_board(a, state)):
                info = state["agents"].get(str(agent["name"]), {})
                if isinstance(info, dict) and info.get("status") == status:
                    members.append((agent, info))

            if not members:
                st.markdown("<div class='tiny'>·</div>", unsafe_allow_html=True)
            else:
                for agent, info in members:
                    name = str(agent["name"])
                    short = "".join(part[:1] for part in name.split("-"))[:4].upper() or name[:4].upper()
                    badge = "<span class='pulse'></span>" if status == "running" else f"<span style='color:{STATUS_COLORS[status]}'>{STATUS_ICONS[status]}</span>"
                    st.markdown(
                        f"<div class='agent' title='{name}'>{badge}<span>{short}</span></div>",
                        unsafe_allow_html=True,
                    )
                    note = str(info.get("notes", "")).strip()
                    if note:
                        st.markdown(f"<div class='tiny'>{note[:42]}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    events = state.get("events", [])
    if isinstance(events, list) and events:
        with st.expander("◷", expanded=False):
            for event in reversed(events[-12:]):
                if not isinstance(event, dict):
                    continue
                agent = str(event.get("agent", ""))
                action = str(event.get("event", ""))
                st.markdown(f"<div class='tiny'>• {agent} · {action}</div>", unsafe_allow_html=True)

    save_state(STATE_PATH, state)


if __name__ == "__main__":
    main()
