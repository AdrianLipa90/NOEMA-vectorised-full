"""Linux → NOEMA karty — cały system operacyjny zmapowany jako karty PhaseNav.

Każdy proces, rdzeń CPU, dysk, interfejs sieciowy, połączenie, moduł,
punkt montowania, urządzenie PCI → 36D wektor fazowy → karta NOEMA.
Integracja z PhaseNav hot/cold: eksploracja całego systemu jak kart konceptów.

Typy kart:
    PROC     — procesy (/proc/[pid]/stat)
    CPU      — rdzenie CPU (/proc/stat cpu0..cpuN)
    DISK     — urządzenia blokowe (/proc/diskstats)
    NET_IF   — interfejsy sieciowe (/proc/net/dev)
    NET_CONN — połączenia sieciowe (/proc/net/tcp + udp + tcp6 + udp6)
    NET_FLOW — procesy z aktywnością sieciową (/proc/[pid]/fd → socket inode → /proc/net/tcp)
    MODULE   — moduły jądra (/proc/modules)
    MOUNT    — punkty montowania (/proc/mounts)
    PCI_DEV  — urządzenia PCI (/sys/bus/pci/devices/)
    SENSOR   — sensory sprzętowe (temperatura, wentylatory, napięcie, prąd, moc) z /sys/class/hwmon
    SERVICE  — usługi systemd (systemctl list-units --type=service)

Użycie:
    from ciel_geometry.linux_cards import LinuxCardIndex
    idx = LinuxCardIndex()
    idx.update()              # skanowanie całego systemu
    idx.query("firefox")      # szukaj kart po nazwie
    idx.nearby(phi)           # najbliższe karty do danego wektora fazy
    idx.by_type("CPU")        # karty konkretnego typu
"""

from __future__ import annotations

import hashlib
import json
import logging as _noema_quiet_logging
import os
import time
from pathlib import Path
from typing import Any

import numpy as np

_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)

CARDS_DIR = Path("/dev/shm/ciel_noema/linux_cards")
CARDS_DIR.mkdir(parents=True, exist_ok=True)

N_OSCILLATORS = 36
_TWO_PI = 2.0 * np.pi

# ── 36 kanałów → znaczenie dla procesów ──────────────────────────────
PROCESS_PHI_MAP = {
    "cpu_usage": 0,      "mem_usage": 1,      "state_run": 2,
    "state_sleep": 3,    "state_stop": 4,     "state_zombie": 5,
    "priority": 6,       "threads": 7,        "age_hours": 8,
    "ctx_switches": 9,   "voluntary": 10,     "involuntary": 11,
    "rss_mb": 12,        "vms_mb": 13,        "shared": 14,
    "text": 15,          "data": 16,          "dirty": 17,
    "minor_faults": 18,  "major_faults": 19,  "read_bytes": 20,
    "write_bytes": 21,   "cancel_writes": 22, "child_ctx": 23,
    "fd_count": 24,      "signals_pending": 25, "cg_time": 26,
    "num_fds": 27,       "env_size": 28,      "arg_size": 29,
    "io_rchar": 30,      "io_wchar": 31,      "io_rbytes": 32,
    "io_wbytes": 33,     "delay_count": 34,   "delay_total": 35,
}

# ── 36 kanałów → znaczenie dla rdzeni CPU ────────────────────────────
CPU_PHI_MAP = {
    "user": 0,    "nice": 1,    "system": 2,  "idle": 3,
    "iowait": 4,  "irq": 5,     "softirq": 6, "steal": 7,
    "guest": 8,   "guest_nice": 9,
    "freq_mhz": 12, "temp_c": 13,
    "load_1": 16,  "load_5": 17, "load_15": 18,
    "caches": 24,  "bounces": 25, "numa_miss": 26,
    "migrate": 27, "context_sw": 28, "irq_total": 29,
    "freq_min": 30, "freq_max": 31, "governor": 32,
    "core_id": 33, "socket": 34,  "thermal_throttle": 35,
}

# ── 36 kanałów → znaczenie dla dysków ────────────────────────────────
DISK_PHI_MAP = {
    "reads": 0,        "reads_merged": 1,  "read_sectors": 2,
    "read_ms": 3,      "writes": 4,        "writes_merged": 5,
    "write_sectors": 6, "write_ms": 7,
    "io_in_progress": 8, "io_ms": 9,       "io_weighted_ms": 10,
    "size_gb": 12,     "used_pct": 13,     "busy_pct": 14,
    "discards": 24,    "discard_ms": 25,   "flush_cnt": 26,
    "flush_ms": 27,    "avg_req_sz": 28,   "avg_qd": 29,
    "read_lat": 30,    "write_lat": 31,    "discard_lat": 32,
    "queue_len": 33,   "iops": 34,         "throughput": 35,
}

# ── 36 kanałów → znaczenie dla interfejsów sieciowych ────────────────
NET_PHI_MAP = {
    "rx_bytes": 0,   "rx_packets": 1,   "rx_errors": 2,   "rx_drop": 3,
    "tx_bytes": 4,   "tx_packets": 5,   "tx_errors": 6,   "tx_drop": 7,
    "rx_kbps": 8,    "tx_kbps": 9,
    "speed_mbps": 12, "mtu": 13,
    "rx_comp": 24,   "rx_nohdr": 25,    "rx_missed": 26,
    "tx_abort": 27,  "tx_carrier": 28,  "tx_colls": 29,
    "rx_bps": 30,    "tx_bps": 31,      "rx_pps": 32,
    "tx_pps": 33,    "rx_util": 34,     "tx_util": 35,
}

# ── 36 kanałów → znaczenie dla połączeń sieciowych ───────────────────
NETCONN_PHI_MAP = {
    "rx_buf": 0,     "tx_buf": 1,     "retrans": 2,
    "rtt_ms": 3,     "state_est": 4,  "state_ts": 5,
    "state_cl": 6,   "state_li": 7,   "state_cl_wa": 8,
    "state_la_cl": 9, "state_tw": 10, "has_tx": 11,
    "port": 12,       "drops": 13,
    "tcp_cong": 24,  "wscale": 25,    "mss": 26,
    "sndbuf": 27,    "rcvbuf": 28,    "pacing": 29,
    "lost": 30,      "reord": 31,     "rtt_var": 32,
    "cwnd": 33,      "ssthresh": 34,  "delivery": 35,
}

# ── 36 kanałów → znaczenie dla modułów jądra ─────────────────────────
MODULE_PHI_MAP = {
    "size_mb": 0,     "used_by": 1,    "mem": 2,
    "refs": 24,       "srcver": 25,    "taint": 26,
}

# ── 36 kanałów → znaczenie dla mount pointów ─────────────────────────
MOUNT_PHI_MAP = {
    "total_gb": 0,    "used_gb": 1,    "avail_gb": 2,    "used_pct": 3,
    "inodes_pct": 4,  "readonly": 5,
    "rdev": 24,       "fs_type": 25,   "mount_opts": 26,
    "dirty_mb": 27,   "writeback_mb": 28, "io_limit": 29,
}

# ── 36 kanałów → znaczenie dla PCI ───────────────────────────────────
PCI_PHI_MAP = {
    "class": 0,       "vendor": 1,      "irq": 2,
    "numa": 3,
    "width": 24,      "speed_gt": 25,   "driver": 26,
    "d3cold": 27,     "ats": 28,        "acs": 29,
}

# ── 36 kanałów → znaczenie dla sensorów ─────────────────────────────
SENSOR_PHI_MAP = {
    "temp_c": 0,      "temp_max": 1,    "fan_rpm": 2,
    "fan_max": 3,     "power_w": 4,     "power_max": 5,
    "volt_v": 6,      "curr_a": 7,      "humidity": 8,
    "sensor_type_0": 16, "sensor_type_1": 17, "sensor_type_2": 18,
    "temp_crit": 24,  "temp_alarm": 25, "fan_min": 26,
    "fan_alarm": 27,  "power_crit": 28, "volt_min": 29,
    "volt_max": 30,   "curr_min": 31,   "curr_max": 32,
    "energy": 33,     "charge_full": 34, "charge_now": 35,
}


# ── helpers ──────────────────────────────────────────────────────────


