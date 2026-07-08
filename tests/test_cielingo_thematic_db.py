from __future__ import annotations

import sqlite3

from cielingo.thematic_db import ThematicDatabaseManager


def test_register_digest_creates_one_db_per_theme(tmp_path) -> None:
    manager = ThematicDatabaseManager(root_dir=tmp_path)
    digest = {
        "url": "https://example.com/ai-memory",
        "title": "AI Memory Systems",
        "summary": "This digest discusses memory and learning.",
        "excerpt": "This digest discusses memory and learning.",
        "content_digest": "abc123",
        "source": "web",
        "content_type": "text/html",
        "status": 200,
        "word_count": 6,
        "sentence_count": 1,
        "keywords": ["ai", "memory", "learning"],
        "quality_score": 0.9,
    }

    result = manager.register_digest(digest, themes=["ai", "memory"])

    assert result["themes"] == ["ai", "memory"]
    assert len(result["dbs"]) == 2
    assert (tmp_path / "ai.sqlite").exists()
    assert (tmp_path / "memory.sqlite").exists()

    with sqlite3.connect(str(tmp_path / "memory.sqlite")) as conn:
        count = conn.execute("SELECT COUNT(*) FROM records").fetchone()[0]
        row = conn.execute("SELECT theme, title, url FROM records LIMIT 1").fetchone()

    assert count == 1
    assert row == ("memory", "AI Memory Systems", "https://example.com/ai-memory")


def test_infer_themes_uses_keywords(tmp_path) -> None:
    manager = ThematicDatabaseManager(root_dir=tmp_path)
    digest = {
        "title": "PhaseNav and web learning",
        "source": "web",
        "keywords": ["phase", "learning", "memory"],
    }

    themes = manager.infer_themes(digest)

    assert "phasenav" in themes
    assert "learning" in themes


def test_low_quality_digest_falls_back_to_general(tmp_path) -> None:
    manager = ThematicDatabaseManager(root_dir=tmp_path)
    digest = {
        "title": "Sparse note",
        "source": "web",
        "keywords": ["x"],
        "quality_score": 0.2,
    }

    assert manager.infer_themes(digest) == ["general"]


def test_list_databases_reports_created_groups(tmp_path) -> None:
    manager = ThematicDatabaseManager(root_dir=tmp_path)
    digest = {
        "url": "https://example.com/ethics",
        "title": "Ethics guide",
        "summary": "Ethics content",
        "excerpt": "Ethics content",
        "content_digest": "def456",
        "source": "web",
        "content_type": "text/html",
        "status": 200,
        "word_count": 4,
        "sentence_count": 1,
        "keywords": ["ethics"],
        "quality_score": 0.8,
    }

    manager.register_digest(digest, themes=["ethics"])
    listing = manager.list_databases()

    assert listing
    assert listing[0]["record_count"] == 1
