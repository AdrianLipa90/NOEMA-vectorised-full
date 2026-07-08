"""NOEMA Paths — single source of truth for all file paths.

Usage:
    from ciel_geometry.paths import P

    # Root directories
    P.MEMORY           # /home/adrian/new_volume_rw/CIEL_memories
    P.LIBRARY          # /home/adrian/new_volume_rw/NOEMA_LIBRARY
    P.PHASE_DATA       # /home/adrian/new_volume_rw/NOEMA_PHASE_DATA
    P.SURFACE          # /dev/shm/ciel_noema
    P.RESULTS          # .../CIEL_PROJECT_CANON/NOEMA/results
    P.MUMMU            # .../NOEMA_LIBRARY/mummu
    P.NEWS             # .../NOEMA_LIBRARY/news
    P.DZIENNIKI        # .../NOEMA_LIBRARY/dzienniki

    # Databases
    P.DB.TASKPLAN      # /tmp/noema_taskplan.db
    P.DB.KNOWLEDGE     # /tmp/noema_knowledge.db
    P.DB.MEMORIES_INDEX  # .../CIEL_memories/memories_index.db

    # State files
    P.STATE.ORCH_PKL   # .../state/ciel_orch_state.pkl
    P.STATE.HTRI_JSON  # .../state/htri_state.json

    # Logs
    P.LOGS.RAW_LOGS    # .../raw_logs
    P.LOGS.SUB_LOG     # .../logs/ciel_sub_log.jsonl

    # Secrets
    P.SECRETS.CIELAPI  # .../secrets/cielapi

    # Surface sub-files
    P.SURFACE_FILE("phi")        # /dev/shm/ciel_noema/phi
    P.SURFACE_FILE("analog")     # /dev/shm/ciel_noema/analog  (directory)
    P.SURFACE_SUBDIR("analog")   # /dev/shm/ciel_noema/analog/

    # Resolve with variable interpolation
    P.resolve("{memory}/local_test/.status.json")
    P.resolve("{surface}/tick")

Config file locations (in priority order):
    1. $NOEMA_PATHS environment variable
    2. ~/.config/noema/paths.json
    3. /home/adrian/new_volume_rw/NOEMA_LIBRARY/CONFIG/paths.json

This is the ONLY place where NOEMA data paths are defined.
Edit the config file to relocate all NOEMA data storage.
"""

from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import json
import os
import re
from pathlib import Path
from typing import Any


# ── Config file discovery ───────────────────────────────────────────────

def _find_config() -> Path:
    """Znajdź plik konfiguracyjny paths.json.

    Kolejność:
        1. $NOEMA_PATHS env var
        2. ~/.config/noema/paths.json
        3. Domyślna ścieżka na New Volume
    """
    env = os.environ.get("NOEMA_PATHS")
    if env:
        p = Path(env).expanduser()
        if p.exists():
            return p

    candidates = [
        Path.home() / ".config" / "noema" / "paths.json",
        Path("/home/adrian/new_volume_rw/NOEMA_LIBRARY/CONFIG/paths.json"),
    ]
    for c in candidates:
        if c.exists():
            return c
    # Fallback: zwróć domyślną ścieżkę nawet jeśli nie istnieje
    return candidates[-1]


# ── Loader ──────────────────────────────────────────────────────────────

_VAR_RE = re.compile(r'\{(\w+)\}')


def _resolve_vars(value: str, var_map: dict[str, str]) -> str:
    """Rozwiń {variable} referencje w stringu."""
    def _replace(m: re.Match) -> str:
        key = m.group(1).lower()
        if key in var_map:
            return var_map[key]
        return m.group(0)  # zostaw nierozwinięte
    return _VAR_RE.sub(_replace, value)


def _expand(value: str) -> str:
    """Rozwiń ~ i zmienne środowiskowe."""
    return os.path.expanduser(os.path.expandvars(value))


class _PathAccessor:
    """Hierarchiczny dostęp do ścieżek z słownika."""

    def __init__(self, data: dict[str, Any], var_map: dict[str, str], prefix: str = ""):
        self._data = data
        self._var_map = var_map
        self._prefix = prefix

    def __getattr__(self, name: str) -> Any:
        key = name.lower()
        # Sprawdź w bieżącym poziomie danych
        if key in self._data:
            val = self._data[key]
            if isinstance(val, dict):
                # Sprawdź czy to słownik z wartościami czy dalszy poziom
                # Jeśli żadna wartość nie jest dictem → to str, zrób accessor
                # Jeśli są dalsze dict → zrób zagnieżdżony accessor
                return _PathAccessor(val, self._var_map, f"{self._prefix}{key}.")
            if isinstance(val, str):
                # Rozwiń zmienne i ~
                resolved = _resolve_vars(val, self._var_map)
                resolved = _expand(resolved)
                return resolved
            return val
        raise AttributeError(f"Paths has no attribute '{name}' (section: {self._prefix or 'root'})")

    def __repr__(self) -> str:
        keys = [k for k in self._data.keys() if not k.startswith('_')]
        return f"<Paths [{', '.join(sorted(keys))}]>"

    def _get_dict(self) -> dict[str, Any]:
        """Zwraca płaski słownik rozwiniętych ścieżek."""
        result = {}
        for k, v in self._data.items():
            if k.startswith('_'):
                continue
            if isinstance(v, dict):
                sub = _PathAccessor(v, self._var_map, f"{self._prefix}{k}.")
                result[k] = sub._get_dict()
            elif isinstance(v, str):
                resolved = _resolve_vars(v, self._var_map)
                result[k] = _expand(resolved)
            else:
                result[k] = v
        return result