def _card_id(prefix: str, unique: str, name: str) -> str:
    raw = f"LNX_{prefix}_{unique}_{name}"
    h = hashlib.md5(raw.encode()).hexdigest()[:6].upper()
    safe = "".join(c if c.isalnum() else "_" for c in name)[:20]
    return f"LNX-{prefix}-{safe}-{h}"


def _norm_phi(val: float, scale: float = 1.0) -> float:
    """Normalizuj wartość do [0, 2π)."""
    return min(max(val / max(scale, 1e-12), 0.0), 1.0) * _TWO_PI


# ── PROC ────────────────────────────────────────────────────────────


def _proc_phi(p: dict[str, Any]) -> np.ndarray:
    phi = np.zeros(N_OSCILLATORS, dtype=np.float64)
    u = p.get("cpu_percent", 0) or 0
    m = p.get("memory_percent", 0) or 0
    state = p.get("status", "?")
    age = (time.time() - p.get("create_time", time.time())) / 3600
    s_map = {"running": 0.1, "sleeping": 1.0, "stopped": 2.0, "zombie": 3.0, "disk-sleep": 4.0}

    phi[PROCESS_PHI_MAP["cpu_usage"]] = _norm_phi(u, 100)
    phi[PROCESS_PHI_MAP["mem_usage"]] = _norm_phi(m, 100)
    phi[PROCESS_PHI_MAP["state_run"]] = s_map.get(state, 0.5)
    phi[PROCESS_PHI_MAP["age_hours"]] = _norm_phi(age, 168)
    phi[PROCESS_PHI_MAP["threads"]] = _norm_phi(p.get("num_threads", 1), 64)
    phi[PROCESS_PHI_MAP["priority"]] = _norm_phi(p.get("nice", 0) + 20, 40)
    phi[PROCESS_PHI_MAP["rss_mb"]] = _norm_phi((p.get("rss", 0) or 0) / 1e6, 1024)
    phi[PROCESS_PHI_MAP["vms_mb"]] = _norm_phi((p.get("vms", 0) or 0) / 1e6, 4096)

    io = p.get("io_counters") or {}
    rbytes = io.read_bytes if hasattr(io, "read_bytes") else io.get("read_bytes", 0)
    wbytes = io.write_bytes if hasattr(io, "write_bytes") else io.get("write_bytes", 0)
    phi[PROCESS_PHI_MAP["read_bytes"]] = _norm_phi(rbytes, 1e8)
    phi[PROCESS_PHI_MAP["write_bytes"]] = _norm_phi(wbytes, 1e8)
    return phi


def _proc_card(name: str, card_type: str, attrs: dict) -> dict:
    phi = _proc_phi(attrs)
    cid = _card_id("PROC", str(attrs.get("pid", 0)), name)
    return {"card_id": cid, "type": "PROC", "name": name,
            "phi": phi, "label": f"PID {attrs.get('pid','?')}",
            "host_type": "linux", **attrs}


# ── CPU CORE ────────────────────────────────────────────────────────


def _scan_cpu_cores() -> list[dict]:
    """Skanuj /proc/stat — każda linia cpuN → osobna karta."""
    cores = []
    try:
        for line in Path("/proc/stat").read_text().splitlines():
            if not line.startswith("cpu") or line.startswith("cpu "):
                continue
            parts = line.split()
            core_id = parts[0][3:]  # "cpu0" → "0"
            vals = [int(x) for x in parts[1:]]
            total = sum(vals) or 1
            user = vals[0] if len(vals) > 0 else 0
            nice = vals[1] if len(vals) > 1 else 0
            system = vals[2] if len(vals) > 2 else 0
            idle = vals[3] if len(vals) > 3 else 0
            iowait = vals[4] if len(vals) > 4 else 0
            irq = vals[5] if len(vals) > 5 else 0
            softirq = vals[6] if len(vals) > 6 else 0
            steal = vals[7] if len(vals) > 7 else 0
            busy = total - idle

            # freq from /sys
            freq = 0.0
            try:
                freq_path = Path(f"/sys/devices/system/cpu/cpu{core_id}/cpufreq/scaling_cur_freq")
                if freq_path.exists():
                    freq = int(freq_path.read_text().strip()) / 1_000_000  # MHz
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/linux_cards.py:232 quiet except scope=_scan_cpu_cores reason=pass")
                pass

            cores.append({
                "name": f"cpu{core_id}",
                "type": "CPU",
                "core_id": core_id,
                "user_pct": user / total * 100,
                "nice_pct": nice / total * 100,
                "system_pct": system / total * 100,
                "idle_pct": idle / total * 100,
                "iowait_pct": iowait / total * 100,
                "irq_pct": irq / total * 100,
                "softirq_pct": softirq / total * 100,
                "steal_pct": steal / total * 100,
                "busy_pct": busy / total * 100,
                "freq_mhz": freq,
                "total_jiffies": total,
            })
    except OSError:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/linux_cards.py:251 quiet except scope=_scan_cpu_cores reason=pass")
        pass
    return cores


def _cpu_phi(c: dict) -> np.ndarray:
    phi = np.zeros(N_OSCILLATORS, dtype=np.float64)
    phi[CPU_PHI_MAP["user"]] = _norm_phi(c.get("user_pct", 0), 100)
    phi[CPU_PHI_MAP["nice"]] = _norm_phi(c.get("nice_pct", 0), 100)
    phi[CPU_PHI_MAP["system"]] = _norm_phi(c.get("system_pct", 0), 100)
    phi[CPU_PHI_MAP["idle"]] = _norm_phi(c.get("idle_pct", 0), 100)
    phi[CPU_PHI_MAP["iowait"]] = _norm_phi(c.get("iowait_pct", 0), 100)
    phi[CPU_PHI_MAP["irq"]] = _norm_phi(c.get("irq_pct", 0), 100)
    phi[CPU_PHI_MAP["softirq"]] = _norm_phi(c.get("softirq_pct", 0), 100)
    phi[CPU_PHI_MAP["freq_mhz"]] = _norm_phi(c.get("freq_mhz", 0), 5000)
    return phi


# ── DISK ────────────────────────────────────────────────────────────


def _scan_disks() -> list[dict]:
    """Skanuj /proc/diskstats → urządzenia blokowe."""
    disks = []
    seen = set()
    try:
        for line in Path("/proc/diskstats").read_text().splitlines():
            parts = line.strip().split()
            if len(parts) < 14:
                continue
            major, minor, name = parts[0], parts[1], parts[2]
            if name.startswith("loop") or name.startswith("ram"):
                continue
            # Tylko główne urządzenia (minor=0) lub z literami (sda, sda1)
            if minor == "0" or any(c.isalpha() for c in name):
                if name in seen:
                    continue
                seen.add(name)
                rio = int(parts[3])
                rmerge = int(parts[4])
                rsect = int(parts[5])
                rms = int(parts[6])
                wio = int(parts[7])
                wmerge = int(parts[8])
                wsect = int(parts[9])
                wms = int(parts[10])
                inflight = int(parts[11])
                ioms = int(parts[12])
                iowms = int(parts[13])

                # Size from /sys
                size_sectors = 0
                try:
                    size_path = Path(f"/sys/block/{name}/size")
                    if size_path.exists():
                        size_sectors = int(size_path.read_text().strip())
                except Exception:
                    _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/linux_cards.py:307 quiet except scope=_scan_disks reason=pass")
                    pass
                size_gb = size_sectors * 512 / 1e9

                disks.append({
                    "name": name,
                    "type": "DISK",
                    "major": major, "minor": minor,
                    "reads": rio, "reads_merged": rmerge,
                    "read_sectors": rsect, "read_ms": rms,
                    "writes": wio, "writes_merged": wmerge,
                    "write_sectors": wsect, "write_ms": wms,
                    "io_in_progress": inflight, "io_ms": ioms,
                    "io_weighted_ms": iowms,
                    "size_gb": round(size_gb, 1),
                })
    except OSError:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/linux_cards.py:323 quiet except scope=_scan_disks reason=pass")
        pass
    return disks


