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
    "idle": "#6b7280",
    "queued": "#2563eb",
    "running": "#0ea5e9",
    "blocked": "#ef4444",
    "completed": "#22c55e",
}


def _inject_argocd_style() -> None:
    st.markdown(
        """
<style>
.stApp { background: #0b1220; color: #dbe4f0; }
.argocd-title { font-weight: 700; font-size: 1.45rem; color: #e5edff; margin-bottom: 0.15rem; }
.argocd-sub { color: #93a4bf; font-size: 0.92rem; margin-bottom: 1rem; }
.argo-kpi {
  background: linear-gradient(180deg,#111b2e 0%,#0f1728 100%);
  border: 1px solid #25324b; border-radius: 10px; padding: 10px 12px; min-height: 92px;
}
.argo-kpi .k { color:#8fa2c1; font-size:0.78rem; text-transform: uppercase; letter-spacing: 0.04em; }
.argo-kpi .v { color:#ecf4ff; font-size:1.28rem; font-weight:700; margin-top:0.35rem; }
.argo-kpi .h { color:#8fa2c1; font-size:0.8rem; margin-top:0.2rem; }
.argo-chip { display:inline-block; padding:3px 10px; border-radius:999px; font-size:0.78rem; font-weight:600; color:white; }
.argo-lane {
  background:#0f1728; border:1px solid #26354f; border-radius:10px; padding:10px; min-height:260px;
}
.argo-lane-title { color:#dce7fb; font-weight:700; margin-bottom:10px; }
.argo-agent {
  background:#131f33; border:1px solid #2a3b59; border-radius:8px; padding:9px 10px; margin-bottom:8px;
}
.argo-agent-name { color:#ecf3ff; font-weight:600; font-size:0.92rem; }
.argo-agent-note { color:#95a8c8; font-size:0.8rem; margin-top:4px; }
.argo-alert {
  border:1px solid #7f1d1d; background:#2a1214; color:#fecaca; border-radius:10px; padding:10px 12px;
}
.argo-ok {
  border:1px solid #14532d; background:#0f2417; color:#bbf7d0; border-radius:10px; padding:10px 12px;
}
</style>
        """,
        unsafe_allow_html=True,
    )


def _chip(label: str, color: str) -> str:
    return f"<span class='argo-chip' style='background:{color};'>{label}</span>"


def _sort_for_board(agent: dict[str, object], state: dict[str, object]) -> tuple[int, str]:
    name = str(agent["name"])
    agent_info = state.get("agents", {}).get(name, {}) if isinstance(state.get("agents"), dict) else {}
    updated = ""
    if isinstance(agent_info, dict):
        updated = str(agent_info.get("updated_at", ""))
    return (0 if updated else 1, updated)


def _render_kpi(label: str, value: str, hint: str = "") -> None:
    st.markdown(
        f"<div class='argo-kpi'><div class='k'>{label}</div><div class='v'>{value}</div><div class='h'>{hint}</div></div>",
        unsafe_allow_html=True,
    )


def main() -> None:
    st.set_page_config(page_title="Kairo Agent Operations", layout="wide")
    _inject_argocd_style()
    st.markdown("<div class='argocd-title'>Kairo Agent Operations</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='argocd-sub'>Argo-style orchestrator board for worker status, runtime activity, and missing agent detection.</div>",
        unsafe_allow_html=True,
    )

    agents = discover_agents()
    if not agents:
        st.error("No agent files found in .Codex/agents or Codex/agents.")
        return

    state = ensure_agents_in_state(load_state(STATE_PATH), agents)
    expected_files = expected_agent_files()
    missing_agents = missing_expected_agents(agents, expected_files)
    state = sync_missing_agents(state, missing_agents)

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
        state["missing_agents"] = []
        state = set_phase(state, "Discovery")
        append_event(state, "orchestrator", "board-reset")
        st.success("Board reset.")

    counts = status_counts(state)
    running_agents = [
        str(agent["name"])
        for agent in agents
        if isinstance(state.get("agents", {}).get(str(agent["name"]), {}), dict)
        and state["agents"][str(agent["name"])].get("status") == "running"
    ]
    sync_status = "OutOfSync" if missing_agents else "Synced"
    sync_color = "#f59e0b" if missing_agents else "#22c55e"
    health_status = "Degraded" if counts["blocked"] > 0 or missing_agents else "Healthy"
    health_color = "#ef4444" if counts["blocked"] > 0 or missing_agents else "#22c55e"

    k1, k2, k3, k4, k5, k6 = st.columns(6)
    with k1:
        _render_kpi("Workers", str(len(agents)), "discovered")
    with k2:
        _render_kpi("Running", str(counts["running"]), ", ".join(running_agents[:2]) if running_agents else "no active workers")
    with k3:
        _render_kpi("Queued", str(counts["queued"]), "awaiting execution")
    with k4:
        _render_kpi("Blocked", str(counts["blocked"]), "needs intervention")
    with k5:
        _render_kpi("Sync", sync_status, "expected worker files")
    with k6:
        _render_kpi("Health", health_status, f"phase: {state.get('phase', 'Discovery')}")

    status_row = f"{_chip(sync_status, sync_color)}&nbsp;&nbsp;{_chip(health_status, health_color)}"
    st.markdown(status_row, unsafe_allow_html=True)

    if running_agents:
        st.markdown(
            f"<div class='argo-ok'><strong>Running now:</strong> {', '.join(running_agents)}</div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown("<div class='argo-ok'><strong>Running now:</strong> none</div>", unsafe_allow_html=True)

    if missing_agents:
        st.markdown(
            f"<div class='argo-alert'><strong>Missing agents detected:</strong> {', '.join(missing_agents)}</div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            "<div class='argo-ok'><strong>Expected agents:</strong> all discovered</div>",
            unsafe_allow_html=True,
        )

    board_cols = st.columns(5)
    for i, status in enumerate(STATUS_VALUES):
        with board_cols[i]:
            st.markdown(
                f"<div class='argo-lane-title'>{STATUS_LABELS[status]}</div>",
                unsafe_allow_html=True,
            )
            st.markdown("<div class='argo-lane'>", unsafe_allow_html=True)
            members = []
            for agent in sorted(agents, key=lambda a: _sort_for_board(a, state)):
                agent_info = state["agents"].get(str(agent["name"]), {})
                if isinstance(agent_info, dict) and agent_info.get("status") == status:
                    members.append((agent, agent_info))

            if not members:
                st.caption("No agents")
            else:
                for agent, agent_info in members:
                    color = STATUS_COLORS.get(status, "#6b7280")
                    st.markdown(
                        (
                            f"<div class='argo-agent'><div class='argo-agent-name'>{agent['name']}</div>"
                            f"{_chip(STATUS_LABELS[status], color)}"
                            "</div>"
                        ),
                        unsafe_allow_html=True,
                    )
                    note = str(agent_info.get("notes", "")).strip()
                    if note:
                        st.caption(f"Note: {note}")
            st.markdown("</div>", unsafe_allow_html=True)

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
