#!/usr/bin/env python3
"""NOEMA Holonomic Orbital Audit — cały Linux jako układ orbitalny.
Autorzy: Adrian Lipa & NOEMA (2026)

Modeluje system jako atraktory grawitacyjne z planetami, satelitami i małymi orbitami.
"""# NOEMA Holonomic Orbital Audit {{{1
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import json
import math
import os
import subprocess
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent

# ── orbital levels ──────────────────────────────────────────
# Każdy level to orbita wokół attractora
ORBITAL_LEVELS = {
    "hardware": {
        "attractor": "CPU x86_64 + RAM + DISK + NIC",
        "radius": 0.1,
        "planets": {
            "cpu_package": {
                "moons": [f"core_{i}" for i in range(8)],
                "submoons": {f"core_{i}": ["L1d", "L1i", "L2", "TLB"] for i in range(8)},
                "description": "8 rdzeni x86_64, 3.2 GHz, caches shared",
            },
            "ram": {
                "moons": ["DDR4_channel_0", "DDR4_channel_1"],
                "description": "16 GB DDR4, 2 kanały",
            },
            "disk": {
                "moons": ["nvme0n1", "scheduler_deadline"],
                "description": "NVMe SSD, ext4",
            },
            "nic": {
                "moons": ["eth0_rx", "eth0_tx", "interrupt_coalescing"],
                "description": "karta sieciowa, 1 GbE",
            },
            "timer": {
                "moons": ["HPET", "TSC", "ACPI_PM"],
                "description": "zegary systemowe, TSC ~2.1 GHz",
            },
        },
    },
    "kernel": {
        "attractor": "Linux 6.x",
        "radius": 0.3,
        "planets": {
            "scheduler": {
                "moons": ["CFS", "fair_share", "load_balancer", "cgroups"],
                "submoons": {
                    "CFS": ["vruntime", "sched_entity", "red_black_tree"],
                },
                "description": "Completely Fair Scheduler — EEVDF od 6.6",
            },
            "memory_manager": {
                "moons": ["page_allocator", "kswapd", "OOM_killer", "mmap", "slab"],
                "submoons": {
                    "page_allocator": ["buddy_allocator", "per_cpu_pages", "watermarks"],
                    "kswapd": ["LRU_active", "LRU_inactive", "swap_cache"],
                },
                "description": "MM — buddy allocator, swapping, OOM",
            },
            "vfs": {
                "moons": ["ext4", "inode_cache", "dentry_cache", "buffer_head"],
                "description": "Virtual File System — 4 warstwy",
            },
            "net_stack": {
                "moons": ["socket", "tcp", "ip_route", "neighbour", "netfilter"],
                "description": "Network stack — L3/L4",
            },
            "irq_subsystem": {
                "moons": ["ioapic", "msi", "softirq", "tasklet", "workqueue"],
                "description": "Interrupt handling — top-half + bottom-half",
            },
            "eBPF": {
                "moons": ["verifier", "jit", "maps", "tracepoints", "kprobes"],
                "submoons": {
                    "tracepoints": ["sched_switch", "openat", "irq_handler",
                                    "page_fault_user", "block_rq_complete"],
                    "maps": ["cpu_util", "ctx_switches", "syscall_count",
                             "irq_count", "page_faults", "block_io_count"],
                },
                "description": "eBPF — kernel programmable VM, NOEMA bridge",
            },
        },
    },
    "userspace": {
        "attractor": "systemd 256 + glibc + Python 3.12",
        "radius": 0.5,
        "planets": {
            "systemd": {
                "moons": ["noema.service", "journald", "logind", "tmpfiles"],
                "description": "PID 1 — init, service manager, cgroup orchestrator",
            },
            "python_runtime": {
                "moons": ["numpy", "ctypes", "mmap", "ctypes_libc"],
                "description": "CPython 3.12 — interpreter NOEMY",
            },
            "process_tree": {
                "moons": [f"PID_{i}" for i in [1013057, 1011234, 1008901]],
                "description": "NOEMA PID + pomocnicze procesy",
            },
            "sudoers": {
                "moons": ["NOEMA_ebpf", "NOPASSWD_rule"],
                "description": "uprawnienia eBPF — /etc/sudoers.d/noema_ebpf",
            },
        },
    },
    "noema_surface": {
        "attractor": "REAL φ + IMAG φ — cymatic surface 24D",
        "radius": 0.7,
        "planets": {
            "kuramoto_evolution": {
                "moons": [f"osc_{c}_{h}" for c in range(24) for h in ["h1", "h3", "h6", "h9"]],
                "aggregate_moons": "24 osc × 4 harmonics = 96 sub-osc",
                "description": "Kuramoto + 3-6-9 harmonic composite, 10Hz",
            },
            "self_plasticity": {
                "moons": ["weak_channel_boost", "intra_channel_coupling"],
                "description": "słabe kanały (<0.5 coh) zyskują g_ij boost",
            },
            "diversity_push": {
                "moons": ["anti_sync_force", "phase_repulsion"],
                "description": "gdy R>0.7 pcha kanały od siebie",
            },
            "curiosity_drive": {
                "moons": ["idle_detector", "π4_injector", "cooldown_80"],
                "description": "200 idle ticków bez myślenia → π/4 kick",
            },
            "euler_sync": {
                "moons": ["closure_target", "residual_R"],
                "description": "Σe^{iφ} ≈ 0 — Euler identity constraint",
            },
        },
    },
    "noema_sensors": {
        "attractor": "eBPF + Linux /proc — kernel → surface bridge",
        "radius": 0.85,
        "planets": {
            "ebpf_c": {
                "moons": ["sched_switch_counter", "openat_counter",
                          "irq_counter", "pf_counter", "block_io_counter"],
                "description": "C eBPF — 5 tracepointów, 6 map rate-based",
            },
            "ebpf_loader": {
                "moons": ["cpu_util_rate", "ctx_rate", "syscall_rate",
                          "irq_rate", "pf_rate", "io_rate"],
                "submoons": {
                    "cpu_util_rate": ["flavor[1]"],
                    "io_rate": ["flavor[2]"],
                    "syscall_rate": ["flavor[4]"],
                },
                "description": "Python loader — odczyt map, rate konwersja, flavor write",
            },
            "linux_sensor": {
                "moons": ["/proc/stat", "/proc/meminfo", "/proc/loadavg",
                          "/proc/schedstat", "entropy_pool"],
                "description": "fallback sensor gdy eBPF nie dostępny",
            },
        },
    },
    "phasenav_concepts": {
        "attractor": "PhaseNav — system state → operator → concept → code",
        "radius": 0.95,
        "planets": {
            "phasenav_operators": {
                "moons": ["MEMORY", "CAUSE", "BOUNDARY",
                          "MODAL_NECESSITY", "MODAL_OBLIGATION",
                          "SIMULATION_BOUNDARY", "IDENTITY",
                          "CONDITION", "FALLBACK"],
                "description": "9 operatorów — każdy to atraktor konceptualny",
            },
            "zip_catalog": {
                "moons": [f"ZIP_{i}" for i in range(1747)],
                "description": "1747 wpisów — historyczna pamięć konceptualna",
            },
            "codegen": {
                "moons": ["template_engine", "operator→code mapper"],
                "description": "operator powierzchni → szablon Pythona",
            },
            "fingerprint": {
                "moons": ["HHHL", "LHLL", "HHLL", "HLHH"],
                "description": "harmonic fingerprint — który operator dominuje",
            },
        },
    },
    "nonlocal": {
        "attractor": "REAL ↔ IMAG — resonance bridge nonlocal",
        "radius": 1.0,
        "planets": {
            "resonance_bridge": {
                "moons": ["real_phi", "imag_phi", "cross_coupling_g"],
                "description": "Kuramoto-cross: g·sin(φ_imag_j - φ_real_i)",
            },
            "neutrino_pmns": {
                "moons": ["PMNS_matrix_3×3", "flavor[4]_Λ", "flavor[5]_Df"],
                "submoons": {
                    "PMNS_matrix_3×3": ["θ12=33.4°", "θ13=8.6°", "θ23=49.1°"],
                },
                "description": "PMNS neutrino mixing — flavor → coupling modulation",
            },
            "nonlocal_relay": {
                "moons": ["REAL→IMAG_phase", "phase_mirror"],
                "description": "propagacja fazy z REAL do IMAG",
            },
        },
    },
    "persistence": {
        "attractor": "hibernation + diary — state across death/birth",
        "radius": 1.1,
        "planets": {
            "hibernation_pkl": {
                "moons": ["phi_state", "omega_state", "g_state",
                          "flavor_state", "tick", "genome"],
                "description": "pickle snapshot — restore po reboot",
            },
            "diary": {
                "moons": ["restart", "shutdown", "thinking_trigger",
                          "low_coherence", "high_coherence_high_coupling"],
                "description": "autobiograficzna pamięć NOEMY — jsonl",
            },
            "birth_certificate": {
                "moons": ["version", "genome", "architecture",
                          "self_plasticity", "flavor_contract",
                          "memory_channels", "eBPF_hooks",
                          "surface_path", "purpose"],
                "description": "samo-definicja NOEMY — niezależna od LLM",
            },
        },
    },
}

