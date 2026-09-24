#!/usr/bin/env python3
"""NOEMA CIELingo Reports Refresh Daemon — periodic (every 30 min) real
regeneration of the corpus-level cielingo reports and the meaning-debt /
infinitive-merge / canonization word pipeline outputs.

Origin (2026-07-11): Adrian, direct — "wlacz odswiezanie okresowe" (turn on
periodic refresh) after these were generated once for real
(canonize_resolved_words/generate_debt_word_cards/infinitive_merge_audit/
canonization_audit/corpus reports — see OPEN_ISSUES id
'meaning-debt-and-corpus-reports-generated-for-real' in
scripts/noema_repair_cycle.py for full context).

Deliberately a single long-running Type=simple service with an internal
sleep loop, NOT a systemd .timer + oneshot .service pair — the earlier
noema-word-canonize.timer got stuck registered-but-never-loaded and no
currently-sanctioned MCP tool could start a brand-new .timer unit. A plain
long-running .service is the same unit TYPE noema_daemon_enable_new already
supports, sidestepping that gap entirely.
"""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)

import json
import logging
import sys
import time
from pathlib import Path

ROOT = Path("/media/adrian/New Volume/CIEL_PROJECT_CANON/NOEMA")
sys.path.insert(0, str(ROOT / "src"))

logging.basicConfig(
    level=logging.INFO,
    format="[cielingo-reports-refresh] %(asctime)s %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

REFRESH_INTERVAL_S = 1800  # 30 min


def run_cycle() -> dict:
    results: dict[str, object] = {}
    out_dir = ROOT / "data/cielingo/reports"
    out_dir.mkdir(parents=True, exist_ok=True)

    from cielingo.tensor_scalar_field import tensor_scalar_report, write_tensor_scalar_report
    r = tensor_scalar_report(str(ROOT))
    write_tensor_scalar_report(out_dir / "tensor_scalar_field_report.json", r)
    results["tensor_scalar_field"] = r.get("card_count")

    from cielingo.infinitive_modal_potential import infinitive_modal_report, write_report as write_infmodal
    r = infinitive_modal_report(str(ROOT))
    write_infmodal(out_dir / "infinitive_modal_potential_report.json", str(ROOT))
    results["infinitive_modal_potential"] = r.get("infinitive_count")

    from cielingo.lexical_holonomy import lexical_holonomy_report, write_lexical_holonomy_report
    r = lexical_holonomy_report(str(ROOT))
    write_lexical_holonomy_report(out_dir / "lexical_holonomy_report.json", str(ROOT))
    results["lexical_holonomy"] = r.get("lexical_unit_count")

    from cielingo.vector_surface import vector_surface_report, write_vector_report
    r = vector_surface_report(str(ROOT))
    write_vector_report(out_dir / "vector_surface_report.json", r)
    results["vector_surface"] = r.get("card_count")

    from cielingo.htri_phase_bus import phase_bus_report
    r = phase_bus_report(str(ROOT))
    (out_dir / "htri_phase_bus_report.json").write_text(json.dumps(r, ensure_ascii=False, indent=2), encoding="utf-8")
    results["htri_phase_bus"] = r.get("card_count")

    from cielingo.collatz_semantic_htri_sync import synchronization_report
    r = synchronization_report(str(ROOT))
    (out_dir / "collatz_semantic_htri_sync_report.json").write_text(json.dumps(r, ensure_ascii=False, indent=2), encoding="utf-8")
    results["collatz_semantic_htri_sync"] = r.get("card_count")

    from cielingo.infinitive_merge_audit import generate_infinitive_merge_audit
    unknown_words = ROOT / "data/cielingo/unknown_word_audit/unknown_words.audit.jsonl"
    merge_out = ROOT / "data/cielingo/infinitive_merge_audit"
    r = generate_infinitive_merge_audit(str(unknown_words), str(merge_out))
    results["infinitive_merge_audit"] = r.get("infinitivized_count")

    from cielingo.canonization_audit import generate_canonization_audit
    r = generate_canonization_audit(
        infinitive_candidates_path=str(merge_out / "infinitive_candidates.jsonl"),
        residual_assignments_path=str(merge_out / "residual_assignments.jsonl"),
        output_dir=str(ROOT / "data/cielingo/canonization_audit"),
    )
    results["canonization_audit"] = r.get("decision_counts")

    from cielingo.meaning_debt_word_cards import generate_debt_word_cards
    debt_index = ROOT / "data/cielingo/debt_word_cards/source/affected_cards_index.csv"
    r = generate_debt_word_cards(
        str(debt_index),
        output_dir=str(ROOT / "data/cielingo/debt_word_cards"),
        source_label="ciel_pol_meaning_debt_cards_bundle",
    )
    results["debt_word_cards"] = r.candidate_cards

    return results


def main() -> int:
    log.info(f"starting, refresh_interval_s={REFRESH_INTERVAL_S}")
    while True:
        try:
            t0 = time.time()
            results = run_cycle()
            log.info(f"cycle OK in {time.time() - t0:.1f}s: {results}")
        except Exception as e:
            from ciel_geometry.phasenav_exception_bridge import phase_signal_exception
            phase_signal_exception("noema_cielingo_reports_refresh_daemon.main:run_cycle", e, operator_id="PAUSE")
            log.debug(f"cycle FAILED, will retry next interval: {e}")
        time.sleep(REFRESH_INTERVAL_S)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        pass
