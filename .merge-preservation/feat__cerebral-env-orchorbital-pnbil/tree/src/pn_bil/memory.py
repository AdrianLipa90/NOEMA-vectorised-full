from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .schema import CanonicalArtifact, FeatureSummary, ImmuneProfile, PhaseVectorRecord


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


class ImmuneMemory:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.profiles: list[ImmuneProfile] = []
        if self.path.exists():
            self.load()

    def load(self) -> None:
        raw = json.loads(self.path.read_text(encoding="utf-8"))
        self.profiles = [ImmuneProfile(**item) for item in raw.get("profiles", [])]

    def save(self) -> None:
        payload = {
            "schema": "pn-bis-immune-memory-v0.1",
            "updated_at_utc": utc_now_iso(),
            "profiles": [p.to_dict() for p in self.profiles],
        }
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    def enroll(
        self,
        label: str,
        artifact: CanonicalArtifact,
        phase_vector: PhaseVectorRecord,
        features: FeatureSummary,
        notes: str = "",
        structure_kind: str | None = None,
    ) -> ImmuneProfile:
        artifact_payload = artifact.to_dict()
        if structure_kind:
            artifact_payload["structure_kind"] = structure_kind
        profile = ImmuneProfile(
            label=label,
            artifact=artifact_payload,
            phase_vector=phase_vector.to_dict(),
            features=features.to_dict(),
            enrolled_at_utc=utc_now_iso(),
            notes=notes,
        )
        self.profiles.append(profile)
        self.save()
        return profile

    def by_sha256(self, sha256: str) -> ImmuneProfile | None:
        for profile in self.profiles:
            if profile.artifact.get("sha256") == sha256:
                return profile
        return None

    def is_empty(self) -> bool:
        return not self.profiles

    def to_dict(self) -> dict[str, Any]:
        return {"profiles": [p.to_dict() for p in self.profiles]}
