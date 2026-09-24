"""NOEMA Settings — hierarchiczny system konfiguracji z walidacją.

Zastępuje rozproszone noema_config.py, ciel_config.py i inne ad-hoc configi.
Jeden punkt prawdy dla wszystkich ustawień NOEMY.

Usage:
    from ciel_geometry.noema_settings import load, validate, dump, NOEMA_DEFAULTS

    settings = load()                    # z domyślnej ścieżki (noema_config.json)
    settings = load("/path/to/config.json")
    errors = validate(settings)          # lista błędów walidacji
    as_json = dump(settings)             # do zapisu

    # Dostęp:
    settings.system.surface_root
    settings.daemons.kuramoto.interval
    settings.coupling.cielingo_enabled
    settings.metrics.kuramoto_r_threshold
"""
from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field, fields, asdict
from pathlib import Path
from typing import Any, Optional

from ciel_geometry.paths import P


# ── Pomocnicze ───────────────────────────────────────────────────────────

def _path(s: str) -> str:
    """Rozwijaj ~ i zmienne środowiskowe w ścieżkach."""
    return os.path.expandvars(os.path.expanduser(s))


def _library_subdir(name: str) -> str:
    """Buduj domyślną podścieżkę w NOEMA_LIBRARY bez polegania na nieistniejących sekcjach paths.json."""
    return str(Path(P.LIBRARY) / name)


_PATH_RE = re.compile(r'^[\w/.\-~$@{}]+$')
_PORT_RE = re.compile(r'^\d{1,5}$')
_FLOAT_RE = re.compile(r'^-?\d+(\.\d+)?$')


# ── Sekcje ustawień ──────────────────────────────────────────────────────

@dataclass
class PathsConfig:
    """Ścieżki systemowe NOEMA — domyślne z centralnego paths.json."""
    surface_root: str = "/dev/shm/ciel_noema"
    memory_root: str = P.MEMORY
    noema_library: str = P.LIBRARY
    # `paths.json` nie gwarantuje sekcji `library_subdirs`, więc domyślnie
    # składamy ścieżki bezpośrednio z `P.LIBRARY`.
    agent_db: str = _library_subdir("agent_db")
    db_root: str = _library_subdir("DB")
    state_root: str = _library_subdir("STATE")
    logs_root: str = _library_subdir("LOGS")
    cards_root: str = _library_subdir("CARDS")
    memories_root: str = _library_subdir("MEMORIES")
    fallback_tmp: str = "/tmp"
    site_root: str = ""  # puste = domyślne (NOEMA_ROOT/site)


@dataclass
class KuramotoConfig:
    """Ustawienia daemona Kuramoto — synchronizacja oscylatorów 36D."""
    interval: float = 0.2        # sek. między krokami
    dt: float = 0.05             # krok całkowania (τ)
    continuous: bool = True      # propagacja ciągła
    cont_every: int = 10         # co ile ticków propagacja ciągła
    harmonic_3: float = 1.0      # wzmocnienie harmonicznej 3
    harmonic_6: float = 0.5      # wzmocnienie harmonicznej 6
    harmonic_9: float = 0.25     # wzmocnienie harmonicznej 9
    coupling_strength: float = 1.0  # siła sprzężenia między M-grupami


@dataclass
class CielingoSyncConfig:
    """Synchronizacja CIELingo ↔ surface NOEMA."""
    interval: float = 60.0       # sek. między synchronizacjami
    blend_min: float = 0.02      # minimalna mieszanka CIEL→NOEMA
    blend_max: float = 0.12      # maksymalna mieszanka
    tau_min: float = 0.01        # minimalna stała czasowa τ
    tau_max: float = 1.0         # maksymalna stała czasowa τ
    tau_default: float = 0.353   # domyślne τ


@dataclass
class PhaseNavConfig:
    """Ustawienia PhaseNav — hot & cold."""
    interval: float = 1.0        # sek. między krokami
    hot_temp: float = 0.9        # temperatura hot (szybkie)
    cold_temp: float = 0.15      # temperatura cold (głębokie)
    hot_steps: int = 1           # kroki PhaseNav hot
    cold_steps: int = 30         # kroki PhaseNav cold


@dataclass
class NeutrinoConfig:
    """Daemon neutrino — wewnętrzna komunikacja."""
    interval: float = 1.0
    queue_max: int = 1000
    ttl: float = 30.0            # sek. ważności wiadomości


@dataclass
class ResonanceBridgeConfig:
    """Most rezonansowy rzeczywisto-wyobrażeniowy."""
    interval: float = 1.0
    mix_ratio: float = 0.5       # stosunek real/imag


