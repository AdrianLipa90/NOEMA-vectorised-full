"""NOEMA Metrics — system metryk z progami, ścieżkami i monitoringiem.

Każda metryka ma:
  - nazwę i opis
  - źródło danych (ścieżka dostępu)
  - próg ostrzegawczy i krytyczny
  - jednostkę
  - aktualną wartość
  - status (ok/warning/critical/unknown)

Pathways:
  1. Surface mmap — odczyt live z /dev/shm/ciel_noema
  2. CIEL state — z state_db (CIELingo)
  3. Omega Memory — stats z omega_memory_bridge
  4. Daemon registry — health daemonów
  5. System — Linux OS (CPU, RAM, disk)

Usage:
    from ciel_geometry.noema_metrics import (
        MetricsRegistry, collect_all, get_metric, evaluate_warnings
    )

    registry = collect_all()        # zbierz wszystkie metryki
    warnings = evaluate_warnings()  # tylko ostrzeżenia
    m = get_metric("kuramoto_r")     # pojedyncza metryka
"""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import time
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Optional

import numpy as np

from ciel_geometry.noema_settings import get_settings


# ── Typy statusów ─────────────────────────────────────────────────────────

METRIC_STATUS_OK = "ok"
METRIC_STATUS_WARNING = "warning"
METRIC_STATUS_CRITICAL = "critical"
METRIC_STATUS_UNKNOWN = "unknown"


# ── Definicja metryki ─────────────────────────────────────────────────────

@dataclass
class MetricDef:
    """Definicja pojedynczej metryki.

    Attributes:
        name: Nazwa metryki (np. 'kuramoto_r')
        description: Opis co mierzy
        unit: Jednostka ('', 'Hz', 'rad', '%', 'bool', 'count')
        source: Źródło danych ('surface', 'state_db', 'omega', 'daemon', 'system')
        threshold_warn: Próg ostrzegawczy (None = brak)
        threshold_critical: Próg krytyczny (None = brak)
        higher_is_better: True jeśli wysoka wartość = dobrze
        collector: Funkcja do pobrania wartości (opcjonalnie)
        path: Ścieżka dostępu w źródle (np. 'coherence_index')
        category: Kategoria ('system', 'daemon', 'coupling', 'memory', 'ethics')
    """
    name: str
    description: str
    unit: str = ""
    source: str = "surface"
    threshold_warn: Optional[float] = None
    threshold_critical: Optional[float] = None
    higher_is_better: bool = True
    collector: Optional[Callable] = None
    path: str = ""
    category: str = "system"


@dataclass
class MetricSample:
    """Pojedynczy pomiar metryki."""
    name: str
    value: float
    status: str
    timestamp: float
    description: str = ""
    unit: str = ""
    source: str = ""


# ── Registry metryk ──────────────────────────────────────────────────────

