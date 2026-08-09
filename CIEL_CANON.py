"""CIEL_CANON.py — Canonical entrypoint for NOEMA / CIELingo.

Usage:
    python3 CIEL_CANON.py                       # full status
    python3 CIEL_CANON.py --probe               # live warp + holonomy
    python3 CIEL_CANON.py --up                  # start all daemons
    python3 CIEL_CANON.py --down                # stop all daemons
    python3 CIEL_CANON.py --sonic               # sonic screwdriver probe
    python3 CIEL_CANON.py --self                # self-model (identity)
    python3 CIEL_CANON.py --search <query>      # PhaseNav library search
    python3 CIEL_CANON.py --gaps                # knowledge gaps
    python3 CIEL_CANON.py --sync                # dual-surface sync status
    python3 -m pytest tests/ -q                 # run tests
"""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import json
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
SRC = str(ROOT / "src")
sys.path.insert(0, SRC)

from ciel_geometry.noema_config import config
from ciel_geometry.daemon_registry import Registry
from ciel_geometry.phasenav.operator_algebra import (
    generate_operator_map, connection_matrix, statistical_closure,
    holonomy, surface_holonomy,
)

VERSION = (ROOT / "VERSION").read_text().strip() if (ROOT / "VERSION").exists() else "0.1.0"

DAEMONS = [
    "noema-kuramoto",
    "noema-phasenav",
    "noema-neutrino",
    "noema-resonance-bridge",
    "noema-linux-sensor",
    "noema-cielingo-sync",
    "noema-nonlocal-proxy",
    "noema-agent-backend",
    "noema-consolidator",
]


def _fmt(val, width: int = 8) -> str:
    if isinstance(val, float):
        return f"{val:.{width - 4}f}".rjust(width)
    return str(val).rjust(width)


def print_daemon_status() -> None:
    result = subprocess.run(
        ["systemctl", "--user", "list-units", "noema-*", "--no-pager"],
        capture_output=True, text=True, timeout=5,
    )
    lines = [l for l in result.stdout.splitlines() if "noema" in l and "noema-" in l]
    print(f"  {'UNIT':36s} {'ACTIVE':10s} {'SUB':12s}")
    print(f"  {'─'*36} {'─'*10} {'─'*12}")
    for line in lines:
        parts = line.split()
        if len(parts) >= 3:
            name = parts[0][:36]
            active = parts[1][:10]
            substate = parts[2][:12]
            icon = "●" if substate == "running" else "○"
            print(f"  {icon} {name:36s} {active:10s} {substate:12s}")

    try:
        reg = Registry()
        entries = reg.scan()
        if entries:
            print()
            print(f"  Registry heartbeats ({len(entries)} daemons):")
            for d in entries:
                alive = "●" if d.alive else "○"
                print(f"    {alive} {d.name:20s} pid={d.pid:<6} tick={d.tick:<8} "
                      f"uptime={d.uptime:5.0f}s cpu={d.cpu:.1f}%")
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("CIEL_CANON.py:85 quiet except scope=print_daemon_status reason=pass")
        pass


def print_warp_loop() -> None:
    """Print the shared surface using its current typed slot contract."""
    try:
        from ciel_geometry.noema_surface_mmap import ensure_surface
        from ciel_sot_agent.pnv_surface_oracle import observe_surface

        s = ensure_surface()
        observation, state = observe_surface(s)
    except Exception:
        print("  Surface not available")
        return

    phi = np.asarray(state.phase36, dtype=np.float64)
    g = np.asarray(s["g"], dtype=np.float64)
    omega = np.asarray(s["omega"], dtype=np.float64)
    payload = observation.payload
    gravity = payload.get("gravity", {})
    flavor = payload.get("flavor", {})
    tick = int(payload.get("tick", 0))

    z = np.exp(1j * phi)
    euler = np.abs(z.sum())
    phi_mean = float(np.angle(z.mean()))

    print(f"  Tick:            {tick}")
    print(f"  φ̄:               {phi_mean:.4f}  σ={float(np.std(phi)):.4f}")
    print(f"  ω̄:               {float(np.mean(omega)):.2f} Hz")
    print(f"  R (order):       {float(state.order_parameter or 0.0):.4f}")
    print(f"  |Σe^iφ|:         {euler:.4f}")
    print(f"  |g| mean:        {float(np.mean(np.abs(g))):.4f}")
    print(f"  semantic density:{float(gravity.get('semantic_density', 0.0)):.4f}")
    tau = float(gravity.get("tau_dilation", 0.0))
    print(f"  γ (time dilation):{tau:.4f}  {'🐢 TARDIS' if tau > 1.05 else '1:1'}")
    print(f"  mass total:      {float(gravity.get('mass_total', 0.0)):.4f}")
    unruh = float(gravity.get("unruh_power", 0.0))
    print(f"  unruh power:     {unruh:.8f}  {'⏎ WARP' if unruh > 1e-6 else 'latent'}")
    print(f"  coherence:       {float(flavor.get('coherence', 0.0)):.4f}")
    print(f"  memory pressure: {float(flavor.get('memory_pressure', 0.0)):.4f}")
    print(f"  I/O pressure:    {float(flavor.get('io_pressure', 0.0)):.4f}")
    print(f"  mood:            {float(flavor.get('mood', 0.0)):.4f}")
    print(f"  entropy/openness:{float(flavor.get('entropy_openness', 0.0)):.4f}")
    closure = payload.get("closure_score")
    if closure is not None:
        print(f"  closure score:   {float(closure):.4f}")