@dataclass
class LinuxSensorConfig:
    """Sensory systemu Linux (temperatury, obciążenie, itp.)."""
    interval: float = 1.0
    smoothing: float = 0.3       # wygładzanie wykładnicze
    cpu_enabled: bool = True
    disk_enabled: bool = True
    net_enabled: bool = True
    temp_enabled: bool = True
    proc_enabled: bool = True


@dataclass
class NonlocalProxyConfig:
    """Proxy nielokalne — przekazywanie między NOEMA a hostem."""
    interval: float = 1.0
    host_port: int = 18200
    enabled: bool = True


@dataclass
class SonicConfig:
    """Diagnostyka soniczna (częstotliwości, rezonanse)."""
    interval: float = 2.0
    freq_min: float = 0.1
    freq_max: float = 100.0
    bins: int = 64


@dataclass
class ConsolidatorConfig:
    """Konsolidacja pamięci — batch zapisów do TieredMemory."""
    interval: int = 300          # sek. między konsolidacjami
    batch: int = 5               # max batch size
    agent_port: int = 18520
    max_age_minutes: int = 60    # max wiek niezakonsolidowanych


@dataclass
class PortalConfig:
    """Ustawienia portalu NOEMA (localhost:18888)."""
    port: int = 18888
    host: str = "localhost"
    ssl: bool = False
    static_dir: str = "site"
    cors_origin: str = "*"


@dataclass
class CouplingConfig:
    """Ustawienia huba CIEL Coupling."""
    cielingo_enabled: bool = True
    omega_memory_enabled: bool = True
    state_db_enabled: bool = True
    ternary_enabled: bool = True
    max_frame_length: int = 10000
    default_ternary_method: str = "delta_phi_vote"
    writing_logger_enabled: bool = True


@dataclass
class MetricsConfig:
    """Progi i konfiguracja systemu metryk."""
    kuramoto_r_threshold: float = 0.7     # poniżej = warning
    coherence_threshold: float = 0.76     # poniżej = warning
    closure_penalty_warn: float = 0.25    # powyżej = attention
    closure_penalty_critical: float = 0.35  # powyżej = critical
    ethical_score_warn: float = 1.5       # poniżej = warning
    soul_invariant_warn: float = 0.8      # poniżej = warning
    daemon_alive_warn: int = 20           # poniżej = warning
    tick_stall_warn: int = 60             # sek. bez ticka = warning
    surface_read_timeout: float = 2.0     # sek. timeout reada
    log_retention_days: int = 30
    metric_history_minutes: int = 60


@dataclass
class DaemonsConfig:
    """Agregacja daemonów — wszystkie konfigi w jednym miejscu."""
    kuramoto: KuramotoConfig = field(default_factory=KuramotoConfig)
    cielingo_sync: CielingoSyncConfig = field(default_factory=CielingoSyncConfig)
    phasenav: PhaseNavConfig = field(default_factory=PhaseNavConfig)
    neutrino: NeutrinoConfig = field(default_factory=NeutrinoConfig)
    resonance_bridge: ResonanceBridgeConfig = field(default_factory=ResonanceBridgeConfig)
    linux_sensor: LinuxSensorConfig = field(default_factory=LinuxSensorConfig)
    nonlocal_proxy: NonlocalProxyConfig = field(default_factory=NonlocalProxyConfig)
    sonic: SonicConfig = field(default_factory=SonicConfig)
    consolidator: ConsolidatorConfig = field(default_factory=ConsolidatorConfig)


# ── Główna struktura ─────────────────────────────────────────────────────

@dataclass
class NoemaSettings:
    """Kompletne ustawienia NOEMY — jeden punkt prawdy.

    Struktura:
        version         — wersja schematu
        system          — ścieżki, root
        daemons         — wszystkie daemony
        coupling        — hub CIEL Coupling
        portal          — web UI
        metrics         — progi i monitoring
    """
    version: str = "2.0"
    system: PathsConfig = field(default_factory=PathsConfig)
    daemons: DaemonsConfig = field(default_factory=DaemonsConfig)
    coupling: CouplingConfig = field(default_factory=CouplingConfig)
    portal: PortalConfig = field(default_factory=PortalConfig)
    metrics: MetricsConfig = field(default_factory=MetricsConfig)


# ── Domyślne ustawienia (singleton) ──────────────────────────────────────

NOEMA_DEFAULTS = NoemaSettings()

# ── Walidacja ────────────────────────────────────────────────────────────