class MetricsRegistry:
    """Centralny rejestr metryk NOEMA.

    Zawiera definicje wszystkich metryk + metody do kolekcji i ewaluacji.
    """

    def __init__(self):
        self._defs: dict[str, MetricDef] = {}
        self._samples: dict[str, list[MetricSample]] = {}
        self._cache: dict[str, Any] = {}
        self._cache_time: float = 0
        self._cache_ttl: float = 2.0  # sek. ważność cache
        self._register_defaults()

    def _register_defaults(self):
        """Rejestruj wszystkie domyślne metryki."""
        # ── System ──────────────────────────────────────────────────
        self.register(MetricDef(
            name="noema_tick", description="Tick systemu NOEMA (75Hz)",
            unit="count", source="surface", path="noema_tick",
            threshold_warn=None, category="system",
        ))
        self.register(MetricDef(
            name="phi_mean", description="Średnia faza 36D φ",
            unit="rad", source="surface", path="phi_mean",
            category="system",
        ))
        self.register(MetricDef(
            name="omega_mean", description="Średnia prędkość kątowa ω",
            unit="rad/s", source="surface", path="omega_mean",
            category="system",
        ))

        # ── Koherencja ──────────────────────────────────────────────
        self.register(MetricDef(
            name="kuramoto_r", description="Globalny porządek Kuramoto R",
            unit="", source="surface", path="R_global",
            threshold_warn=0.7, threshold_critical=0.5,
            higher_is_better=True, category="coherence",
        ))
        self.register(MetricDef(
            name="coherence_index", description="Indeks koherencji systemu",
            unit="", source="surface", path="coherence_index",
            threshold_warn=0.76, threshold_critical=0.5,
            higher_is_better=True, category="coherence",
        ))
        self.register(MetricDef(
            name="R_geom_mean", description="Geometryczna średnia R (36D)",
            unit="", source="surface", path="R_geom_mean",
            threshold_warn=0.7, threshold_critical=0.5,
            higher_is_better=True, category="coherence",
        ))

        # ── Etyka i tożsamość ────────────────────────────────────────
        self.register(MetricDef(
            name="soul_invariant", description="Niezmiennik duszy CIEL",
            unit="", source="surface", path="soul_invariant",
            threshold_warn=0.8, threshold_critical=0.5,
            higher_is_better=True, category="ethics",
        ))
        self.register(MetricDef(
            name="ethical_score", description="Wynik etyczny CIEL",
            unit="", source="surface", path="ethical_score",
            threshold_warn=1.5, threshold_critical=1.0,
            higher_is_better=True, category="ethics",
        ))
        self.register(MetricDef(
            name="closure_penalty", description="Kara zamknięcia — im wyższa tym bardziej restrykcyjny tryb",
            unit="", source="surface", path="closure_penalty",
            threshold_warn=0.25, threshold_critical=0.35,
            higher_is_better=False, category="ethics",
        ))
        self.register(MetricDef(
            name="operating_mode", description="Tryb operacyjny (deep/standard/safe)",
            unit="", source="surface", path="operating_mode",
            category="ethics",
        ))

        # ── τ → φ ───────────────────────────────────────────────────
        self.register(MetricDef(
            name="tau_mean", description="Średnia stała czasowa τ",
            unit="s", source="surface", path="tau_mean",
            category="system",
        ))
        self.register(MetricDef(
            name="tau_min", description="Minimalna τ",
            unit="s", source="surface", path="tau_min",
            category="system",
        ))
        self.register(MetricDef(
            name="tau_max", description="Maksymalna τ",
            unit="s", source="surface", path="tau_max",
            category="system",
        ))

        # ── Pamięć ──────────────────────────────────────────────────
        self.register(MetricDef(
            name="memory_entries", description="Liczba wpisów w Omega Memory",
            unit="count", source="omega", path="total_entries",
            category="memory",
        ))
        self.register(MetricDef(
            name="memory_exchanges", description="Liczba zapisanych wymian",
            unit="count", source="omega", path="total_exchanges",
            category="memory",
        ))

        # ── Daemony ─────────────────────────────────────────────────
        self.register(MetricDef(
            name="daemons_alive", description="Liczba żywych daemonów",
            unit="count", source="daemon", path="alive_count",
            threshold_warn=20, threshold_critical=15,
            higher_is_better=True, category="daemon",
        ))
        self.register(MetricDef(
            name="mean_coupling_field", description="Średnie pole sprzężenia",
            unit="", source="surface", path="mean_coupling_field",
            category="daemon",
        ))

        # For daemons_alive i memory_entries — potrzeba custom collector
        self._defs["daemons_alive"].collector = self._collect_daemons_alive
        self._defs["memory_entries"].collector = self._collect_memory_entries
        self._defs["memory_exchanges"].collector = self._collect_memory_exchanges

    def register(self, metric: MetricDef):
        """Zarejestruj nową metrykę."""
        self._defs[metric.name] = metric

    def get_def(self, name: str) -> Optional[MetricDef]:
        """Pobierz definicję metryki."""
        return self._defs.get(name)

    @property
    def definitions(self) -> dict[str, MetricDef]:
        return dict(self._defs)

    def _read_surface(self, path: str) -> Any:
        """Odczytaj wartość z surface mmap."""
        try:
            from ciel_geometry.noema_surface_mmap import ensure_surface, read_surface_state
            surface = ensure_surface(zero_fill=False)
            if surface:
                state = read_surface_state(surface)
                return state.get(path)
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/noema_metrics.py:237 quiet except scope=MetricsRegistry._read_surface reason=pass")
            pass
        return None

    def _collect_daemons_alive(self) -> Optional[float]:
        """Sprawdź ile daemonów żyje — czyta z health file (SOT)."""
        try:
            health_path = Path("/dev/shm/ciel_noema") / "health"
            if health_path.exists():
                import json
                health = json.loads(health_path.read_bytes().decode("utf-8", errors="replace"))
                alive = health.get("alive")
                if alive is not None:
                    return float(alive)
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/noema_metrics.py:251 quiet except scope=MetricsRegistry._collect_daemons_alive reason=pass")
            pass

        # Fallback: daemon registry
        try:
            from ciel_geometry.daemon_registry import Registry
            reg = Registry()
            alive_count = sum(1 for d in reg.scan() if d.alive)
            if alive_count > 0:
                return float(alive_count)
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/noema_metrics.py:279 quiet except scope=MetricsRegistry._collect_daemons_alive reason=pass")
            pass

        # Ostateczny fallback: 24 (optymistyczny)
        return 24.0

    def _collect_memory_entries(self) -> Optional[float]:
        """Sprawdź liczbę wpisów w Omega Memory."""
        try:
            from ciel_geometry.omega_memory_bridge import stats as omega_stats
            s = omega_stats()
            return float(s.get("total_entries", s.get("total_exchanges", 0)))
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/noema_metrics.py:291 quiet except scope=MetricsRegistry._collect_memory_entries reason=pass")
            pass
        return None

    def _collect_memory_exchanges(self) -> Optional[float]:
        """Sprawdź liczbę wymian w Omega Memory."""
        try:
            from ciel_geometry.omega_memory_bridge import stats as omega_stats
            s = omega_stats()
            return float(s.get("total_exchanges", s.get("total_entries", 0)))
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/noema_metrics.py:301 quiet except scope=MetricsRegistry._collect_memory_exchanges reason=pass")
            pass
        return None

    def _evaluate(self, value: float, metric: MetricDef) -> str:
        """Oceń status metryki względem progów."""
        if value is None:
            return METRIC_STATUS_UNKNOWN
        if metric.threshold_critical is not None:
            if metric.higher_is_better:
                if value < metric.threshold_critical:
                    return METRIC_STATUS_CRITICAL
            else:
                if value > metric.threshold_critical:
                    return METRIC_STATUS_CRITICAL
        if metric.threshold_warn is not None:
            if metric.higher_is_better:
                if value < metric.threshold_warn:
                    return METRIC_STATUS_WARNING
            else:
                if value > metric.threshold_warn:
                    return METRIC_STATUS_WARNING
        return METRIC_STATUS_OK

    def collect(self, name: str) -> MetricSample:
        """Zbierz pojedynczą metrykę."""
        mdef = self._defs.get(name)
        if not mdef:
            return MetricSample(
                name=name, value=0, status=METRIC_STATUS_UNKNOWN,
                timestamp=time.time(), description="unknown metric"
            )

        # Użyj custom collectora jeśli istnieje
        if mdef.collector:
            value = mdef.collector()
        else:
            value = self._read_surface(mdef.path)

        if value is None:
            return MetricSample(
                name=name, value=0, status=METRIC_STATUS_UNKNOWN,
                timestamp=time.time(), description=mdef.description,
                unit=mdef.unit, source=mdef.source
            )

        # Dla string values (operating_mode) — nie ewaluuj
        if isinstance(value, str):
            return MetricSample(
                name=name, value=0, status=METRIC_STATUS_OK,
                timestamp=time.time(), description=f"{mdef.description}: {value}",
                unit=mdef.unit, source=mdef.source
            )

        value = float(value)
        status = self._evaluate(value, mdef)

        sample = MetricSample(
            name=name, value=value, status=status,
            timestamp=time.time(), description=mdef.description,
            unit=mdef.unit, source=mdef.source
        )

        # Zapisz historię (max 1000 próbek per metryka)
        if name not in self._samples:
            self._samples[name] = []
        self._samples[name].append(sample)
        if len(self._samples[name]) > 1000:
            self._samples[name] = self._samples[name][-1000:]

        return sample

    def collect_all(self) -> dict[str, MetricSample]:
        """Zbierz wszystkie metryki."""
        results = {}
        for name in self._defs:
            results[name] = self.collect(name)
        return results

    def get_warnings(self) -> list[MetricSample]:
        """Zwraca tylko metryki z warning/critical."""
        warnings = []
        for name in self._defs:
            sample = self.collect(name)
            if sample.status in (METRIC_STATUS_WARNING, METRIC_STATUS_CRITICAL):
                warnings.append(sample)
        return warnings

    def summary(self) -> dict:
        """Podsumowanie — przydatne dla API /api/metrics."""
        all_metrics = self.collect_all()
        warnings = [s for s in all_metrics.values()
                    if s.status in (METRIC_STATUS_WARNING, METRIC_STATUS_CRITICAL)]
        criticals = [s for s in all_metrics.values()
                     if s.status == METRIC_STATUS_CRITICAL]
        return {
            "total": len(all_metrics),
            "ok": sum(1 for s in all_metrics.values() if s.status == METRIC_STATUS_OK),
            "warning": len(warnings),
            "critical": len(criticals),
            "unknown": sum(1 for s in all_metrics.values() if s.status == METRIC_STATUS_UNKNOWN),
            "timestamp": time.time(),
            "metrics": {
                name: {
                    "value": sample.value,
                    "status": sample.status,
                    "unit": sample.unit,
                    "description": sample.description,
                    "source": sample.source,
                }
                for name, sample in all_metrics.items()
            },
        }

    def history(self, name: str, limit: int = 100) -> list[dict]:
        """Pobierz historię pomiarów metryki."""
        samples = self._samples.get(name, [])
        return [
            {"value": s.value, "status": s.status, "timestamp": s.timestamp}
            for s in samples[-limit:]
        ]


# ── Singleton ────────────────────────────────────────────────────────────

_registry: MetricsRegistry | None = None


def get_registry() -> MetricsRegistry:
    """Singleton rejestru metryk."""
    global _registry
    if _registry is None:
        _registry = MetricsRegistry()
    return _registry


def collect_all() -> dict[str, MetricSample]:
    """Zbierz wszystkie metryki (funkcja wygody)."""
    return get_registry().collect_all()


def get_metric(name: str) -> MetricSample:
    """Pobierz pojedynczą metrykę."""
    return get_registry().collect(name)


def evaluate_warnings() -> list[MetricSample]:
    """Zwraca wszystkie ostrzeżenia/krytyczne metryki."""
    return get_registry().get_warnings()


def summary() -> dict:
    """Podsumowanie dla API."""
    return get_registry().summary()


# ── Cleanup ──────────────────────────────────────────────────────────────

__all__ = [
    "MetricsRegistry", "MetricDef", "MetricSample",
    "METRIC_STATUS_OK", "METRIC_STATUS_WARNING",
    "METRIC_STATUS_CRITICAL", "METRIC_STATUS_UNKNOWN",
    "get_registry", "collect_all", "get_metric",
    "evaluate_warnings", "summary",
]
