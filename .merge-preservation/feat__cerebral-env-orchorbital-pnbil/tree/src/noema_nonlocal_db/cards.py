"""Card loader/validator for the NOEMA nonlocal database bootstrap layer."""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


@dataclass(frozen=True)
class NoemaCard:
    card_id: str
    path: str
    payload: dict[str, Any]


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_cards(root: str | Path, rel_dir: str = "cards/noema_nonlocal_db") -> list[NoemaCard]:
    """Load NOEMA nonlocal DB cards deterministically."""
    base = Path(root).resolve() / rel_dir
    cards: list[NoemaCard] = []
    if not base.exists():
        return cards
    for path in sorted(base.glob("*.noema.card.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        card_id = str(payload.get("card_id", path.stem))
        cards.append(NoemaCard(card_id=card_id, path=path.relative_to(Path(root).resolve()).as_posix(), payload=payload))
    return cards


def validate_cards(cards: Iterable[NoemaCard]) -> dict[str, Any]:
    """Validate card ids, dependency targets and epistemic boundary fields."""
    card_list = list(cards)
    ids = [c.card_id for c in card_list]
    id_set = set(ids)
    errors: list[dict[str, Any]] = []
    if len(ids) != len(id_set):
        errors.append({"code": "duplicate_card_id", "severity": "high"})
    for card in card_list:
        payload = card.payload
        if payload.get("schema") != "noema/nonlocal-db-card/v0.1":
            errors.append({"code": "bad_schema", "card_id": card.card_id, "path": card.path})
        if not payload.get("epistemic_boundary"):
            errors.append({"code": "missing_epistemic_boundary", "card_id": card.card_id, "path": card.path})
        for dep in payload.get("depends_on", []):
            if dep not in id_set:
                errors.append({"code": "missing_dependency", "card_id": card.card_id, "missing": dep, "path": card.path})
    return {
        "card_count": len(card_list),
        "ids": ids,
        "errors": errors,
        "valid": not errors,
    }


def card_registry_digest(cards: Iterable[NoemaCard]) -> str:
    rows = []
    for card in sorted(cards, key=lambda c: c.card_id):
        rows.append({"card_id": card.card_id, "path": card.path, "payload": card.payload})
    data = json.dumps(rows, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return _sha256_text(data)


__all__ = ["NoemaCard", "load_cards", "validate_cards", "card_registry_digest"]
