"""NOEMA path registry — one source of truth for runtime locations.

The registry prefers an explicit JSON configuration but always exposes the same
public contract. A clean checkout, wheel installation, test runner, or new host
therefore receives deterministic local paths instead of an empty accessor.

Configuration discovery order:

1. ``$NOEMA_PATHS``;
2. ``~/.config/noema/paths.json``;
3. the historical host configuration path;
4. a generated local fallback rooted at ``$NOEMA_RUNTIME_ROOT`` or
   ``/tmp/noema``.

No fallback path is promoted to an external NOEMA Source of Truth. It is only a
local runtime configuration used when no operator-supplied configuration exists.
"""

from __future__ import annotations

import json
import logging
import os
import re
from pathlib import Path
from typing import Any

log = logging.getLogger(__name__)
_VAR_RE = re.compile(r"\{(\w+)\}")
_REPO_ROOT = Path(__file__).resolve().parents[2]


def _expand(value: str) -> str:
    return os.path.expanduser(os.path.expandvars(value))


def _find_config() -> Path | None:
    env = os.environ.get("NOEMA_PATHS")
    if env:
        candidate = Path(env).expanduser()
        if candidate.is_file():
            return candidate

    candidates = (
        Path.home() / ".config" / "noema" / "paths.json",
        Path("/home/adrian/new_volume_rw/NOEMA_LIBRARY/CONFIG/paths.json"),
    )
    return next((candidate for candidate in candidates if candidate.is_file()), None)


def _default_config() -> dict[str, Any]:
    runtime = Path(os.environ.get("NOEMA_RUNTIME_ROOT", "/tmp/noema")).expanduser()
    memory = Path(os.environ.get("NOEMA_MEMORY_ROOT", runtime / "memory")).expanduser()
    library = Path(os.environ.get("NOEMA_LIBRARY_ROOT", runtime / "library")).expanduser()
    phase_data = Path(os.environ.get("NOEMA_PHASE_DATA_ROOT", runtime / "phase_data")).expanduser()
    surface = Path(os.environ.get("NOEMA_SURFACE_ROOT", "/dev/shm/ciel_noema")).expanduser()
    memory_state = memory / "state"
    memory_logs = memory / "logs"
    memory_data = memory / "data"

    roots = {
        "repo": str(_REPO_ROOT),
        "runtime": str(runtime),
        "memory": str(memory),
        "library": str(library),
        "phase_data": str(phase_data),
        "surface": str(surface),
        "results": str(_REPO_ROOT / "results"),
        "mummu": str(library / "mummu"),
        "news": str(library / "news"),
        "dzienniki": str(library / "dzienniki"),
    }
    raw_logs = memory / "raw_logs"
    sub_log = memory_logs / "ciel_sub_log.jsonl"
    beta_log = memory_logs / "subconsciousness_beta_log.jsonl"
    return {
        "roots": roots,
        "databases": {
            "taskplan": str(runtime / "db" / "noema_taskplan.db"),
            "knowledge": str(runtime / "db" / "noema_knowledge.db"),
            "memories_index": str(memory / "memories_index.db"),
            "raw_memory": str(memory / "raw_memory.db"),
            "card_db": str(runtime / "db" / "cielingo_cards.db"),
        },
        "state": {
            "orch_pkl": str(memory_state / "ciel_orch_state.pkl"),
            "orch_state_pkl": str(memory_state / "ciel_orch_state.pkl"),
            "orbital_registry": str(memory_state / "orbital_registry.json"),
            "last_metrics_json": str(memory_state / "last_metrics.json"),
            "pipeline_config": str(runtime / "config" / "pipeline.json"),
            "htri_json": str(memory_state / "htri_state.json"),
            "ciel_json": str(memory_state / "ciel_state.json"),
            "phase_memory": str(memory_state / "cielingo_phase_memory"),
        },
        "logs": {
            "raw_logs": str(raw_logs),
            "raw_logs_dir": str(raw_logs),
            "sub_log": str(sub_log),
            "ciel_sub_log": str(sub_log),
            "beta_log": str(beta_log),
            "subconsciousness_beta_log": str(beta_log),
            "consciousness_log": str(memory_logs / "consciousness.log"),
            "memory_consolidator": str(memory_logs / "memory_consolidator.log"),
        },
        "secrets": {
            "cielapi": str(runtime / "secrets" / "cielapi"),
            "anthropic": str(runtime / "secrets" / "anthropic_api_key"),
        },
        "surface_subdirs": {
            "analog": str(surface / "analog"),
            "state": str(surface / "state"),
        },
        "surface_files": {
            "binding_status": str(surface / "ciel_binding_status"),
            "tick": str(surface / "tick"),
        },
        "phase_data_subdirs": {},
        "library_subdirs": {
            "mummu": str(library / "mummu"),
            "news": str(library / "news"),
            "dzienniki": str(library / "dzienniki"),
        },
        "daemon_pids": {},
        "data_files": {
            "hunches": str(memory_data / "hunches.jsonl"),
            "intentions": str(memory_data / "intentions.jsonl"),
            "projects": str(memory_data / "projects.json"),
            "routines": str(memory_data / "routines.json"),
            "ciel_entries": str(memory_data / "ciel_entries.jsonl"),
            "ciel_dziennik": str(memory_data / "ciel_dziennik.jsonl"),
        },
    }


