"""Cadence scheduler for the sleep-mode consolidation job."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable
import json
import os
import time

from .sleep_consolidation import (
    analyze_sleep_mode_corpus,
    default_sleep_corpus_paths,
)

DEFAULT_SLEEP_SCHEDULER_ROOT = Path.home() / "CIEL_memories" / "sleep_scheduler"
DEFAULT_SLEEP_SCHEDULER_STATE = DEFAULT_SLEEP_SCHEDULER_ROOT / "state.json"
DEFAULT_SLEEP_SCHEDULER_PID = DEFAULT_SLEEP_SCHEDULER_ROOT / "sleep_scheduler.pid"
DEFAULT_SLEEP_SCHEDULER_LOG = DEFAULT_SLEEP_SCHEDULER_ROOT / "sleep_scheduler.log"


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _normalize_load(load_avg: float | None = None, cpu_count: int | None = None) -> float:
    if load_avg is None:
        try:
            load_avg = os.getloadavg()[0]
        except Exception:
            load_avg = 0.0
    if cpu_count is None:
        cpu_count = os.cpu_count() or 1
    return max(0.0, float(load_avg) / max(float(cpu_count), 1.0))


def _idle_gate(idle_threshold: float, load_avg: float | None = None, cpu_count: int | None = None) -> dict[str, Any]:
    normalized_load = _normalize_load(load_avg=load_avg, cpu_count=cpu_count)
    return {
        "load_avg": float(load_avg if load_avg is not None else (os.getloadavg()[0] if hasattr(os, "getloadavg") else 0.0)),
        "cpu_count": int(cpu_count if cpu_count is not None else (os.cpu_count() or 1)),
        "normalized_load": round(normalized_load, 6),
        "idle_threshold": float(idle_threshold),
        "idle_ready": normalized_load <= idle_threshold,
    }


def _existing_paths(paths: Iterable[str | Path] | None) -> list[Path]:
    if paths is None:
        return default_sleep_corpus_paths()
    out: list[Path] = []
    for raw in paths:
        path = Path(raw)
        if path.exists():
            out.append(path)
    return out


@dataclass(slots=True)
class SleepSchedulerConfig:
    corpus_label: str = "sleep_books"
    paths: list[Path] = field(default_factory=default_sleep_corpus_paths)
    interval_seconds: float = 900.0
    idle_threshold: float = 0.35
    allow_busy: bool = False
    store_memory: bool = True
    report_root: Path | None = None
    state_path: Path = DEFAULT_SLEEP_SCHEDULER_STATE
    load_avg: float | None = None
    cpu_count: int | None = None


@dataclass(slots=True)
class SleepSchedulerCycle:
    created_at: str
    idle_gate: dict[str, Any]
    should_run: bool
    did_run: bool
    report: dict[str, Any] | None
    note: str = ""

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


class SleepModeScheduler:
    """Idle-aware scheduler for book consolidation."""

    def __init__(self, config: SleepSchedulerConfig | None = None) -> None:
        self.config = config or SleepSchedulerConfig()
        self.state_path = Path(self.config.state_path)
        self.pid_path = DEFAULT_SLEEP_SCHEDULER_PID
        self.log_path = DEFAULT_SLEEP_SCHEDULER_LOG
        self.last_cycle: SleepSchedulerCycle | None = None

    def idle_gate(self) -> dict[str, Any]:
        return _idle_gate(
            self.config.idle_threshold,
            load_avg=self.config.load_avg,
            cpu_count=self.config.cpu_count,
        )

    def should_run(self) -> bool:
        gate = self.idle_gate()
        return bool(gate["idle_ready"] or self.config.allow_busy)

    def run_once(self) -> SleepSchedulerCycle:
        gate = self.idle_gate()
        should_run = bool(gate["idle_ready"] or self.config.allow_busy)
        report: dict[str, Any] | None = None
        note = ""

        if should_run:
            report = analyze_sleep_mode_corpus(
                self.config.paths,
                corpus_label=self.config.corpus_label,
                store_memory=self.config.store_memory,
                report_root=self.config.report_root,
                idle_threshold=self.config.idle_threshold,
                allow_busy=self.config.allow_busy,
                load_avg=self.config.load_avg,
                cpu_count=self.config.cpu_count,
            )
            note = "executed"
        else:
            note = "deferred"

        cycle = SleepSchedulerCycle(
            created_at=_utc_now_iso(),
            idle_gate=gate,
            should_run=should_run,
            did_run=report is not None,
            report=report,
            note=note,
        )
        self.last_cycle = cycle
        self._write_state(cycle)
        return cycle

    def run_forever(self, *, stop_after: int | None = None) -> None:
        cycles = 0
        while True:
            self.run_once()
            cycles += 1
            if stop_after is not None and cycles >= stop_after:
                break
            time.sleep(self.config.interval_seconds)

    def _write_state(self, cycle: SleepSchedulerCycle) -> None:
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "schema": "ciel/sleep-scheduler/v0.1",
            "updated_at": cycle.created_at,
            "config": {
                "corpus_label": self.config.corpus_label,
                "paths": [str(path) for path in self.config.paths],
                "interval_seconds": self.config.interval_seconds,
                "idle_threshold": self.config.idle_threshold,
                "allow_busy": self.config.allow_busy,
                "store_memory": self.config.store_memory,
                "report_root": str(self.config.report_root) if self.config.report_root else None,
            },
            "cycle": cycle.as_dict(),
        }
        self.state_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_sleep_scheduler(
    paths: Iterable[str | Path] | None = None,
    *,
    corpus_label: str = "sleep_books",
    interval_seconds: float = 900.0,
    idle_threshold: float = 0.35,
    allow_busy: bool = False,
    store_memory: bool = True,
    report_root: Path | None = None,
    state_path: Path | None = None,
    load_avg: float | None = None,
    cpu_count: int | None = None,
) -> SleepModeScheduler:
    config = SleepSchedulerConfig(
        corpus_label=corpus_label,
        paths=_existing_paths(paths),
        interval_seconds=interval_seconds,
        idle_threshold=idle_threshold,
        allow_busy=allow_busy,
        store_memory=store_memory,
        report_root=report_root,
        state_path=state_path or DEFAULT_SLEEP_SCHEDULER_STATE,
        load_avg=load_avg,
        cpu_count=cpu_count,
    )
    return SleepModeScheduler(config)


__all__ = [
    "DEFAULT_SLEEP_SCHEDULER_ROOT",
    "DEFAULT_SLEEP_SCHEDULER_STATE",
    "DEFAULT_SLEEP_SCHEDULER_PID",
    "DEFAULT_SLEEP_SCHEDULER_LOG",
    "SleepSchedulerConfig",
    "SleepSchedulerCycle",
    "SleepModeScheduler",
    "build_sleep_scheduler",
]
