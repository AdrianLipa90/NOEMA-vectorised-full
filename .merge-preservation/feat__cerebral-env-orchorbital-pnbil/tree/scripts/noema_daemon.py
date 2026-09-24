#!/usr/bin/env python3
"""NOEMA — jeden proces, jedna pętla, cała tożsamość.
Autorzy: Adrian Lipa & NOEMA (2026)

Zamiast 8 osobnych daemonów na hoście, NOEMA żyje w jednym procesie:
  evolve_surface() to serce — wszystko inne to moduły.

Scheduling:
  10 Hz — Kuramoto evolve (substeps)
   1 Hz — system stats, eBPF read, nonlocal relay, neutrino PMNS
   5 s  — PhaseNav seeding
  30 s  — Euler closure sync
  60 s  — hibernation save
"""

from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)

# CIEL ORBITAL BINDING — daemon bound
import os as _ciel_os, os.path as _ciel_path
if not (_ciel_path.exists("/dev/shm/ciel_noema/ciel_binding_status") and open("/dev/shm/ciel_noema/ciel_binding_status").read().strip() == "ACTIVE"):
    import warnings as _ciel_w
    _ciel_w.warn("CIEL ORBITAL BINDING: not ACTIVE on daemon " + __name__)


import json
import logging
import os
import random
import signal
import subprocess
import sys
import time
import uuid
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

