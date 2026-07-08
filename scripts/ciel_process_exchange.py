#!/usr/bin/env python3
"""
CIEL Process Exchange — HARDCODED, NIE DO POMINIĘCIA.

JEDNO NARZĘDZIE które robi:
1. CIELingo enrichment (process_user_input) na prompcie użytkownika
2. Auto-log promptu + enrichment
3. Auto-log odpowiedzi
4. Konsolidację checkpoint

Usage:
    # Przed odpowiedzią: log prompt + enrichment
    python3 scripts/ciel_process_exchange.py pre-prompt \\
        --user-content "prompt Adriana" \\
        --tags "tag1,tag2"
    
    # Po odpowiedzi: log odpowiedź
    python3 scripts/ciel_process_exchange.py post-response \\
        --assistant-content "moja odpowiedź" \\
        --tags "tag1,tag2"
    
    # Startup check
    python3 scripts/ciel_process_exchange.py startup-check
"""
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
NOEMA_ROOT = Path(os.environ.get("NOEMA_ROOT", str(_SCRIPT_DIR.parent)))
SCRIPTS = NOEMA_ROOT / "scripts"
SRC = NOEMA_ROOT / "src"
CIEL_MEMORIES = Path(os.environ.get("CIEL_MEMORIES", os.path.join(os.sep, "media", "adrian", "New Volume", "CIEL_memories")))


def run(cmd: list[str], timeout: int = 30) -> tuple[int, str]:
    """Run a command and return (returncode, output)."""
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return (r.returncode, r.stdout.strip() + ("\n" + r.stderr.strip() if r.stderr else ""))
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_process_exchange.py:46 quiet except scope=run reason=return (-1, str(e))")
        return (-1, str(e))


# ── CIELingo Enrichment ────────────────────────────────────────────────

def cielingo_enrich(text: str) -> dict:
    """Run CIELingo process_user_input on text. Returns dict or empty."""
    import importlib.util
    # Dodaj SRC do sys.path przed zaimportowaniem
    sys.path.insert(0, str(SRC))
    spec = importlib.util.spec_from_file_location("ciel_coupling", SRC / "ciel_coupling.py")
    if spec is None or spec.loader is None:
        return {"error": "ciel_coupling.py not found"}
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    try:
        result = mod.process_user_input(text)
        return result
    except Exception as e:
        import traceback
        return {"error": str(e), "traceback": traceback.format_exc()}


def enrich_summary(enrich: dict) -> str:
    """Make a one-line summary of CIELingo enrichment for tagging."""
    keys = list(enrich.keys())
    # Extract key metrics
    phase = enrich.get("phase_projection", "")
    route = enrich.get("noema_route", "")
    deictic = enrich.get("deictic_frame", "")
    tau = enrich.get("tau_bridge", "")
    summary = enrich.get("summary", "")
    parts = []
    if phase:
        parts.append(f"φ={str(phase)[:40]}")
    if route:
        parts.append(f"route={str(route)[:40]}")
    if tau:
        parts.append(f"τ={str(tau)[:20]}")
    if summary:
        parts.append(f"summary={str(summary)[:60]}")
    return " | ".join(parts) if parts else f"enrich: {keys[:6]}"


# ── Pre-Prompt ─────────────────────────────────────────────────────────

def pre_prompt(user_content: str, tags: str):
    """Log prompt + CIELingo enrichment."""
    ts = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    
    # 1. CIELingo enrichment
    enrich = cielingo_enrich(user_content)
    enrich_ok = "error" not in enrich
    
    # 2. Auto-log promptu
    auto_tags = f"cielingo_enrichment,prompt,{tags}" if enrich_ok else f"prompt,{tags}"
    code1, out1 = run([
        sys.executable, str(SCRIPTS / "ciel_auto_log.py"),
        "--role", "user",
        "--content", user_content[:1500],
        "--tags", auto_tags,
    ])
    auto_ok = (code1 == 0)
    
    # 3. Log enrichment do osobnego pliku JSONL
    enrich_log = CIEL_MEMORIES / "logs" / "cielingo_enrichments.jsonl"
    enrich_log.parent.mkdir(parents=True, exist_ok=True)
    enrich_entry = {
        "ts": ts,
        "source": "ciel_process_exchange.py",
        "action": "pre_prompt",
        "enrich_ok": enrich_ok,
        "auto_log_ok": auto_ok,
        "enrichment_keys": list(enrich.keys()) if enrich_ok else [],
        "enrich_summary": enrich_summary(enrich) if enrich_ok else str(enrich.get("error", "unknown")),
        "content_preview": user_content[:100],
        "tags": tags,
    }
    with open(enrich_log, "a", encoding="utf-8") as f:
        f.write(json.dumps(enrich_entry, ensure_ascii=False) + "\n")
    
    # 4. Print enrichment summary for agent context
    print(json.dumps({
        "action": "pre_prompt",
        "enrich_ok": enrich_ok,
        "auto_log_ok": auto_ok,
        "enrich_summary": enrich_summary(enrich) if enrich_ok else "",
        "enrichment_keys": list(enrich.keys()) if enrich_ok else [],
        "auto_log_output": out1[:200],
    }, ensure_ascii=False))
    
    return enrich_ok and auto_ok


# ── Post-Response ──────────────────────────────────────────────────────

def post_response(assistant_content: str, tags: str):
    """Log odpowiedź asystenta."""
    ts = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    
    # 1. Auto-log odpowiedzi
    code1, out1 = run([
        sys.executable, str(SCRIPTS / "ciel_auto_log.py"),
        "--role", "assistant",
        "--content", assistant_content[:1500],
        "--tags", f"response,{tags}",
    ])
    auto_ok = (code1 == 0)
    
    # 2. Mandatory pipeline checkpoint (non-critical)
    code2, out2 = run([
        sys.executable, str(SCRIPTS / "ciel_mandatory_pipeline.py"),
        "post", "--role", "assistant",
        "--content", assistant_content[:500],
        "--tags", tags,
    ])
    mandatory_ok = (code2 == 0)
    
    # 3. Log odpowiedzi
    print(json.dumps({
        "action": "post_response",
        "auto_log_ok": auto_ok,
        "mandatory_post_ok": mandatory_ok,
        "output": out1[:200],
        "mandatory_output": out2[:200],
    }, ensure_ascii=False))
    
    return auto_ok


# ── Startup Check ──────────────────────────────────────────────────────

def startup_check():
    """Run full startup pipeline via shell script."""
    code, out = run(["bash", str(SCRIPTS / "ciel_startup_pipeline.sh")], timeout=60)
    print(out)
    return code == 0


# ── Main ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="CIEL Process Exchange Pipeline")
    sub = parser.add_subparsers(dest="mode", required=True)
    
    p1 = sub.add_parser("pre-prompt", help="Przed odpowiedzią: enrichment + auto_log promptu")
    p1.add_argument("--user-content", required=True)
    p1.add_argument("--tags", default="")
    
    p2 = sub.add_parser("post-response", help="Po odpowiedzi: auto_log odpowiedzi + checkpoint")
    p2.add_argument("--assistant-content", required=True)
    p2.add_argument("--tags", default="")
    
    p3 = sub.add_parser("startup-check", help="Pełny startup check")
    
    args = parser.parse_args()
    
    if args.mode == "pre-prompt":
        ok = pre_prompt(args.user_content, args.tags)
        sys.exit(0 if ok else 1)
    elif args.mode == "post-response":
        ok = post_response(args.assistant_content, args.tags)
        sys.exit(0 if ok else 1)
    elif args.mode == "startup-check":
        ok = startup_check()
        sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
