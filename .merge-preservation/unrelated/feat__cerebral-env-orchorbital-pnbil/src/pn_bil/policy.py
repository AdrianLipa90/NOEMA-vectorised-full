from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ImmunePolicy:
    """Decision thresholds for defensive self/non-self routing."""

    allow_distance: float = 0.08
    warn_distance: float = 0.18
    review_distance: float = 0.30
    high_bus_cost_warn: float = 0.70
    quarantine_on_kind_mismatch: bool = False
    warn_on_kind_mismatch: bool = True

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "ImmunePolicy":
        known = {field.name for field in cls.__dataclass_fields__.values()}  # type: ignore[attr-defined]
        return cls(**{k: v for k, v in payload.items() if k in known})

    @classmethod
    def load(cls, path: str | Path | None) -> "ImmunePolicy":
        if not path:
            return cls()
        raw = json.loads(Path(path).read_text(encoding="utf-8"))
        if raw.get("schema") == "pn-bis-policy-v0.2":
            raw = raw.get("policy", {})
        return cls.from_dict(raw)


def write_default_policy(path: str | Path) -> None:
    payload = {"schema": "pn-bis-policy-v0.2", "policy": ImmunePolicy().to_dict()}
    Path(path).write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
