#!/usr/bin/env python3
"""Deterministic fail-loud migration for NOEMA critical continuity paths.

This tool intentionally patches only audited source snippets.  Every exact
replacement must match once; drift aborts the migration instead of guessing.
It is designed for the audit/fail-loud-critical-state-20260821 branch.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class PatchDrift(RuntimeError):
    pass


def replace_once(path: Path, old: str, new: str, label: str) -> None:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise PatchDrift(f"{label}: expected exactly one source match in {path}, got {count}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def rewrite_section_quiet_passes(path: Path, start: str, end: str, label: str) -> int:
    text = path.read_text(encoding="utf-8")
    a = text.find(start)
    b = text.find(end, a + len(start))
    if a < 0 or b < 0:
        raise PatchDrift(f"{label}: section markers not found")
    section = text[a:b]
    pattern = re.compile(
        r'(?P<indent>^[ ]*)except Exception:\n'
        r'(?P=indent)    _NOEMA_QUIET_EXCEPT_LOGGER\.exception\([^\n]*\)\n'
        r'(?P=indent)    (?P<action>pass|return)\n',
        re.MULTILINE,
    )
    section_new, count = pattern.subn(
        lambda m: f"{m.group('indent')}except Exception:\n{m.group('indent')}    raise\n",
        section,
    )
    if count == 0:
        raise PatchDrift(f"{label}: expected at least one quiet pass/return")
    path.write_text(text[:a] + section_new + text[b:], encoding="utf-8")
    return count


def patch_surface() -> None:
    path = ROOT / "src/ciel_geometry/noema_surface_mmap.py"

    replace_once(
        path,
        '''try:\n    from .noema_config import config as _noema_cfg\n    _CFG_SURFACE_ROOT = _noema_cfg.surface_root\nexcept Exception:\n    _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/noema_surface_mmap.py:43 quiet except scope=<module> reason=assign_fallback")\n    _CFG_SURFACE_ROOT = "/dev/shm/ciel_noema"\n''',
        '''from .noema_config import config as _noema_cfg\n_CFG_SURFACE_ROOT = _noema_cfg.surface_root\n\n\nclass SurfaceStateIntegrityError(RuntimeError):\n    """Existing NOEMA surface state cannot be restored without mutation."""\n\n''',
        "surface.config_import",
    )

    replace_once(
        path,
        '''        try:\n            from .phasenav.continuous_propagator import evolve_continuous\n            phi_new, _, _ = evolve_continuous(\n                phi, dt=dt * cont_every, hbar=0.1,\n                coupling=coupling, omega_eff=effective_omega,\n            )\n        except Exception:\n            _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/noema_surface_mmap.py:1091 quiet except scope=evolve_surface reason=assign_fallback")\n            phi_new = (phi + dt * (effective_omega + coupling)) % (2.0 * np.pi)\n''',
        '''        try:\n            from .phasenav.continuous_propagator import evolve_continuous\n            phi_new, _, _ = evolve_continuous(\n                phi, dt=dt * cont_every, hbar=0.1,\n                coupling=coupling, omega_eff=effective_omega,\n            )\n        except Exception as exc:\n            raise RuntimeError("continuous PhaseNav propagation failed; refusing silent Kuramoto substitution") from exc\n''',
        "surface.continuous_propagator",
    )

    replace_once(
        path,
        '''    try:\n        from .phasenav.operator_algebra import surface_holonomy\n        surf_gamma, winding = surface_holonomy(phi)\n    except Exception:\n        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/noema_surface_mmap.py:1337 quiet except scope=sync_surface_holonomy reason=assign_fallback")\n        surf_gamma, winding = 0.0, 0\n''',
        '''    try:\n        from .phasenav.operator_algebra import surface_holonomy\n        surf_gamma, winding = surface_holonomy(phi)\n    except Exception as exc:\n        raise RuntimeError("surface holonomy failed; refusing synthetic zero holonomy") from exc\n''',
        "surface.holonomy",
    )

    replace_once(
        path,
        '''    path = root / "ciel_state.json"\n    if not path.exists():\n        return {}\n    try:\n        with open(path) as f:\n            return dict(json.load(f))\n    except (OSError, json.JSONDecodeError):\n        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/noema_surface_mmap.py:1209 quiet except scope=read_ciel_internal_state reason=return {}")\n        return {}\n''',
        '''    path = root / "ciel_state.json"\n    if not path.exists():\n        return {}\n    try:\n        with open(path, encoding="utf-8") as f:\n            raw = json.load(f)\n    except (OSError, json.JSONDecodeError) as exc:\n        raise SurfaceStateIntegrityError(f"existing CIEL state cannot be restored: {path}") from exc\n    if not isinstance(raw, dict):\n        raise SurfaceStateIntegrityError(f"CIEL state root must be an object: {path}")\n    return dict(raw)\n''',
        "surface.ciel_state_read",
    )

    replace_once(
        path,
        '''def ensure_surface(root: Path = DEFAULT_SURFACE_ROOT, *, zero_fill: bool = False) -> dict[str, np.memmap]:\n    root.mkdir(parents=True, exist_ok=True)\n    surface: dict[str, np.memmap] = {}\n    for spec in surface_specs():\n        path = _surface_path(root, spec)\n        if not path.exists() or path.stat().st_size != spec.nbytes:\n            with path.open("wb") as handle:\n                handle.truncate(spec.nbytes)\n        for _attempt in range(3):\n            try:\n                mem = np.memmap(path, dtype=spec.dtype, mode="r+", shape=spec.shape)\n                break\n            except (ValueError, OSError):\n                _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/noema_surface_mmap.py:1229 quiet except scope=ensure_surface reason=With")\n                with path.open("wb") as handle:\n                    handle.truncate(spec.nbytes)\n        else:\n            raise RuntimeError(f"cannot mmap {path} after 3 attempts")\n        if zero_fill:\n            mem[...] = 0\n            mem.flush()\n        surface[spec.name] = mem\n    return surface\n\n\ndef open_surface(root: Path = DEFAULT_SURFACE_ROOT, mode: str = "r+") -> dict[str, np.memmap]:\n    surface: dict[str, np.memmap] = {}\n    for spec in surface_specs():\n        path = _surface_path(root, spec)\n        if not path.exists():\n            raise FileNotFoundError(path)\n        for _attempt in range(3):\n            try:\n                surface[spec.name] = np.memmap(path, dtype=spec.dtype, mode=mode, shape=spec.shape)\n                break\n            except (ValueError, OSError):\n                _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/noema_surface_mmap.py:1251 quiet except scope=open_surface reason=With")\n                with path.open("wb") as handle:\n                    handle.truncate(spec.nbytes)\n        else:\n            raise RuntimeError(f"cannot mmap {path} after 3 attempts")\n    return surface\n''',
        '''def ensure_surface(root: Path = DEFAULT_SURFACE_ROOT, *, zero_fill: bool = False) -> dict[str, np.memmap]:\n    root.mkdir(parents=True, exist_ok=True)\n    surface: dict[str, np.memmap] = {}\n    for spec in surface_specs():\n        path = _surface_path(root, spec)\n        if not path.exists():\n            with path.open("xb") as handle:\n                handle.truncate(spec.nbytes)\n        else:\n            actual = path.stat().st_size\n            if actual != spec.nbytes:\n                raise SurfaceStateIntegrityError(\n                    f"surface field size mismatch for {path}: {actual} != {spec.nbytes}; refusing truncate"\n                )\n        try:\n            mem = np.memmap(path, dtype=spec.dtype, mode="r+", shape=spec.shape)\n        except (ValueError, OSError) as exc:\n            raise SurfaceStateIntegrityError(f"cannot mmap existing surface field without mutation: {path}") from exc\n        if zero_fill:\n            mem[...] = 0\n            mem.flush()\n        surface[spec.name] = mem\n    return surface\n\n\ndef open_surface(root: Path = DEFAULT_SURFACE_ROOT, mode: str = "r+") -> dict[str, np.memmap]:\n    surface: dict[str, np.memmap] = {}\n    for spec in surface_specs():\n        path = _surface_path(root, spec)\n        if not path.exists():\n            raise FileNotFoundError(path)\n        actual = path.stat().st_size\n        if actual != spec.nbytes:\n            raise SurfaceStateIntegrityError(\n                f"surface field size mismatch for {path}: {actual} != {spec.nbytes}; refusing truncate"\n            )\n        try:\n            surface[spec.name] = np.memmap(path, dtype=spec.dtype, mode=mode, shape=spec.shape)\n        except (ValueError, OSError) as exc:\n            raise SurfaceStateIntegrityError(f"cannot mmap existing surface field without mutation: {path}") from exc\n    return surface\n''',
        "surface.mmap_integrity",
    )

    replace_once(
        path,
        '''    if _prev_path.exists():\n        try:\n            _existing_cache = json.loads(_prev_path.read_text("utf-8"))\n        except Exception:\n            pass\n    # Fallback do live z surface mmap jeśli cache nie istnieje\n    if not _existing_cache.get("closure_penalty_raw"):\n        try:\n            _surface_live = read_surface_state(surface)\n            _existing_cache = {\n                "coherence_index": _surface_live.get("coherence_index"),\n                "soul_invariant": _surface_live.get("soul_invariant"),\n                "ethical_score": _surface_live.get("ethical_score"),\n                "mood_normalized": None,\n                "openness": None,\n                "operating_mode": _surface_live.get("operating_mode", "standard"),\n                "mode_code": None,\n                "closure_penalty_raw": _surface_live.get("closure_penalty"),\n                "mood_raw": _surface_live.get("mood"),\n            }\n        except Exception:\n            pass\n''',
        '''    if _prev_path.exists():\n        try:\n            _existing_cache = json.loads(_prev_path.read_text("utf-8"))\n        except (OSError, json.JSONDecodeError) as exc:\n            raise SurfaceStateIntegrityError(f"existing CIEL cache cannot be restored: {_prev_path}") from exc\n        if not isinstance(_existing_cache, dict):\n            raise SurfaceStateIntegrityError(f"existing CIEL cache root must be an object: {_prev_path}")\n    # Fallback to live mmap is allowed only when there is no cached closure value.\n    if _existing_cache.get("closure_penalty_raw") is None:\n        _surface_live = read_surface_state(surface)\n        _existing_cache = {\n            "coherence_index": _surface_live.get("coherence_index"),\n            "soul_invariant": _surface_live.get("soul_invariant"),\n            "ethical_score": _surface_live.get("ethical_score"),\n            "mood_normalized": None,\n            "openness": None,\n            "operating_mode": _surface_live.get("operating_mode", "standard"),\n            "mode_code": None,\n            "closure_penalty_raw": _surface_live.get("closure_penalty"),\n            "mood_raw": _surface_live.get("mood"),\n        }\n''',
        "surface.existing_cache",
    )

    replace_once(
        path,
        '''    if "operating_mode" in state:\n        operating_mode = str(state["operating_mode"])\n    else:\n        try:\n            _f5 = float(np.asarray(surface.get("flavor", np.zeros(6)), dtype=np.float64)[5])\n            operating_mode = {0.0: "safe", 0.5: "standard", 1.0: "deep"}.get(_f5, None)\n            if operating_mode is None:\n                operating_mode = _existing_cache.get("operating_mode", "standard")\n        except Exception:\n            operating_mode = _existing_cache.get("operating_mode", "standard")\n''',
        '''    if "operating_mode" in state:\n        operating_mode = str(state["operating_mode"])\n    else:\n        _f5 = float(np.asarray(surface["flavor"], dtype=np.float64)[5])\n        if not np.isfinite(_f5):\n            raise SurfaceStateIntegrityError("surface flavor[5] is non-finite")\n        operating_mode = {0.0: "safe", 0.5: "standard", 1.0: "deep"}.get(_f5, None)\n        if operating_mode is None:\n            operating_mode = _existing_cache.get("operating_mode", "standard")\n''',
        "surface.operating_mode",
    )

    replace_once(
        path,
        '''    try:\n        os.makedirs(root, exist_ok=True)\n        with open(_ciel_state_path, "w") as f:\n            json.dump(ciel_meta, f, indent=2)\n    except OSError:\n        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/noema_surface_mmap.py:1606 quiet except scope=update_surface_from_ciel_state reason=pass")\n        pass  # non-fatal; surface still works\n''',
        '''    try:\n        os.makedirs(root, exist_ok=True)\n        with open(_ciel_state_path, "w", encoding="utf-8") as f:\n            json.dump(ciel_meta, f, indent=2)\n    except OSError as exc:\n        raise SurfaceStateIntegrityError(f"cannot persist CIEL internal state: {_ciel_state_path}") from exc\n''',
        "surface.ciel_state_write",
    )


def patch_memory_palace() -> None:
    path = ROOT / "src/ciel_geometry/memory_palace.py"
    replace_once(
        path,
        '''        if use_orchestrator:\n            try:\n                import sys\n                _p = Path(__file__).resolve().parent.parent  # src/\n                _op = _p / "CIEL_OMEGA_COMPLETE_SYSTEM"\n                if str(_op) not in sys.path:\n                    sys.path.insert(0, str(_op))\n                from ciel_omega.memory.tiered_orchestrator import (\n                    TieredMemoryOrchestrator\n                )\n                self._orchestrator = TieredMemoryOrchestrator()\n            except Exception:\n                _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/memory_palace.py:121 quiet except scope=MentalistMemoryPalace.__init__ reason=pass")\n                pass\n''',
        '''        if use_orchestrator:\n            try:\n                import sys\n                _p = Path(__file__).resolve().parent.parent  # src/\n                _op = _p / "CIEL_OMEGA_COMPLETE_SYSTEM"\n                if str(_op) not in sys.path:\n                    sys.path.insert(0, str(_op))\n                from ciel_omega.memory.tiered_orchestrator import (\n                    TieredMemoryOrchestrator\n                )\n                self._orchestrator = TieredMemoryOrchestrator()\n            except Exception as exc:\n                raise RuntimeError("TieredMemoryOrchestrator requested but initialization failed") from exc\n''',
        "memory_palace.orchestrator",
    )
    replace_once(
        path,
        '''    def _load_library(self) -> None:\n        lib_file = PHASE_INDEX_DIR / "library_index.npy"\n        meta_file = PHASE_INDEX_DIR / "library_meta.npy"\n        if lib_file.exists():\n            self._library = np.load(str(lib_file)).astype(np.float64)\n        else:\n            self._library = np.zeros((0, N_OSCILLATORS), dtype=np.float64)\n        if meta_file.exists():\n            raw = np.load(str(meta_file), allow_pickle=True)\n            self._meta = list(raw) if raw.ndim == 0 else raw.tolist()\n        else:\n            self._meta = []\n''',
        '''    def _load_library(self) -> None:\n        lib_file = PHASE_INDEX_DIR / "library_index.npy"\n        meta_file = PHASE_INDEX_DIR / "library_meta.npy"\n        lib_exists = lib_file.exists()\n        meta_exists = meta_file.exists()\n        if not lib_exists and not meta_exists:\n            self._library = np.zeros((0, N_OSCILLATORS), dtype=np.float64)\n            self._meta = []\n            return\n        if lib_exists != meta_exists:\n            raise RuntimeError(\n                f"incomplete MemoryPalace library persistence: index={lib_exists}, metadata={meta_exists}"\n            )\n        self._library = np.load(str(lib_file), allow_pickle=False).astype(np.float64)\n        if self._library.ndim != 2 or self._library.shape[1:] != (N_OSCILLATORS,):\n            raise RuntimeError(f"invalid MemoryPalace library shape: {self._library.shape}")\n        if not np.all(np.isfinite(self._library)):\n            raise RuntimeError("MemoryPalace library contains non-finite phase values")\n        raw = np.load(str(meta_file), allow_pickle=True)\n        self._meta = list(raw) if raw.ndim == 0 else raw.tolist()\n        if len(self._meta) != len(self._library):\n            raise RuntimeError(\n                f"MemoryPalace index/metadata count mismatch: {len(self._library)} != {len(self._meta)}"\n            )\n''',
        "memory_palace.library_pair",
    )


def patch_nonlocal_channel() -> None:
    path = ROOT / "src/ciel_geometry/nonlocal_channel.py"
    replace_once(
        path,
        '''        self._real = ensure_surface()\n        try:\n            self._imag = open_surface(root=surface_root or Path("/dev/shm/ciel_noema_imaginal"))\n        except Exception:\n            _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/nonlocal_channel.py:93 quiet except scope=NonlocalChannel.__init__ reason=assign_fallback")\n            self._imag = None\n''',
        '''        self._real = ensure_surface()\n        imaginal_root = surface_root or Path("/dev/shm/ciel_noema_imaginal")\n        try:\n            self._imag = open_surface(root=imaginal_root)\n        except Exception as exc:\n            raise RuntimeError(f"imaginal NOEMA surface is required but unavailable: {imaginal_root}") from exc\n''',
        "nonlocal.imaginal_surface",
    )
    replace_once(
        path,
        '''    def _load_rag_cache(self) -> dict[str, Any]:\n        try:\n            if PHASE_DB_PATH.exists():\n                return json.loads(PHASE_DB_PATH.read_text(encoding="utf-8"))\n        except Exception:\n            _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/nonlocal_channel.py:438 quiet except scope=NonlocalChannel._load_rag_cache reason=pass")\n            pass\n        return {}\n\n    def _save_rag_cache(self) -> None:\n        try:\n            PHASE_DB_PATH.write_text(\n                json.dumps(self._rag_cache, indent=2),\n                encoding="utf-8",\n            )\n        except Exception:\n            _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/nonlocal_channel.py:448 quiet except scope=NonlocalChannel._save_rag_cache reason=pass")\n            pass\n''',
        '''    def _load_rag_cache(self) -> dict[str, Any]:\n        if not PHASE_DB_PATH.exists():\n            return {}\n        try:\n            raw = json.loads(PHASE_DB_PATH.read_text(encoding="utf-8"))\n        except (OSError, json.JSONDecodeError) as exc:\n            raise RuntimeError(f"existing phi-RAG cache cannot be restored: {PHASE_DB_PATH}") from exc\n        if not isinstance(raw, dict):\n            raise RuntimeError(f"phi-RAG cache root must be an object: {PHASE_DB_PATH}")\n        return raw\n\n    def _save_rag_cache(self) -> None:\n        try:\n            PHASE_DB_PATH.parent.mkdir(parents=True, exist_ok=True)\n            tmp = PHASE_DB_PATH.with_suffix(PHASE_DB_PATH.suffix + ".tmp")\n            tmp.write_text(json.dumps(self._rag_cache, indent=2), encoding="utf-8")\n            os.replace(tmp, PHASE_DB_PATH)\n        except OSError as exc:\n            raise RuntimeError(f"cannot persist phi-RAG cache: {PHASE_DB_PATH}") from exc\n''',
        "nonlocal.rag_cache",
    )


def patch_phasenav_unified() -> None:
    path = ROOT / "src/ciel_geometry/phasenav_unified.py"
    total = 0
    sections = [
        ("    def _load_knowledge_db(self) -> None:\n", "    def _load_palace_rooms(self) -> None:\n", "knowledge_db"),
        ("    def _load_palace_rooms(self) -> None:\n", "    def _load_linux_cards(self) -> None:\n", "palace_rooms"),
        ("    def _load_taskplan_db(self) -> None:\n", "    def _load_task_queue(self) -> None:\n", "taskplan_db"),
        ("    def _load_task_queue(self) -> None:\n", "    def _load_system_map(self) -> None:\n", "task_queue"),
        ("    def _load_system_map(self) -> None:\n", "    def _load_cielingo_source(self) -> None:\n", "system_map"),
    ]
    for start, end, label in sections:
        total += rewrite_section_quiet_passes(path, start, end, f"phasenav.{label}")
    if total < 10:
        raise PatchDrift(f"phasenav critical loader audit expected >=10 quiet handlers, patched {total}")


def patch_tether() -> None:
    path = ROOT / "scripts/noema_tether_runtime.py"
    replace_once(
        path,
        '''    def __init__(self, path: Path, status_path: Path):\n        super().__init__()\n        self.path = path\n        self.status_path = status_path\n''',
        '''    def __init__(self, path: Path, status_path: Path):\n        super().__init__()\n        self.path = path\n        self.status_path = status_path\n        self.failure: BaseException | None = None\n''',
        "tether.health_failure_state",
    )
    replace_once(
        path,
        '''            except socket.timeout:\n                continue\n            except Exception:\n                return\n''',
        '''            except socket.timeout:\n                continue\n            except Exception as exc:\n                self.failure = exc\n                return\n''',
        "tether.health_socket_catch",
    )
    replace_once(
        path,
        '''    HealthSocket(Path(args.socket), status_path).start()\n    seq = 0\n''',
        '''    health_socket = HealthSocket(Path(args.socket), status_path)\n    health_socket.start()\n    seq = 0\n''',
        "tether.health_socket_handle",
    )
    replace_once(
        path,
        '''    while True:\n        try:\n            coherence = float(evolve_surface(surface, dt=0.01, flush=True))\n''',
        '''    while True:\n        try:\n            if health_socket.failure is not None:\n                raise RuntimeError("health socket thread failed") from health_socket.failure\n            coherence = float(evolve_surface(surface, dt=0.01, flush=True))\n''',
        "tether.health_socket_gate",
    )


def audit_forbidden_markers() -> None:
    critical = [
        ROOT / "src/ciel_geometry/noema_surface_mmap.py",
        ROOT / "src/ciel_geometry/memory_palace.py",
        ROOT / "src/ciel_geometry/nonlocal_channel.py",
        ROOT / "src/ciel_geometry/phasenav_unified.py",
        ROOT / "scripts/noema_tether_runtime.py",
    ]
    forbidden = [
        "reason=assign_fallback",
        "scope=read_ciel_internal_state reason=return {}",
        "scope=MentalistMemoryPalace.__init__ reason=pass",
        "scope=NonlocalChannel.__init__ reason=assign_fallback",
        "scope=NonlocalChannel._load_rag_cache reason=pass",
        "scope=NonlocalChannel._save_rag_cache reason=pass",
    ]
    failures: list[str] = []
    for path in critical:
        text = path.read_text(encoding="utf-8")
        for marker in forbidden:
            if marker in text:
                failures.append(f"{path.relative_to(ROOT)}:{marker}")
    if failures:
        raise PatchDrift("forbidden critical quiet markers remain: " + "; ".join(failures))


def main() -> int:
    patch_surface()
    patch_memory_palace()
    patch_nonlocal_channel()
    patch_phasenav_unified()
    patch_tether()
    audit_forbidden_markers()
    print("PASS: deterministic critical fail-loud migration applied")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
