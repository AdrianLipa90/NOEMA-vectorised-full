"""CIELingo local canonization audit.

This module checks the results of the unknown-word and infinitive-merge stages
and canonizes only what can be canonized locally without pretending dictionary
truth.

Canonicalization levels used here:

* ``external_canon``: requires imported/open-source lexical evidence. This patch
  does not create any external canon entries because no Wiktionary/SGJP/
  Morfeusz/plWordNet extract is present.
* ``local_morphology_canon_candidate``: deterministic local infinitive mapping
  accepted as a CIELingo-local candidate, still awaiting source verification.
* ``local_residual_set_canon``: owned residual set membership is canonical as a
  CIELingo workflow/taxonomy fact, not as lexical POS/lemma truth.
* ``deferred``: not enough evidence; keep review/source queue.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import datetime as dt
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable, Mapping

SCHEMA = "cielingo/canonization-audit/v0.1"
TRUSTED_LOCAL_INFINITIVE_MAPPING_TYPES = {
    "verbal_noun_owanie_to_ować",
    "finite_u_family_to_ować",
    "adverbial_participle_ując_to_ować",
    "adverbial_participle_ając_to_ać",
}
LOW_CONFIDENCE_MAPPING_TYPES = {
    "verbal_noun_anie_to_ać_low_conf",
}


def utc_now() -> str:
    return dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_json(payload: Any) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


def read_jsonl(path: str | Path) -> list[dict[str, Any]]:
    p = Path(path)
    if not p.exists():
        return []
    out: list[dict[str, Any]] = []
    with p.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def write_jsonl(path: str | Path, rows: Iterable[Mapping[str, Any]]) -> int:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with p.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(dict(row), ensure_ascii=False, sort_keys=True) + "\n")
            count += 1
    return count


@dataclass(frozen=True)
class CanonizationDecision:
    schema: str
    decision_id: str
    source_kind: str
    surface: str
    source_card_id: str | None
    proposed_canonical_form: str | None
    canonicalization_level: str
    decision: str
    confidence: float
    gate_result: str
    evidence_status: str
    canon_scope: str
    rationale: str
    required_next_action: str
    source_payload_digest: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def decide_infinitive(candidate: Mapping[str, Any]) -> CanonizationDecision:
    mapping_type = str(candidate.get("mapping_type", ""))
    confidence = float(candidate.get("confidence", 0.0))
    surface = str(candidate.get("source_surface", ""))
    infinitive = str(candidate.get("infinitive_candidate", ""))
    source_card_id = candidate.get("source_card_id")
    digest = sha256_json(candidate)
    if mapping_type in TRUSTED_LOCAL_INFINITIVE_MAPPING_TYPES and confidence >= 0.44:
        return CanonizationDecision(
            schema=SCHEMA,
            decision_id="canon_decision:" + sha256_json({"kind": "infinitive", "digest": digest})[:24],
            source_kind="infinitive_candidate",
            surface=surface,
            source_card_id=str(source_card_id) if source_card_id else None,
            proposed_canonical_form=infinitive,
            canonicalization_level="local_morphology_canon_candidate",
            decision="accept_local_canonical_infinitive_mapping",
            confidence=round(confidence, 6),
            gate_result="PASS_LOCAL_ONLY",
            evidence_status="local_rule_no_external_dictionary_evidence",
            canon_scope="CIELingo_local_mapping_not_dictionary_canon",
            rationale=f"Trusted deterministic local mapping type {mapping_type}; source verification still required.",
            required_next_action="verify_with_SGJP_Morfeusz_Wiktionary_then_promote_or_retract",
            source_payload_digest=digest,
        )
    return CanonizationDecision(
        schema=SCHEMA,
        decision_id="canon_decision:" + sha256_json({"kind": "infinitive_deferred", "digest": digest})[:24],
        source_kind="infinitive_candidate",
        surface=surface,
        source_card_id=str(source_card_id) if source_card_id else None,
        proposed_canonical_form=infinitive or None,
        canonicalization_level="deferred",
        decision="keep_as_candidate_pending_morphology_source_review",
        confidence=round(confidence, 6),
        gate_result="BLOCKED_LOW_CONFIDENCE_OR_HIGH_AMBIGUITY",
        evidence_status="local_rule_no_external_dictionary_evidence",
        canon_scope="none",
        rationale=f"Mapping type {mapping_type} is not safe enough for local canonization.",
        required_next_action="review_manually_and_verify_with_SGJP_Morfeusz_Wiktionary",
        source_payload_digest=digest,
    )


def decide_residual_assignment(assignment: Mapping[str, Any]) -> CanonizationDecision:
    residual_set_id = str(assignment.get("residual_set_id", ""))
    surface = str(assignment.get("surface", ""))
    source_card_id = assignment.get("source_card_id")
    confidence = float(assignment.get("confidence", 0.0))
    digest = sha256_json(assignment)
    return CanonizationDecision(
        schema=SCHEMA,
        decision_id="canon_decision:" + sha256_json({"kind": "residual", "digest": digest})[:24],
        source_kind="residual_assignment",
        surface=surface,
        source_card_id=str(source_card_id) if source_card_id else None,
        proposed_canonical_form=residual_set_id,
        canonicalization_level="local_residual_set_canon",
        decision="accept_local_residual_set_membership_only",
        confidence=round(confidence, 6),
        gate_result="PASS_WORKFLOW_TAXONOMY_ONLY",
        evidence_status="local_assignment_no_external_dictionary_evidence",
        canon_scope="CIELingo_workflow_taxonomy_not_lexical_truth",
        rationale="Residual set membership is a local workflow fact. It does not canonize POS, lemma, or dictionary meaning.",
        required_next_action=str(assignment.get("next_action", "source_lookup_or_human_review")),
        source_payload_digest=digest,
    )


def generate_canonization_audit(
    *,
    infinitive_candidates_path: str | Path,
    residual_assignments_path: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    infinitives = read_jsonl(infinitive_candidates_path)
    residuals = read_jsonl(residual_assignments_path)
    decisions = [decide_infinitive(x) for x in infinitives] + [decide_residual_assignment(x) for x in residuals]

    accepted_infinitives = [d.as_dict() for d in decisions if d.decision == "accept_local_canonical_infinitive_mapping"]
    deferred_infinitives = [d.as_dict() for d in decisions if d.source_kind == "infinitive_candidate" and d.decision != "accept_local_canonical_infinitive_mapping"]
    residual_canon = [d.as_dict() for d in decisions if d.source_kind == "residual_assignment"]
    all_decisions = [d.as_dict() for d in decisions]

    paths = {
        "canonization_decisions": out / "canonization_decisions.jsonl",
        "canonical_infinitive_map": out / "canonical_infinitive_map.local.jsonl",
        "deferred_infinitive_candidates": out / "deferred_infinitive_candidates.jsonl",
        "canonical_residual_set_assignments": out / "canonical_residual_set_assignments.local.jsonl",
    }
    write_jsonl(paths["canonization_decisions"], all_decisions)
    write_jsonl(paths["canonical_infinitive_map"], accepted_infinitives)
    write_jsonl(paths["deferred_infinitive_candidates"], deferred_infinitives)
    write_jsonl(paths["canonical_residual_set_assignments"], residual_canon)

    report = {
        "schema": "cielingo/canonization-audit-report/v0.1",
        "created_at_utc": utc_now(),
        "input_counts": {"infinitive_candidates": len(infinitives), "residual_assignments": len(residuals)},
        "decision_counts": {
            "accepted_local_infinitive_mappings": len(accepted_infinitives),
            "deferred_infinitive_candidates": len(deferred_infinitives),
            "accepted_local_residual_set_assignments": len(residual_canon),
            "external_dictionary_canon_entries": 0,
        },
        "canonization_policy": {
            "external_canon_requires": ["Wiktionary/SGJP/Morfeusz/plWordNet evidence", "human or supervised review", "append-only promotion event"],
            "local_infinitive_canon_scope": "CIELingo local morphology map only",
            "local_residual_canon_scope": "CIELingo workflow taxonomy only",
            "numeric_order_semantics": False,
        },
        "outputs": {k: str(v) for k, v in paths.items()},
        "epistemic_boundary": "No external lexical evidence was imported. This audit canonizes only local mapping/set-membership facts, not dictionary truth.",
    }
    report["digest"] = sha256_json(report)
    (out / "canonization_audit_report.json").write_text(json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    return report


__all__ = [
    "CanonizationDecision",
    "decide_infinitive",
    "decide_residual_assignment",
    "generate_canonization_audit",
]
