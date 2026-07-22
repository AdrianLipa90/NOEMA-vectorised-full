#!/usr/bin/env python3
"""Generate receipt-backed metrics from the canonical NOEMA knowledge database.

The generator is deliberately limited to exact database observations.  It does
not infer orbital physics, fabricate edge phases, or promote legacy orbital
tables whose method contains free parameters.  Every output identifies its
SQLite source, query specification and read-back receipt.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import sqlite3
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB = Path("/media/adrian/New Volume/CIEL_memories/state/noema_knowledge.db")
DEFAULT_OUTPUT = Path("/media/adrian/New Volume/CIEL_memories/state/noema_certified_database_metrics.json")


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def digest_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def digest_file(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def scalar_row(connection: sqlite3.Connection, query: str) -> dict[str, Any]:
    row = connection.execute(query).fetchone()
    if row is None:
        raise RuntimeError("aggregate query returned no row")
    return {key: row[key] for key in row.keys()}


def distribution(connection: sqlite3.Connection, query: str) -> list[dict[str, Any]]:
    return [{key: row[key] for key in row.keys()} for row in connection.execute(query)]


def finite_or_none(value: Any) -> float | None:
    if value is None:
        return None
    number = float(value)
    return number if math.isfinite(number) else None


def collect(db_path: Path) -> tuple[dict[str, Any], dict[str, str]]:
    queries = {
        "database_integrity": "PRAGMA integrity_check",
        "document_coverage": """
            SELECT COUNT(*) AS documents,
                   SUM(CASE WHEN full_text_len > 0 THEN 1 ELSE 0 END) AS documents_with_text,
                   SUM(CASE WHEN source_url IS NOT NULL AND TRIM(source_url) <> '' THEN 1 ELSE 0 END) AS documents_with_source_url,
                   SUM(CASE WHEN source_reliability IS NOT NULL THEN 1 ELSE 0 END) AS documents_with_source_reliability,
                   SUM(CASE WHEN confidence IS NOT NULL THEN 1 ELSE 0 END) AS documents_with_confidence,
                   SUM(CASE WHEN consistency_score IS NOT NULL THEN 1 ELSE 0 END) AS documents_with_consistency,
                   SUM(COALESCE(full_text_len, 0)) AS observed_text_characters,
                   AVG(confidence) AS confidence_mean,
                   AVG(consistency_score) AS consistency_mean,
                   AVG(source_reliability) AS source_reliability_mean
            FROM doc_analysis
        """,
        "concept_coverage": """
            SELECT COUNT(*) AS assignments,
                   COUNT(DISTINCT doc_idx) AS documents_with_assignments,
                   COUNT(DISTINCT operator_id) AS distinct_operators,
                   SUM(CASE WHEN score IS NOT NULL THEN 1 ELSE 0 END) AS assignments_with_score,
                   AVG(score) AS score_mean
            FROM doc_concepts
        """,
        "concept_methods": """
            SELECT COALESCE(method, 'NULL') AS method, COUNT(*) AS assignments
            FROM doc_concepts GROUP BY COALESCE(method, 'NULL') ORDER BY method
        """,
        "source_types": """
            SELECT COALESCE(source_type, 'NULL') AS source_type, COUNT(*) AS documents
            FROM doc_analysis GROUP BY COALESCE(source_type, 'NULL') ORDER BY source_type
        """,
        "legacy_orbital_methods": """
            SELECT COALESCE(method, 'NULL') AS method, COUNT(*) AS rows
            FROM doc_orbital_position GROUP BY COALESCE(method, 'NULL') ORDER BY method
        """,
    }
    uri = f"file:{db_path}?mode=ro"
    connection = sqlite3.connect(uri, uri=True)
    connection.row_factory = sqlite3.Row
    try:
        integrity = connection.execute(queries["database_integrity"]).fetchone()[0]
        if integrity != "ok":
            raise RuntimeError(f"SQLite integrity_check failed: {integrity}")
        document = scalar_row(connection, queries["document_coverage"])
        concepts = scalar_row(connection, queries["concept_coverage"])
        for key in ("confidence_mean", "consistency_mean", "source_reliability_mean"):
            document[key] = finite_or_none(document[key])
        concepts["score_mean"] = finite_or_none(concepts["score_mean"])
        metrics = {
            "schema": "noema.certified-database-metrics/v1",
            "generated_at": utc_now(),
            "epistemic_class": "exact_database_aggregate",
            "database": {"path": str(db_path), "sha256": digest_file(db_path), "integrity_check": integrity},
            "document_coverage": document,
            "phasenav_assignment_coverage": concepts,
            "phasenav_assignment_methods": distribution(connection, queries["concept_methods"]),
            "source_type_distribution": distribution(connection, queries["source_types"]),
            "physical_orbital_metrics": {
                "status": "unavailable",
                "reason": "database does not contain source-backed edge phase_shift, resonance, harmonic, or global coherence measurements",
            },
            "legacy_document_orbital_tables": {
                "status": "not_certified",
                "reason": "legacy placement method includes free parameters; its rows are not promoted by this generator",
                "methods": distribution(connection, queries["legacy_orbital_methods"]),
            },
            "query_sha256": {name: digest_bytes(query.encode("utf-8")) for name, query in queries.items()},
        }
    finally:
        connection.close()
    return metrics, queries


def write_once(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    partial = path.with_name(f".{path.name}.{os.getpid()}.{time.monotonic_ns()}.partial")
    try:
        with partial.open("xb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(partial, path)
        if path.read_bytes() != payload:
            raise RuntimeError("output read-back mismatch")
    finally:
        if partial.exists():
            partial.unlink()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    db_path = args.db.resolve(strict=True)
    metrics, _queries = collect(db_path)
    payload = canonical_bytes(metrics)
    output_sha256 = digest_bytes(payload)
    receipt = {
        "schema": "noema.certified-database-metrics-receipt/v1",
        "generated_at": utc_now(),
        "source_database_path": str(db_path),
        "source_database_sha256": metrics["database"]["sha256"],
        "output_path": str(args.output),
        "output_sha256": output_sha256,
        "epistemic_class": metrics["epistemic_class"],
        "physical_orbital_metrics_status": metrics["physical_orbital_metrics"]["status"],
        "legacy_document_orbital_tables_status": metrics["legacy_document_orbital_tables"]["status"],
    }
    if args.write:
        write_once(args.output, payload)
        receipt_path = args.output.parent / "receipts" / "noema_certified_database_metrics" / f"{output_sha256}.json"
        write_once(receipt_path, canonical_bytes(receipt))
        receipt["receipt_path"] = str(receipt_path)
        receipt["read_back_verified"] = True
    print(json.dumps({"metrics": metrics, "receipt": receipt, "written": args.write}, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
