#!/usr/bin/env python3
"""Native (no subprocess, no shelling out to lsof/netstat/dpkg) forensic
snapshot of one running process via /proc only — run only through
noema_run_script, never raw bash.

Usage: noema_investigate_pid.py <pid>

Reports: binary path (exe symlink), cmdline, cwd, start time, open file
descriptors (paths + sockets), and any TCP/UDP connections owned by this
process (cross-referenced from /proc/net/{tcp,tcp6,udp,udp6} by socket
inode) — the same raw data lsof/netstat would show, read directly instead
of shelling out.
"""
from __future__ import annotations
import json
import os
import socket
import struct
import sys
import time


def _read(path: str) -> str | None:
    try:
        with open(path, "rb") as f:
            return f.read().decode(errors="replace")
    except (FileNotFoundError, PermissionError):
        return None


def _proc_net_by_inode() -> dict[str, dict]:
    """Parse /proc/net/{tcp,tcp6,udp,udp6} -> {inode: {proto, local, remote, state}}."""
    out: dict[str, dict] = {}
    for proto, path in [
        ("tcp", "/proc/net/tcp"), ("tcp6", "/proc/net/tcp6"),
        ("udp", "/proc/net/udp"), ("udp6", "/proc/net/udp6"),
    ]:
        raw = _read(path)
        if not raw:
            continue
        lines = raw.splitlines()[1:]
        for line in lines:
            parts = line.split()
            if len(parts) < 10:
                continue
            local, remote, state, inode = parts[1], parts[2], parts[3], parts[9]

            def fmt(hex_addr: str) -> str:
                addr_hex, port_hex = hex_addr.split(":")
                port = int(port_hex, 16)
                if len(addr_hex) == 8:
                    addr = socket.inet_ntoa(struct.pack("<I", int(addr_hex, 16)))
                else:
                    addr = "[ipv6]"
                return f"{addr}:{port}"

            out[inode] = {
                "proto": proto,
                "local": fmt(local),
                "remote": fmt(remote),
                "state": state,
            }
    return out


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: noema_investigate_pid.py <pid>")
        return 2
    pid = sys.argv[1]
    base = f"/proc/{pid}"
    if not os.path.exists(base):
        print(json.dumps({"pid": pid, "error": "process not found"}))
        return 0

    report: dict = {"pid": pid, "collected_at": time.strftime("%Y-%m-%dT%H:%M:%S")}

    try:
        report["exe"] = os.readlink(f"{base}/exe")
    except (FileNotFoundError, PermissionError) as e:
        report["exe"] = f"<unreadable: {e}>"

    cmdline_raw = _read(f"{base}/cmdline") or ""
    report["cmdline"] = cmdline_raw.replace("\x00", " ").strip()

    try:
        report["cwd"] = os.readlink(f"{base}/cwd")
    except (FileNotFoundError, PermissionError) as e:
        report["cwd"] = f"<unreadable: {e}>"

    status = _read(f"{base}/status") or ""
    for line in status.splitlines():
        if line.startswith(("Uid:", "Gid:", "PPid:", "State:", "VmRSS:")):
            k, v = line.split(":", 1)
            report[f"status_{k}"] = v.strip()

    # stat time -> approximate start time relative to boot
    stat = _read(f"{base}/stat")
    if stat:
        report["stat_raw_tail"] = " ".join(stat.split()[-5:])

    # open file descriptors
    fds = []
    net_inodes = []
    fd_dir = f"{base}/fd"
    try:
        for fd in os.listdir(fd_dir):
            try:
                target = os.readlink(f"{fd_dir}/{fd}")
            except (FileNotFoundError, PermissionError):
                continue
            fds.append(target)
            if target.startswith("socket:["):
                net_inodes.append(target[8:-1])
    except (FileNotFoundError, PermissionError) as e:
        fds = [f"<unreadable: {e}>"]
    report["open_fds_count"] = len(fds)
    report["open_fds_sample"] = fds[:100]

    if net_inodes:
        net_map = _proc_net_by_inode()
        report["network_connections"] = [
            net_map[i] for i in net_inodes if i in net_map
        ]
    else:
        report["network_connections"] = []

    # child processes
    children = []
    for p in os.listdir("/proc"):
        if not p.isdigit():
            continue
        stat_line = _read(f"/proc/{p}/stat")
        if stat_line and f") " in stat_line:
            ppid_field = stat_line.split(") ", 1)[1].split()[1]
            if ppid_field == pid:
                children.append(p)
    report["child_pids"] = children

    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
