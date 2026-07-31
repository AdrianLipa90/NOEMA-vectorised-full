#!/usr/bin/env python3
"""OpenCode UserPromptSubmit hook: prompt -> CIELingo analysis -> model context."""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import json
import contextlib
import io
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
SRC = PROJECT / "src"
for _path in (PROJECT, SRC, PROJECT / "integration", PROJECT / "scripts"):
    path_s = str(_path)
    if path_s not in sys.path:
        sys.path.insert(0, path_s)

from ciel_geometry.prompt_inject import (
    collect_noema_metrics_summary,
    build_prompt_inject_context,
    should_include_metrics,
)

_AUXILIARY_HOOK_OUTPUT = None


def _get_auxiliary_hook_output():
    global _AUXILIARY_HOOK_OUTPUT
    if _AUXILIARY_HOOK_OUTPUT is not None:
        return _AUXILIARY_HOOK_OUTPUT
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            with contextlib.redirect_stderr(io.StringIO()):
                from scripts.ciel_auxiliary_entrance import build_auxiliary_hook_output as _build_auxiliary_hook_output
        _AUXILIARY_HOOK_OUTPUT = _build_auxiliary_hook_output
    except Exception:
        _AUXILIARY_HOOK_OUTPUT = None
    return _AUXILIARY_HOOK_OUTPUT


def _extract_message(data: dict) -> str:
    message = data.get("message") or data.get("prompt") or data.get("content") or ""
    if isinstance(message, list):
        parts = []
        for block in message:
            if isinstance(block, dict) and block.get("type") == "text":
                parts.append(str(block.get("text", "")))
            elif isinstance(block, str):
                parts.append(block)
        return " ".join(parts)
    return str(message)


def _read_cielingo_message() -> str:
    """Odczytaj wiadomość od CIELingo z per_message.json na surface."""
    surface = Path("/dev/shm/ciel_noema")
    msg_file = surface / "per_message.json"
    if not msg_file.exists():
        return ""
    try:
        data = json.loads(msg_file.read_text())
        msg = data.pop("message", "") or ""
        # Wyczyść message po odczycie (zapisz resztę z powrotem)
        if msg:
            data["message"] = ""
            msg_file.write_text(json.dumps(data))
        return str(msg).strip()
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/cielingo_premodel_inject.py:47 quiet except scope=_read_cielingo_message reason=return \"\"")
        return ""


def main() -> None:
    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/cielingo_premodel_inject.py:55 quiet except scope=main reason=assign_fallback")
        data = {}

    message = _extract_message(data).strip()
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        # Odczytaj wiadomość od CIELingo z surface
        cielingo_msg = _read_cielingo_message()
        metrics_summary = collect_noema_metrics_summary()
    
    if not message and not cielingo_msg and not metrics_summary.get("metrics"):
        print(json.dumps({"continue": True}))
        return

    build_auxiliary_hook_output = _get_auxiliary_hook_output()
    if build_auxiliary_hook_output is not None and message:
        try:
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                output = build_auxiliary_hook_output(message, cielingo_msg=cielingo_msg, metrics=metrics_summary)
            print(json.dumps(output, ensure_ascii=False))
            return
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/cielingo_premodel_inject.py:66 quiet except scope=main reason=auxiliary_fallback")
            pass

    cielingo_block = ""
    if cielingo_msg:
        cielingo_block = (
            "=== CIELINGO_MESSAGE ===\n"
            f"CIELingo mówi: {cielingo_msg}\n"
            "=== CIELINGO_MESSAGE_END ==="
        )

    # Wyciągnij act i operator z analizy PhaseNav żeby warunkowo włączyć metryki
    _act = ""
    _operator = ""
    _disposition = "ACCEPT"
    if message:
        try:
            from ciel_geometry.phase_nav_lang import analyze_prompt as _analyze_prompt
            _pn = _analyze_prompt(message)
            _operator = str(_pn.get("operator", ""))
        except Exception:
            pass
        try:
            from cielingo_core.dialogue_competence import assess_dialogue_signal
            _sig = assess_dialogue_signal(message)
            _act = str(_sig.act) if hasattr(_sig, "act") else ""
        except Exception:
            pass

    full_context = build_prompt_inject_context(
        message=message,
        cielingo_block=cielingo_block,
        metrics_summary=metrics_summary,
        include_metrics=should_include_metrics(
            act=_act,
            operator=_operator,
            disposition=_disposition,
        ),
    )

    print(json.dumps({
        "continue": True,
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": full_context,
        },
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
