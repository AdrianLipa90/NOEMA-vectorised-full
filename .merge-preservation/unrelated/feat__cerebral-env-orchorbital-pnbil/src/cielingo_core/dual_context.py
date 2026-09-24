"""Separated public and private context stores for CIELingo.

The module intentionally stores records, hashes and provenance rather than
silently learning from a filesystem.  A caller must explicitly add a reviewed
``ContextRecord`` to a lane.  Public and private stores have no shared index.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import StrEnum
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Iterable


class ContextLane(StrEnum):
    PUBLIC = "public"
    PRIVATE = "private"
    QUARANTINE = "quarantine"
    REJECT = "reject"


@dataclass(frozen=True)
class ContextRecord:
    """A reviewed source reference; scanner manifests never include ``text``."""

    source_id: str
    source_path: str
    sha256: str
    lane: ContextLane
    license_id: str
    confidence: float
    retention: str = "review_required"
    provenance: dict[str, Any] = field(default_factory=dict)
    text: str = ""

    def public_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data.pop("text", None)
        data["lane"] = self.lane.value
        return data


class ContextAccessError(PermissionError):
    pass


def _stable_id(path: str, digest: str) -> str:
    return hashlib.sha256(f"{path}\0{digest}".encode("utf-8")).hexdigest()[:24]


class DualContextStore:
    """File-backed lane stores with encrypted private payloads.

    Encryption is deliberately fail-closed: a private lane cannot be opened
    without a valid Fernet key, and it cannot fall back to a plaintext file.
    """

    SCHEMA = "CIELINGO_DUAL_CONTEXT_V0_1"

    def __init__(self, root: str | Path, *, private_key: bytes | None = None) -> None:
        self.root = Path(root)
        self.private_key = private_key

    @staticmethod
    def generate_private_key() -> bytes:
        from cryptography.fernet import Fernet

        return Fernet.generate_key()

    def _path(self, lane: ContextLane) -> Path:
        suffix = ".private.fernet" if lane is ContextLane.PRIVATE else ".json"
        return self.root / f"{lane.value}_context{suffix}"

    def _fernet(self):
        if not self.private_key:
            raise ContextAccessError("private context requires an owner-supplied encryption key")
        from cryptography.fernet import Fernet

        return Fernet(self.private_key)

    def _load(self, lane: ContextLane) -> list[dict[str, Any]]:
        path = self._path(lane)
        if not path.exists():
            return []
        raw = path.read_bytes()
        if lane is ContextLane.PRIVATE:
            raw = self._fernet().decrypt(raw)
        data = json.loads(raw.decode("utf-8"))
        if data.get("schema") != self.SCHEMA or data.get("lane") != lane.value:
            raise ValueError(f"invalid {lane.value} context store")
        return list(data.get("records", []))

    def _save(self, lane: ContextLane, records: Iterable[dict[str, Any]]) -> None:
        if lane not in {ContextLane.PUBLIC, ContextLane.PRIVATE}:
            raise ContextAccessError("only reviewed public or private records may be persisted")
        payload = json.dumps(
            {"schema": self.SCHEMA, "lane": lane.value, "records": list(records)},
            ensure_ascii=False,
            sort_keys=True,
        ).encode("utf-8")
        if lane is ContextLane.PRIVATE:
            payload = self._fernet().encrypt(payload)
        path = self._path(lane)
        path.parent.mkdir(parents=True, exist_ok=True)
        temp = path.with_name(f".{path.name}.{os.getpid()}.tmp")
        temp.write_bytes(payload)
        os.replace(temp, path)

    def add(self, record: ContextRecord) -> None:
        if record.lane not in {ContextLane.PUBLIC, ContextLane.PRIVATE}:
            raise ContextAccessError("quarantined and rejected sources cannot enter a context store")
        if not record.source_id:
            record = ContextRecord(
                source_id=_stable_id(record.source_path, record.sha256),
                source_path=record.source_path,
                sha256=record.sha256,
                lane=record.lane,
                license_id=record.license_id,
                confidence=record.confidence,
                retention=record.retention,
                provenance=record.provenance,
                text=record.text,
            )
        records = self._load(record.lane)
        serialised = record.public_dict()
        serialised["text"] = record.text
        by_id = {item["source_id"]: item for item in records}
        by_id[record.source_id] = serialised
        self._save(record.lane, by_id.values())

    def records(self, lane: ContextLane) -> list[ContextRecord]:
        if lane not in {ContextLane.PUBLIC, ContextLane.PRIVATE}:
            return []
        return [
            ContextRecord(
                source_id=item["source_id"], source_path=item["source_path"],
                sha256=item["sha256"], lane=ContextLane(item["lane"]),
                license_id=item["license_id"], confidence=float(item["confidence"]),
                retention=item.get("retention", "review_required"),
                provenance=dict(item.get("provenance", {})), text=item.get("text", ""),
            )
            for item in self._load(lane)
        ]

    def remove_source(self, lane: ContextLane, source_id: str) -> bool:
        records = self._load(lane)
        kept = [record for record in records if record.get("source_id") != source_id]
        if len(kept) == len(records):
            return False
        self._save(lane, kept)
        return True

    def query(self, lane: ContextLane, query: str, *, limit: int = 5) -> list[ContextRecord]:
        """Small lexical retrieval, intentionally restricted to the requested lane."""
        if lane not in {ContextLane.PUBLIC, ContextLane.PRIVATE}:
            return []
        tokens = {token.casefold() for token in query.split() if len(token) > 2}
        scored: list[tuple[int, ContextRecord]] = []
        for record in self.records(lane):
            score = sum(token in record.text.casefold() for token in tokens)
            if score:
                scored.append((score, record))
        return [record for _, record in sorted(scored, key=lambda value: value[0], reverse=True)[:limit]]
