"""
ciel_confidence_system — Confidence-scored data ingestion + uncertainty tracking.

Public API:
  engine.score_confidence()      — score text confidence (0.0–1.0)
  engine.ConfidenceResult        — structured confidence breakdown
  engine.SOURCE_WEIGHTS          — source type → base weight mapping
  ingest.ingest_text()           — ingest content with confidence scoring
  ingest.extract_fragments()     — split text into meaningful fragments
  schema.migrate()               — DB schema migration
  backfill.backfill()            — backfill confidence for existing docs
  report.summary()               — overall uncertainty summary
  report.low_confidence_docs()   — docs below threshold
  report.unresolved_uncertainty()— unresolved uncertainty log entries
"""

from .engine import score_confidence, ConfidenceResult, SOURCE_WEIGHTS
from .ingest import ingest_text, extract_fragments
from .schema import migrate as migrate_schema
from .backfill import backfill as backfill_confidence

__all__ = [
    "score_confidence", "ConfidenceResult", "SOURCE_WEIGHTS",
    "ingest_text", "extract_fragments",
    "migrate_schema", "backfill_confidence",
]
