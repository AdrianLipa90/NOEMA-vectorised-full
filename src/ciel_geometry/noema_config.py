"""Unified configuration for all NOEMA daemons.

Usage:
    from ciel_geometry.noema_config import config

    interval = config.kuramoto.interval
    dt = config.kuramoto.dt

A missing configuration file is an explicit clean-checkout condition and uses
compiled defaults.  An existing but unreadable or malformed file is *not*
missing state: it is a configuration-integrity failure and must stop startup.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path

from ciel_geometry.paths import P


class NoemaConfigError(RuntimeError):
    """Existing NOEMA configuration is unreadable, malformed, or inconsistent."""


@dataclass
class KuramotoConfig:
    interval: float = 0.2
    dt: float = 0.05
    continuous: bool = True
    cont_every: int = 10


@dataclass
class CielingoSyncConfig:
    interval: float = 60.0
    blend_min: float = 0.02
    blend_max: float = 0.12
    tau_min: float = 0.01
    tau_max: float = 1.0
    tau_default: float = 0.353


@dataclass
class NeutrinoConfig:
    interval: float = 1.0


@dataclass
class ResonanceBridgeConfig:
    interval: float = 1.0


@dataclass
class LinuxSensorConfig:
    interval: float = 1.0
    smoothing: float = 0.3


@dataclass
class PhaseNavConfig:
    interval: float = 1.0


@dataclass
class NonlocalProxyConfig:
    interval: float = 1.0


@dataclass
class SonicConfig:
    interval: float = 2.0


@dataclass
class ConsolidatorConfig:
    interval: int = 300
    batch: int = 5
    agent_port: int = 18520


@dataclass
class NoemaConfig:
    surface_root: str = "/dev/shm/ciel_noema"
    memory_root: str = P.MEMORY
    kuramoto: KuramotoConfig = field(default_factory=KuramotoConfig)
    cielingo_sync: CielingoSyncConfig = field(default_factory=CielingoSyncConfig)
    neutrino: NeutrinoConfig = field(default_factory=NeutrinoConfig)
    resonance_bridge: ResonanceBridgeConfig = field(default_factory=ResonanceBridgeConfig)
    linux_sensor: LinuxSensorConfig = field(default_factory=LinuxSensorConfig)
    phasenav: PhaseNavConfig = field(default_factory=PhaseNavConfig)
    nonlocal_proxy: NonlocalProxyConfig = field(default_factory=NonlocalProxyConfig)
    sonic: SonicConfig = field(default_factory=SonicConfig)
    consolidator: ConsolidatorConfig = field(default_factory=ConsolidatorConfig)


def _default_config_path() -> Path:
    return Path(os.environ.get(
        "NOEMA_CONFIG",
        str(Path(__file__).resolve().parent.parent.parent / "noema_config.json"),
    ))


def load_config(path: str | Path | None = None) -> NoemaConfig:
    p = Path(path) if path else _default_config_path()
    if not p.exists():
        return NoemaConfig()

    try:
        raw = json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        raise NoemaConfigError(f"existing NOEMA config cannot be loaded: {p}") from exc
    if not isinstance(raw, dict):
        raise NoemaConfigError(f"NOEMA config root must be an object: {p}")

    # Accept both the historical flat layout and v2's explicit sections.
    daemons = raw.get("daemons", {})
    system = raw.get("system", {})
    if not isinstance(daemons, dict):
        raise NoemaConfigError("NOEMA config 'daemons' section must be an object")
    if not isinstance(system, dict):
        raise NoemaConfigError("NOEMA config 'system' section must be an object")

    def _section(name: str) -> dict:
        value = raw.get(name, daemons.get(name, {}))
        if value is None:
            return {}
        if not isinstance(value, dict):
            raise NoemaConfigError(f"NOEMA config section {name!r} must be an object")
        return value

    def _merge(cfg_cls, data: dict):
        keys = {f.name for f in cfg_cls.__dataclass_fields__.values()}
        return cfg_cls(**{k: v for k, v in data.items() if k in keys})

    k = _section("kuramoto")
    ns = NoemaConfig(
        surface_root=raw.get("surface_root", system.get("surface_root", NoemaConfig.surface_root)),
        memory_root=raw.get("memory_root", system.get("memory_root", NoemaConfig.memory_root)),
        kuramoto=_merge(KuramotoConfig, k) if k else KuramotoConfig(),
        cielingo_sync=_merge(CielingoSyncConfig, _section("cielingo_sync")),
        neutrino=_merge(NeutrinoConfig, _section("neutrino")),
        resonance_bridge=_merge(ResonanceBridgeConfig, _section("resonance_bridge")),
        linux_sensor=_merge(LinuxSensorConfig, _section("linux_sensor")),
        phasenav=_merge(PhaseNavConfig, _section("phasenav")),
        nonlocal_proxy=_merge(NonlocalProxyConfig, _section("nonlocal_proxy")),
        sonic=_merge(SonicConfig, _section("sonic")),
        consolidator=_merge(ConsolidatorConfig, _section("consolidator")),
    )
    return ns


config = load_config()