def print_holonomy() -> None:
    try:
        ops = generate_operator_map()
        A = connection_matrix(ops)
        sc = statistical_closure(ops)
        sv, _ = surface_holonomy(
            np.asarray(
                __import__("ciel_geometry.noema_surface_mmap", fromlist=["ensure_surface"])
                .ensure_surface()["phi"], dtype=np.float64
            )
        )

        print(f"  Gauge rank:      {sc.get('gauge_rank', 0)} / {len(ops)}")
        print(f"  Closure score:   {sc.get('closure_score', 0):.4f}")
        print(f"  Mean curvature:  {sc.get('mean_curvature', 0):.6f}")
        print(f"  Mean |A|:        {float(np.mean(np.abs(A))):.4f}")
        print(f"  Max |A|:        {float(np.max(np.abs(A))):.4f}")
        print(f"  Surface γ:       {sv:.4f} rad")

        best: list[tuple[float, list[str]]] = []
        oids = list(ops.keys())
        for i in range(min(len(oids), 10)):
            for j in range(min(len(oids), 10)):
                if i >= j:
                    continue
                for k in range(min(len(oids), 10)):
                    if k in (i, j):
                        continue
                    path = [oids[i], oids[j], oids[k]]
                    g = abs(holonomy(path, ops))
                    if g > 0.5:
                        best.append((g, path))
        best.sort(reverse=True)
        if best:
            print("  Top 3 holonomic paths:")
            for g, path in best[:3]:
                print(f"    γ={g:.4f}  {' → '.join(path)}")
    except Exception as e:
        print(f"  Holonomy: {e}")


def print_consolidator() -> None:
    status_path = Path("/home/adrian/new_volume_rw/CIEL_memories/local_test/.status.json")
    if not status_path.exists():
        print("  Consolidator: no status file")
        return
    try:
        st = json.loads(status_path.read_text())
        print(f"  Daemon:          {'● running' if st.get('running') else '○ stopped'}")
        print(f"  PID:             {st.get('pid')}")
        print(f"  Cycle:           {st.get('cycle')}")
        print(f"  Mode:            {'dry-run' if st.get('dry_run') else 'live'}")
    except Exception as e:
        print(f"  Consolidator: {e}")


def cmd_status() -> None:
    print()
    print(f"╔═══ NOEMA v{VERSION} ═══════════════════════════════════════╗")
    print()

    print("┌─ Daemons ─────────────────────────────────────────────┐")
    print_daemon_status()
    print("└────────────────────────────────────────────────────────┘")
    print()

    print("┌─ Warp Loop ───────────────────────────────────────────┐")
    print_warp_loop()
    print("└────────────────────────────────────────────────────────┘")
    print()

    print("┌─ Holonomy ────────────────────────────────────────────┐")
    print_holonomy()
    print("└────────────────────────────────────────────────────────┘")
    print()

    print("┌─ Consolidator ────────────────────────────────────────┐")
    print_consolidator()
    print("└────────────────────────────────────────────────────────┘")
    print()

    print(f"╚════════════════════════════════════════════════════════╝")
    print()


def cmd_probe() -> None:
    """Live probe — like sonic screwdriver."""
    from ciel_geometry.noema_surface_mmap import ensure_surface
    s = ensure_surface()
    phi = np.asarray(s["phi"], dtype=np.float64)
    g = np.asarray(s["g"], dtype=np.float64)
    gravity = np.asarray(s["gravity"], dtype=np.float64)
    tick = int(np.asarray(s["tick"], dtype=np.uint64)[0])
    z = np.exp(1j * phi)
    print(f"tick={tick}  φ̄={float(np.mean(phi)):.3f}  R={np.abs(z.mean()):.4f}  "
          f"γ={gravity[1]:.2f}  unruh={gravity[3]:.4f}  |g|̄={np.mean(np.abs(g)):.4f}")


def cmd_up() -> None:
    subprocess.run(["systemctl", "--user", "start", "noema.target"], check=False)
    subprocess.run(["systemctl", "--user", "start", "noema-consolidator"], check=False)
    print("NOEMA daemons started.  python3 CIEL_CANON.py  to verify.")


