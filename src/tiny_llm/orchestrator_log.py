from __future__ import annotations

import argparse
from datetime import UTC, datetime
import hashlib
from pathlib import Path

from tiny_llm.agents_runtime import (
    append_event,
    discover_agents,
    ensure_agents_in_state,
    expected_agent_files,
    load_state,
    missing_expected_agents,
    save_state,
    sync_missing_agents,
)


STATE_PATH = Path("runs/agent_dashboard/state.json")
AGENTS_POLICY_PATH = Path("AGENTS.md")
STATUS_VALUES = ("idle", "queued", "running", "blocked", "completed")


def _now_iso() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat()


def _run_id() -> str:
    return datetime.now(tz=UTC).strftime("run-%Y%m%dT%H%M%SZ")


def _load_runtime_state(state_path: Path = STATE_PATH) -> dict[str, object]:
    agents = discover_agents()
    state = ensure_agents_in_state(load_state(state_path), agents)
    missing = missing_expected_agents(agents, expected_agent_files())
    state = sync_missing_agents(state, missing)
    return state


def _load_agents_policy(path: Path | None = None) -> dict[str, str]:
    policy_path = path or AGENTS_POLICY_PATH
    if not policy_path.exists():
        raise FileNotFoundError(f"Missing policy file: {policy_path}")
    text = policy_path.read_text(encoding="utf-8")
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]
    return {"path": str(policy_path), "sha256_12": digest}


def _save_runtime_state(state: dict[str, object], state_path: Path = STATE_PATH) -> None:
    state["last_updated"] = _now_iso()
    save_state(state_path, state)


def start_run(task: str, state_path: Path = STATE_PATH) -> dict[str, object]:
    state = _load_runtime_state(state_path=state_path)
    state["run_id"] = _run_id()
    state["current_agent"] = "orchestrator"
    state["status"] = "running"
    state["message"] = task
    state["next_action"] = "Match task to worker agents"
    state["agents_directory"] = ".Codex/agents/"
    state["runtime_directory"] = "runs/agent_dashboard/"

    append_event(state, "orchestrator", "task-received", note=task)
    try:
        policy = _load_agents_policy()
        state["agents_policy"] = policy
        append_event(
            state,
            "orchestrator",
            "agents-md-read",
            note=f"{policy['path']} sha={policy['sha256_12']}",
        )
    except FileNotFoundError as exc:
        state["agents_policy"] = {"path": str(AGENTS_POLICY_PATH), "sha256_12": "missing"}
        append_event(state, "orchestrator", "agents-md-missing", note=str(exc))
    _save_runtime_state(state, state_path=state_path)
    return state


def log_step(
    *,
    status: str,
    message: str,
    next_action: str = "",
    agent: str = "orchestrator",
    state_path: Path = STATE_PATH,
) -> dict[str, object]:
    if status not in STATUS_VALUES:
        raise ValueError(f"Invalid status '{status}'. Expected one of: {', '.join(STATUS_VALUES)}")
    state = _load_runtime_state(state_path=state_path)
    state["status"] = status
    state["message"] = message
    state["current_agent"] = agent
    if next_action:
        state["next_action"] = next_action

    append_event(state, agent, f"status->{status}", note=message)
    _save_runtime_state(state, state_path=state_path)
    return state


def complete_run(message: str = "Task handled", state_path: Path = STATE_PATH) -> dict[str, object]:
    state = _load_runtime_state(state_path=state_path)
    state["status"] = "completed"
    state["message"] = message
    state["current_agent"] = "orchestrator"
    state["next_action"] = "idle"
    append_event(state, "orchestrator", "run-complete", note=message)
    _save_runtime_state(state, state_path=state_path)
    return state


def block_run(message: str, state_path: Path = STATE_PATH) -> dict[str, object]:
    state = _load_runtime_state(state_path=state_path)
    state["status"] = "blocked"
    state["message"] = message
    state["current_agent"] = "orchestrator"
    append_event(state, "orchestrator", "run-blocked", note=message)
    _save_runtime_state(state, state_path=state_path)
    return state


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Write orchestrator runtime logs for the agent dashboard.")
    sub = parser.add_subparsers(dest="command", required=True)

    start = sub.add_parser("start", help="Start a run and log that AGENTS.md was read.")
    start.add_argument("--task", required=True, help="User task text.")

    step = sub.add_parser("step", help="Log a step for the current run.")
    step.add_argument("--status", required=True, choices=STATUS_VALUES)
    step.add_argument("--message", required=True)
    step.add_argument("--agent", default="orchestrator")
    step.add_argument("--next_action", default="")

    complete = sub.add_parser("complete", help="Mark the current run complete.")
    complete.add_argument("--message", default="Task handled")

    blocked = sub.add_parser("blocked", help="Mark the current run blocked.")
    blocked.add_argument("--message", required=True)

    return parser


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()
    if args.command == "start":
        state = start_run(task=args.task)
    elif args.command == "step":
        state = log_step(
            status=args.status,
            message=args.message,
            next_action=args.next_action,
            agent=args.agent,
        )
    elif args.command == "complete":
        state = complete_run(message=args.message)
    elif args.command == "blocked":
        state = block_run(message=args.message)
    else:  # pragma: no cover
        parser.error(f"Unknown command: {args.command}")
        return

    print(f"run_id={state.get('run_id', '')} status={state.get('status', '')} current_agent={state.get('current_agent', '')}")


if __name__ == "__main__":
    main()
