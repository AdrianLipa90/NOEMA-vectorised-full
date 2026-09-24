#!/usr/bin/env python3
"""
CIEL Mandatory Memory Pipeline — HARDCODED, NIE DO POMINIĘCIA.

Przed każdą odpowiedzią i po każdej odpowiedzi wymusza zapis do pamięci.
Wywolywany przez opencode hooks i/lub wpisany w prompt agenta.

Usage (pre-response):
    python3 scripts/ciel_mandatory_pipeline.py pre --role user --content "<prompt>" --tags "tag1,tag2"

Usage (post-response):
    python3 scripts/ciel_mandatory_pipeline.py post --role assistant --content "<odpowiedź>" --tags "tag1,tag2"

Usage (checkpoint):
    python3 scripts/ciel_mandatory_pipeline.py checkpoint
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

PROJECT = Path(__file__).resolve().parent.parent
SRC = PROJECT / "src"
for _path in (PROJECT, SRC):
    path_s = str(_path)
    if path_s not in sys.path:
        sys.path.insert(0, path_s)

from ciel_geometry.prompt_inject import PROMPT_INJECT_TIMEOUT_SECONDS


# ── Paths (env var override; fallback dynamiczny, bez hardcoded /home) ──
_SCRIPT_DIR = Path(__file__).resolve().parent
NOEMA_ROOT = Path(os.environ.get("NOEMA_ROOT", str(_SCRIPT_DIR.parent)))
SCRIPTS = NOEMA_ROOT / "scripts"
MEMORY_ROOT = Path(os.environ.get("CIEL_MEMORIES", os.path.join(os.sep, "media", "adrian", "New Volume", "CIEL_memories")))
LOGS_DIR = MEMORY_ROOT / "logs"
SESSIONS_DIR = MEMORY_ROOT / "logs" / "sessions"
SYSTEM_LOGS = MEMORY_ROOT / "logs" / "system"
ERROR_LOGS = MEMORY_ROOT / "logs" / "errors"
STATE_LOGS = MEMORY_ROOT / "logs" / "state"
SURFACE = Path("/dev/shm/ciel_noema")
AGENT_HINT = SURFACE / "agent_hint"


def ensure_dirs():
    """Utwórz strukturę katalogów jeśli nie istnieje."""
    for d in [LOGS_DIR, SESSIONS_DIR, SYSTEM_LOGS, ERROR_LOGS, STATE_LOGS, SURFACE]:
        d.mkdir(parents=True, exist_ok=True)


def timestamp() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S%z")


def date_str() -> str:
    return time.strftime("%Y-%m-%d")


def log_file() -> Path:
    """Plik logu na dzisiaj."""
    ensure_dirs()
    return SESSIONS_DIR / f"{date_str()}.jsonl"


def write_jsonl(filepath: Path, data: dict):
    """Dopisz JSONL z rotacją przy 10MB."""
    if filepath.exists() and filepath.stat().st_size > 10_000_000:
        backup = filepath.with_suffix(f".{int(time.time())}.jsonl")
        filepath.rename(backup)
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")


def run_script(name: str, args: list[str] | None = None) -> tuple[int, str]:
    """Wykonaj skrypt NOEMY."""
    script = SCRIPTS / name
    if not script.exists():
        return (-1, f"SCRYPT NOT FOUND: {script}")
    cmd = [sys.executable, str(script)]
    if args:
        cmd.extend(args)
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return (r.returncode, r.stdout.strip()[:500] + (r.stderr.strip()[:200] if r.stderr else ""))
    except subprocess.TimeoutExpired:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_mandatory_pipeline.py:81 quiet except scope=run_script reason=return (-1, \"TIMEOUT\")")
        raise
        return (-1, "TIMEOUT")
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_mandatory_pipeline.py:83 quiet except scope=run_script reason=return (-1, str(e))")
        raise
        return (-1, str(e))


def write_agent_hint(action: str, details: dict):
    """Zapisz agent_hint na surface."""
    try:
        hint = {
            "ts": timestamp(),
            "action": action,
            "details": details,
            "pid": os.getpid(),
        }
        AGENT_HINT.write_text(json.dumps(hint, indent=2, ensure_ascii=False))
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_mandatory_pipeline.py:97 quiet except scope=write_agent_hint reason=pass")
        raise
        pass  # surface może nie być dostępny


# ── Pre-response: przed KAŻDĄ odpowiedzią ────────────────────────────

def pre_response(role: str, content: str, tags: str):
    ensure_dirs()
    ts = timestamp()
    today = date_str()

    # 1. LOG PROMPT do session logu
    entry = {
        "ts": ts,
        "date": today,
        "role": role,
        "content": content[:2000],
        "tags": tags.split(",") if tags else [],
        "phase": "pre_response",
    }
    write_jsonl(log_file(), entry)

    # 2. CHECKPOINT (szybki)
    code, out = run_script("noema_checkpoint.py", ["--quick"])
    checkpoint_ok = (code == 0)

    # 3. LOG do system/consciousness_log
    sys_entry = {
        "ts": ts,
        "type": "interaction",
        "role": role,
        "phase": "pre",
        "checkpoint_ok": checkpoint_ok,
        "checkpoint_output": out,
    }
    write_jsonl(SYSTEM_LOGS / "consciousness_log.jsonl", sys_entry)

    # 4. WRITE agent_hint
    write_agent_hint("pre_response", {
        "role": role,
        "content_preview": content[:100],
        "checkpoint_ok": checkpoint_ok,
    })

    # 5. CIELingo premodel inject — enrichment przed odpowiedzią
    _inject_script = SCRIPTS / "cielingo_premodel_inject.py"
    if _inject_script.exists():
        try:
            _inject_payload = json.dumps({"message": content[:8000]})
            _inj = subprocess.run(
                [sys.executable, str(_inject_script)],
                input=_inject_payload,
                capture_output=True,
                text=True,
                timeout=PROMPT_INJECT_TIMEOUT_SECONDS,
            )
            if _inj.returncode == 0 and _inj.stdout.strip():
                _ctx_path = SURFACE / "cielingo_premodel_context.json"
                _ctx_path.write_text(_inj.stdout.strip())
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_mandatory_pipeline.py:154 quiet except scope=pre_response reason=pass")
            raise
            pass  # non-fatal

    return checkpoint_ok


# ── Post-response: po KAŻDEJ odpowiedzi ──────────────────────────────

def post_response(role: str, content: str, tags: str):
    ensure_dirs()
    ts = timestamp()
    today = date_str()

    # 1. LOG ODPOWIEDZI do session logu
    entry = {
        "ts": ts,
        "date": today,
        "role": role,
        "content": content[:2000],
        "tags": tags.split(",") if tags else [],
        "phase": "post_response",
    }
    write_jsonl(log_file(), entry)

    # 2. AUTO LOG (ciel_auto_log.py)
    code, out = run_script("ciel_auto_log.py", [
        "--role", role,
        "--content", content[:500],
        "--tags", tags or "auto",
    ])
    auto_log_ok = (code == 0)

    # 3. LOG do system/consciousness_log
    sys_entry = {
        "ts": ts,
        "type": "interaction",
        "role": role,
        "phase": "post",
        "auto_log_ok": auto_log_ok,
    }
    write_jsonl(SYSTEM_LOGS / "consciousness_log.jsonl", sys_entry)

    # 4. WRITE agent_hint
    write_agent_hint("post_response", {
        "role": role,
        "response_preview": content[:100],
        "auto_log_ok": auto_log_ok,
    })

    # 5. KEY INJECT "KONTYNUUJ" — automatycznie, zawsze na końcu
    run_script("noema_key_inject.py", ["KONTYNUUJ"])

    return auto_log_ok


# ── Checkpoint only ──────────────────────────────────────────────────

def do_checkpoint():
    code, out = run_script("noema_checkpoint.py", ["--quick"])
    result = {
        "ts": timestamp(),
        "ok": code == 0,
        "output": out,
        "phase": "checkpoint",
    }
    write_jsonl(SYSTEM_LOGS / "checkpoint.jsonl", result)
    return result


# ── Main ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="CIEL Mandatory Memory Pipeline")
    parser.add_argument("mode", choices=["pre", "post", "checkpoint"])
    parser.add_argument("--role", default="assistant")
    parser.add_argument("--content", default="")
    parser.add_argument("--tags", default="")
    args = parser.parse_args()

    if args.mode == "pre":
        ok = pre_response(args.role, args.content, args.tags)
        sys.exit(0 if ok else 1)

    elif args.mode == "post":
        ok = post_response(args.role, args.content, args.tags)
        sys.exit(0 if ok else 1)

    elif args.mode == "checkpoint":
        result = do_checkpoint()
        print(json.dumps(result, ensure_ascii=False))
        sys.exit(0 if result["ok"] else 1)


if __name__ == "__main__":
    main()