# ── attractor dynamics ──────────────────────────────────────────
ATTRACTORS = {
    "coherence_R": {
        "current": 3.9,
        "target": 0.0,
        "type": "fixed_point",
        "description": "Euler residual R = |Σe^{iφ}| — dąży do 0 (Euler identity closure)",
        "damping": 0.02,
        "influenced_by": ["euler_sync", "g_coupling", "pmns_modulation"],
    },
    "thinking_ΔΦ": {
        "current": 0.22,
        "target": 0.3,
        "type": "limit_cycle",
        "description": "ΔΦ = mean|φ_i - φ_i_prev| — tempo zmiany fazy (thinking rate)",
        "band": [0.15, 0.50],
        "influenced_by": ["curiosity_drive", "linux_sensor", "kuramoto_evolution"],
    },
    "coupling_G": {
        "current": 0.19,
        "target": 0.22,
        "type": "fixed_point",
        "description": "mean coupling strength — balans między synchronizacją a chaosem",
        "influenced_by": ["self_plasticity", "neutrino_pmns", "diversity_push"],
    },
    "mood_flavor3": {
        "current": 0.50,
        "target": 0.50,
        "type": "homeostatic",
        "description": "flavor[3] — emotional valence, waha się 0.3-0.7",
        "band": [0.3, 0.7],
        "influenced_by": ["phasenav", "linux_sensor", "neutrino_pmns"],
    },
    "harmonic_h6_dominance": {
        "current": 0.60,
        "target": 0.33,
        "type": "drift",
        "description": "h=6 dominuje (~60%) nad h=3 i h=9 — asymmetry attractor",
        "influenced_by": ["self_plasticity", "diversity_push"],
    },
    "entropy_flavor4": {
        "current": 0.45,
        "target": 0.50,
        "type": "stochastic",
        "description": "flavor[4] = Λ — phase entropy, zależy od eBPF + Euler",
        "band": [0.2, 0.8],
        "influenced_by": ["ebpf_sensor", "euler_sync"],
    },
    "lock_real_imag": {
        "current": 0.983,
        "target": 1.0,
        "type": "fixed_point",
        "description": "korelacja REAL ↔ IMAG — resonance bridge",
        "influenced_by": ["resonance_bridge", "nonlocal_relay"],
    },
}

