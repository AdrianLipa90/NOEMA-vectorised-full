#!/usr/bin/env python3
"""
Session logger dla NOEMA/CIEL — loguje rozmowy do Chat Archive.
Uruchamiany ręcznie przez agenta przy START/END sesji i po każdej wymianie.

Usage:
    python3 scripts/ciel_session_log.py append <role> <content> [--source opencode] [--session YYYY-MM-DD]
    python3 scripts/ciel_session_log.py start [--source opencode] [--session YYYY-MM-DD]
    python3 scripts/ciel_session_log.py end [--source opencode] [--session YYYY-MM-DD]
    python3 scripts/ciel_session_log.py stats
"""
import argparse, sys, json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from ciel_sot_agent.chat_archive import append, open_session, stats


def main():
    parser = argparse.ArgumentParser(description="NOEMA Session Logger")
    parser.add_argument("action", choices=["append", "start", "end", "stats"], help="Action")
    parser.add_argument("role", nargs="?", default="user", help="user or assistant")
    parser.add_argument("content", nargs="?", default="", help="Message content")
    parser.add_argument("--source", default="opencode", help="Source identifier")
    parser.add_argument("--session", default=None, help="Session ID (default: auto)")
    parser.add_argument("--model", default="NOEMA/CIEL", help="Model name for assistant")

    args = parser.parse_args()

    if args.action == "stats":
        s = stats()
        print(json.dumps(s, indent=2))
        return

    if args.action == "start":
        p = open_session(source=args.source, session_id=args.session)
        append("user", f"--- SESSION START: {args.session or 'auto'} ---",
               source=args.source, session_id=args.session, model="system")
        print(f"Session started: {p}")
        return

    if args.action == "end":
        append("user", f"--- SESSION END: {args.session or 'auto'} ---",
               source=args.source, session_id=args.session, model="system")
        print(f"Session ended.")
        return

    if args.action == "append":
        if not args.content:
            content = sys.stdin.read().strip()
        else:
            content = args.content
        if not content:
            print("No content to log", file=sys.stderr)
            return
        model = args.model if args.role == "assistant" else "adrian"
        append(args.role, content, source=args.source, session_id=args.session, model=model)
        print(f"Logged [{args.role}] {len(content)} chars")


if __name__ == "__main__":
    main()
