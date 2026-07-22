#!/usr/bin/env python3
"""Command-line surface for the no-weight CIEL cerebral model."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from ciel_cerebral_model import CerebralLanguageModel

# Keep the CLI explicitly attached to the CIEL SOT package surface.
try:
    import ciel_sot_agent as _ciel_sot_agent  # noqa: F401
except ImportError:  # pragma: no cover - model bootstrap handles project paths
    _ciel_sot_agent = None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="CIEL cerebral language model")
    parser.add_argument("text", nargs="?", help="one input sentence")
    parser.add_argument("--status", action="store_true", help="print cerebral state")
    parser.add_argument("--json", action="store_true", help="print the full frame as JSON")
    parser.add_argument("--no-persist", action="store_true", help="do not update semantic state")
    parser.add_argument("--new-session", action="store_true", help="reset local working context before processing")
    parser.add_argument("--session-id", help="resume or create a named local session")
    parser.add_argument("--export-context", metavar="PATH", help="write a portable local context handoff")
    parser.add_argument("--import-context", metavar="PATH", help="restore a verified local context handoff")
    args = parser.parse_args(argv)

    if args.new_session and args.import_context:
        parser.error("--new-session i --import-context wzajemnie się wykluczają")
    if args.session_id:
        os.environ["CIEL_SESSION_ID"] = args.session_id
    model = CerebralLanguageModel(Path(__file__).resolve().parent.parent)
    if args.import_context:
        try:
            model.import_context(Path(args.import_context))
        except ValueError as exc:
            parser.error(str(exc))
    if args.new_session:
        model.new_session(reason="cli_user_requested")
    if args.status:
        if args.export_context:
            model.export_context(Path(args.export_context))
        print(json.dumps(model.status(), ensure_ascii=False, indent=2))
        return 0
    if not args.text and not args.export_context:
        parser.error("podaj tekst albo użyj --status")
    result = model.process(args.text, persist=not args.no_persist) if args.text else None
    handoff = model.export_context(Path(args.export_context)) if args.export_context else None
    if result is None:
        print(json.dumps(handoff, ensure_ascii=False, indent=2, default=str))
        return 0
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    else:
        print(result["reply"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