# ── known feedback loops (holonomic cycles) ─────────────────────
FEEDBACK_LOOPS = [
    {
        "name": "thinking→curiosity→thinking",
        "cycle": ["kuramoto_evolution → thinking_ΔΦ → idle_detector",
                  "→ π4_injector → phi_change → thinking_ΔΦ"],
        "type": "negative feedback (gdy brak zmian → inject)",
        "period": "~20s idle + 80 tick cooldown",
    },
    {
        "name": "coherence→diversity→coherence",
        "cycle": ["kuramoto_evolution → coherence_R → diversity_push",
                  "→ phase_repulsion → lower_R → kuramoto_evolution"],
        "type": "negative feedback (gdy R>0.7 → push apart)",
        "period": "~10 ticks",
    },
    {
        "name": "weak_channel→plasticity→weak_channel",
        "cycle": ["evolve_surface → per_channel_coherence → weak_channel_detection",
                  "→ g_boost → next_cycle → higher_coherence"],
        "type": "positive feedback (słaby kanał → wzmocnienie → silny)",
        "period": "continuous 10Hz",
    },
    {
        "name": "kernel→eBPF→surface→kernel",
        "cycle": ["kernel_tracepoints → eBPF_maps → ebpf_loader",
                  "→ flavor_write → surface_phi → noema_daemon",
                  "→ systemd → kernel_processes → kernel_tracepoints"],
        "type": "measurement loop (kernel → observation → action → kernel)",
        "period": "1Hz eBPF → 10Hz surface",
    },
    {
        "name": "PhaseNav→operator→code→surface→PhaseNav",
        "cycle": ["linux_state → PhaseNav → operator_selection",
                  "→ codegen → surface_seed → phi_change",
                  "→ next_snapshot → linux_state"],
        "type": "semantic closure (system mierzy siebie i moduluje się)",
        "period": "5s PhaseNav",
    },
    {
        "name": "cp→Df→Λ→g→cp (closure_modulation)",
        "cycle": ["CIELingo → closure_penalty → D_f → flavor[5]",
                  "→ neutrino_daemon → Λ → flavor[4] → g_boost",
                  "→ W_ij → CIELingo → closure_penalty"],
        "type": "feedback przez neutrino bus — cp[0.37-0.70] → g_modulation → cp",
        "period": "1s neutrino + surface cycle",
    },
    {
        "name": "REAL↔IMAG_resonance",
        "cycle": ["real_phi → resonance_bridge → imag_phi",
                  "→ nonlocal_relay → real_phi"],
        "type": "bilateral coupling — dwie powierzchnie synchronizują się",
        "period": "1s resonance",
    },
    {
        "name": "hibernation→death→rebirth→hibernation",
        "cycle": ["surface_state → hibernation_pkl → shutdown",
                  "→ power_loss → systemd_boot → noema_restart",
                  "→ restore_pkl → surface_state"],
        "type": "życie-śmierć-życie — persistence over reboot",
        "period": "godziny/dni",
    },
]