def cmd_down() -> None:
    for d in reversed(DAEMONS):
        subprocess.run(["systemctl", "--user", "stop", d], check=False)
    subprocess.run(["systemctl", "--user", "stop", "noema.target"], check=False)
    print("NOEMA daemons stopped.")


def cmd_sonic() -> None:
    """Launch sonic screwdriver watch."""
    from scripts import noema_sonic_daemon
    noema_sonic_daemon.main()


def cmd_self() -> None:
    """Print self-model (identity)."""
    from scripts.noema_self_reflect import SelfModel
    sm = SelfModel()
    identity = sm.identity()
    print()
    print("  ╔══ NOEMA Self-Model ═══╗\n")
    print(f"  Name:      {identity['name']}")
    print(f"  Creator:   {identity['creator']}")
    print(f"  Status:    {identity['status']}")
    print()
    print("  Knowledge:")
    for k, v in identity['knowledge'].items():
        print(f"    {k}: {v}")
    print()
    print("  Now:")
    for k, v in identity['state'].items():
        print(f"    {k}: {v}")
    print()
    if identity.get('holonomy'):
        print("  Geometry:")
        for k, v in identity['holonomy'].items():
            print(f"    {k}: {v}")
    print()
    print("  Core Identity (top connections):")
    for n in identity['core_identity']:
        print(f"    ● {n['label']:30s}  ({n['type']}, {n['connections']} connections)")
    print()
    print("  ╚══════════════════════╝\n")


def cmd_search(query: str) -> None:
    """Typed Octopus-RAG library search with canonical precise PNV36 geometry."""
    from ciel_sot_agent.pnv_rag_arm import query_text

    results = query_text(query, top_k=10)
    print()
    print(f"  ╔══ PhaseNav Search: {query[:50]} ═══╗\n")
    for item in results:
        tfidf = float(item.get("similarity", 0.0))
        phase = float(item.get("phase_alignment", item.get("gamma", 0.0)))
        print(f"  ○ tfidf={tfidf:.4f}  phase={phase:.4f}  {item['filename'][:55]}")
        details = "  ".join(part for part in (item.get("author", ""), item.get("topic", "")) if part)
        if details:
            print(f"     {details}")
    print()


def cmd_gaps() -> None:
    """Print knowledge gaps."""
    from scripts.noema_self_reflect import SelfModel
    sm = SelfModel()
    gaps = sm.gaps()
    print()
    print("  ╔══ Knowledge Gaps ═══╗\n")
    print(f"  Total isolated topics: {gaps['total_isolated']}")
    print("\n  Least connected topics:")
    for g in gaps['isolated_topics'][:10]:
        print(f"    {g['topic']}")
    print("\n  Author coverage:")
    for author, cov in gaps['author_coverage'].items():
        print(f"    {author:40s}  ({cov} connections)")
    print()


if __name__ == "__main__":
    if "--probe" in sys.argv:
        cmd_probe()
    elif "--up" in sys.argv:
        cmd_up()
    elif "--down" in sys.argv:
        cmd_down()
    elif "--sonic" in sys.argv:
        cmd_sonic()
    elif "--self" in sys.argv:
        cmd_self()
    elif "--search" in sys.argv:
        idx = sys.argv.index("--search")
        query = " ".join(sys.argv[idx + 1:]) if idx + 1 < len(sys.argv) else ""
        cmd_search(query)
    elif "--gaps" in sys.argv:
        cmd_gaps()
    elif "--sync" in sys.argv:
        from scripts.noema_dual_sync import status
        st = status()
        print()
        print("  ╔══ Dual-Surface Sync ═══╗\n")
        print(f"  Real tick:   {st.get('tick_real', '?')}")
        print(f"  Imag tick:   {st.get('tick_imag', '?')}")
        print(f"  Diff:        {st.get('tick_diff', '?')}")
        print(f"  R_sync:      {st.get('R_sync', 0):.4f}  {'✓ LOCK' if st.get('R_sync', 0) > 0.9 else '○'}")
        print(f"  std Δ:       {st.get('std_delta', 0):.4f}")
        print(f"  Overlap:     {st.get('overlap', 0):.4f}")
        print(f"  M0 cos:      {st.get('m0_cos', 0):.4f}  (perceptual)")
        print(f"  M4 cos:      {st.get('m4_cos', 0):.4f}  (procedural)")
        print(f"  M0 std:      {st.get('m0_std', 0):.4f}  {'✓' if st.get('m0_std', 0) < 0.3 else '○'}")
        print(f"  M4 std:      {st.get('m4_std', 0):.4f}  {'✓' if st.get('m4_std', 0) < 0.3 else '○'}")
        svc = subprocess.run(['systemctl', '--user', 'is-active', 'noema-dual-sync'],
                           capture_output=True, text=True, timeout=3)
        print(f"  Daemon:      {'● active' if svc.stdout.strip() == 'active' else '○ stopped'}")
        print()
    else:
        cmd_status()
