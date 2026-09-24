#!/usr/bin/env python3
"""CLI for NOEMA Registry — manage daemon registration tokens.

Usage:
    python scripts/noema_register_cli.py register <name> [--claims ...]
    python scripts/noema_register_cli.py list [--timeout 30]
    python scripts/noema_register_cli.py heartbeat <token>
    python scripts/noema_register_cli.py unregister <token>
    python scripts/noema_register_cli.py check <token> <file>
    python scripts/noema_register_cli.py cleanup
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from ciel_geometry.noema_registry import registry


def cmd_register(args: argparse.Namespace) -> int:
    claims = args.claims if args.claims else None
    token = registry.register(args.name, surface_claims=claims)
    print(token)
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    active = registry.list_active(timeout=args.timeout)
    if not active:
        print("No active registrations.")
        return 0
    print(f"{'NAME':<16} {'PID':>6} {'TOKEN':<36} {'CLAIMS':<30} {'HEARTBEAT':<22}")
    print("-" * 110)
    for entry in active:
        hb_age = f"{time.time() - entry['heartbeat_at']:.1f}s ago" if 'heartbeat_at' in entry else "?"
        print(f"{entry.get('name', '?'):<16} {entry.get('pid', 0):>6} "
              f"{entry.get('token', '?'):<36} "
              f"{','.join(entry.get('surface_claims', [])):<30} "
              f"{hb_age:<22}")
    return 0


def cmd_heartbeat(args: argparse.Namespace) -> int:
    ok = registry.heartbeat(args.token)
    return 0 if ok else 1


def cmd_unregister(args: argparse.Namespace) -> int:
    ok = registry.unregister(args.token)
    return 0 if ok else 1


def cmd_check(args: argparse.Namespace) -> int:
    ok = registry.check_access(args.token, args.file)
    print("ACCESS_GRANTED" if ok else "ACCESS_DENIED")
    return 0 if ok else 1


def cmd_cleanup(args: argparse.Namespace) -> int:
    removed = registry.cleanup()
    print(f"Removed {removed} stale registration(s).")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="NOEMA Registry CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    p_register = sub.add_parser("register", help="Register a daemon")
    p_register.add_argument("name", help="Daemon name")
    p_register.add_argument("--claims", nargs="*", help="Surface file claims")
    p_register.set_defaults(func=cmd_register)

    p_list = sub.add_parser("list", help="List active registrations")
    p_list.add_argument("--timeout", type=float, default=30.0, help="Heartbeat timeout (s)")
    p_list.set_defaults(func=cmd_list)

    p_hb = sub.add_parser("heartbeat", help="Send heartbeat")
    p_hb.add_argument("token", help="Registration token")
    p_hb.set_defaults(func=cmd_heartbeat)

    p_unreg = sub.add_parser("unregister", help="Unregister")
    p_unreg.add_argument("token", help="Registration token")
    p_unreg.set_defaults(func=cmd_unregister)

    p_check = sub.add_parser("check", help="Check surface file access")
    p_check.add_argument("token", help="Registration token")
    p_check.add_argument("file", help="Surface file name")
    p_check.set_defaults(func=cmd_check)

    p_clean = sub.add_parser("cleanup", help="Remove stale registrations")
    p_clean.set_defaults(func=cmd_cleanup)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