class _NoemaPaths:
    """Główny accessor ścieżek NOEMA.

    Użycie:
        from ciel_geometry.paths import P
        P.MEMORY
        P.DB.TASKPLAN
        P.STATE.ORCH_PKL
    """

    def __init__(self):
        self._raw: dict[str, Any] = {}
        self._var_map: dict[str, str] = {}
        self._accessor: _PathAccessor | None = None
        self._config_path: Path | None = None
        self._loaded = False

    def _load(self) -> None:
        """Załaduj konfigurację z pliku."""
        if self._loaded:
            return
        self._config_path = _find_config()
        if self._config_path.exists():
            try:
                self._raw = json.loads(self._config_path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/paths.py:174 quiet except scope=_NoemaPaths._load reason=assign_fallback")
                self._raw = {}
        else:
            self._raw = {}

        # Zbuduj mapę zmiennych z sekcji 'roots'
        roots = self._raw.get("roots", {})
        self._var_map = {}
        for k, v in roots.items():
            if isinstance(v, str):
                self._var_map[k.lower()] = _expand(v)

        # Dodaj też 'library' i 'memory' z roots
        # (już są w var_map przez pętlę wyżej)

        self._accessor = _PathAccessor(self._raw, self._var_map)
        self._loaded = True

    def surface_file(self, name: str) -> str:
        """Zwraca ścieżkę do pliku na powierzchni mmap.

        Args:
            name: nazwa pliku/podścieżki (bez '{surface}/')
        """
        return self.resolve(f"{{surface}}/{name}")

    def surface_subdir(self, name: str) -> str:
        """Zwraca ścieżkę do podkatalogu na powierzchni (z / na końcu)."""
        return self.resolve(f"{{surface}}/{name}") + "/"

    def resolve(self, template: str) -> str:
        """Rozwiń string ze zmiennymi {variable}.

        Zmienne pochodzą z sekcji 'roots' w paths.json.

        Args:
            template: string z {variable} referencjami

        Returns:
            Rozwinięta ścieżka absolutna
        """
        self._load()
        resolved = _resolve_vars(template, self._var_map)
        return _expand(resolved)

    def __getattr__(self, name: str) -> Any:
        self._load()
        key = name.lower()

        # 1. Sprawdź czy to alias roota (MEMORY → roots.memory)
        if key in self._var_map:
            return self._var_map[key]

        # 2. Sprawdź czy to nazwa sekcji (DB → databases, STATE → state)
        section_map = {
            "db": "databases",
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
        section_key = section_map.get(key, key)
        if section_key in self._raw:
            return _PathAccessor(self._raw[section_key], self._var_map, f"{section_key}.")

        # 3. Fallback: deleguj do accessora
        if self._accessor is not None:
            try:
                return getattr(self._accessor, name)
            except AttributeError:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/paths.py:249 quiet except scope=_NoemaPaths.__getattr__ reason=pass")
                pass

        raise AttributeError(
            f"NoemaPaths has no attribute '{name}'. "
            f"Available sections: {list(section_map.keys())}, "
            f"roots: {list(self._var_map.keys())}"
        )

    def __repr__(self) -> str:
        self._load()
        if self._accessor:
            return repr(self._accessor)
        return "<NoemaPaths (not loaded)>"

    @property
    def config_path(self) -> Path | None:
        """Ścieżka do używanego pliku konfiguracyjnego."""
        self._load()
        return self._config_path

    def dump(self) -> str:
        """Zwraca wszystkie rozwinięte ścieżki jako JSON string."""
        self._load()
        d = self._accessor._get_dict() if self._accessor else {}
        return json.dumps(d, indent=2, ensure_ascii=False)

    def reload(self) -> None:
        """Wymuś przeładowanie konfiguracji."""
        self._loaded = False
        self._load()


# ── Singleton ───────────────────────────────────────────────────────────

P = _NoemaPaths()

# ── Quick test ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"Config: {P.config_path}")
    print(f"Memory root: {P.MEMORY}")
    print(f"Library: {P.LIBRARY}")
    print(f"Phase data: {P.PHASE_DATA}")
    print(f"Surface: {P.SURFACE}")
    print(f"TaskPlan DB: {P.DB.TASKPLAN}")
    print(f"Knowledge DB: {P.DB.KNOWLEDGE}")
    print(f"Orch state: {P.STATE.ORCH_PKL}")
    print(f"Raw logs: {P.LOGS.RAW_LOGS}")
    print(f"Secrets: {P.SECRETS.CIELAPI}")
    print(f"Surface file 'tick': {P.surface_file('tick')}")
    print(f"Dump:\n{P.dump()}")
