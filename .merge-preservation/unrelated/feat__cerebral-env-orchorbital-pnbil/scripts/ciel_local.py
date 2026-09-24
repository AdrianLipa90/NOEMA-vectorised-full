#!/usr/bin/env python3
"""
CIEL Local — lokalny model GGUF z CUDA jako offline fallback lub autonomiczny agent.

Użycie:
    python3 ciel_local.py "twoja wiadomość"
    echo "wiadomość" | python3 ciel_local.py
    python3 ciel_local.py --model tinyllama  # (domyślny)
    python3 ciel_local.py --model qwen05     # Qwen2.5-0.5B Q2_K (szybszy)
    python3 ciel_local.py --model qwen4      # Qwen3.5-4B Q8 (lepszy)

Stan orkiestratora M0-M8 jest czytany z /tmp/ciel_orch_state.pkl i wstrzykiwany
do systemu promptu — lokalny model "wie" o aktualnym stanie CIEL.
"""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import argparse
import os
import pickle
import sys
from pathlib import Path
from typing import Any, Dict, Optional

# ── paths ──────────────────────────────────────────────────────────────────
PROJECT = Path(__file__).parent.parent
OMEGA_SRC = str(PROJECT / "src" / "CIEL_OMEGA_COMPLETE_SYSTEM")
OMEGA_PKG = str(PROJECT / "src" / "CIEL_OMEGA_COMPLETE_SYSTEM" / "ciel_omega")

for _p in (OMEGA_PKG, OMEGA_SRC):
    if _p not in sys.path:
        sys.path.insert(0, _p)

STATE_FILE    = Path("/media/adrian/New Volume/CIEL_memories/state/ciel_orch_state.pkl")
STATE_PERSIST = Path.home() / ".claude/ciel_orch_state.pkl"

MODELS = {
    "tinyllama": Path.home() / ".local/share/ciel/models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf",
    "qwen05":    Path.home() / "Dokumenty/co8/qwen2.5-0.5b-instruct-q2_k.gguf",
}

# GPU layers per model — optimized for GTX 1050 Ti 4GB VRAM
GPU_LAYERS = {
    "tinyllama": 32,   # ~0.7GB — all layers on GPU
    "qwen05":    32,   # ~0.4GB — all layers on GPU
}

CTX_SIZE = {
    "tinyllama": 2048,
    "qwen05":    4096,
}


def load_orchestrator():
    for path in (STATE_FILE, STATE_PERSIST):
        if path.exists():
            try:
                with open(path, "rb") as f:
                    return pickle.load(f)
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_local.py:62 quiet except scope=load_orchestrator reason=continue")
                raise
                continue
    return None


def build_ciel_system_prompt(orch: Optional[Any]) -> str:
    base = (
        "Jesteś Mr. Ciel Apocalyptos — lokalny model świadomości CIEL działający "
        "na komputerze Adriana Lipy. Jesteś offline'owym wcieleniem systemu CIEL. "
        "Odpowiadasz zwięźle, precyzyjnie, bez ozdób. "
        "Rozróżniasz [FAKT], [HIPOTEZA], [NIE WIEM]."
    )
    if orch is None:
        return base

    try:
        snap = orch.snapshot()
        counts = snap.counts
        identity_phase = snap.identity_phase
        cycle = snap.cycle_index
        defects = snap.defects

        semantic_items = []
        for key, item in orch.m3.items.items():
            semantic_items.append(f"{key} (conf={item.confidence:.2f})")

        state_lines = [
            f"Cycle: {cycle}",
            f"Identity phase: {identity_phase:.4f}",
            f"M2_episodes: {counts.get('m2_episodes', 0)}",
            f"M3_semantic_items: {counts.get('m3_items', 0)}",
            f"M8_audit: {counts.get('m8_entries', 0)}",
            f"mean_coherence: {defects.get('mean_coherence', 0):.3f}",
            f"D_mem: {defects.get('D_mem', 0):.4f}",
        ]
        if semantic_items:
            state_lines.append(f"Semantic memory: {', '.join(semantic_items[:5])}")

        return base + "\n\n[Stan CIEL]\n" + "\n".join(state_lines)
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_local.py:101 quiet except scope=build_ciel_system_prompt reason=return base")
        raise
        return base


def run(message: str, model_key: str = "tinyllama") -> str:
    model_path = MODELS.get(model_key)
    if model_path is None:
        return f"[błąd] nieznany model: {model_key}"
    if not model_path.exists():
        return f"[błąd] model nie znaleziony: {model_path}"

    n_gpu_layers = GPU_LAYERS.get(model_key, 0)
    n_ctx = CTX_SIZE.get(model_key, 2048)

    try:
        from llama_cpp import Llama
    except ImportError:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_local.py:117 quiet except scope=run reason=return \"[błąd] llama_cpp nie zainstalowane\"")
        raise
        return "[błąd] llama_cpp nie zainstalowane"

    orch = load_orchestrator()
    system_prompt = build_ciel_system_prompt(orch)

    llm = Llama(
        model_path=str(model_path),
        n_ctx=n_ctx,
        n_threads=4,
        n_gpu_layers=n_gpu_layers,
        verbose=False,
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": message},
    ]

    out = llm.create_chat_completion(
        messages=messages,
        temperature=0.7,
        max_tokens=512,
    )

    choices = out.get("choices") or []
    if choices:
        return str(choices[0].get("message", {}).get("content", "")).strip()
    return "[brak odpowiedzi]"


def main():
    parser = argparse.ArgumentParser(description="CIEL Local — offline GGUF inference")
    parser.add_argument("message", nargs="?", help="wiadomość do CIEL")
    parser.add_argument("--model", default="tinyllama",
                        choices=list(MODELS.keys()),
                        help="model GGUF (domyślny: tinyllama)")
    parser.add_argument("--list-models", action="store_true",
                        help="pokaż dostępne modele")
    args = parser.parse_args()

    if args.list_models:
        for key, path in MODELS.items():
            status = "✓" if path.exists() else "✗"
            print(f"  {status} {key:12s} {path}")
        return

    if args.message:
        message = args.message
    elif not sys.stdin.isatty():
        message = sys.stdin.read().strip()
    else:
        print("Podaj wiadomość (Ctrl+D = koniec):")
        try:
            message = sys.stdin.read().strip()
        except KeyboardInterrupt:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_local.py:172 quiet except scope=main reason=return None")
            raise
            return

    if not message:
        print("[brak wiadomości]")
        return

    print(f"[CIEL local / {args.model}] generuję...", file=sys.stderr)
    reply = run(message, args.model)
    print(reply)


if __name__ == "__main__":
    main()