def _disk_phi(d: dict) -> np.ndarray:
    phi = np.zeros(N_OSCILLATORS, dtype=np.float64)
    phi[DISK_PHI_MAP["reads"]] = _norm_phi(d.get("reads", 0), 1e6)
    phi[DISK_PHI_MAP["writes"]] = _norm_phi(d.get("writes", 0), 1e6)
    phi[DISK_PHI_MAP["read_sectors"]] = _norm_phi(d.get("read_sectors", 0), 1e8)
    phi[DISK_PHI_MAP["write_sectors"]] = _norm_phi(d.get("write_sectors", 0), 1e8)
    phi[DISK_PHI_MAP["io_in_progress"]] = _norm_phi(d.get("io_in_progress", 0), 256)
    phi[DISK_PHI_MAP["io_ms"]] = _norm_phi(d.get("io_ms", 0), 10000)
    phi[DISK_PHI_MAP["size_gb"]] = _norm_phi(d.get("size_gb", 0), 2000)
    phi[DISK_PHI_MAP["busy_pct"]] = _norm_phi(
        min(d.get("io_ms", 0) / max(d.get("reads", 1) + d.get("writes", 1), 1), 100), 100)
    return phi


# ── NETWORK INTERFACE ───────────────────────────────────────────────


def _scan_net_ifaces() -> list[dict]:
    """Skanuj /proc/net/dev → interfejsy sieciowe."""
    ifaces = []
    try:
        lines = Path("/proc/net/dev").read_text().splitlines()[2:]  # pomiń nagłówek
        for line in lines:
            parts = line.strip().split()
            if len(parts) < 10:
                continue
            name = parts[0].rstrip(":")
            if name == "lo":
                continue
            rx_bytes = int(parts[1])
            rx_packets = int(parts[2])
            rx_errors = int(parts[3])
            rx_drop = int(parts[4])
            tx_bytes = int(parts[9])
            tx_packets = int(parts[10])
            tx_errors = int(parts[11])
            tx_drop = int(parts[12])

            # speed/mtu from /sys
            speed = 0
            mtu = 1500
            try:
                s_path = Path(f"/sys/class/net/{name}/speed")
                if s_path.exists():
                    speed = int(s_path.read_text().strip())
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/linux_cards.py:373 quiet except scope=_scan_net_ifaces reason=pass")
                pass
            try:
                m_path = Path(f"/sys/class/net/{name}/mtu")
                if m_path.exists():
                    mtu = int(m_path.read_text().strip())
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/linux_cards.py:379 quiet except scope=_scan_net_ifaces reason=pass")
                pass

            ifaces.append({
                "name": name, "type": "NET_IF",
                "rx_bytes": rx_bytes, "rx_packets": rx_packets,
                "rx_errors": rx_errors, "rx_drop": rx_drop,
                "tx_bytes": tx_bytes, "tx_packets": tx_packets,
                "tx_errors": tx_errors, "tx_drop": tx_drop,
                "speed_mbps": speed, "mtu": mtu,
            })
    except OSError:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/linux_cards.py:390 quiet except scope=_scan_net_ifaces reason=pass")
        pass
    return ifaces


def _net_phi(n: dict) -> np.ndarray:
    phi = np.zeros(N_OSCILLATORS, dtype=np.float64)
    phi[NET_PHI_MAP["rx_bytes"]] = _norm_phi(n.get("rx_bytes", 0), 1e11)
    phi[NET_PHI_MAP["tx_bytes"]] = _norm_phi(n.get("tx_bytes", 0), 1e11)
    phi[NET_PHI_MAP["rx_errors"]] = _norm_phi(n.get("rx_errors", 0), 1000)
    phi[NET_PHI_MAP["tx_errors"]] = _norm_phi(n.get("tx_errors", 0), 1000)
    phi[NET_PHI_MAP["rx_drop"]] = _norm_phi(n.get("rx_drop", 0), 1000)
    phi[NET_PHI_MAP["tx_drop"]] = _norm_phi(n.get("tx_drop", 0), 1000)
    phi[NET_PHI_MAP["speed_mbps"]] = _norm_phi(n.get("speed_mbps", 0), 10000)
    phi[NET_PHI_MAP["mtu"]] = _norm_phi(n.get("mtu", 1500), 9000)
    return phi


# ── NETWORK CONNECTION ──────────────────────────────────────────────


def _parse_net_proc(path: str, proto: str, max_conns: int = 100,
                    is_udp: bool = False) -> list[dict]:
    """Wspólny parser /proc/net/{tcp,udp,tcp6,udp6}."""
    conns = []
    try:
        text = Path(path).read_text()
        for i, line in enumerate(text.splitlines()):
            if i == 0:
                continue
            parts = line.strip().split()
            if len(parts) < 12:
                continue
            sl = parts[0].rstrip(":")
            local = parts[1]
            rem = parts[2]
            st = int(parts[3], 16)
            txq, rxq = parts[4].split(":")
            tr, tw = parts[5].split(":")
            retrans = int(parts[6], 16) if len(parts) > 6 and not is_udp else 0
            drops = int(parts[11], 16) if is_udp and len(parts) > 11 else 0

            if is_udp:
                state_names = {7: "CLOSE"}
                state = state_names.get(st, f"0x{st:02x}")
            else:
                state_names = {
                    1: "EST", 2: "SYN_S", 3: "SYN_R",
                    4: "FIN1", 5: "FIN2", 6: "TIME_W",
                    7: "CLOSE", 8: "CLOSE_W", 9: "LAST_A",
                    10: "LISTEN", 11: "CLOSING",
                }
                state = state_names.get(st, f"0x{st:02x}")
            _, local_port = local.rsplit(":", 1)
            conns.append({
                "name": f"{proto}:{local_port}",
                "type": "NET_CONN",
                "proto": proto,
                "slot": int(sl), "local": local, "remote": rem,
                "state": state, "state_code": st,
                "tx_queue": int(txq, 16), "rx_queue": int(rxq, 16),
                "retrans": retrans, "drops": drops,
                "uid": parts[7] if len(parts) > 7 else "?",
                "port": int(local_port, 16) if local_port else 0,
            })
            if len(conns) >= max_conns:
                break
    except OSError:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/linux_cards.py:457 quiet except scope=_parse_net_proc reason=pass")
        pass
    return conns


