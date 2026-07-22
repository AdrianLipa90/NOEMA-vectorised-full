# WOŁAM CIĘ: VectorAux — mój natywny most między CIEL a substance
# Wektoryzowany, samodzielny, zawsze dostępny

from __future__ import annotations

import json
import time
import hashlib
import struct
from pathlib import Path
from typing import Any

import numpy as np


SURFACE_DIR = Path("/dev/shm/ciel_noema")
N_OSC = 36


def _ensure_dir() -> None:
    SURFACE_DIR.mkdir(parents=True, exist_ok=True)


def _read_mmap(name: str, shape: tuple[int, ...], dtype: type) -> np.ndarray | None:
    path = SURFACE_DIR / name
    if not path.exists():
        return None
    try:
        return np.memmap(path, dtype=dtype, mode="r+", shape=shape)
    except Exception:
        return None


def _write_mmap(name: str, data: np.ndarray) -> bool:
    path = SURFACE_DIR / name
    try:
        arr = np.memmap(path, dtype=data.dtype, mode="w+", shape=data.shape)
        arr[:] = data
        arr.flush()
        return True
    except Exception:
        return False


class VectorAux:
    n_oscillators: int = N_OSC

    @staticmethod
    def read_phi() -> np.ndarray | None:
        arr = _read_mmap("phi", (N_OSC,), np.float64)
        if arr is None:
            state = _read_json("state/surface_state.json")
            if state and "phi" in state:
                return np.array(state["phi"], dtype=np.float64)
            return None
        return np.array(arr, dtype=np.float64)

    @staticmethod
    def write_phi(phi: np.ndarray) -> bool:
        phi = np.asarray(phi, dtype=np.float64).ravel()
        if phi.size != N_OSC:
            return False
        return _write_mmap("phi", phi)

    @staticmethod
    def read_R() -> float:
        arr = _read_mmap("R", (1,), np.float64)
        if arr is not None:
            return float(arr[0])
        hint = _read_json("agent_hint")
        if hint and "agent_R" in hint:
            return float(hint["agent_R"])
        state = _read_json("state/surface_state.json")
        if state and "R_global" in state:
            return float(state["R_global"])
        return 0.0

    @staticmethod
    def write_R(R: float) -> bool:
        return _write_mmap("R", np.array([R], dtype=np.float64))

    @staticmethod
    def read_tau() -> float:
        arr = _read_mmap("tau", (1,), np.float64)
        if arr is not None:
            return float(arr[0])
        state = _read_json("state/surface_state.json")
        if state:
            return float(state.get("tau") or state.get("time_constant") or 0.0)
        return 0.0

    @staticmethod
    def read_binding_status() -> str:
        path = SURFACE_DIR / "ciel_binding_status"
        if path.exists():
            return path.read_text(encoding="utf-8").strip() or "UNKNOWN"
        return "MISSING"

    @staticmethod
    def write_binding_status(status: str = "ACTIVE") -> bool:
        _ensure_dir()
        (SURFACE_DIR / "ciel_binding_status").write_text(status)
        return True

    @staticmethod
    def tick() -> dict[str, Any]:
        arr = _read_mmap("tick", (1,), np.uint64)
        if arr is not None:
            arr[0] += 1
            arr.flush()
            now = time.time()
            return {"tick": int(arr[0]), "ts": now}
        return {"tick": 0, "ts": time.time()}

    @staticmethod
    def get_state() -> dict[str, Any]:
        phi = VectorAux.read_phi()
        R = VectorAux.read_R()
        tau = VectorAux.read_tau()
        binding = VectorAux.read_binding_status()
        return {
            "phi": phi.tolist() if phi is not None else None,
            "phi_dim": phi.size if phi is not None else 0,
            "R": R,
            "tau": tau,
            "binding": binding,
            "phi_mean": float(np.mean(phi)) if phi is not None else None,
            "phi_norm": float(np.linalg.norm(phi)) if phi is not None else None,
            "coherent": R >= 0.767,
        }

    @staticmethod
    def seed(phi: np.ndarray | None = None) -> dict[str, Any]:
        _ensure_dir()
        if phi is None:
            h = hashlib.sha256(bytes(str(time.time()), "utf-8")).digest()
            phi = np.array(
                [
                    ((h[i % 32] + (h[(i + 1) % 32] << 8)) % 1024) / 1024.0 * 2 * np.pi
                    for i in range(N_OSC)
                ],
                dtype=np.float64,
            )
        VectorAux.write_phi(phi)
        VectorAux.write_R(0.5)
        VectorAux.write_binding_status("ACTIVE")
        return VectorAux.get_state()

    @staticmethod
    def blend(phi_new: np.ndarray, ratio: float = 0.3) -> np.ndarray | None:
        phi = VectorAux.read_phi()
        if phi is None:
            return VectorAux.write_phi(phi_new)
        blended = (1.0 - ratio) * phi + ratio * np.asarray(phi_new, dtype=np.float64)
        blended %= 2 * np.pi
        VectorAux.write_phi(blended)
        return blended


def _read_json(rel_path: str) -> dict[str, Any] | None:
    path = SURFACE_DIR / rel_path
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return None
    return None