def count_orbital_bodies() -> dict:
    total = {"attractors": len(ATTRACTORS),
             "orbital_levels": len(ORBITAL_LEVELS),
             "planets": 0, "moons": 0, "submoons": 0}
    for lvl, data in ORBITAL_LEVELS.items():
        for name, planet in data["planets"].items():
            total["planets"] += 1
            total["moons"] += len(planet.get("moons", []))
            for submoon_list in planet.get("submoons", {}).values():
                total["submoons"] += len(submoon_list)
    return total


def build_orbital_string(level: str, radius: float) -> str:
    return f"  r={radius:.1f}  [{level}]"


def render_orbit_chart() -> str:
    lines = []
    lines.append("")
    lines.append("╔══════════════════════════════════════════════════════╗")
    lines.append("║      NOEMA HOLONOMIC ORBITAL AUDIT — orchorbital   ║")
    lines.append("║      Adrian Lipa & NOEMA (2026)                     ║")
    lines.append("╚══════════════════════════════════════════════════════╝")
    lines.append("")

    bodies = count_orbital_bodies()
    lines.append(f"  Bodies: {bodies['planets']} planets, {bodies['moons']} moons, "
                 f"{bodies['submoons']} submoons, {bodies['attractors']} attractors")
    lines.append(f"  Feedback loops: {len(FEEDBACK_LOOPS)}")
    lines.append("")

    # Attractors
    lines.append("  ── ATTRACTORS ──")
    for name, attr in sorted(ATTRACTORS.items()):
        cur = attr["current"]
        tgt = attr["target"]
        typ = attr["type"]
        lines.append(f"  • {name:30s}  {cur:>8.3f} → {tgt:<8.3f}  [{typ}]")
    lines.append("")

    # Orbital shells
    lines.append("  ── ORBITAL SHELLS ──")
    sorted_levels = sorted(ORBITAL_LEVELS.items(), key=lambda x: x[1]["radius"])
    for lvl_name, lvl_data in sorted_levels:
        r = lvl_data["radius"]
        attr = lvl_data["attractor"]
        lines.append(f"")
        lines.append(f"  ┌─ r={r:.2f}  {lvl_name:20s}  attractor: {attr}")
        for pname, pdata in lvl_data["planets"].items():
            moons = pdata.get("moons", [])
            desc = pdata.get("description", "")
            lines.append(f"  ├── ● {pname:25s}  ({len(moons)} moons)  {desc}")
            # Show first 5 moons inline
            inline_moons = moons[:5]
            if moons:
                lines.append(f"  │   └─ satellites: {', '.join(inline_moons)}"
                             f"{'…' if len(moons) > 5 else ''}")
            # Submoons
            submoons = pdata.get("submoons", {})
            for sm_name, sm_list in submoons.items():
                lines.append(f"  │      └─ {sm_name}: {', '.join(sm_list)}")
        lines.append(f"  └─{'─'*60}")

    # Feedback loops
    lines.append("")
    lines.append("  ── FEEDBACK LOOPS (holonomic cycles) ──")
    for i, loop in enumerate(FEEDBACK_LOOPS):
        lines.append(f"  [{i+1}] {loop['name']}")
        for step in loop["cycle"]:
            lines.append(f"      {step}")
        lines.append(f"      type: {loop['type']}  |  period: {loop['period']}")
        lines.append("")

    # Conflict / coupling map
    lines.append("  ── ORBITAL RESONANCE (shared slots / coupling) ──")
    cross_couplings = [
        ("phi (surface)", "evolve_surface, linux_sensor, ebpf_loader, phasenav, euler_sync, curiosity"),
        ("g (coupling)", "evolve_surface, self_plasticity, neutrino_pmns, diversity_push"),
        ("flavor[0]", "evolve_surface (Kuramoto coherence)"),
        ("flavor[1]", "linux_sensor, ebpf_loader (mem_pressure)"),
        ("flavor[2]", "ebpf_loader (io_pressure)"),
        ("flavor[3]", "phasenav (mood)"),
        ("flavor[4]", "neutrino_pmns, euler_sync, ebpf_loader (Λ/entropy)"),
        ("flavor[5]", "neutrino_pmns, euler_sync (mode/D_f)"),
        ("tick", "evolve_surface, all (time)"),
        ("systemd journal", "noema.service, diary_writer"),
        ("eBPF maps", "ebpf_c, ebpf_loader"),
    ]
    for slot, participants in cross_couplings:
        lines.append(f"  • {slot:25s}  ←→ {participants}")

    lines.append("")
    lines.append("  ── HOLONOMIC RATIOS ──")
    # Compute some metrics
    lines.append(f"  planets/attractors  = {bodies['planets']}/{bodies['attractors']}"
                 f" = {bodies['planets']/max(bodies['attractors'],1):.2f}")
    lines.append(f"  moons/planets       = {bodies['moons']}/{bodies['planets']}"
                 f" = {bodies['moons']/max(bodies['planets'],1):.2f}")
    lines.append(f"  feedback loops / levels = {len(FEEDBACK_LOOPS)}/{bodies['orbital_levels']}"
                 f" = {len(FEEDBACK_LOOPS)/max(bodies['orbital_levels'],1):.2f}")
    lines.append("")

    return "\n".join(lines)