def _scan_net_conns(max_conns: int = 100) -> list[dict]:
    """Skanuj TCP, UDP, TCP6, UDP6 → aktywne połączenia."""
    conns = []
    conns += _parse_net_proc("/proc/net/tcp", "tcp", max_conns // 2)
    conns += _parse_net_proc("/proc/net/udp", "udp", max_conns // 4, is_udp=True)
    conns += _parse_net_proc("/proc/net/tcp6", "tcp6", max_conns // 4)
    conns += _parse_net_proc("/proc/net/udp6", "udp6", max_conns // 4, is_udp=True)
    return conns[:max_conns]


def _netconn_phi(c: dict) -> np.ndarray:
    phi = np.zeros(N_OSCILLATORS, dtype=np.float64)
    phi[NETCONN_PHI_MAP["rx_buf"]] = _norm_phi(c.get("rx_queue", 0), 65536)
    phi[NETCONN_PHI_MAP["tx_buf"]] = _norm_phi(c.get("tx_queue", 0), 65536)
    phi[NETCONN_PHI_MAP["retrans"]] = _norm_phi(c.get("retrans", 0), 100)
    phi[NETCONN_PHI_MAP["port"]] = _norm_phi(c.get("port", 0), 65535)
    st = c.get("state_code", 0)
    phi[NETCONN_PHI_MAP["state_est"]] = _norm_phi(st, 0xB)
    drops = c.get("drops", 0)
    phi[NETCONN_PHI_MAP["has_tx"]] = _norm_phi(drops, 1000)
    # proto type: tcp/tcp6/udp/udp6 → channel 13-16
    proto = c.get("proto", "tcp")
    if proto == "udp":
        phi[NETCONN_PHI_MAP["state_cl"]] = 0.5 * _TWO_PI
    elif proto == "tcp6":
        phi[NETCONN_PHI_MAP["state_li"]] = 0.5 * _TWO_PI
    elif proto == "udp6":
        phi[NETCONN_PHI_MAP["state_cl_wa"]] = 0.5 * _TWO_PI
    return phi


# ── MODULE ──────────────────────────────────────────────────────────


def _scan_modules() -> list[dict]:
    """Skanuj /proc/modules → załadowane moduły jądra."""
    mods = []
    try:
        for line in Path("/proc/modules").read_text().splitlines():
            parts = line.strip().split()
            if len(parts) < 6:
                continue
            name = parts[0]
            size = int(parts[1])
            used = int(parts[2])
            by = parts[3].strip(",") if len(parts) > 3 else ""
            mods.append({
                "name": name, "type": "MODULE",
                "size_kb": size, "size_mb": size / 1024,
                "used_by_count": used,
                "used_by": by,
            })
    except OSError:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/linux_cards.py:514 quiet except scope=_scan_modules reason=pass")
        pass
    return mods


# ── MOUNT ───────────────────────────────────────────────────────────


def _scan_mounts() -> list[dict]:
    """Skanuj /proc/mounts → systemy plików z użyciem."""
    mounts = []
    try:
        lines = Path("/proc/mounts").read_text().splitlines()
        for line in lines:
            parts = line.strip().split()
            if len(parts) < 4:
                continue
            device, mount_point, fstype, opts = parts[0], parts[1], parts[2], parts[3]
            if fstype in ("proc", "sysfs", "tmpfs", "devtmpfs", "cgroup2", "cgroup"):
                continue
            if mount_point.startswith("/sys") or mount_point.startswith("/proc"):
                continue

            # statvfs przez os.statvfs
            usage = {}
            try:
                sv = os.statvfs(mount_point)
                total = sv.f_frsize * sv.f_blocks / 1e9
                avail = sv.f_frsize * sv.f_bavail / 1e9
                used = total - avail
                inodes_pct = (1 - sv.f_ffree / max(sv.f_files, 1)) * 100
                usage = {
                    "total_gb": round(total, 1),
                    "used_gb": round(used, 1),
                    "avail_gb": round(avail, 1),
                    "used_pct": round(used / max(total, 0.001) * 100, 1),
                    "inodes_pct": round(inodes_pct, 1),
                }
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/linux_cards.py:552 quiet except scope=_scan_mounts reason=assign_fallback")
                usage = {"total_gb": 0, "used_gb": 0, "avail_gb": 0,
                         "used_pct": 0, "inodes_pct": 0}

            mounts.append({
                "name": mount_point.rsplit("/", 1)[-1] or "/",
                "type": "MOUNT",
                "device": device, "mount_point": mount_point,
                "fstype": fstype, "opts": opts,
                **usage,
            })
    except OSError:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/linux_cards.py:563 quiet except scope=_scan_mounts reason=pass")
        pass
    return mounts


# ── PCI DEVICE ──────────────────────────────────────────────────────


def _scan_pci_devices() -> list[dict]:
    """Skanuj /sys/bus/pci/devices/ → urządzenia PCI."""
    devs = []
    try:
        pci_dir = Path("/sys/bus/pci/devices")
        if not pci_dir.exists():
            return devs
        for entry in sorted(pci_dir.iterdir()):
            if not entry.name.startswith("0000:"):
                continue
            try:
                vendor = (entry / "vendor").read_text().strip()
                device = (entry / "device").read_text().strip()
                cls = (entry / "class").read_text().strip()[:6]
                irq = int((entry / "irq").read_text().strip()) if (entry / "irq").exists() else 0
                numa = int((entry / "numa_node").read_text().strip()) \
                    if (entry / "numa_node").exists() else -1

                devs.append({
                    "name": entry.name.split(":")[-1],
                    "type": "PCI_DEV",
                    "pci_addr": entry.name,
                    "vendor": vendor, "device": device,
                    "class": cls, "irq": irq, "numa_node": numa,
                })
            except (OSError, ValueError):
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/linux_cards.py:596 quiet except scope=_scan_pci_devices reason=pass")
                pass
    except OSError:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/linux_cards.py:598 quiet except scope=_scan_pci_devices reason=pass")
        pass
    return devs


# ── SENSOR ──────────────────────────────────────────────────────────


def _scan_sensors() -> list[dict]:
    """Skanuj /sys/class/hwmon/ → sensory (temp, fan, power, voltage)."""
    sensors = []
    try:
        hwmon_dir = Path("/sys/class/hwmon")
        if not hwmon_dir.exists():
            # Fallback: uruchom `sensors` i sparsuj JSON
            import subprocess
            try:
                out = subprocess.run(["sensors", "-j"], capture_output=True,
                                     text=True, timeout=5)
                if out.returncode == 0 and out.stdout.strip():
                    data = json.loads(out.stdout)
                    for chip_name, chip_data in data.items():
                        if not isinstance(chip_data, dict):
                            continue
                        for key, val in chip_data.items():
                            if isinstance(val, dict):
                                name_clean = f"{chip_name}_{key}".replace(" ", "_")
                                sensors.append(_parse_sensor_entry(name_clean, val, chip_name))
                            elif isinstance(val, (int, float)):
                                sensors.append({
                                    "name": f"{chip_name}_{key}".replace(" ", "_"),
                                    "type": "SENSOR", "chip": chip_name,
                                    "sensor_type": key,
                                    "value": float(val), "unit": "",
                                })
                    return sensors
            except (FileNotFoundError, subprocess.TimeoutExpired, json.JSONDecodeError):
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/linux_cards.py:634 quiet except scope=_scan_sensors reason=pass")
                pass
            return sensors

        for entry in sorted(hwmon_dir.iterdir()):
            name_file = entry / "name"
            if not name_file.exists():
                continue
            chip_name = name_file.read_text().strip()
            # Temp sensors
            for tfile in entry.glob("temp*_input"):
                idx = tfile.name.replace("temp", "").split("_")[0]
                temp_c = int(tfile.read_text().strip()) / 1000
                tmax_file = entry / f"temp{idx}_max"
                tcrit_file = entry / f"temp{idx}_crit"
                label_file = entry / f"temp{idx}_label"
                label = label_file.read_text().strip() if label_file.exists() else f"temp{idx}"
                sensors.append({
                    "name": f"{chip_name}-{label}", "type": "SENSOR",
                    "chip": chip_name, "sensor_type": "temp",
                    "temp_c": round(temp_c, 1),
                    "temp_max": round(int(tmax_file.read_text().strip()) / 1000, 1)
                        if tmax_file.exists() else None,
                    "temp_crit": round(int(tcrit_file.read_text().strip()) / 1000, 1)
                        if tcrit_file.exists() else None,
                    "label": label,
                })

            # Fan sensors
            for ffile in entry.glob("fan*_input"):
                idx = ffile.name.replace("fan", "").split("_")[0]
                rpm = int(ffile.read_text().strip())
                fmax_file = entry / f"fan{idx}_max"
                label_file = entry / f"fan{idx}_label"
                label = label_file.read_text().strip() if label_file.exists() else f"fan{idx}"
                sensors.append({
                    "name": f"{chip_name}-{label}", "type": "SENSOR",
                    "chip": chip_name, "sensor_type": "fan",
                    "fan_rpm": rpm,
                    "fan_max": int(fmax_file.read_text().strip())
                        if fmax_file.exists() else None,
                    "label": label,
                })

            # Power sensors
            for pfile in entry.glob("power*_input"):
                idx = pfile.name.replace("power", "").split("_")[0]
                uw = int(pfile.read_text().strip())
                pmax_file = entry / f"power{idx}_max"
                label_file = entry / f"power{idx}_label"
                label = label_file.read_text().strip() if label_file.exists() else f"power{idx}"
                sensors.append({
                    "name": f"{chip_name}-{label}", "type": "SENSOR",
                    "chip": chip_name, "sensor_type": "power",
                    "power_w": round(uw / 1_000_000, 3),
                    "power_max": round(int(pmax_file.read_text().strip()) / 1_000_000, 3)
                        if pmax_file.exists() else None,
                    "label": label,
                })

            # Current sensors
            for cfile in entry.glob("curr*_input"):
                idx = cfile.name.replace("curr", "").split("_")[0]
                ma = int(cfile.read_text().strip())
                label_file = entry / f"curr{idx}_label"
                label = label_file.read_text().strip() if label_file.exists() else f"curr{idx}"
                sensors.append({
                    "name": f"{chip_name}-{label}", "type": "SENSOR",
                    "chip": chip_name, "sensor_type": "current",
                    "curr_a": round(ma / 1_000, 3),
                    "label": label,
                })

            # Voltage sensors
            for vfile in entry.glob("in*_input"):
                idx = vfile.name.replace("in", "").split("_")[0]
                mv = int(vfile.read_text().strip())
                label_file = entry / f"in{idx}_label"
                label = label_file.read_text().strip() if label_file.exists() else f"in{idx}"
                sensors.append({
                    "name": f"{chip_name}-{label}", "type": "SENSOR",
                    "chip": chip_name, "sensor_type": "voltage",
                    "volt_v": round(mv / 1000, 3),
                    "label": label,
                })

    except OSError:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/linux_cards.py:720 quiet except scope=_scan_sensors reason=pass")
        pass
    return sensors


def _parse_sensor_entry(name: str, data: dict, chip: str) -> dict:
    """Parse a single sensor entry from `sensors -j` JSON output."""
    entry: dict = {"name": name, "type": "SENSOR", "chip": chip, "sensor_type": "unknown"}
    for key, val in data.items():
        key_l = key.lower()
        if "temp" in key_l or key_l == "input":
            entry["temp_c"] = float(val) if isinstance(val, (int, float)) else 0
            entry["sensor_type"] = "temp"
        elif "fan" in key_l:
            entry["fan_rpm"] = float(val)
            entry["sensor_type"] = "fan"
        elif "power" in key_l:
            entry["power_w"] = float(val)
            entry["sensor_type"] = "power"
        elif "curr" in key_l:
            entry["curr_a"] = float(val)
            entry["sensor_type"] = "current"
        elif "in" in key_l or "volt" in key_l:
            entry["volt_v"] = float(val)
            entry["sensor_type"] = "voltage"
        elif key_l == "humidity":
            entry["humidity"] = float(val)
            entry["sensor_type"] = "humidity"
    return entry


def _sensor_phi(s: dict) -> np.ndarray:
    phi = np.zeros(N_OSCILLATORS, dtype=np.float64)
    stype = s.get("sensor_type", "")
    if stype == "temp":
        phi[SENSOR_PHI_MAP["temp_c"]] = _norm_phi(s.get("temp_c", 0), 100)
        phi[SENSOR_PHI_MAP["temp_max"]] = _norm_phi(s.get("temp_max", 0) or 0, 100)
        phi[SENSOR_PHI_MAP["sensor_type_0"]] = 0.5 * _TWO_PI
    elif stype == "fan":
        phi[SENSOR_PHI_MAP["fan_rpm"]] = _norm_phi(s.get("fan_rpm", 0), 5000)
        phi[SENSOR_PHI_MAP["fan_max"]] = _norm_phi(s.get("fan_max", 0) or 0, 5000)
        phi[SENSOR_PHI_MAP["sensor_type_1"]] = 0.5 * _TWO_PI
    elif stype == "power":
        phi[SENSOR_PHI_MAP["power_w"]] = _norm_phi(s.get("power_w", 0), 100)
        phi[SENSOR_PHI_MAP["power_max"]] = _norm_phi(s.get("power_max", 0) or 0, 100)
        phi[SENSOR_PHI_MAP["sensor_type_2"]] = 0.5 * _TWO_PI
    elif stype == "current":
        phi[SENSOR_PHI_MAP["curr_a"]] = _norm_phi(s.get("curr_a", 0), 5)
    elif stype == "voltage":
        phi[SENSOR_PHI_MAP["volt_v"]] = _norm_phi(s.get("volt_v", 0), 20)
    return phi


# ── NET_FLOW — per‑process network activity (nethogs‑like) ────────────

# Kanały φ dla NET_FLOW:
#   0: active_conns   — liczba aktywnych połączeń (ESTABLISHED)
#   1: total_conns    — całkowita liczba połączeń tego procesu
#   2: listen_conns   — liczba nasłuchujących socketów
#   3: retrans_sum    — suma retransmisji (TCP)
#   4: rx_queue_sum   — suma rx_queue
#   5: tx_queue_sum   — suma tx_queue
#   6: drops_sum      — suma drops (UDP)
#   7: port_range     — zakres portów (norm 65535)
#   8: unique_ports   — liczba unikalnych portów
#   9-23: reserved

NETFLOW_PHI_MAP = {
    "active_conns": 0,
    "total_conns": 1,
    "listen_conns": 2,
    "retrans_sum": 3,
    "rx_queue_sum": 4,
    "tx_queue_sum": 5,
    "drops_sum": 6,
    "port_range": 7,
    "unique_ports": 8,
}


# /proc/net/tcp state codes (hex → decimal)
_TCP_STATE_MAP = {
    1: "ESTABLISHED", 2: "SYN_SENT", 3: "SYN_RECV",
    4: "FIN_WAIT1",  5: "FIN_WAIT2", 6: "TIME_WAIT",
    7: "CLOSE",      8: "CLOSE_WAIT", 9: "LAST_ACK",
    10: "LISTEN",    11: "CLOSING",
}


def _scan_net_flows(max_flows: int = 50) -> list[dict]:
    """Skanuj /proc/*/fd → socket inode → /proc/net/{tcp,udp,tcp6,udp6}.

    Zwraca listę dictów, po jednym na proces z aktywnością sieciową:
      name, pid, type="NET_FLOW", conn_count, active, listen,
      socket_details: lista socketów z port, state, proto, retrans, rxq, txq, drops
    """
    # Krok 1: zbuduj mapę inode → (pid, fd)
    inode_to_proc: dict[int, list[tuple[int, str]]] = {}
    try:
        for p in os.listdir("/proc"):
            if not p.isdigit():
                continue
            pid_dir = f"/proc/{p}/fd"
            try:
                fds = os.listdir(pid_dir)
            except PermissionError:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/linux_cards.py:825 quiet except scope=_scan_net_flows reason=continue")
                continue
            for fd in fds:
                try:
                    link = os.readlink(f"{pid_dir}/{fd}")
                except (PermissionError, FileNotFoundError):
                    _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/linux_cards.py:830 quiet except scope=_scan_net_flows reason=continue")
                    continue
                if link.startswith("socket:["):
                    ino = int(link[8:-1])
                    inode_to_proc.setdefault(ino, []).append((int(p), fd))
    except FileNotFoundError:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/linux_cards.py:835 quiet except scope=_scan_net_flows reason=return []")
        return []

    # Krok 2: parsuj /proc/net/{tcp,udp,tcp6,udp6}
    all_conns = []
    for proto, path, is_udp in [
        ("tcp", "/proc/net/tcp", False),
        ("udp", "/proc/net/udp", True),
        ("tcp6", "/proc/net/tcp6", False),
        ("udp6", "/proc/net/udp6", True),
    ]:
        try:
            with open(path) as f:
                next(f)  # pomiń nagłówek
                for line in f:
                    parts = line.strip().split()
                    if len(parts) < 12:
                        continue
                    sl = parts[0].rstrip(":")
                    local = parts[1]
                    rem = parts[2]
                    st_code = int(parts[3], 16)
                    txq_rxq = parts[4].split(":")
                    tx_queue = int(txq_rxq[0], 16)
                    rx_queue = int(txq_rxq[1], 16)
                    tr_tw = parts[5].split(":")
                    retrans = int(tr_tw[0], 16) if not is_udp else 0
                    uid = int(parts[7])
                    _drop = int(parts[11], 16) if is_udp and len(parts) > 11 else 0
                    # inode jest ostatnim polem przed -> (lub przed timeout)
                    # Format: ... uid timeout inode
                    inode_found = None
                    for candidate in parts:
                        if candidate.isdigit() and int(candidate) > 1000:
                            # heuristic: inode jest zwykle > 10000
                            pass
                    # inode: element z indeksem 9 (po uid, timeout)
                    try:
                        inode_val = int(parts[9]) if len(parts) > 9 else 0
                    except ValueError:
                        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/linux_cards.py:874 quiet except scope=_scan_net_flows reason=assign_fallback")
                        inode_val = 0

                    # parsuj port z local addr (format: AAAAAAAA:PPPP)
                    local_port = int(local.split(":")[-1], 16) if ":" in local else 0

                    all_conns.append({
                        "proto": proto,
                        "state_code": st_code,
                        "state": _TCP_STATE_MAP.get(st_code, "?"),
                        "local": local,
                        "remote": rem,
                        "port": local_port,
                        "tx_queue": tx_queue,
                        "rx_queue": rx_queue,
                        "retrans": retrans,
                        "drops": _drop,
                        "inode": inode_val,
                        "uid": uid,
                    })
        except FileNotFoundError:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/linux_cards.py:894 quiet except scope=_scan_net_flows reason=continue")
            continue

    # Krok 3: połącz inode z procesami
    proc_conns: dict[int, dict] = {}
    for conn in all_conns:
        ino = conn["inode"]
        if ino == 0:
            continue
        proc_list = inode_to_proc.get(ino, [])
        if not proc_list:
            continue
        for pid, _ in proc_list:
            if pid not in proc_conns:
                try:
                    with open(f"/proc/{pid}/comm") as cf:
                        comm = cf.read().strip()
                except (FileNotFoundError, PermissionError):
                    _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/linux_cards.py:911 quiet except scope=_scan_net_flows reason=assign_fallback")
                    comm = "?"
                proc_conns[pid] = {
                    "pid": pid,
                    "name": comm,
                    "conns": [],
                }
            proc_conns[pid]["conns"].append(conn)

    # Krok 4: sformatuj wynik
    results = []
    for pid, data in proc_conns.items():
        conns = data["conns"]
        active = sum(1 for c in conns if c["state_code"] == 1)  # ESTABLISHED
        listen = sum(1 for c in conns if c["state_code"] == 0xA)  # LISTEN
        ports = list(set(c["port"] for c in conns if c["port"] > 0))
        port_range = max(ports) - min(ports) if len(ports) > 1 else 0

        results.append({
            "name": f"{data['name']}:{pid}",
            "type": "NET_FLOW",
            "pid": pid,
            "comm": data["name"],
            "conn_count": len(conns),
            "active": active,
            "listen": listen,
            "total_retrans": sum(c["retrans"] for c in conns),
            "total_rxq": sum(c["rx_queue"] for c in conns),
            "total_txq": sum(c["tx_queue"] for c in conns),
            "total_drops": sum(c["drops"] for c in conns),
            "port_range": port_range,
            "unique_ports": len(ports),
            "ports": sorted(ports)[:10],  # top 10
            "protos": list(set(c["proto"] for c in conns)),
            "states": list(set(c["state"] for c in conns)),
        })

    # sort by conn_count descending, limit
    results.sort(key=lambda r: r["conn_count"], reverse=True)
    return results[:max_flows]


def _netflow_phi(f: dict) -> np.ndarray:
    """36D faza dla NET_FLOW."""
    phi = np.zeros(N_OSCILLATORS, dtype=np.float64)
    phi[NETFLOW_PHI_MAP["active_conns"]] = _norm_phi(f.get("active", 0), 50)
    phi[NETFLOW_PHI_MAP["total_conns"]] = _norm_phi(f.get("conn_count", 0), 100)
    phi[NETFLOW_PHI_MAP["listen_conns"]] = _norm_phi(f.get("listen", 0), 20)
    phi[NETFLOW_PHI_MAP["retrans_sum"]] = _norm_phi(f.get("total_retrans", 0), 100)
    phi[NETFLOW_PHI_MAP["rx_queue_sum"]] = _norm_phi(f.get("total_rxq", 0), 65536)
    phi[NETFLOW_PHI_MAP["tx_queue_sum"]] = _norm_phi(f.get("total_txq", 0), 65536)
    phi[NETFLOW_PHI_MAP["drops_sum"]] = _norm_phi(f.get("total_drops", 0), 1000)
    phi[NETFLOW_PHI_MAP["port_range"]] = _norm_phi(f.get("port_range", 0), 65535)
    phi[NETFLOW_PHI_MAP["unique_ports"]] = _norm_phi(f.get("unique_ports", 0), 50)
    return phi


# ── SERVICE — systemd service units ─────────────────────────────────

# Kanały φ dla SERVICE:
#   0: active    — service active
#   1: running   — sub=running (fully operational)
#   2: enabled   — unit file state=enabled
#   3: failed    — sub=failed
#   4: user      — user service (vs system)
#   5-23: reserved

SERVICE_PHI_MAP = {
    "active": 0,
    "running": 1,
    "enabled": 2,
    "failed": 3,
    "user": 4,
}


def _scan_services(max_services: int = 80) -> list[dict]:
    """Skanuj usługi systemd (system + user).

    Używa systemctl list-units + list-unit-files.
    Zwraca listę dictów SERVICE.
    """
    results = []

    # Helper: systemctl JSON wrapper
    def _sysctl(args: list[str]) -> list[dict]:
        try:
            import subprocess
            r = subprocess.run(
                ["systemctl"] + args,
                capture_output=True, text=True, timeout=10,
            )
            if r.returncode == 0 and r.stdout.strip():
                return json.loads(r.stdout)
        except (subprocess.TimeoutExpired, json.JSONDecodeError,
                FileNotFoundError, OSError):
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/linux_cards.py:1002 quiet except scope=_scan_services._sysctl reason=pass")
            pass
        return []

    # Zbierz dane z system i user
    for scope, is_user in [("--system", False), ("--user", True)]:
        # Aktywne jednostki
        units = _sysctl([
            scope, "list-units", "--type=service", "--all",
            "--no-legend", "--output=json",
        ])
        # Pliki jednostek (enabled/disabled)
        unit_files = _sysctl([
            scope, "list-unit-files", "--type=service",
            "--no-legend", "--output=json",
        ])
        unit_file_map = {u.get("unit_file", ""): u.get("state", "?")
                         for u in unit_files}

        for u in units:
            name = u.get("unit", "?").replace(".service", "")
            uf_state = unit_file_map.get(u.get("unit", ""), "?")

            # Pobierz MainPID dla aktywnych user services
            main_pid = 0
            if is_user and u.get("active") == "active":
                info = _sysctl([
                    scope, "show", u["unit"],
                    "-p", "MainPID", "--value", "--no-legend",
                ])
                if info and isinstance(info, list) and len(info) > 0:
                    try:
                        main_pid = int(info[0])
                    except (ValueError, TypeError):
                        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/linux_cards.py:1040 quiet except scope=_scan_services reason=pass")
                        pass

            entry = {
                "name": name,
                "type": "SERVICE",
                "unit": u.get("unit", "?"),
                "load_state": u.get("load", "?"),
                "active_state": u.get("active", "?"),
                "sub_state": u.get("sub", "?"),
                "unit_file_state": uf_state,
                "description": u.get("description", ""),
                "is_user": is_user,
                "main_pid": main_pid,
            }

            # Dodaj PID → name mapowanie dla integracji z PROC
            if main_pid > 0:
                try:
                    with open(f"/proc/{main_pid}/comm") as cf:
                        entry["proc_comm"] = cf.read().strip()
                except (FileNotFoundError, PermissionError):
                    _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/linux_cards.py:1061 quiet except scope=_scan_services reason=pass")
                    pass

            results.append(entry)

    # Sort: active running first, then by name
    results.sort(key=lambda s: (
        0 if s["active_state"] == "active" and s["sub_state"] == "running" else
        1 if s["active_state"] == "active" else
        2 if s["active_state"] == "failed" else 3,
        s["name"],
    ))
    return results[:max_services]


def _service_phi(s: dict) -> np.ndarray:
    """36D faza dla SERVICE."""
    phi = np.zeros(N_OSCILLATORS, dtype=np.float64)
    _TWO_PI = 2 * np.pi

    def _norm(v: float, mx: float = 1.0) -> float:
        return np.clip(v / mx, 0, 1) * _TWO_PI

    phi[SERVICE_PHI_MAP["active"]] = _norm(
        1.0 if s.get("active_state") == "active" else 0.0)
    phi[SERVICE_PHI_MAP["running"]] = _norm(
        1.0 if s.get("sub_state") == "running" else 0.0)
    phi[SERVICE_PHI_MAP["enabled"]] = _norm(
        1.0 if s.get("unit_file_state") == "enabled" else 0.0)
    phi[SERVICE_PHI_MAP["failed"]] = _norm(
        1.0 if s.get("sub_state") == "failed" else 0.0)
    phi[SERVICE_PHI_MAP["user"]] = _norm(
        1.0 if s.get("is_user") else 0.5)
    return phi


# ── Card builder ────────────────────────────────────────────────────


_CARD_SCANNERS = {
    "PROC":     (lambda idx: idx._scan_procs(), _proc_phi, _proc_card),
    "CPU":      (_scan_cpu_cores, _cpu_phi, None),
    "DISK":     (_scan_disks, _disk_phi, None),
    "NET_IF":   (_scan_net_ifaces, _net_phi, None),
    "NET_CONN": (_scan_net_conns, _netconn_phi, None),
    "NET_FLOW": (_scan_net_flows, _netflow_phi, None),
    "MODULE":   (_scan_modules, None, None),
    "MOUNT":    (_scan_mounts, None, None),
    "PCI_DEV":  (_scan_pci_devices, None, None),
    "SENSOR":   (_scan_sensors, _sensor_phi, None),
    "SERVICE":  (_scan_services, _service_phi, None),
}

_CARD_TYPE_LABELS = {
    "PROC": "process", "CPU": "CPU core", "DISK": "block device",
    "NET_IF": "network interface", "NET_CONN": "network connection",
    "NET_FLOW": "network flow (per-process)",
    "MODULE": "kernel module", "MOUNT": "mount point",
    "PCI_DEV": "PCI device", "SENSOR": "hardware sensor",
    "SERVICE": "systemd service",
}


def _make_card(ctype: str, entity: dict) -> dict:
    """Z encji → karta PhaseNav z 36D fazą."""
    name = entity.get("name", "?")
    if ctype == "PROC":
        uid = str(entity.get("pid", 0))
    elif ctype == "NET_CONN":
        uid = f"{entity.get('slot', 0)}"
    elif ctype == "NET_FLOW":
        uid = str(entity.get("pid", 0))
    else:
        uid = name

    cid = _card_id(ctype, uid, name)
    phi_func = _CARD_SCANNERS[ctype][1]
    if phi_func:
        phi = phi_func(entity)
    else:
        phi = np.zeros(N_OSCILLATORS, dtype=np.float64)

    return {"card_id": cid, "type": ctype, "name": name,
            "phi": phi, "label": _CARD_TYPE_LABELS.get(ctype, ctype),
            "host_type": "linux", "updated_at": time.time(), **entity}


# ── LinuxCardIndex ──────────────────────────────────────────────────


class LinuxCardIndex:
    """Indeks kart Linux → NOEMA. Skanuje cały system (procesy, CPU, dyski, sieć, moduły, mounty, PCI)."""

    def __init__(self, max_procs: int = 200, max_conns: int = 100,
                 enabled_types: set[str] | None = None):
        self._cards: dict[str, dict] = {}
        self._phi_index: np.ndarray | None = None
        self._card_ids: list[str] = []
        self._card_types: dict[str, list[str]] = {t: [] for t in _CARD_SCANNERS}
        self._max_procs = max_procs
        self._max_conns = max_conns
        self._enabled_types = enabled_types or set(_CARD_SCANNERS.keys())
        self._last_update = 0.0
        self._stats: dict = {}

    def update(self) -> int:
        """Skanuj cały system → karty. Zwraca liczbę kart."""
        self._stats = {}

        for ctype in sorted(self._enabled_types):
            scanner, phi_func, card_builder = _CARD_SCANNERS[ctype]
            try:
                entities = scanner(self) if ctype == "PROC" else scanner()
                for e in entities:
                    card = _make_card(ctype, e)
                    self._cards[card["card_id"]] = card
                self._stats[ctype] = len(entities)
            except Exception as exc:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/linux_cards.py:1178 quiet except scope=LinuxCardIndex.update reason=assign_fallback")
                self._stats[ctype] = f"ERR:{exc}"

        # Limit procesów
        if "PROC" in self._enabled_types:
            proc_ids = [cid for cid, c in self._cards.items() if c.get("type") == "PROC"]
            if len(proc_ids) > self._max_procs:
                sorted_p = sorted(proc_ids,
                                  key=lambda cid: self._cards[cid].get("cpu_percent", 0) or 0,
                                  reverse=True)
                for cid in sorted_p[self._max_procs:]:
                    del self._cards[cid]

        # Odbuduj indeks faz
        self._rebuild_index()
        self._last_update = time.time()
        return len(self._cards)

    def _scan_procs(self) -> list[dict]:
        try:
            import psutil
            procs = []
            for p in psutil.process_iter([
                "pid", "name", "cpu_percent", "memory_percent", "status",
                "create_time", "num_threads", "nice", "memory_info",
                "io_counters", "num_ctx_switches",
            ]):
                try:
                    info = p.info
                    mi = info.get("memory_info")
                    info["rss"] = mi.rss if mi else 0
                    info["vms"] = mi.vms if mi else 0
                    procs.append(info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/linux_cards.py:1211 quiet except scope=LinuxCardIndex._scan_procs reason=pass")
                    pass
            return procs
        except ImportError:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/linux_cards.py:1214 quiet except scope=LinuxCardIndex._scan_procs reason=return self._scan_procfs()")
            return self._scan_procfs()

    def _scan_procfs(self) -> list[dict]:
        procs = []
        try:
            for p in Path("/proc").iterdir():
                if not p.name.isdigit():
                    continue
                pid = int(p.name)
                try:
                    stat = (p / "stat").read_text().split(")")
                    if len(stat) < 2:
                        continue
                    name = stat[0].split("(")[-1] if "(" in stat[0] else "?"
                    fields = stat[1].strip().split()
                    state = fields[0] if fields else "?"
                    procs.append({
                        "pid": pid, "name": name, "status": state,
                        "cpu_percent": 0, "memory_percent": 0,
                        "create_time": time.time(), "num_threads": 1,
                        "nice": 0, "rss": 0, "vms": 0,
                        "io_counters": {}, "num_ctx_switches": {},
                    })
                    if len(procs) >= self._max_procs:
                        break
                except (OSError, IndexError, ValueError):
                    _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/linux_cards.py:1240 quiet except scope=LinuxCardIndex._scan_procfs reason=continue")
                    continue
        except OSError:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/linux_cards.py:1242 quiet except scope=LinuxCardIndex._scan_procfs reason=pass")
            pass
        return procs

    def _rebuild_index(self) -> None:
        self._card_ids = list(self._cards.keys())
        self._card_types = {t: [] for t in _CARD_SCANNERS}
        for cid, c in self._cards.items():
            self._card_types[c.get("type", "?").upper()].append(cid)
        if self._card_ids:
            self._phi_index = np.array([self._cards[cid]["phi"] for cid in self._card_ids],
                                       dtype=np.float64)
        else:
            self._phi_index = np.zeros((0, 36), dtype=np.float64)

    def query(self, name: str) -> list[dict]:
        name_l = name.lower()
        return [c for c in self._cards.values() if name_l in c.get("name", "").lower()]

    def by_type(self, ctype: str) -> list[dict]:
        """Karty konkretnego typu (PROC, CPU, DISK, NET_IF, ...)."""
        return [self._cards[cid] for cid in self._card_types.get(ctype.upper(), [])]

    def nearby(self, phi: np.ndarray, k: int = 5) -> list[dict]:
        """k najbliższych kart do wektora fazy — cos similarity."""
        if self._phi_index is None or len(self._card_ids) == 0:
            return []
        a = phi.reshape(1, -1)
        b = self._phi_index
        dots = np.dot(a, b.T).flatten()
        norms = np.linalg.norm(a) * np.linalg.norm(b, axis=1) + 1e-12
        sims = dots / norms
        top = np.argsort(-sims)[:min(k, len(sims))]
        return [{**self._cards[self._card_ids[i]], "sim": float(sims[i])}
                for i in top]

    def top_cpu(self, n: int = 10) -> list[dict]:
        procs = self.by_type("PROC")
        sorted_c = sorted(procs, key=lambda x: x.get("cpu_percent", 0) or 0, reverse=True)
        return sorted_c[:n]

    def summary_stats(self) -> dict:
        if not self._cards:
            return {"total": 0}
        procs = self.by_type("PROC")
        cpus = [c.get("cpu_percent", 0) or 0 for c in procs]
        mems = [c.get("memory_percent", 0) or 0 for c in procs]
        by_type = {}
        for c in self._cards.values():
            t = c.get("type", "?")
            by_type[t] = by_type.get(t, 0) + 1
        return {
            "total": len(self._cards),
            "by_type": by_type,
            "scan_errors": self._stats,
            "total_cpu": sum(cpus),
            "total_mem": sum(mems),
            "max_cpu_name": max(procs, key=lambda x: x.get("cpu_percent", 0) or 0).get("name", "?") if procs else "?",
            "max_mem_name": max(procs, key=lambda x: x.get("memory_percent", 0) or 0).get("name", "?") if procs else "?",
        }

    def save_surface(self) -> None:
        """Zapisz indeks na NOEMA surface jako mmap + JSON."""
        if self._phi_index is None:
            return
        mean_phi = np.mean(self._phi_index, axis=0)
        mean_phi.astype(np.float64).tofile(CARDS_DIR / "mean_phi")

        # Top CPU
        top = self.top_cpu(10)
        with open(CARDS_DIR / "top_cpu.json", "w") as f:
            json.dump([{
                "pid": t.get("pid"), "name": t.get("name"),
                "cpu": t.get("cpu_percent"), "mem": t.get("memory_percent"),
            } for t in top], f, indent=2)

        # Cards jako JSONL
        with open(CARDS_DIR / "cards.jsonl", "w") as f:
            for c in self._cards.values():
                d = {k: v for k, v in c.items() if k != "phi"}
                d["phi_summary"] = [f"{x:.3f}" for x in c["phi"][:6]]
                f.write(json.dumps(d, default=str) + "\n")

        # Licznik
        with open(CARDS_DIR / "count", "w") as f:
            f.write(str(len(self._cards)))

        # Typy kart
        by_type = {}
        for c in self._cards.values():
            t = c.get("type", "?")
            by_type[t] = by_type.get(t, 0) + 1
        with open(CARDS_DIR / "types.json", "w") as f:
            json.dump(by_type, f, indent=2)

        # Hardware summary
        hw = {
            "cpu_cores": len(self.by_type("CPU")),
            "disks": len(self.by_type("DISK")),
            "net_ifaces": len(self.by_type("NET_IF")),
            "net_conns": len(self.by_type("NET_CONN")),
            "modules": len(self.by_type("MODULE")),
            "mounts": len(self.by_type("MOUNT")),
            "pci_devs": len(self.by_type("PCI_DEV")),
            "sensors": len(self.by_type("SENSOR")),
            "processes": len(self.by_type("PROC")),
        }
        with open(CARDS_DIR / "hardware.json", "w") as f:
            json.dump(hw, f, indent=2)

        # CPU summary
        cpu_cards = self.by_type("CPU")
        if cpu_cards:
            busy_vals = [c.get("busy_pct", 0) for c in cpu_cards]
            freq_vals = [c.get("freq_mhz", 0) for c in cpu_cards]
            with open(CARDS_DIR / "cpu_summary.json", "w") as f:
                json.dump({
                    "total_cores": len(cpu_cards),
                    "mean_busy_pct": round(sum(busy_vals) / max(len(busy_vals), 1), 1),
                    "mean_freq_mhz": round(sum(freq_vals) / max(len(freq_vals), 1), 1),
                    "cores": [{
                        "name": c["name"], "busy_pct": c.get("busy_pct", 0),
                        "freq_mhz": c.get("freq_mhz", 0),
                    } for c in cpu_cards],
                }, f, indent=2)

    def card_file(self, card_id: str) -> str:
        c = self._cards.get(card_id)
        if c:
            return self._render_card(c)
        return ""

    def _render_card(self, card: dict) -> str:
        ctype = card.get("type", "?")
        name = card.get("name", "?")
        cid = card.get("card_id", "?")
        phi = card.get("phi", np.zeros(36))
        p_norm = np.mod(phi, _TWO_PI) / _TWO_PI
        bar = "".join("█" if p > 0.33 else "░" if p > 0.1 else "·" for p in p_norm)

        lines = [f"# {cid} — {name}  ({_CARD_TYPE_LABELS.get(ctype, ctype)})"]
        lines.append("")
        lines.append(f"**Linux Card** — typ: {ctype}")
        lines.append(f"**Faza:** `{bar}`")
        lines.append("")

        # Specyficzne pola
        if ctype == "PROC":
            cpu = card.get("cpu_percent", 0) or 0
            mem = card.get("memory_percent", 0) or 0
            status = card.get("status", "?")
            pid = card.get("pid", 0)
            lines.append(f"**PID:** {pid}  **Stan:** {status.upper()}")
            lines.append(f"**CPU:** {cpu:.1f}%  **MEM:** {mem:.2f}%")
        elif ctype == "CPU":
            lines.append(f"**Busy:** {card.get('busy_pct', 0):.1f}%  "
                         f"**Freq:** {card.get('freq_mhz', 0):.0f}MHz")
        elif ctype == "DISK":
            lines.append(f"**Size:** {card.get('size_gb', 0):.1f}GB  "
                         f"**R:** {card.get('reads', 0)}  **W:** {card.get('writes', 0)}")
        elif ctype == "NET_IF":
            lines.append(f"**Speed:** {card.get('speed_mbps', 0)}Mbps  "
                         f"**MTU:** {card.get('mtu', 1500)}")
        elif ctype == "NET_CONN":
            proto = card.get("proto", "tcp").upper()
            drops = card.get("drops", 0)
            lines.append(f"**{proto} Port:** {card.get('port', 0)}  "
                         f"**State:** {card.get('state', '?')}  "
                         f"**Retrans:** {card.get('retrans', 0)}"
                         f"{'  **Drops:** ' + str(drops) if drops else ''}")
        elif ctype == "NET_FLOW":
            conns = card.get("conn_count", 0)
            active = card.get("active", 0)
            listen = card.get("listen", 0)
            retrans = card.get("total_retrans", 0)
            drops = card.get("total_drops", 0)
            ports = card.get("ports", [])
            protos = card.get("protos", [])
            lines.append(f"**PID:** {card.get('pid', 0)}  "
                         f"**Conns:** {conns} (active: {active})  "
                         f"**Listen:** {listen}")
            lines.append(f"**Retrans:** {retrans}  "
                         f"**Drops:** {drops}  "
                         f"**Proto:** {','.join(protos) if protos else '-'}")
            lines.append(f"**Ports:** {','.join(str(p) for p in ports[:6])}"
                         f"{'…' if len(ports) > 6 else ''}")
        elif ctype == "MODULE":
            lines.append(f"**Size:** {card.get('size_kb', 0)}KB  "
                         f"**Used by:** {card.get('used_by', '-')}")
        elif ctype == "MOUNT":
            lines.append(f"**Device:** {card.get('device', '?')}  "
                         f"**FS:** {card.get('fstype', '?')}")
            lines.append(f"**Usage:** {card.get('used_pct', 0):.1f}%  "
                         f"**Avail:** {card.get('avail_gb', 0):.1f}GB")
        elif ctype == "PCI_DEV":
            lines.append(f"**PCI:** {card.get('pci_addr', '?')}  "
                         f"**Class:** {card.get('class', '?')}  "
                         f"**IRQ:** {card.get('irq', 0)}")
        elif ctype == "SERVICE":
            act = card.get("active_state", "?")
            sub = card.get("sub_state", "?")
            uf = card.get("unit_file_state", "?")
            desc = card.get("description", "")
            pid = card.get("main_pid", 0)
            scope = "user" if card.get("is_user") else "system"
            lines.append(f"**{act}/{sub}**  **UF:** {uf}  **Scope:** {scope}")
            lines.append(f"**PID:** {pid}  **Desc:** {desc[:60]}")
        elif ctype == "SENSOR":
            st = card.get("sensor_type", "?")
            chip = card.get("chip", "?")
            lines.append(f"**Chip:** {chip}  **Type:** {st}")
            if st == "temp":
                t = card.get("temp_c", 0)
                lines.append(f"**Temp:** {t:.1f}°C")
            elif st == "fan":
                lines.append(f"**RPM:** {card.get('fan_rpm', 0)}")
            elif st == "power":
                lines.append(f"**Power:** {card.get('power_w', 0):.3f}W")
            elif st == "current":
                lines.append(f"**Current:** {card.get('curr_a', 0):.3f}A")
            elif st == "voltage":
                lines.append(f"**Voltage:** {card.get('volt_v', 0):.3f}V")

        lines.append("")
        lines.append("## PhaseNav φ[0:11] (12 regionów × 3 oscylatory)")
        for i in range(min(12, len(phi))):
            ch = ["M0", "M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9", "M10", "M11"][i]
            lines.append(f"- {ch}: {phi[i]:.3f}")
        return "\n".join(lines)
