#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import signal
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
PKG_PARENT = ROOT.parent
for candidate in (PKG_PARENT, ROOT):
    candidate_str = str(candidate)
    if candidate_str not in sys.path:
        sys.path.insert(0, candidate_str)

from ciel_omega.memory.sleep_scheduler import (  # noqa: E402
    DEFAULT_SLEEP_SCHEDULER_LOG,
    DEFAULT_SLEEP_SCHEDULER_PID,
    DEFAULT_SLEEP_SCHEDULER_STATE,
    build_sleep_scheduler,
)

_RUNNING = True


def _json_default(obj: Any) -> Any:
    try:
        import numpy as np  # noqa: WPS433

        if isinstance(obj, (np.ndarray,)):
            return obj.tolist()
        if isinstance(obj, (np.floating, np.integer)):
            return obj.item()
    except Exception:
        return str(obj)
    return str(obj)


def _handle_signal(signum, frame):  # noqa: ANN001
    global _RUNNING
    _RUNNING = False


def _write_pid(pid_path: Path) -> None:
    pid_path.parent.mkdir(parents=True, exist_ok=True)
    pid_path.write_text(str(os.getpid()), encoding="utf-8")


def _remove_pid(pid_path: Path) -> None:
    try:
        pid_path.unlink()
    except FileNotFoundError:
        pass


def _read_state(state_path: Path) -> dict[str, Any]:
    if not state_path.exists():
        return {"error": "STATE_MISSING", "path": str(state_path)}
    try:
        return json.loads(state_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"error": f"{type(exc).__name__}: {exc}", "path": str(state_path)}


def run_daemon(args: argparse.Namespace) -> None:
    scheduler = build_sleep_scheduler(
        args.paths or None,
        corpus_label=args.corpus_label,
        interval_seconds=args.interval,
        idle_threshold=args.idle_threshold,
        allow_busy=args.allow_busy,
        store_memory=not args.no_store,
        report_root=Path(args.report_root) if args.report_root else None,
        state_path=Path(args.state_path) if args.state_path else DEFAULT_SLEEP_SCHEDULER_STATE,
        load_avg=args.load_avg,
        cpu_count=args.cpu_count,
    )

    signal.signal(signal.SIGTERM, _handle_signal)
    signal.signal(signal.SIGINT, _handle_signal)
    _write_pid(Path(args.pid_path) if args.pid_path else DEFAULT_SLEEP_SCHEDULER_PID)
    print(f"[sleep-daemon] PID={os.getpid()} interval={args.interval}s idle={args.idle_threshold}")

    while _RUNNING:
        cycle = scheduler.run_once()
        print(json.dumps(cycle.as_dict(), ensure_ascii=False, default=_json_default))
        if args.once:
            break
        if not _RUNNING:
            break
        if args.interval > 0:
            import time

            time.sleep(args.interval)

    _remove_pid(Path(args.pid_path) if args.pid_path else DEFAULT_SLEEP_SCHEDULER_PID)
    print("[sleep-daemon] stopped.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Sleep-mode consolidation daemon")
    parser.add_argument("paths", nargs="*", help="Optional book/pdf paths; defaults to the canonical sleep corpus")
    parser.add_argument("--corpus-label", default="sleep_books")
    parser.add_argument("--interval", type=float, default=900.0)
    parser.add_argument("--idle-threshold", type=float, default=0.35)
    parser.add_argument("--allow-busy", action="store_true")
    parser.add_argument("--no-store", action="store_true")
    parser.add_argument("--report-root", default="", help="Report output root")
    parser.add_argument("--state-path", default="", help="Scheduler state JSON path")
    parser.add_argument("--pid-path", default="", help="PID file path")
    parser.add_argument("--load-avg", type=float, default=None)
    parser.add_argument("--cpu-count", type=int, default=None)
    parser.add_argument("--once", action="store_true", help="Run one cycle and exit")
    parser.add_argument("--daemon", action="store_true", help="Run detached in the background")
    parser.add_argument("--status", action="store_true")
    parser.add_argument("--stop", action="store_true")
    args = parser.parse_args()

    pid_path = Path(args.pid_path) if args.pid_path else DEFAULT_SLEEP_SCHEDULER_PID
    state_path = Path(args.state_path) if args.state_path else DEFAULT_SLEEP_SCHEDULER_STATE

    if args.status:
        print(json.dumps(_read_state(state_path), ensure_ascii=False, default=_json_default, indent=2))
        return 0

    if args.stop:
        if pid_path.exists():
            os.kill(int(pid_path.read_text(encoding="utf-8").strip()), signal.SIGTERM)
            print("Stopped")
        else:
            print("Daemon not running")
        return 0

    if args.daemon and not args.once:
        if os.fork() != 0:
            return 0
        os.setsid()
        if os.fork() != 0:
            return 0
        log_path = DEFAULT_SLEEP_SCHEDULER_LOG
        log_path.parent.mkdir(parents=True, exist_ok=True)
        sys.stdout = open(log_path, "a", encoding="utf-8")
        sys.stderr = sys.stdout

    run_daemon(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