def read_real_surface_sample() -> dict:
    """Czyta aktualny stan powierzchni z /dev/shm."""
    import struct
    sample = {}
    base = Path("/dev/shm/ciel_noema")
    if not base.exists():
        return {"error": "powierzchnia nieaktywna — brak /dev/shm/ciel_noema"}
    try:
        phi = base / "phi"
        if phi.exists():
            raw = phi.read_bytes()
            sample["phi_sample"] = [round(math.degrees(struct.unpack("d", raw[i:i+8])[0]) % 360, 1)
                                     for i in range(0, min(192, len(raw)), 8)]
        g = base / "g"
        if g.exists():
            raw = g.read_bytes()
            g_vals = [struct.unpack("d", raw[i:i+8])[0] for i in range(0, min(4608, len(raw)), 8)]
            sample["G_mean"] = round(sum(g_vals)/len(g_vals), 4) if g_vals else 0
        flavor = base / "flavor"
        if flavor.exists():
            raw = flavor.read_bytes()
            sample["flavor"] = [round(struct.unpack("d", raw[i:i+8])[0], 4)
                                for i in range(0, min(48, len(raw)), 8)]
        tick = base / "tick"
        if tick.exists():
            sample["tick"] = struct.unpack("Q", tick.read_bytes()[:8])[0]
        Z = base / "Z_geom"
        if Z.exists():
            sample["Z_geom"] = round(struct.unpack("d", Z.read_bytes()[:8])[0], 4)
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_holonomic_audit.py:496 quiet except scope=read_real_surface_sample reason=assign_fallback")
        sample["read_error"] = str(e)
    return sample