def validate(settings: NoemaSettings) -> list[str]:
    """Waliduj ustawienia, zwraca listę błędów."""
    errors: list[str] = []

    # System paths
    p = settings.system
    if not p.surface_root or not isinstance(p.surface_root, str):
        errors.append("system.surface_root: wymagany string")
    if p.fallback_tmp and not os.path.isabs(os.path.expanduser(p.fallback_tmp)):
        errors.append(f"system.fallback_tmp: ścieżka bezwzględna, dostałem '{p.fallback_tmp}'")

    # Daemon intervals — muszą być dodatnie
    for daemon_name, cfg in [
        ("kuramoto", settings.daemons.kuramoto),
        ("cielingo_sync", settings.daemons.cielingo_sync),
        ("phasenav", settings.daemons.phasenav),
        ("neutrino", settings.daemons.neutrino),
        ("resonance_bridge", settings.daemons.resonance_bridge),
        ("linux_sensor", settings.daemons.linux_sensor),
        ("nonlocal_proxy", settings.daemons.nonlocal_proxy),
        ("sonic", settings.daemons.sonic),
        ("consolidator", settings.daemons.consolidator),
    ]:
        interval = getattr(cfg, "interval", None)
        if interval is not None and interval <= 0:
            errors.append(f"daemons.{daemon_name}.interval: musi być > 0, dostałem {interval}")

    # Kuramoto specifics
    k = settings.daemons.kuramoto
    if k.dt <= 0 or k.dt >= 1:
        errors.append(f"daemons.kuramoto.dt: musi być w (0,1), dostałem {k.dt}")
    if k.cont_every < 1:
        errors.append(f"daemons.kuramoto.cont_every: musi być >= 1, dostałem {k.cont_every}")

    # Coupling
    c = settings.coupling
    if c.max_frame_length < 100:
        errors.append(f"coupling.max_frame_length: musi być >= 100, dostałem {c.max_frame_length}")

    # Portal port
    port = settings.portal.port
    if port < 1024 or port > 65535:
        errors.append(f"portal.port: musi być 1024-65535, dostałem {port}")

    # Metrics thresholds
    m = settings.metrics
    if not 0 < m.kuramoto_r_threshold <= 1:
        errors.append(f"metrics.kuramoto_r_threshold: musi być w (0,1], dostałem {m.kuramoto_r_threshold}")
    if not 0 < m.coherence_threshold <= 1:
        errors.append(f"metrics.coherence_threshold: musi być w (0,1], dostałem {m.coherence_threshold}")
    if m.closure_penalty_warn >= m.closure_penalty_critical:
        errors.append(f"metrics.closure_penalty_warn ({m.closure_penalty_warn}) musi być < critical ({m.closure_penalty_critical})")
    if m.tick_stall_warn < 1:
        errors.append(f"metrics.tick_stall_warn: musi być >= 1, dostałem {m.tick_stall_warn}")

    return errors


# ── Ładowanie i zapis ────────────────────────────────────────────────────

def _default_config_path() -> Path:
    """Ścieżka do domyślnego pliku konfiguracyjnego."""
    env = os.environ.get("NOEMA_CONFIG")
    if env:
        return Path(env)
    # relative to this file: NOEMA_ROOT/noema_config.json
    return Path(__file__).resolve().parent.parent.parent / "noema_config.json"


def _deep_merge(target: dict, source: dict) -> dict:
    """Rekurencyjne scalanie dictów (source→target)."""
    for k, v in source.items():
        if k in target and isinstance(target[k], dict) and isinstance(v, dict):
            _deep_merge(target[k], v)
        else:
            target[k] = v
    return target


def _resolve_type(t: Any, _globals: dict | None = None) -> type:
    """Rozwiąż typ — jeśli string (z __future__ annotations), znajdź w globals."""
    if isinstance(t, str):
        g = _globals or globals()
        # Obsłuż Optional[X], List[X] itp.
        if t.startswith("Optional[") and t.endswith("]"):
            return _resolve_type(t[9:-1], g)
        if t.startswith("List[") and t.endswith("]"):
            return list
        if t.startswith("dict[") or t.startswith("Dict["):
            return dict
        if t in g:
            return g[t]
        # Próbuj w __builtins__
        import builtins
        if t in dir(builtins):
            return getattr(builtins, t)
        return object
    return t


def _from_dict(cls: type, data: dict) -> Any:
    """Rekurencyjna deserializacja z dict → dataclass."""
    cls = _resolve_type(cls)
    if not hasattr(cls, "__dataclass_fields__"):
        return data
    field_defs = {f.name: f for f in fields(cls)}
    kwargs = {}
    for fname, fdef in field_defs.items():
        if fname in data:
            val = data[fname]
            ftype = _resolve_type(fdef.type)
            # Próbuj rekurencyjnie
            if hasattr(ftype, "__dataclass_fields__") and isinstance(val, dict):
                kwargs[fname] = _from_dict(ftype, val)
            elif hasattr(ftype, "__origin__") and ftype.__origin__ is list and isinstance(val, list):
                kwargs[fname] = val
            else:
                kwargs[fname] = val
        # else: użyj domyślnego
    return cls(**kwargs)


