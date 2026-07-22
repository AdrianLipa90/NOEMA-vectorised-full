#!/usr/bin/env python3
"""Faza 2 quiet-except — batch 4: HTTP handlery i pozostałe pliki.

APPLY=1 env var żeby zapisać.
"""
from __future__ import annotations
import os, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APPLY = os.environ.get("APPLY", "0") == "1"
LOGGER_PAT = re.compile(r'^(\s*)_NOEMA_QUIET_EXCEPT_LOGGER\.exception\(')

TARGET_FILES = [
    # HTTP handlery — raise zmienia odpowiedź na HTTP 500 zamiast JSON, daemon przeżyje
    "scripts/noema_portal_daemon.py",
    "scripts/serve_portal.py",
    "scripts/cielingo_mcp_server.py",
    "scripts/ciel_agent_backend.py",
    "scripts/ciel_browser_surface.py",
    "scripts/noema_imaginal_server.py",
    # Pozostałe
    "scripts/catalog_zips_noema.py",
    "scripts/build_definition_db_library.py",
    "scripts/noema_indexer.py",
    "scripts/ciel_benchmark_retrieval.py",
    "scripts/noema_phase_archiver.py",
    "scripts/bootstrap_audio_orbital_stack.py",
    "scripts/build_orbital_definition_registry.py",
    "scripts/noema_linux_body_bridge.py",
    "scripts/ciel_noema_x25519_exchange.py",
    "scripts/ciel_system_report.py",
    "scripts/build_memory_portal.py",
    "scripts/ciel_auto_log.py",
    "scripts/ciel_session_end.py",
    "scripts/ciel_noema_nonlocal_proxy.py",
    "scripts/ciel_lora_train.py",
    "scripts/ciel_noema_neutrino_daemon.py",
    "scripts/ciel_noema_nonlocal_listener.py",
    "scripts/ciel_lora_init.py",
    "scripts/ciel_noema_linux_sensor_daemon.py",
    "scripts/cielingo_premodel_inject.py",
    "scripts/ciel_process_exchange.py",
    "scripts/ciel_log_write.py",
    "scripts/ciel_repo_cards_throttle.py",
    "scripts/noema_handoff_auto.py",
    "scripts/ciel_knowledge_query.py",
    "scripts/noema_learn_file.py",
    "scripts/ciel_voynich_astro.py",
    "scripts/normalize_definition_registry.py",
    "scripts/noema_status.py",
    "scripts/bootstrap_audio_orbital_and_catalog.py",
    "scripts/build_nonlocal_definition_edges.py",
    "scripts/noema_voice_trigger.py",
    "scripts/noema_symbiotic_monitor.py",
    "scripts/optimize_wij.py",
    "scripts/ebpf_noema_daemon.py",
    "scripts/generate_orbital_cards.py",
    "scripts/mc_holonomic_convergence.py",
    "scripts/ciel_subconscious_supervisor.py",
    "scripts/run_ciel_gguf.py",
    "scripts/ciel_lora_train.py",
    "scripts/stress_pc_noema_htri_phasenav.py",
    "scripts/kuramoto_sym.py",
    "scripts/generate_object_cards_py.py",
    "scripts/ciel_collatz_router.py",
    "scripts/resolve_memory_orbital.py",
    "scripts/kuramoto_harmonic_comparison.py",
    "scripts/noema_erb_bench.py",
    "scripts/ciel_news_reader.py",
    "scripts/generate_site.py",
    "scripts/couple_assistant.py",
    "scripts/htri_bench.py",
    "scripts/import_chatgpt_logs.py",
    "scripts/ciel_chat_gui.py",
    "scripts/ciel_binding_plus.py",
    "scripts/generate_repo_cards.py",
    "scripts/classify_docs.py",
    "scripts/noema_repair_cycle.py",
    "scripts/consolidate_raw_logs_to_tsm.py",
    "scripts/noema_codegen.py",
    "scripts/ciel_mandatory_pipeline.py",
    "scripts/noema_hibernation.py",
    "scripts/build_orbital_definition_registry.py",
    "scripts/ciel_confidence_system/ingest.py",
    "scripts/ciel_confidence_system/report.py",
    "scripts/ciel_confidence_system/engine.py",
]


def process_file(rel: str) -> dict:
    path = ROOT / rel
    if not path.exists():
        return {"path": rel, "error": "not found", "injected": 0}
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    injections: list[int] = []
    for i, line in enumerate(lines):
        m = LOGGER_PAT.match(line)
        if not m:
            continue
        j = i + 1
        while j < len(lines) and not lines[j].strip():
            j += 1
        if (lines[j].strip() if j < len(lines) else "") == "raise":
            continue
        injections.append(i)
    if injections and APPLY:
        for idx in reversed(injections):
            indent = LOGGER_PAT.match(lines[idx]).group(1)
            lines.insert(idx + 1, f"{indent}raise\n")
        path.write_text("".join(lines), encoding="utf-8")
    return {"path": rel, "injected": len(injections), "applied": APPLY and bool(injections)}


total = 0
changed = 0
for rel in TARGET_FILES:
    r = process_file(rel)
    n = r.get("injected", 0)
    if n:
        mode = "APPLY" if APPLY else "DRY  "
        print(f"{mode} {rel}: +{n}")
        total += n
        if r.get("applied"):
            changed += 1
    elif "error" in r:
        pass  # pomiń brakujące

mode = "APPLY" if APPLY else "DRY-RUN"
print(f"\n{mode}: {total} raise łącznie, {changed if APPLY else total} plików")
