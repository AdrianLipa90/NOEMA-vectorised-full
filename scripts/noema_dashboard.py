#!/usr/bin/env python3
"""noema-dashboard — terminal monitor NOEMA (24 oscylatory + serwer urojony + Linux).

Użycie:
    .venv/bin/python3 scripts/noema_dashboard.py
    .venv/bin/python3 scripts/noema_dashboard.py --dev   # development mode
    .venv/bin/python3 scripts/noema_dashboard.py --once  # pojedynczy snapshot

Klawisze:
    q/ESC — wyjście    r — refresh    p — sortuj procesy po CPU
    m — sortuj po MEM    o — toggle oscylatorów (8/24)    h — help
"""

from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import os
import struct
import sys
import time
from pathlib import Path

import numpy as np

SURFACE = Path("/dev/shm/ciel_noema")
IMAGINAL = Path("/dev/shm/ciel_noema_imaginal")

CHANNELS = np.array([
    "M0_PERCEPT", "M1_WORKING", "M2_MEMORY", "M3_AFFECT",
    "M4_MOTO", "M5_IDENTITY", "M6_EXEC", "M7_BRAID",
    "M8_PERC2", "M9_WORK2", "M10_MEM2", "M11_AFF2",
    "M12_SCOPE", "M13_MODAL", "M14_TENSE", "M15_ASPECT",
    "M16_EVID", "M17_NEG", "M18_CAUSE", "M19_COND",
    "M20_PURP", "M21_MANN", "M22_DEG", "M23_DISC",
])

GRAV_LABELS = ["density", "γ", "mass", "unruh", "scars", "agent", "rate", "sever"]
FLAV_LABELS = ["cpu_coh", "mem_pr", "io_wait", "load_mood", "entropy", "sys_mode"]

# ── wektoryzowany reader ──────────────────────────────────────────


def read_mmap(path: Path, n: int = 24) -> np.ndarray:
    try:
        raw = path.read_bytes()
        if len(raw) >= n * 8:
            return np.frombuffer(raw[:n * 8], dtype=np.float64).copy()
    except (FileNotFoundError, OSError):
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_dashboard.py:47 quiet except scope=read_mmap reason=pass")
        pass
    return np.zeros(n, dtype=np.float64)


def read_tick() -> int:
    try:
        raw = (SURFACE / "tick").read_bytes()
        return struct.unpack("Q", raw[:8])[0] if len(raw) >= 8 else 0
    except (FileNotFoundError, OSError):
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_dashboard.py:56 quiet except scope=read_tick reason=return 0")
        return 0

# ── wektoryzowane metryki ─────────────────────────────────────────


def osc_metrics(phi: np.ndarray) -> dict:
    """Wszystkie metryki z 24-fazowego wektora — zero pętli."""
    p_norm = np.mod(phi, 2 * np.pi) / (2 * np.pi)
    z = np.exp(1j * phi)
    R = abs(z.sum())
    coh = R / max(len(phi), 1)
    # klasyfikacja faz
    green = np.sum(p_norm < 0.33)
    yellow = np.sum((p_norm >= 0.33) & (p_norm < 0.66))
    red = np.sum(p_norm >= 0.66)
    return {
        "R": R, "coh": coh, "green": green, "yellow": yellow, "red": red,
        "p_norm": p_norm, "z": z,
    }


def sync_metric(phi_a: np.ndarray, phi_b: np.ndarray) -> float:
    """R_sync między dwiema powierzchniami."""
    return float(np.abs(np.mean(np.exp(1j * (phi_a - phi_b)))))


