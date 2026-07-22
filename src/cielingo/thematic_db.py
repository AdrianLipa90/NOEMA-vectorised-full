"""CIELingo thematic SQLite stores.

The manager creates one SQLite database per inferred theme so learned web
digests can be grouped by topic instead of being flattened into a single store.
"""
from __future__ import annotations

import json
import re
import sqlite3
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from .web_digest import WebDigest
from ciel_geometry.paths import P

DEFAULT_THEME = "general"
MIN_THEME_TOKEN_LENGTH = 4
MAX_THEME_CANDIDATES = 5
LOW_QUALITY_THEME_LIMIT = 1
MEDIUM_QUALITY_THEME_LIMIT = 2
QUALITY_GENERAL_THRESHOLD = 0.35
QUALITY_MINIMUM_THRESHOLD = 0.65


def _slugify(theme: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", theme.lower()).strip("-")
    return slug or "untitled"


def _unique(seq: Iterable[str]) -> list[str]:
    out: list[str] = []
    for item in seq:
        if item and item not in out:
            out.append(item)
    return out


@dataclass(frozen=True)
class ThematicDBInfo:
    theme: str
    path: str
    record_count: int

    def as_dict(self) -> dict[str, Any]:
        return {
            "theme": self.theme,
            "path": self.path,
            "record_count": self.record_count,
        }


class ThematicDatabaseManager:
    """Create and maintain one SQLite DB per theme."""

    def __init__(self, root_dir: str | Path | None = None):
        self.root_dir = (
            Path(root_dir)
            if root_dir is not None
            else Path(P.MEMORY) / "state" / "thematic_dbs"
        )
        self.root_dir.mkdir(parents=True, exist_ok=True)

    def db_path(self, theme: str) -> Path:
        return self.root_dir / f"{_slugify(theme)}.sqlite"

    def _ensure_schema(self, conn: sqlite3.Connection) -> None:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at REAL NOT NULL,
                theme TEXT NOT NULL,
                url TEXT NOT NULL,
                title TEXT NOT NULL,
                summary TEXT NOT NULL,
                excerpt TEXT NOT NULL,
                content_digest TEXT NOT NULL,
                source TEXT NOT NULL,
                content_type TEXT NOT NULL,
                status INTEGER NOT NULL,
                word_count INTEGER NOT NULL,
                sentence_count INTEGER NOT NULL,
                keywords_json TEXT NOT NULL,
                payload_json TEXT NOT NULL
            )
            """
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_records_theme_digest ON records(theme, content_digest)"
        )
        conn.execute(
            "CREATE UNIQUE INDEX IF NOT EXISTS idx_records_theme_unique ON records(theme, content_digest, url)"
        )

    def infer_themes(self, digest: WebDigest | dict[str, Any]) -> list[str]:
        if isinstance(digest, WebDigest):
            title = digest.title
            keywords = list(digest.keywords)
            source = digest.source
            quality_score = float(digest.quality_score)
            phase_profile = dict(digest.phase_profile)
        else:
            title = str(digest.get("title", ""))
            keywords = list(digest.get("keywords", []) or [])
            source = str(digest.get("source", "web"))
            quality_score = float(digest.get("quality_score", 0.5) or 0.5)
            phase_profile = dict(digest.get("phase_profile", {}) or {})

        if phase_profile:
            quality_score = float(phase_profile.get("composite", quality_score) or quality_score)

        themes = []
        if source and source not in {"web", "rss", "web_search"}:
            themes.append(source)

        if title:
            title_bits = [
                bit
                for bit in re.findall(
                    rf"[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ0-9]{{{MIN_THEME_TOKEN_LENGTH},}}",
                    title.lower(),
                )[:2]
            ]
            themes.extend(title_bits)

        themes.extend(keywords[:4])
        themes = [theme for theme in _unique(themes) if len(theme) >= MIN_THEME_TOKEN_LENGTH]

        if quality_score < QUALITY_GENERAL_THRESHOLD:
            return [DEFAULT_THEME]

        limit = MAX_THEME_CANDIDATES
        if quality_score < QUALITY_MINIMUM_THRESHOLD:
            limit = LOW_QUALITY_THEME_LIMIT if quality_score < 0.5 else MEDIUM_QUALITY_THEME_LIMIT

        return themes[:limit] or [DEFAULT_THEME]

    def register_digest(
        self,
        digest: WebDigest | dict[str, Any],
        *,
        themes: list[str] | None = None,
    ) -> dict[str, Any]:
        payload = digest.as_dict() if isinstance(digest, WebDigest) else dict(digest)
        inferred = themes or self.infer_themes(payload)
        dbs: list[ThematicDBInfo] = []

        for theme in inferred:
            path = self.db_path(theme)
            conn = sqlite3.connect(str(path), timeout=10)
            try:
                self._ensure_schema(conn)
                conn.execute(
                    """
                    INSERT OR IGNORE INTO records (
                        created_at, theme, url, title, summary, excerpt,
                        content_digest, source, content_type, status,
                        word_count, sentence_count, keywords_json, payload_json
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        time.time(),
                        theme,
                        str(payload.get("url", "")),
                        str(payload.get("title", "")),
                        str(payload.get("summary", "")),
                        str(payload.get("excerpt", "")),
                        str(payload.get("content_digest", "")),
                        str(payload.get("source", "")),
                        str(payload.get("content_type", "")),
                        int(payload.get("status", 0) or 0),
                        int(payload.get("word_count", 0) or 0),
                        int(payload.get("sentence_count", 0) or 0),
                        json.dumps(payload.get("keywords", []), ensure_ascii=False),
                        json.dumps(payload, ensure_ascii=False, sort_keys=True),
                    ),
                )
                conn.commit()
                count = conn.execute("SELECT COUNT(*) FROM records").fetchone()[0]
                dbs.append(ThematicDBInfo(theme=theme, path=str(path), record_count=int(count)))
            finally:
                conn.close()

        return {
            "themes": inferred,
            "dbs": [db.as_dict() for db in dbs],
            "count": len(dbs),
        }

    def list_databases(self) -> list[dict[str, Any]]:
        if not self.root_dir.exists():
            return []
        rows: list[dict[str, Any]] = []
        for path in sorted(self.root_dir.glob("*.sqlite")):
            theme = path.stem.replace("-", " ")
            try:
                conn = sqlite3.connect(str(path), timeout=5)
                try:
                    count = conn.execute("SELECT COUNT(*) FROM records").fetchone()[0]
                except Exception:
                    count = 0
                finally:
                    conn.close()
            except Exception:
                count = 0
            rows.append({"theme": theme, "path": str(path), "record_count": int(count)})
        return rows


__all__ = ["ThematicDBInfo", "ThematicDatabaseManager"]
