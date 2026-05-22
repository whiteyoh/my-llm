from __future__ import annotations

from pathlib import Path

import streamlit as st

from tiny_llm.agents_runtime import (
    STATUS_VALUES,
    discover_agents,
    ensure_agents_in_state,
    load_state,
    save_state,
    set_agent_status,
    set_phase,
    status_counts,
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
    "idle": "#64748b",
    "queued": "#1d4ed8",
    "running": "#0891b2",
    "blocked": "#dc2626",
    "completed": "#16a34a",
}


def _status_badge(status: str) -> str:
    color = STATUS_COLORS.get(status, "#64748b")
    label = STATUS_LABELS.get(status, status.title())
    return (
        f"<span style='display:inline-block;padding:2px 10px;border-radius:999px;"
        f"background:{color};color:white;font-size:0.8rem;font-weight:600;'>{label}</span>"
    )


def _sort_for_board(agent: dict[str, object], state: dict[str, object]) -> tuple[int, str]:
    name = str(agent["name"])
    agent_info = state.get("agents", {}).get(name, {}) if isinstance(state.get("agents"), dict) else {}
    updated = ""
    if isinstance(agent_info, dict):
        updated = str(agent_info.get("updated_at", ""))
    return (0 if updated else 1, updated)


def main() -> None:
    st.set_page_config(page_title="Kairo Agent Operations", layout="wide")
    st.title("Kairo Agent Operations Dashboard")
    st.caption("Live board for orchestrator + worker visibility during development and classroom prep.")

    agents = discover_agents()
    if not agents:
        st.error("No agent files found in .Codex/agents or Codex/agents.")
        return

    state = ensure_agents_in_state(load_state(STATE_PATH), agents)

    sidebar = st.sidebar
    sidebar.header("Session Controls")
    phase = sidebar.selectbox("Current phase", PHASES, index=PHASES.index(str(state.get("phase", "Discovery"))))
    state = set_phase(state, phase)

    auto_refresh = sidebar.toggle("Auto refresh board", value=True)
    if auto_refresh:
        auto_refresh_fn = getattr(st, "autorefresh", None)
        if callable(auto_refresh_fn):
            auto_refresh_fn(interval=5000, key="agents-dashboard-autorefresh")
        else:
            sidebar.caption("Auto refresh unavailable in this Streamlit version.")

    if sidebar.button("Refresh Now"):
        st.rerun()

    if sidebar.button("Reset Board"):
        for agent in agents:
            state = set_agent_status(state, str(agent["name"]), "idle", note="Board reset")
        state["events"] = []
        state = set_phase(state, "Discovery")
        st.success("Board reset.")

    counts = status_counts(state)
    metric_cols = st.columns(6)
    metric_cols[0].metric("Agents", len(agents))
    metric_cols[1].metric("Running", counts["running"])
    metric_cols[2].metric("Queued", counts["queued"])
    metric_cols[3].metric("Blocked", counts["blocked"])
    metric_cols[4].metric("Completed", counts["completed"])
    metric_cols[5].metric("Phase", str(state.get("phase", "Discovery")))

    board_cols = st.columns(5)
    for i, status in enumerate(STATUS_VALUES):
        with board_cols[i]:
            st.subheader(STATUS_LABELS[status])
            members = []
            for agent in sorted(agents, key=lambda a: _sort_for_board(a, state)):
                agent_info = state["agents"].get(str(agent["name"]), {})
                if isinstance(agent_info, dict) and agent_info.get("status") == status:
                    members.append((agent, agent_info))

            if not members:
                st.caption("No agents")

            for agent, agent_info in members:
                st.markdown(f"**{agent['name']}**  \n{_status_badge(status)}", unsafe_allow_html=True)
                desc = str(agent.get("description", "")).strip()
                if desc:
                    st.caption(desc)
                note = str(agent_info.get("notes", "")).strip()
                if note:
                    st.caption(f"Note: {note}")
                st.markdown("---")

    st.subheader("Agent Controls")
    for agent in agents:
        name = str(agent["name"])
        info = state["agents"].get(name, {})
        if not isinstance(info, dict):
            info = {"status": "idle", "notes": "", "updated_at": ""}

        with st.expander(name):
            st.caption(str(agent.get("description", "")))
            use_when = agent.get("use_when", [])
            if isinstance(use_when, list) and use_when:
                st.write("Use when:")
                for item in use_when[:3]:
                    st.write(f"- {item}")

            current_status = str(info.get("status", "idle"))
            status = st.selectbox(
                "Status",
                STATUS_VALUES,
                index=STATUS_VALUES.index(current_status) if current_status in STATUS_VALUES else 0,
                key=f"status-{name}",
            )
            note = st.text_input("Note", value=str(info.get("notes", "")), key=f"note-{name}")
            if st.button("Apply", key=f"apply-{name}"):
                state = set_agent_status(state, name, status, note=note)
                save_state(STATE_PATH, state)
                st.success(f"Updated {name} -> {status}.")

    st.subheader("Activity Feed")
    events = state.get("events", [])
    if not isinstance(events, list) or not events:
        st.caption("No activity yet.")
    else:
        for event in reversed(events[-30:]):
            if not isinstance(event, dict):
                continue
            timestamp = str(event.get("timestamp", ""))
            agent = str(event.get("agent", ""))
            action = str(event.get("event", ""))
            note = str(event.get("note", "")).strip()
            line = f"`{timestamp}` • **{agent}** • `{action}`"
            if note:
                line += f" • {note}"
            st.markdown(line)

    save_state(STATE_PATH, state)


if __name__ == "__main__":
    main()