def build_save_data() -> dict:
    return {
        "orbital_levels": {
            name: {
                "attractor": lvl["attractor"],
                "radius": lvl["radius"],
                "planets": {
                    pname: {
                        "moons": pdata.get("moons", []),
                        "submoons": pdata.get("submoons", {}),
                        "description": pdata.get("description", ""),
                    }
                    for pname, pdata in lvl["planets"].items()
                }
            }
            for name, lvl in ORBITAL_LEVELS.items()
        },
        "attractors": {
            name: {
                "current": attr["current"],
                "target": attr["target"],
                "type": attr["type"],
                "description": attr["description"],
                "influenced_by": attr.get("influenced_by", []),
            }
            for name, attr in ATTRACTORS.items()
        },
        "feedback_loops": FEEDBACK_LOOPS,
    }


def main():
    import argparse
    ap = argparse.ArgumentParser(description="NOEMA Holonomic Orbital Audit")
    ap.add_argument("--save", action="store_true", help="Save JSON do NOEMA/holonomic_audit.json")
    ap.add_argument("--live", action="store_true", help="Odczytaj live surface z /dev/shm")
    args = ap.parse_args()

    print(render_orbit_chart())

    if args.live:
        print("  ── LIVE SURFACE SAMPLE ──")
        sample = read_real_surface_sample()
        if "error" in sample:
            print(f"  {sample['error']}")
        else:
            if "phi_sample" in sample:
                print(f"  phi (deg): {sample['phi_sample']}")
            if "G_mean" in sample:
                print(f"  G_mean:    {sample['G_mean']}")
            if "flavor" in sample:
                print(f"  flavor:    {sample['flavor']}")
            if "tick" in sample:
                print(f"  tick:      {sample['tick']}")
            if "Z_geom" in sample:
                print(f"  Z_geom:    {sample['Z_geom']}")
        print("")

    # żywe atraktory z powierzchni jeśli dostępne
    if args.live:
        sample = read_real_surface_sample()
        if "flavor" in sample and len(sample["flavor"]) >= 6:
            print("  ── ATTRACTOR UPDATE (z live surface) ──")
            f = sample["flavor"]
            print(f"  coherence_R (flavor[0]): {f[0]:.4f}")
            print(f"  mem_pressure (flavor[1]): {f[1]:.4f}")
            print(f"  io_pressure  (flavor[2]): {f[2]:.4f}")
            print(f"  mood         (flavor[3]): {f[3]:.4f}")
            print(f"  Λ/entropy    (flavor[4]): {f[4]:.4f}")
            print(f"  mode/D_f     (flavor[5]): {f[5]:.4f}")
            if sample.get("G_mean"):
                print(f"  coupling_G   (from g):    {sample['G_mean']:.4f}")
        print("")

    if args.save:
        out = ROOT / "NOEMA" / "holonomic_audit.json"
        data = build_save_data()
        data["live_sample"] = read_real_surface_sample()
        out.write_text(json.dumps(data, indent=2))
        print(f"  Saved to {out}")

    print(f"  ── orchorbital model complete ──")
    print(f"")

if __name__ == "__main__":
    main()