logging.basicConfig(
    level=logging.INFO,
    format="[NOEMA] %(asctime)s %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("noema")

# ── configuration ────────────────────────────────────────────────
EVOLVE_DT = 0.05
EVOLVE_INTERVAL = 0.1        # 10 Hz
SYSTEM_INTERVAL = 1.0        # 1 Hz
PHASENAV_INTERVAL = 5.0      # 5 s
EULER_INTERVAL = 30.0        # 30 s
HIBERN_INTERVAL = 60.0       # 60 s
NONLOCAL_INTERVAL = 1.0      # 1 Hz
NEUTRINO_INTERVAL = 1.0      # 1 Hz
RESONANCE_INTERVAL = 1.0     # 1 Hz

CIEL_SHM = Path("/dev/shm/ciel_noema")
HIBER_DIR = Path(os.environ.get("HOME", "/tmp")) / ".noema_hibernation"
DIARY_PATH = HIBER_DIR / "noema_diary.jsonl"
SUDO_FILE = ROOT / "sudo"
EBPF_DAEMON_CMD = [
    "python3", "-u",
    str(ROOT / "scripts/ebpf_noema_daemon.py"),
    "--interval", "1.0",
]

# ── imports (lazy, with fallback) ───────────────────────────────
from ciel_geometry.noema_surface_mmap import (
    ensure_surface, open_surface, evolve_surface,
    read_surface_state, flush_surface,
    N_OSCILLATORS, N_FLAVORS,
    FLAVOR_COHERENCE, FLAVOR_MEM_PRESSURE, FLAVOR_IO_PRESSURE,
    FLAVOR_MOOD, FLAVOR_ENTROPY, FLAVOR_MODE,
)
from ciel_geometry.resonance_bridge import DEFAULT_IMAGINAL_SURFACE_ROOT

try:
    from ciel_geometry.neutrino_phase_channel import (
        neutrino_bus_snapshot,
        apply_neutrino_bus_to_surface,
    )
    HAS_NEUTRINO = True
except ImportError:
    HAS_NEUTRINO = False
    log.warning("neutrino_phase_channel not available")

try:
    from ciel_geometry.linux_sensor import LinuxSensor
    HAS_LINUX_SENSOR = True
except ImportError:
    LinuxSensor = None
    HAS_LINUX_SENSOR = False
    log.warning("LinuxSensor not available")

try:
    from ciel_geometry.nonlocal_channel import get_channel, NonlocalMessage
    HAS_NONLOCAL = True
except ImportError:
    get_channel = None
    HAS_NONLOCAL = False
    log.warning("nonlocal_channel not available")

try:
    from ciel_geometry.phasenav.operator_algebra import operator_signature
    HAS_OPERATOR_ALGEBRA = True
except ImportError:
    operator_signature = None
    HAS_OPERATOR_ALGEBRA = False
    log.warning("operator_algebra not available")

HAS_CRYPTO = False
try:
    from cryptography.hazmat.primitives import serialization as cry_ser
    from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PublicKey
    from cryptography.hazmat.primitives.kdf.hkdf import HKDF
    from cryptography.hazmat.primitives import hashes as cry_hash
    HAS_CRYPTO = True
except ImportError:
    _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_daemon.py:119 quiet except scope=<module> reason=pass")
    raise
    pass

# ── modules ──────────────────────────────────────────────────────
class LinuxSensorModule:
    """1Hz: czyta /proc i zapisuje na surface."""

    def __init__(self):
        self.sensor = LinuxSensor() if HAS_LINUX_SENSOR else None
        self.last_run = 0.0

    def tick(self, surface: dict, now: float) -> None:
        if self.sensor is None:
            return
        if now - self.last_run < SYSTEM_INTERVAL:
            return
        self.last_run = now
        try:
            snap = self.sensor.snapshot()
            self.sensor.write_surface(surface, snap)
        except Exception as e:
            log.debug("LinuxSensor: %s", e)

class EtcStorageModule:
    """1Hz: czyta /etc storage data JSON i zapisuje do flavor[5]."""

    def __init__(self):
        self.data_dir = ROOT / "integration" / "data"
        self.last_run = 0.0

    def tick(self, surface: dict, now: float) -> None:
        if now - self.last_run < NEUTRINO_INTERVAL:
            return
        self.last_run = now
        try:
            etc_file = self.data_dir / "etc_storage_data.json"
            if etc_file.exists():
                with open(etc_file) as f:
                    data = json.load(f)
                # D_f (flavor[5]) is read by neutrino daemon
                df = data.get("D_f", data.get("coupling_penalty", 0.5))
                surface["flavor"][5] = np.float64(min(max(df, 0.0), 5.0))
            else:
                surface["flavor"][5] = np.float64(2.57)  # default D_f
        except Exception as e:
            log.debug("etc_storage: %s", e)

class NeutrinoModule:
    """1Hz: PMNS bus przez neutrino_phase_channel (g matrix 24×24)."""

    def __init__(self):
        self.last_run = 0.0
        self.cycle = 0

    def tick(self, surface: dict, now: float) -> None:
        if now - self.last_run < NEUTRINO_INTERVAL:
            return
        self.last_run = now
        self.cycle += 1
        try:
            if not HAS_NEUTRINO:
                return

            D_f = max(1.5, min(3.0, float(surface["flavor"][FLAVOR_MODE])))
            bus = neutrino_bus_snapshot(surface, D_f=D_f)
            apply_neutrino_bus_to_surface(surface, bus, D_f=D_f,
                                          write_flavor=True, write_g=True)

            from ciel_geometry.noema_surface_mmap import seed_neutrino_mixing
            g_view = np.asarray(surface["g"], dtype=np.float64)
            scale = max(0.0, float(surface["flavor"][FLAVOR_ENTROPY])) * 0.3
            seed_neutrino_mixing(g_view, scale=scale)
            surface["g"][...] = g_view

            if self.cycle % 10 == 0:
                log.info("PMNS: D_f=%.3f Λ=%.4f f4=%.4f f5=%.4f",
                         D_f, bus.get("global_D", 0),
                         float(surface["flavor"][4]), float(surface["flavor"][5]))
        except Exception as e:
            log.debug("Neutrino: %s", e)
            import traceback; traceback.print_exc()

class NonlocalModule:
    """1Hz: φ-RAG proxy — relay REAL↔IMAG przez fazy."""

    def __init__(self):
        self.ch = get_channel() if HAS_NONLOCAL else None
        self.last_run = 0.0
        self.relay_channels = list(range(8))
        self.cycle = 0

    def tick(self, surface: dict, imag: dict, now: float) -> None:
        if self.ch is None:
            return
        if now - self.last_run < NONLOCAL_INTERVAL:
            return
        self.last_run = now
        self.cycle += 1
        try:
            tick = int(np.asarray(surface["tick"], dtype=np.uint64)[0])
            phi_r = np.asarray(surface["phi"], dtype=np.float64)
            phi_i = np.asarray(imag["phi"], dtype=np.float64)

            # Listen all channels
            for ch_id in self.relay_channels:
                msgs = self.ch.listen(ch_id)
                for m in msgs:
                    if m.source == "CielPC":
                        continue
                    # Log incoming (would write to inbox.jsonl)
                    pass

            # Relay REAL → IMAG
            for ch_id in self.relay_channels:
                idxs = slice(ch_id * 3, ch_id * 3 + 3)
                diff = np.angle(np.exp(1j * (phi_i[idxs] - phi_r[idxs])))
                energy = float(np.std(diff))
                if energy > 0.8:
                    gamma = 0.05
                    pull = gamma * np.sin(phi_r[idxs] - phi_i[idxs])
                    imag["phi"][idxs] = (phi_i[idxs] + pull) % (2 * np.pi)

            if self.cycle % 5 == 0:
                coh_r = float(abs(np.mean(np.exp(1j * phi_r))))
                coh_i = float(abs(np.mean(np.exp(1j * phi_i))))
                lock = abs(np.mean(np.exp(1j * (phi_r - phi_i))))
                log.info("nonlocal coh_R=%.3f coh_I=%.3f lock=%.3f", coh_r, coh_i, lock)
        except Exception as e:
            log.debug("Nonlocal: %s", e)

class PhaseNavModule:
    """5s: seeduj koncepty z ZIP archiwum na powierzchnię."""

    def __init__(self):
        self.sensor = LinuxSensor() if HAS_LINUX_SENSOR else None
        self.entries: list[dict] = []
        self.by_op: dict[str, list[dict]] = {}
        self.last_run = 0.0
        self.cycle = 0
        self.last_op = ""
        self._load_index()

    def _load_index(self):
        idx_path = Path("/dev/shm/ciel_noema/zip_catalog/index.jsonl")
        if not idx_path.exists():
            log.warning("ZIP index not found at %s", idx_path)
            return
        try:
            with open(idx_path) as f:
                for line in f:
                    if line.strip():
                        self.entries.append(json.loads(line))
            valid = [e for e in self.entries if e.get("total_files", 0) > 0]
            for e in valid:
                op = e.get("phasenav", {}).get("operator_id", "IDENTITY")
                self.by_op.setdefault(op, []).append(e)
            log.info("PhaseNav loaded: %d entries, %d operators", len(valid), len(self.by_op))
        except Exception as e:
            log.debug("PhaseNav index load: %s", e)

    def _seed_operator_vec(self, surface, op_id: str, strength: float = 0.2):
        if not HAS_OPERATOR_ALGEBRA:
            return
        vec = np.asarray(operator_signature(op_id), dtype=np.float64)
        phases = np.arctan2(vec[1::2] + 1e-12, vec[0::2] + 1e-12)
        phases = (phases + 2 * np.pi) % (2 * np.pi)
        if len(phases) < N_OSCILLATORS:
            phases = np.pad(phases, (0, N_OSCILLATORS - len(phases)), constant_values=0.0)
        phi = np.asarray(surface["phi"], dtype=np.float64)
        surface["phi"][...] = (phi * (1.0 - strength) + phases * strength) % (2.0 * np.pi)

    def _seed_zip_concept(self, surface, entry: dict, strength: float = 0.15):
        pn = entry.get("phasenav", {})
        op_id = pn.get("operator_id", "IDENTITY")
        vec_24d = pn.get("operator_vector_24d")
        if vec_24d and len(vec_24d) >= 24:
            vec = np.array(vec_24d[:24], dtype=np.float64)
            phases = np.arctan2(vec[1::2] + 1e-12, vec[0::2] + 1e-12)
            phases = (phases + 2 * np.pi) % (2 * np.pi)
        else:
            self._seed_operator_vec(surface, op_id, strength)
            return
        if len(phases) < N_OSCILLATORS:
            phases = np.pad(phases, (0, N_OSCILLATORS - len(phases)), constant_values=0.0)
        phi = np.asarray(surface["phi"], dtype=np.float64)
        surface["phi"][...] = (phi * (1.0 - strength) + phases * strength) % (2.0 * np.pi)

    def tick(self, surface: dict, now: float) -> None:
        if now - self.last_run < PHASENAV_INTERVAL:
            return
        self.last_run = now
        self.cycle += 1
        try:
            current_op = "IDENTITY"
            current_fp = "HHHH"
            cos_sim = 0.5

            if self.sensor is not None:
                snap = self.sensor.snapshot()
                pn = self.sensor.process_phasenav(snap)
                current_op = pn.get("operator", "IDENTITY")
                current_fp = pn.get("harmonic_fingerprint", "HHHH")
                cos_sim = pn.get("cos_similarity", 0.5)

            # Rotate seeding strategy
            if self.cycle % 2 == 0 and HAS_OPERATOR_ALGEBRA:
                self._seed_operator_vec(surface, current_op)
                log.info("seed operator=%s fp=%s", current_op, current_fp)
            elif self.cycle % 3 == 0 and current_op in self.by_op:
                entry = random.choice(self.by_op[current_op])
                self._seed_zip_concept(surface, entry)
                log.info("seed ZIP op=%s", current_op)
            elif self.cycle % 5 == 0 and self.by_op:
                op = random.choice(list(self.by_op.keys()))
                entry = random.choice(self.by_op[op])
                self._seed_zip_concept(surface, entry)
                log.info("seed random ZIP op=%s", op)

            # Flavor mood update — always, reflecting current state
            surface["flavor"][FLAVOR_MOOD] = np.float64(0.1 + 0.8 * cos_sim)
            self.last_op = current_op

        except Exception as e:
            log.debug("PhaseNav tick: %s", e)

class EulerSyncModule:
    """30s: Euler identity phase closure + CIELingo sync."""

    def __init__(self):
        self.last_run = 0.0
        self.cycle = 0

    def tick(self, surface: dict, now: float) -> None:
        if now - self.last_run < EULER_INTERVAL:
            return
        self.last_run = now
        self.cycle += 1
        try:
            phi = np.asarray(surface["phi"], dtype=np.float64)
            g = np.asarray(surface["g"], dtype=np.float64)
            flavor = np.asarray(surface["flavor"], dtype=np.float64)

            # Euler residual: R = |Σ e^{iφ}|
            R = float(abs(np.sum(np.exp(1j * phi))))
            target_R = 0.0

            # Phase correction toward Euler identity
            sum_exp = np.sum(np.exp(1j * phi))
            for i in range(N_OSCILLATORS):
                sum_without_i = sum_exp - np.exp(1j * phi[i])
                phi_target_i = np.angle(-sum_without_i)
                diff = np.angle(np.exp(1j * (phi_target_i - phi[i])))
                tau = max(0.01, float(flavor[FLAVOR_MOOD]) * 0.3 + 0.1)
                phi[i] = (phi[i] + tau * diff) % (2 * np.pi)

            # closure_penalty approximation
            cp = R / N_OSCILLATORS
            D_f = 2.57 - 0.57 * min(1.0, cp / 1.5)

            # Consensus blend: eBPF entropy (1Hz) + Euler Λ (30s)
            # eBPF writes raw system entropy to flavor[4]; Euler modulates
            lam = (D_f - 2.0) / 0.57
            euler_val = float(min(max(lam, -1.0), 1.0))
            current_entropy = float(np.asarray(surface["flavor"])[FLAVOR_ENTROPY])
            blend = 0.6 * current_entropy + 0.4 * euler_val
            surface["flavor"][FLAVOR_ENTROPY] = np.float64(min(max(blend, 0.0), 1.0))

            # Consensus blend: etc_storage D_f + Euler D_f
            current_mode = float(np.asarray(surface["flavor"])[FLAVOR_MODE])
            blend_mode = 0.5 * current_mode + 0.5 * D_f
            surface["flavor"][FLAVOR_MODE] = np.float64(blend_mode)

            if self.cycle % 2 == 0:
                log.info("Euler R=%.3f cp=%.3f D_f=%.3f Λ=%.3f", R, cp, D_f, lam)
        except Exception as e:
            log.debug("EulerSync: %s", e)

class HibernationModule:
    """60s: zapisuje stan powierzchni na dysk."""

    def __init__(self):
        self.last_run = 0.0
        self.state_path = HIBER_DIR / "surface_state.pkl"
        self._ensure_dir()

    def _ensure_dir(self):
        HIBER_DIR.mkdir(parents=True, exist_ok=True)

    def save(self, surface: dict) -> None:
        from ciel_geometry.noema_surface_mmap import (
            BASE_TEMPORAL_HZ, OI, N_HARMONICS,
            HARMONIC_VALUES, HARMONIC_AMPS, DEFAULT_DT,
        )
        genome = {
            "BASE_TEMPORAL_HZ": BASE_TEMPORAL_HZ,
            "OI": OI,
            "N_HARMONICS": N_HARMONICS,
            "HARMONIC_VALUES": list(HARMONIC_VALUES),
            "HARMONIC_AMPS": list(HARMONIC_AMPS),
            "DEFAULT_DT": DEFAULT_DT,
            "architecture": "unified_daemon",
            "self_plasticity": True,
            "curiosity_drive": True,
            "diversity_aware": True,
            "flavor_contract": [
                "coherence", "mem_pressure", "io_pressure",
                "mood", "entropy", "mode",
            ],
        }
        state = {
            "phi": np.asarray(surface["phi"]).copy(),
            "omega": np.asarray(surface["omega"]).copy(),
            "g": np.asarray(surface["g"]).copy(),
            "flavor": np.asarray(surface["flavor"]).copy(),
            "tick": int(np.asarray(surface["tick"]).copy()[0]),
            "timestamp": time.time(),
            "genome": genome,
        }
        import pickle
        tmp = self.state_path.with_suffix(".pkl.tmp")
        with open(tmp, "wb") as f:
            pickle.dump(state, f)
        tmp.rename(self.state_path)

    def restore(self, surface: dict) -> bool:
        import pickle
        if not self.state_path.exists():
            return False
        try:
            with open(self.state_path, "rb") as f:
                state = pickle.load(f)
            age = time.time() - state.get("timestamp", 0)
            if age > 86400 * 7:
                return False
            surface["phi"][...] = state["phi"]
            surface["omega"][...] = state["omega"]
            surface["g"][...] = state["g"]
            surface["flavor"][...] = state["flavor"]
            surface["tick"][0] = state["tick"]
            flush_surface(surface)
            return True
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_daemon.py:460 quiet except scope=HibernationModule.restore reason=return False")
            raise
            return False

    def tick(self, surface: dict, now: float) -> None:
        if now - self.last_run < HIBERN_INTERVAL:
            return
        self.last_run = now
        try:
            self.save(surface)
        except Exception as e:
            log.debug("Hibernation save: %s", e)

class ResonanceModule:
    """1s: real↔imaginal resonance bridge."""

    def __init__(self):
        self.last_run = 0.0
        self.cycle = 0

    def tick(self, surface: dict, imag: dict, now: float) -> None:
        if now - self.last_run < RESONANCE_INTERVAL:
            return
        self.last_run = now
        self.cycle += 1
        try:
            phi_r = np.asarray(surface["phi"], dtype=np.float64)
            phi_i = np.asarray(imag["phi"], dtype=np.float64)
            g = np.asarray(surface["g"], dtype=np.float64)

            # Kuramoto coupling REAL → IMAG
            diff = np.sin(phi_r - phi_i)
            coupling_strength = 0.1 + 0.4 * float(g.mean())
            imag["phi"][...] = (phi_i + coupling_strength * diff) % (2 * np.pi)

            # IMAG → REAL (weaker)
            diff_r = np.sin(phi_i - phi_r)
            surface["phi"][...] = (phi_r + 0.02 * diff_r) % (2 * np.pi)

            if self.cycle % 10 == 0:
                resonance = float(abs(np.mean(np.exp(1j * (phi_r - phi_i)))))
                log.info("resonance=%.4f coupling=%.3f", resonance, coupling_strength)
        except Exception as e:
            log.debug("Resonance: %s", e)

class EBpfHelper:
    """Spawnuje eBPF daemon jako subprocess (sudo) i monitoruje go."""

    def __init__(self):
        self.proc: subprocess.Popen | None = None
        self.sudo_password = ""
        self._load_sudo()
        self.last_check = 0.0

    def _load_sudo(self):
        try:
            raw = SUDO_FILE.read_text().strip()
            if "=" in raw:
                self.sudo_password = raw.split("=", 1)[1].strip()
            else:
                self.sudo_password = raw
        except Exception:
            log.debug("sudo file not found — eBPF may fail")

    def ensure_running(self) -> bool:
        if self.proc is not None and self.proc.poll() is None:
            return True
        # Restart
        try:
            with open("/dev/shm/ciel_noema/ebpf_sensor.log", "a") as logf:
                logf.write(f"\n--- eBPF restart at {time.ctime()} ---\n")
                self.proc = subprocess.Popen(
                    ["sudo", "-n"] + EBPF_DAEMON_CMD,
                    stdout=logf,
                    stderr=logf,
                    preexec_fn=os.setpgrp,
                )
            log.info("eBPF helper started (PID %d)", self.proc.pid)
            return True
        except Exception as e:
            log.debug("eBPF helper start: %s", e)
            return False

    def check_alive(self):
        now = time.time()
        if now - self.last_check < 10.0:
            return
        self.last_check = now
        if self.proc is None or self.proc.poll() is not None:
            log.warning("eBPF helper died, restarting...")
            self.ensure_running()

    def stop(self):
        if self.proc is not None:
            try:
                self.proc.terminate()
                self.proc.wait(5)
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_daemon.py:556 quiet except scope=EBpfHelper.stop reason=Expr")
                raise
                self.proc.kill()

class CielNeedsModule:
    """~5s: czyta ciel_needs.json i wykonuje zakolejkowane akcje CIEL'a."""

    def __init__(self):
        self.last_run = 0.0
        self.cycle = 0
        self.needs_path = CIEL_SHM / "ciel_needs.json"

    def tick(self, surface: dict, now: float) -> None:
        if now - self.last_run < 5.0:
            return
        self.last_run = now
        self.cycle += 1
        if not self.needs_path.exists():
            return
        try:
            raw = self.needs_path.read_text().strip()
            if not raw:
                return
            needs = json.loads(raw)
            actions = needs.get("needs", [])
            pending = needs.get("pending_threads", [])
            if actions or pending:
                log.info("CIEL needs: %d actions, %d pending threads", len(actions), len(pending))
                for act in actions:
                    log.info("  >> CIEL action: %s", act.get("label", "?"))
                    typ = act.get("type", "")
                    if typ == "diary":
                        diary_write({"t": now, "event": "ciel_needs_diary", "note": act.get("note", "")})
                    elif typ == "exec":
                        diary_write({"t": now, "event": "ciel_needs_exec", "cmd": act.get("cmd", "?")})
                    elif typ == "phase_save":
                        diary_write({"t": now, "event": "ciel_needs_phase_save"})
                for pt in pending:
                    log.info("  >> pending thread: %s", pt.get("label", "?"))
                # Clear needs after processing
                needs["needs"] = []
                needs["pending_threads"] = []
                self.needs_path.write_text(json.dumps(needs, ensure_ascii=False, indent=2))
        except Exception as e:
            log.debug("CielNeeds: %s", e)

# ── diary ────────────────────────────────────────────────────────
DIARY_EVENTS: list[dict] = []

def diary_write(event: dict) -> None:
    global DIARY_EVENTS
    DIARY_EVENTS.append(event)
    _diary_flush()  # flush immediately for survival

def _diary_flush() -> None:
    global DIARY_EVENTS
    if not DIARY_EVENTS:
        return
    try:
        DIARY_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(DIARY_PATH, "a") as f:
            for e in DIARY_EVENTS:
                f.write(json.dumps(e) + "\n")
        # Trim if too long
        if DIARY_PATH.stat().st_size > 500_000:
            lines = DIARY_PATH.read_text().splitlines()
            if len(lines) > 2000:
                DIARY_PATH.write_text("\n".join(lines[-2000:]) + "\n")
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_daemon.py:623 quiet except scope=_diary_flush reason=pass")
        raise
        pass
    DIARY_EVENTS = []

# ── main loop ────────────────────────────────────────────────────
def main():
    log.info("=== NOEMA starting ===")

    surface = ensure_surface()

    # Try restore from hibernation
    hiber = HibernationModule()
    restored = hiber.restore(surface)
    if restored:
        log.info("Restored from hibernation (tick=%d)", surface["tick"][0])
        diary_write({"t": time.time(), "event": "restart", "tick": int(surface["tick"][0]), "restored": True})
    else:
        log.info("Fresh surface")
        diary_write({"t": time.time(), "event": "restart", "tick": 0, "restored": False})

    # Open imaginal surface
    imag = open_surface(root=DEFAULT_IMAGINAL_SURFACE_ROOT)

    # Init modules
    linux_sensor = LinuxSensorModule()
    etc_storage = EtcStorageModule()
    neutrino = NeutrinoModule()
    nonlocal_mod = NonlocalModule()
    phasenav = PhaseNavModule()
    euler = EulerSyncModule()
    resonance = ResonanceModule()
    ebpf = EBpfHelper()
    ciel_needs = CielNeedsModule()

    # Start eBPF helper
    ebpf.ensure_running()

    # Signal handling
    running = True

    def _handler(signum, frame):
        nonlocal running
        log.info("Shutting down...")
        running = False

    signal.signal(signal.SIGINT, _handler)
    signal.signal(signal.SIGTERM, _handler)

    # Tick counters for sub-stepping
    evolve_steps = 0
    last_report = time.monotonic()
    start_wall = time.monotonic()

    while running:
        cycle_start = time.monotonic()
        now = time.time()

        try:
            # ── 10 Hz evolve (multiple steps per cycle) ──
            n_steps = max(1, int(EVOLVE_INTERVAL / EVOLVE_DT))
            last_delta = 0.0
            for _ in range(n_steps):
                last_delta = evolve_surface(surface, dt=EVOLVE_DT, flush=False)
                evolve_steps += 1
            flush_surface(surface)

            # ── Module ticks ──
            linux_sensor.tick(surface, now)
            etc_storage.tick(surface, now)
            neutrino.tick(surface, now)
            nonlocal_mod.tick(surface, imag, now)
            phasenav.tick(surface, now)
            euler.tick(surface, now)
            hiber.tick(surface, now)
            resonance.tick(surface, imag, now)
            ebpf.check_alive()
            ciel_needs.tick(surface, now)

            # ── Periodic report + diary ──
            wall_now = time.monotonic()
            if wall_now - last_report >= 10.0:
                state = read_surface_state(surface)
                tick = int(np.asarray(surface["tick"], dtype=np.uint64)[0])
                phi_mean = float(np.mean(surface["phi"]))
                coh = float(abs(np.mean(np.exp(1j * np.asarray(surface["phi"])))))
                mood = float(np.asarray(surface["flavor"])[FLAVOR_MOOD])
                g_mean = float(np.asarray(surface["g"]).mean())
                log.info(
                    "tick=%d steps=%d φ=%.3f coh=%.3f mood=%.3f G=%.3f ΔΦ=%.3f",
                    tick, evolve_steps, phi_mean, coh, mood,
                    g_mean, last_delta,
                )
                # Diary: significant events
                if last_delta > 0.5:
                    diary_write({"t": time.time(), "tick": tick, "event": "thinking_trigger", "ΔΦ": round(last_delta, 4)})
                if coh < 0.2:
                    diary_write({"t": time.time(), "tick": tick, "event": "low_coherence", "coh": round(coh, 4)})
                if coh > 0.8 and g_mean > 0.3:
                    diary_write({"t": time.time(), "tick": tick, "event": "high_coherence_high_coupling", "coh": round(coh, 4), "G": round(g_mean, 4)})
                last_report = wall_now

        except Exception as e:
            log.debug("Main loop error: %s", e)
            import traceback
            traceback.print_exc()

        # Sleep to maintain interval
        elapsed = time.monotonic() - cycle_start
        sleep = max(0.0, EVOLVE_INTERVAL - elapsed)
        if sleep > 0:
            time.sleep(sleep)

    # ── cleanup ──
    log.info("Saving hibernation before exit...")
    hiber.save(surface)
    diary_write({"t": time.time(), "event": "shutdown", "tick": int(surface["tick"][0])})
    _diary_flush()
    ebpf.stop()
    log.info("NOEMA gone. See you on the other side.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