def _to_dict(obj: Any) -> dict:
    """Rekurencyjna serializacja dataclass → dict."""
    if hasattr(obj, "__dataclass_fields__"):
        return {f.name: _to_dict(getattr(obj, f.name)) for f in fields(obj)}
    elif isinstance(obj, dict):
        return {k: _to_dict(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_to_dict(v) for v in obj]
    return obj


def load(path: str | Path | None = None) -> NoemaSettings:
    """Wczytaj ustawienia z pliku JSON.

    Args:
        path: Ścieżka do pliku JSON. Jeśli None, używa NOEMA_CONFIG env
              lub domyślnej ścieżki.

    Returns:
        NoemaSettings z scalonymi ustawieniami.
    """
    p = Path(path) if path else _default_config_path()

    if not p.exists():
        return NoemaSettings()

    try:
        raw = json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        import warnings
        warnings.warn(f"Cannot load config from {p}: {e}")
        return NoemaSettings()

    # Wersja 1.x → 2.0 migracja
    if "version" not in raw or raw.get("version", "1.0").startswith("1."):
        raw = _migrate_v1_to_v2(raw)

    settings = _from_dict(NoemaSettings, raw)

    # Rozwijaj ścieżki (~, ${VAR})
    for path_field in ["surface_root", "memory_root", "noema_library",
                        "agent_db", "db_root", "state_root", "logs_root",
                        "cards_root", "memories_root", "fallback_tmp", "site_root"]:
        val = getattr(settings.system, path_field, None)
        if val:
            setattr(settings.system, path_field, _path(val))

    return settings


def _migrate_v1_to_v2(raw: dict) -> dict:
    """Migracja z formatu v1 (noema_config.py) do v2 (NoemaSettings)."""
    v2: dict = {"version": "2.0", "system": {}, "daemons": {}, "coupling": {}, "portal": {}, "metrics": {}}

    # System paths
    if "surface_root" in raw:
        v2["system"]["surface_root"] = raw["surface_root"]
    if "memory_root" in raw:
        v2["system"]["memory_root"] = raw["memory_root"]
    if "noema_library" in raw:
        v2["system"]["noema_library"] = raw["noema_library"]
    if "paths" in raw:
        v2["system"] = {**v2["system"], **raw["paths"]}

    # Daemon configs — mapowanie sekcji
    daemon_map = {
        "kuramoto": "kuramoto",
        "cielingo_sync": "cielingo_sync",
        "neutrino": "neutrino",
        "resonance_bridge": "resonance_bridge",
        "linux_sensor": "linux_sensor",
        "phasenav": "phasenav",
        "nonlocal_proxy": "nonlocal_proxy",
        "sonic": "sonic",
        "consolidator": "consolidator",
    }
    for old_key, new_key in daemon_map.items():
        if old_key in raw:
            v2["daemons"][new_key] = raw[old_key]

    return v2


def dump(settings: NoemaSettings, indent: int = 2) -> str:
    """Serializuj ustawienia do JSON string."""
    return json.dumps(_to_dict(settings), indent=indent, ensure_ascii=False)


def save(settings: NoemaSettings, path: str | Path | None = None) -> None:
    """Zapisz ustawienia do pliku JSON."""
    p = Path(path) if path else _default_config_path()
    p.write_text(dump(settings), encoding="utf-8")


# ── Quick access ─────────────────────────────────────────────────────────

_settings_cache: NoemaSettings | None = None


def get_settings(force_reload: bool = False) -> NoemaSettings:
    """Singleton z lazy loading + cache."""
    global _settings_cache
    if _settings_cache is None or force_reload:
        _settings_cache = load()
    return _settings_cache


__all__ = [
    "NoemaSettings", "NOEMA_DEFAULTS",
    "PathsConfig", "DaemonsConfig", "CouplingConfig",
    "PortalConfig", "MetricsConfig",
    "KuramotoConfig", "CielingoSyncConfig", "PhaseNavConfig",
    "NeutrinoConfig", "ResonanceBridgeConfig", "LinuxSensorConfig",
    "NonlocalProxyConfig", "SonicConfig", "ConsolidatorConfig",
    "load", "dump", "save", "validate", "get_settings",
]