def _resolve_vars(value: str, var_map: dict[str, str]) -> str:
    def replace(match: re.Match[str]) -> str:
        return var_map.get(match.group(1).lower(), match.group(0))

    previous = value
    for _ in range(8):
        resolved = _VAR_RE.sub(replace, previous)
        if resolved == previous:
            break
        previous = resolved
    return _expand(previous)


class _PathAccessor:
    def __init__(self, data: dict[str, Any], var_map: dict[str, str], prefix: str = ""):
        self._data = data
        self._var_map = var_map
        self._prefix = prefix

    def __getattr__(self, name: str) -> Any:
        key = name.lower()
        if key not in self._data:
            raise AttributeError(f"Paths has no attribute {name!r} (section: {self._prefix or 'root'})")
        value = self._data[key]
        if isinstance(value, dict):
            return _PathAccessor(value, self._var_map, f"{self._prefix}{key}.")
        if isinstance(value, str):
            return _resolve_vars(value, self._var_map)
        return value

    def __repr__(self) -> str:
        keys = sorted(key for key in self._data if not key.startswith("_"))
        return f"<Paths [{', '.join(keys)}]>"

    def as_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in self._data.items():
            if key.startswith("_"):
                continue
            if isinstance(value, dict):
                result[key] = _PathAccessor(value, self._var_map, f"{self._prefix}{key}.").as_dict()
            elif isinstance(value, str):
                result[key] = _resolve_vars(value, self._var_map)
            else:
                result[key] = value
        return result


class _NoemaPaths:
    _SECTION_MAP = {
        "db": "databases",
        "databases": "databases",
        "state": "state",
        "logs": "logs",
        "secrets": "secrets",
        "roots": "roots",
        "data_files": "data_files",
        "surface_subdirs": "surface_subdirs",
        "surface_files": "surface_files",
        "phase_data_subdirs": "phase_data_subdirs",
        "library_subdirs": "library_subdirs",
        "daemon_pids": "daemon_pids",
    }

    def __init__(self) -> None:
        self._raw: dict[str, Any] = {}
        self._var_map: dict[str, str] = {}
        self._accessor: _PathAccessor | None = None
        self._config_path: Path | None = None
        self._loaded = False
        self._using_fallback = False

    def _load(self) -> None:
        if self._loaded:
            return

        self._config_path = _find_config()
        loaded: dict[str, Any] | None = None
        if self._config_path is not None:
            try:
                candidate = json.loads(self._config_path.read_text(encoding="utf-8"))
                if isinstance(candidate, dict) and isinstance(candidate.get("roots"), dict):
                    loaded = candidate
            except (json.JSONDecodeError, OSError) as exc:
                log.warning("Cannot load NOEMA path configuration %s: %s", self._config_path, exc)

        if loaded is None:
            loaded = _default_config()
            self._using_fallback = True
            log.info("Using local NOEMA path fallback rooted at %s", loaded["roots"]["runtime"])

        self._raw = loaded
        roots = self._raw.get("roots", {})
        self._var_map = {
            str(key).lower(): _expand(str(value))
            for key, value in roots.items()
            if isinstance(value, (str, os.PathLike))
        }
        self._accessor = _PathAccessor(self._raw, self._var_map)
        self._loaded = True

    def resolve(self, template: str) -> str:
        self._load()
        return _resolve_vars(template, self._var_map)

    def surface_file(self, name: str) -> str:
        return str(Path(self.resolve("{surface}")) / name)

    def surface_subdir(self, name: str) -> str:
        return str(Path(self.resolve("{surface}")) / name) + os.sep

    def __getattr__(self, name: str) -> Any:
        self._load()
        key = name.lower()

        if key == "surface_file":
            return self.surface_file
        if key == "surface_subdir":
            return self.surface_subdir
        if key in self._var_map:
            return self._var_map[key]

        section_key = self._SECTION_MAP.get(key, key)
        if section_key in self._raw:
            value = self._raw[section_key]
            if isinstance(value, dict):
                return _PathAccessor(value, self._var_map, f"{section_key}.")
            return value

        if self._accessor is not None:
            try:
                return getattr(self._accessor, name)
            except AttributeError:
                pass

        raise AttributeError(
            f"NoemaPaths has no attribute {name!r}. "
            f"Available sections: {sorted(self._SECTION_MAP)}, roots: {sorted(self._var_map)}"
        )

    @property
    def config_path(self) -> Path | None:
        self._load()
        return self._config_path

    @property
    def using_fallback(self) -> bool:
        self._load()
        return self._using_fallback

    def dump(self) -> str:
        self._load()
        data = self._accessor.as_dict() if self._accessor else {}
        return json.dumps(data, indent=2, ensure_ascii=False)

    def reload(self) -> None:
        self._raw = {}
        self._var_map = {}
        self._accessor = None
        self._config_path = None
        self._loaded = False
        self._using_fallback = False
        self._load()


P = _NoemaPaths()

__all__ = ["P"]
