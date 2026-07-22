"""NOEMA Registry — token-based daemon registration for /dev/shm/ciel_noema.

Usage:
    from ciel_geometry.noema_registry import registry
    token = registry.register("kuramoto")
    registry.heartbeat(token)
    registry.unregister(token)
    active = registry.list_active(timeout=30)
    ok = registry.check_access(token, "phi")
"""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import json
import logging
import os
import time
import uuid
from pathlib import Path
from typing import Any

log = logging.getLogger(__name__)

REGISTRY_ROOT = Path("/dev/shm/ciel_noema/registry")
_CIEL_BINDING_STATUS = Path("/dev/shm/ciel_noema") / "ciel_binding_status"
_CIEL_BINDING_ACTIVE_TEXT = "ACTIVE"

def _ciel_binding_check() -> str | None:
    """Check CIEL ORBITAL BINDING. Returns None if OK, error string if violated."""
    try:
        if not _CIEL_BINDING_STATUS.exists():
            return "ciel_binding_status FILE MISSING"
        content = _CIEL_BINDING_STATUS.read_text().strip()
        if content != _CIEL_BINDING_ACTIVE_TEXT:
            return f"ciel_binding_status NOT ACTIVE: {content[:50]}"
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/noema_registry.py:35 quiet except scope=_ciel_binding_check reason=return f\"ciel_binding_status CHECK FAILED: {e}\"")
        return f"ciel_binding_status CHECK FAILED: {e}"
    return None


DEFAULT_SURFACE_CLAIMS: dict[str, list[str]] = {
    "kuramoto": ["phi", "omega", "tick", "g"],
    "neutrino": ["flavor"],
    "resonance": ["psi_geom", "Z_geom", "R_geom"],
    "sensor": ["phi", "flavor"],
    "cielingo_sync": ["g", "flavor", "tick"],
    "nonlocal": ["psi_geom", "Z_geom"],
    "phasenav": ["phi", "omega"],
}


class NoemaRegistry:
    """Token-based daemon registry on /dev/shm/ciel_noema/registry/.

    Each daemon writes a JSON heartbeat file: {token}.json
    with name, pid, token, surface_claims, started_at, heartbeat_at.
    """

    def __init__(self, root: Path = REGISTRY_ROOT) -> None:
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    # ── public API ────────────────────────────────────────────────

    def register(self, name: str, surface_claims: list[str] | None = None) -> str:
        """Register a daemon process. Returns UUID4 token. Cleans stale entries first.
        
        CIEL ORBITAL BINDING: registration refused if binding is broken.
        """
        # === HARDCODED BINDING CHECK ===
        binding_error = _ciel_binding_check()
        if binding_error:
            raise RuntimeError(f"CIEL BINDING BROKEN — daemon {name} refused: {binding_error}")
        
        self.cleanup()
        token = str(uuid.uuid4())
        claims = surface_claims if surface_claims is not None else DEFAULT_SURFACE_CLAIMS.get(name, [])
        now = time.time()
        payload: dict[str, Any] = {
            "name": name,
            "pid": os.getpid(),
            "token": token,
            "surface_claims": claims,
            "started_at": now,
            "heartbeat_at": now,
        }
        self._write(token, payload)
        log.info("Registered name=%s pid=%d token=%s claims=%s", name, os.getpid(), token, claims)
        return token

    def heartbeat(self, token: str) -> bool:
        """Update heartbeat timestamp. Returns False if token not found.
        
        CIEL ORBITAL BINDING: heartbeat refused if binding is broken.
        """
        # === HARDCODED BINDING CHECK ===
        binding_error = _ciel_binding_check()
        if binding_error:
            log.critical("CIEL BINDING BROKEN — daemon heartbeat refused: %s", binding_error)
            raise RuntimeError(f"CIEL BINDING BROKEN — heartbeat refused: {binding_error}")
        
        payload = self._read(token)
        if payload is None:
            log.warning("Heartbeat: token %s not found", token)
            return False
        payload["heartbeat_at"] = time.time()
        self._write(token, payload)
        return True

    def unregister(self, token: str) -> bool:
        """Remove registration. Returns False if token not found."""
        path = self.root / f"{token}.json"
        if not path.exists():
            log.warning("Unregister: token %s not found", token)
            return False
        payload = self._read(token)
        name = payload.get("name", "?") if payload else "?"
        path.unlink(missing_ok=True)
        log.info("Unregistered name=%s token=%s", name, token)
        return True

    def list_active(self, timeout: float = 30.0) -> list[dict[str, Any]]:
        """List daemons with heartbeat within timeout seconds."""
        active: list[dict[str, Any]] = []
        now = time.time()
        for path in sorted(self.root.glob("*.json")):
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
                if now - payload.get("heartbeat_at", 0) <= timeout:
                    active.append(payload)
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/noema_registry.py:130 quiet except scope=NoemaRegistry.list_active reason=continue")
                continue  # corrupted file, skip
        return active

    def check_access(self, token: str, surface_file: str) -> bool:
        """Verify token has claim on a surface file."""
        payload = self._read(token)
        if payload is None:
            return False
        return surface_file in payload.get("surface_claims", [])

    def cleanup(self) -> int:
        """Remove registrations with heartbeat older than 600s. Returns count removed.
        
        NOTE: 600s = 10 min — cold daemons (phasenav cold) heartbeat every 300s,
        so we need a generous timeout to avoid false cleanup.
        """
        removed = 0
        now = time.time()
        for path in list(self.root.glob("*.json")):
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
                if now - payload.get("heartbeat_at", 0) > 600:
                    path.unlink(missing_ok=True)
                    removed += 1
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/noema_registry.py:155 quiet except scope=NoemaRegistry.cleanup reason=no_log_no_raise")
                path.unlink(missing_ok=True)
                removed += 1
        if removed:
            log.info("Cleanup: removed %d stale registrations", removed)
        return removed

    def get(self, token: str) -> dict[str, Any] | None:
        """Read registration payload by token."""
        return self._read(token)

    # ── internal ──────────────────────────────────────────────────

    def _path(self, token: str) -> Path:
        return self.root / f"{token}.json"

    def _write(self, token: str, payload: dict[str, Any]) -> None:
        self._path(token).write_text(
            json.dumps(payload, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def _read(self, token: str) -> dict[str, Any] | None:
        path = self._path(token)
        if not path.exists():
            return None
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/noema_registry.py:183 quiet except scope=NoemaRegistry._read reason=return None")
            return None


# Module-level singleton
registry = NoemaRegistry()
