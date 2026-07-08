"""Unified configuration for all NOEMA daemons.

Usage:
    from ciel_geometry.noema_config import config

    interval = config.kuramoto.interval
    dt = config.kuramoto.dt
"""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import json
import os
from dataclasses import dataclass, field
from pathlib import Path

from ciel_geometry.paths import P


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
        raw = json.loads(p.read_text())
    except (json.JSONDecodeError, OSError):
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/noema_config.py:103 quiet except scope=load_config reason=return NoemaConfig()")
        return NoemaConfig()

    def _merge(cfg_cls, data: dict):
        keys = {f.name for f in cfg_cls.__dataclass_fields__.values()}
        return cfg_cls(**{k: v for k, v in data.items() if k in keys})

    k = raw.get("kuramoto", {})
    ns = NoemaConfig(
        surface_root=raw.get("surface_root", NoemaConfig.surface_root),
        memory_root=raw.get("memory_root", NoemaConfig.memory_root),
        kuramoto=_merge(KuramotoConfig, k) if k else KuramotoConfig(),
        cielingo_sync=_merge(CielingoSyncConfig, raw.get("cielingo_sync", {})),
        neutrino=_merge(NeutrinoConfig, raw.get("neutrino", {})),
        resonance_bridge=_merge(ResonanceBridgeConfig, raw.get("resonance_bridge", {})),
        linux_sensor=_merge(LinuxSensorConfig, raw.get("linux_sensor", {})),
        phasenav=_merge(PhaseNavConfig, raw.get("phasenav", {})),
        nonlocal_proxy=_merge(NonlocalProxyConfig, raw.get("nonlocal_proxy", {})),
        sonic=_merge(SonicConfig, raw.get("sonic", {})),
        consolidator=_merge(ConsolidatorConfig, raw.get("consolidator", {})),
    )
    return ns


config = load_config()