def top_processes(n: int = 8, sort_by: str = "cpu") -> list[dict]:
    try:
        import psutil
        procs = []
        for p in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]):
            try:
                info = p.info
                if info["cpu_percent"] is not None and info["cpu_percent"] > 0.5:
                    procs.append(info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_dashboard.py:92 quiet except scope=top_processes reason=pass")
                pass
        key = "cpu_percent" if sort_by == "cpu" else "memory_percent"
        procs.sort(key=lambda x: x[key] or 0, reverse=True)
        return procs[:n]
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_dashboard.py:97 quiet except scope=top_processes reason=return []")
        return []


def linux_load() -> dict:
    try:
        l = open("/proc/loadavg").read().split()
        cpu_info = open("/proc/stat").readlines()[0].split()
        idle = int(cpu_info[4])
        total = sum(int(x) for x in cpu_info[1:])
        mem = open("/proc/meminfo").read().split()
        mt = int(mem[mem.index("MemTotal:") + 1])
        ma = int(mem[mem.index("MemAvailable:") + 1])
        return {
            "load": float(l[0]),
            "load5": float(l[1]),
            "load15": float(l[2]),
            "cpu_idle": idle,
            "cpu_total": total,
            "mem_pct": 100 * (mt - ma) / mt if mt else 0,
            "mem_gb": (mt - ma) / 1e6,
            "total_gb": mt / 1e6,
            "procs": int(l[3].split("/")[0]),
            "total_procs": int(l[3].split("/")[1]),
        }
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_dashboard.py:122 quiet except scope=linux_load reason=return {\"load\": 0, \"mem_pct\": 0, \"mem_gb\": 0}")
        return {"load": 0, "mem_pct": 0, "mem_gb": 0}

# ── systemd ────────────────────────────────────────────────────────


def daemon_status() -> list[dict]:
    try:
        import subprocess
        r = subprocess.run(
            ["systemctl", "--user", "list-units", "noema-*", "--no-pager",
             "--plain", "--no-legend"],
            capture_output=True, text=True, timeout=5,
        )
        out = []
        for line in r.stdout.strip().split("\n"):
            parts = line.split()
            if len(parts) >= 3:
                out.append({"unit": parts[0], "status": parts[2]})
        return out
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_dashboard.py:142 quiet except scope=daemon_status reason=return []")
        return []

# ── render ─────────────────────────────────────────────────────────


def _bar(pct: float, width: int = 16) -> str:
    """Pasek postępu — numpy-free, czysty str."""
    filled = int(pct * width)
    return "█" * filled + "░" * (width - filled)


def render_tui(console, show_osc: int = 24, sort_procs: str = "cpu") -> str:
    """Wektoryzowany render — wszystkie obliczenia numpy, składanie str."""
    from rich.table import Table
    from rich.panel import Panel
    from rich.text import Text
    from rich.columns import Columns
    from rich.layout import Layout
    from rich.align import Align
    from rich.style import Style

    # ── READ (wektoryzowany) ──
    phi = read_mmap(SURFACE / "phi", 24)
    omega = read_mmap(SURFACE / "omega", 24)
    gravity = read_mmap(SURFACE / "gravity", 8)
    flavor = read_mmap(SURFACE / "flavor", 6)
    tick = read_tick()

    phi_i = read_mmap(IMAGINAL / "phi", 24) if IMAGINAL.exists() else np.zeros(0)
    omega_i = read_mmap(IMAGINAL / "omega", 24) if IMAGINAL.exists() else np.zeros(0)

    # analog bus
    a_hot = read_mmap(SURFACE / "analog" / "phi_hot", 24) \
        if (SURFACE / "analog" / "phi_hot").exists() else np.zeros(0)
    a_temp = read_mmap(SURFACE / "analog" / "temp", 1)[0] \
        if (SURFACE / "analog" / "temp").exists() else 0.0

    # ── METRYKI (wektoryzowane) ──
    m = osc_metrics(phi)
    m_i = osc_metrics(phi_i) if len(phi_i) == 24 else None
    sysinfo = linux_load()
    daemons = daemon_status()

    # Euler
    R = m["R"]
    z_sum = m["z"].sum()

    # real surface bars — wektoryzowane
    p_norm = m["p_norm"]
    bars_vec = np.clip((p_norm * 16).astype(int), 0, 16)
    colors = np.where(p_norm < 0.33, "green",
                      np.where(p_norm < 0.66, "yellow", "red"))

    # ── HEADER ──
    uptime_s = time.time() - _start_time
    hz = omega * 0.159
    mean_hz = float(np.mean(np.abs(hz)))

    alive_n = sum(1 for d in daemons if d.get("status") == "active") if daemons else 0

    hdr = Text()
    hdr.append("NOEMA", style="bold cyan")
    hdr.append(f"  t:{tick}", style="bold white")
    hdr.append(f"  up:{int(uptime_s//3600)}h{int((uptime_s%3600)//60)}m", style="dim")
    hdr.append(f"  load:{sysinfo['load']:.2f}", style="white")
    hdr.append(f"  MEM:{sysinfo['mem_pct']:.0f}%", style="green" if sysinfo['mem_pct'] < 80 else "red")
    hdr.append(f"  procs:{sysinfo['procs']}", style="dim")
    hdr.append(f"  coh:{m['coh']:.3f}", style="bold green" if m['coh'] > 0.5 else "bold yellow")
    hdr.append(f"  ω̄:{float(np.mean(np.abs(omega))):.2f}", style="cyan")
    hdr.append(f"  Hz̄:{mean_hz:.2f}", style="dim")
    hdr.append(f"  daemons:{alive_n}", style="blue" if alive_n > 10 else "red")
    hdr.append(f"  Σe^iφ={abs(z_sum):.2f}", style="yellow")

    header = Panel(hdr, style="bold")

    # ── 24 OSCILLATORS (wektoryzowane) ──
    osc_lines = []
    half = show_osc // 2
    for i in range(show_osc):
        b = "█" * bars_vec[i] + "░" * (16 - bars_vec[i])
        hz_str = f"{abs(omega[i])*0.159:5.2f}Hz" if abs(omega[i]) > 0.01 else "     -"
        osc_lines.append(
            f"[{colors[i]}]{i:02d} {CHANNELS[i]:<9}[/{colors[i]}] "
            f"[{colors[i]}]{b}[/{colors[i]}] "
            f"[cyan]{omega[i]:6.2f}[/cyan] "
            f"[dim]{hz_str}[/dim]"
        )

    osc_col1 = Text("\n".join(osc_lines[:half]))
    osc_col2 = Text("\n".join(osc_lines[half:]))

    # coherence bar
    coh_bar = _bar(m["coh"], 20)
    euler_info = Text(
        f"  [bold]Euler Σe^iφ[/bold]  |Σ|={R:.2f}  R/24={R/24:.3f}\n"
        f"  {'LOW (locked)' if R < 6 else 'HIGH (drifting)'}\n"
        f"  coh [green]●[/] {m['green']}  [yellow]●[/] {m['yellow']}  [red]●[/] {m['red']}\n"
        f"  [green]{coh_bar}[/] {m['coh']:.4f}"
    )

    osc_panel = Panel(
        Columns([osc_col1, osc_col2, euler_info], equal=True),
        title=f"24 Kuramoto Oscillators — harmonic φ_eff (3-6-9)",
        border_style="cyan",
    )

    # ── SYSTEM + PROCESSES (z linux_cards) ──
    sys_t = Table(show_header=False, box=None, padding=(0, 2))
    sys_t.add_column("k", style="bold")
    sys_t.add_column("v")
    sys_t.add_column("k2", style="bold")
    sys_t.add_column("v2")
    sys_t.add_row("CPU load", f"{sysinfo['load']:.2f}",
                  "Mem", f"{sysinfo['mem_gb']:.1f}/{sysinfo['total_gb']:.0f} GB")
    sys_t.add_row("Load 5/15", f"{sysinfo['load5']:.2f} / {sysinfo['load15']:.2f}",
                  "Procs", f"{sysinfo['procs']}/{sysinfo['total_procs']}")

    # Linux cards from surface — wektoryzowany odczyt
    try:
        import json as _json
        lc_dir = SURFACE / "linux_cards"

        # Hardware summary
        hw_file = lc_dir / "hardware.json"
        if hw_file.exists():
            hw = _json.loads(hw_file.read_text())
            sys_t.add_row("HW cores", str(hw.get("cpu_cores", "?")),
                          "disks", str(hw.get("disks", "?")))
            sys_t.add_row("net if", str(hw.get("net_ifaces", "?")),
                          "PCI devs", str(hw.get("pci_devs", "?")))
            sys_t.add_row("modules", str(hw.get("modules", "?")),
                          "mounts", str(hw.get("mounts", "?")))
            sys_t.add_row("sensors", str(hw.get("sensors", "?")),
                          "net conns", str(hw.get("net_conns", "?")) + " (TCP+UDP)")

        # CPU summary
        cpu_file = lc_dir / "cpu_summary.json"
        if cpu_file.exists():
            cpu = _json.loads(cpu_file.read_text())
            busy = cpu.get("mean_busy_pct", 0)
            freq = cpu.get("mean_freq_mhz", 0)
            cpu_bar = _bar(busy / 100, 10)
            sys_t.add_row("CPU ⊗ busy", f"{busy:.1f}%{cpu_bar}",
                          "freq", f"{freq:.0f}MHz")

        # Sensor summary — temperatura CPU + wentylatory
        try:
            sns_file = lc_dir / "cards.jsonl"
            if sns_file.exists():
                temps = []
                fans = []
                for line in sns_file.read_text().splitlines():
                    if not line.strip():
                        continue
                    c = _json.loads(line)
                    if c.get("type") != "SENSOR":
                        continue
                    st = c.get("sensor_type", "")
                    if st == "temp":
                        t = c.get("temp_c", 0)
                        if t:
                            temps.append((c.get("label", "?"), t))
                    elif st == "fan":
                        r = c.get("fan_rpm", 0)
                        if r:
                            fans.append((c.get("label", "?"), r))
                if temps:
                    max_temp = max(t[1] for t in temps)
                    sys_t.add_row("CPU temp", f"{max_temp:.0f}°C",
                                  "fans", f"{len(fans)} running" if fans else "—")
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_dashboard.py:313 quiet except scope=render_tui reason=pass")
            pass

        # Top CPU processes
        lc_top = lc_dir / "top_cpu.json"
        if lc_top.exists():
            procs = _json.loads(lc_top.read_text())
            for p in procs[:5]:
                cpu = p.get("cpu", 0) or 0
                mem = p.get("mem", 0) or 0
                pbar = _bar(cpu / 100, 10)
                sys_t.add_row(
                    f"● {p['name'][:18]}", f"{cpu:5.1f}%{pbar}" if cpu > 0 else "      -",
                    "", f"mem {mem:.1f}%"
                )
        # nearby processes (PhaseNav match)
        nearby_file = lc_dir / "nearby_surface.json"
        if nearby_file.exists():
            nearby = _json.loads(nearby_file.read_text())
            sys_t.add_row("─── PhaseNav nearby ───", "", "", "")
            for n in nearby[:3]:
                sys_t.add_row(
                    f"  {n['name'][:18]}",
                    f"SIM:{n.get('sim',0):.3f}",
                    f"PID:{n.get('pid',0)}",
                    f"CPU:{n.get('cpu',0):.1f}%",
                )
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_dashboard.py:340 quiet except scope=render_tui reason=pass")
        pass

    # daemony
    dae_t = Table(show_header=True, box=None, padding=(0, 2))
    dae_t.add_column("", width=2)
    dae_t.add_column("daemon", width=18)
    dae_t.add_column("status", width=8)
    for d in (daemons or []):
        name = d["unit"].replace("noema-", "").replace(".service", "")
        act = d["status"] == "active"
        dae_t.add_row(
            Text("●" if act else "○", style="green" if act else "red"),
            Text(name, style="green" if act else "red"),
            Text(d["status"], style="green" if act else "dim"),
        )

    system_panel = Panel(
        Columns([
            Panel(sys_t, title="Linux Resources", border_style="blue"),
            Panel(dae_t, title="Systemd Daemons", border_style="blue"),
        ]),
        border_style="dim"
    )

    # ── IMAGINAL SURFACE ──
    imag_parts = []
    if len(phi_i) == 24:
        i_bars = np.clip((np.mod(phi_i, 2 * np.pi) / (2 * np.pi) * 10).astype(int), 0, 10)
        i_colors = np.where(np.mod(phi_i, 2 * np.pi) / (2 * np.pi) < 0.33, "green",
                            np.where(np.mod(phi_i, 2 * np.pi) / (2 * np.pi) < 0.66, "yellow", "red"))
        i_lines = []
        for i in range(24):
            b = "█" * i_bars[i] + "░" * (10 - i_bars[i])
            i_lines.append(
                f"[{i_colors[i]}]{i:02d} {CHANNELS[i]:<9} {b}[/{i_colors[i]}] "
                f"[cyan]{omega_i[i]:.2f}[/cyan]"
            )
        i_body = Text("\n".join(i_lines[:12]) + "\n" + "\n".join(i_lines[12:]))

        r_sync = sync_metric(phi, phi_i)
        tick_i = 0
        try:
            raw = (IMAGINAL / "tick").read_bytes()
            tick_i = struct.unpack("Q", raw[:8])[0] if len(raw) >= 8 else 0
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_dashboard.py:385 quiet except scope=render_tui reason=pass")
            pass

        i_info = Text(
            f"  Real coh:  {m['coh']:.4f}\n"
            f"  Imag coh:  {m_i['coh']:.4f}\n"
            f"  R_sync:    {r_sync:.4f}\n"
            f"  Δtick:     {tick - tick_i}\n"
            f"  Imag circ: {m_i['green']}G/{m_i['yellow']}Y/{m_i['red']}R"
        )
        imag_parts = [i_body, i_info]
    else:
        imag_parts = [Text("Brak imaginal surface", style="red")]

    if len(a_hot) == 24:
        a_coh = float(abs(np.exp(1j * a_hot).sum()) / 24)
        a_cold = read_mmap(SURFACE / "analog" / "phi_cold", 24) \
            if (SURFACE / "analog" / "phi_cold").exists() else np.zeros(0)
        a_c_coh = float(abs(np.exp(1j * a_cold).sum()) / 24) if len(a_cold) == 24 else 0
        imag_parts.append(Text(
            f"\n[magenta]Analog Bus[/magenta]\n"
            f"  Hot R:  {a_coh:.4f}\n"
            f"  Cold R: {a_c_coh:.4f}\n"
            f"  Temp:   {a_temp:.2f}"
        ))

    imag_panel = Panel(
        Columns(imag_parts),
        title=f"Imaginal Surface — dual sync PLL | Real:{m['coh']:.3f} Imag:{m_i['coh'] if m_i else 0:.3f}",
        border_style="magenta",
    )

    # ── GRAVITY + NEUTRINO ──
    g_t = Table(show_header=True, header_style="bold", box=None, padding=(0, 2))
    for i in range(min(8, len(gravity))):
        g_t.add_column(GRAV_LABELS[i], justify="center")
    g_t.add_row(*[f"{gravity[i]:.2f}" for i in range(8)])

    D_f = abs(gravity[0])
    lam = (D_f - 2) / 0.57 if D_f > 2 else 0.0
    fl_text = " | ".join(f"{FLAV_LABELS[i]}:{flavor[i]:.2f}" for i in range(min(6, len(flavor))))

    neur_t = Table(show_header=False, box=None, padding=(0, 1))
    neur_t.add_column("k", style="bold")
    neur_t.add_column("v")
    neur_t.add_row("D_f (cp→)", f"{D_f:.3f}")
    neur_t.add_row("Λ (D_f→)", f"{lam:.3f}")
    neur_t.add_row("g_boost", f"{gravity[5]:.3f}" if len(gravity) > 5 else "—")
    neur_t.add_row("Flavor 0-5", fl_text)
    neur_t.add_row("Scars", f"{gravity[4]:.0f}" if len(gravity) > 4 else "—")

    metrics_panel = Panel(
        Columns([
            Panel(g_t, title="Gravity (8 slotów)", border_style="green"),
            Panel(neur_t, title="Neutrino PMNS Bus", border_style="yellow"),
        ]),
        title="NOEMA Core Metrics",
        border_style="blue"
    )

    # ── FOOTER ──
    footer_text = Text(
        f" [reverse] q quit [/reverse]  "
        f" [reverse] h help [/reverse]  "
        f" [reverse] o toggle osc [/reverse]  "
        f" [reverse] p/m sort procs [/reverse]  "
        f" tick:{tick}  coh:{m['coh']:.3f}  R:{R:.1f}  "
        f"density:{gravity[0]:.2f} γ:{gravity[1]:.2f} "
        f"mass:{gravity[2]:.2f} unruh:{gravity[3]:.2f} "
        f"load:{sysinfo['load']:.2f}",
        no_wrap=True
    )

    # ── assemble ──
    parts = [
        header,
        osc_panel,
        system_panel,
        imag_panel,
        metrics_panel,
        Panel(footer_text, style="dim"),
    ]

    with console.capture() as cap:
        for p in parts:
            console.print(p)
    return cap.get()


# ── main ───────────────────────────────────────────────────────────

_start_time = time.time()
MODE = "full"  # full | simple | once
SHOW_OSC = 24
SORT_PROCS = "cpu"


def key_listener(stop):
    try:
        import tty, termios, select
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        tty.setraw(fd)
        global SHOW_OSC, SORT_PROCS
        while not stop.is_set():
            if select.select([sys.stdin], [], [], 0.05)[0]:
                ch = sys.stdin.read(1)
                if ch in ("q", "Q", "\x1b"):
                    stop.set()
                    break
                elif ch in ("o", "O"):
                    SHOW_OSC = 8 if SHOW_OSC == 24 else 24
                elif ch in ("p", "P"):
                    SORT_PROCS = "cpu"
                elif ch in ("m", "M"):
                    SORT_PROCS = "mem"
                elif ch in ("r", "R"):
                    pass  # refresh
                elif ch in ("h", "H"):
                    pass  # help on next render
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_dashboard.py:505 quiet except scope=key_listener reason=pass")
        pass


def main():
    from rich.console import Console
    from rich.live import Live
    import threading

    console = Console()

    if "--once" in sys.argv:
        console.print(render_tui(console, SHOW_OSC, SORT_PROCS))
        return

    stop = threading.Event()
    t = threading.Thread(target=key_listener, args=(stop,), daemon=True)
    t.start()

    def gen():
        return render_tui(console, SHOW_OSC, SORT_PROCS)

    try:
        with Live(gen(), refresh_per_second=4, screen=True,
                  vertical_overflow="visible") as live:
            while not stop.is_set():
                live.update(gen())
                time.sleep(0.25)
    except KeyboardInterrupt:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_dashboard.py:533 quiet except scope=main reason=Expr")
        stop.set()
    finally:
        console.print("[dim]🟉 dashboard closed[/dim]")


if __name__ == "__main__":
    main()
