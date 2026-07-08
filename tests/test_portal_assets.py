from __future__ import annotations

import re
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SITE_ROOT = PROJECT_ROOT / "site"


def test_index_references_existing_local_scripts() -> None:
    index = (SITE_ROOT / "index.html").read_text()
    srcs = re.findall(r'<script[^>]+src="([^"]+)"', index)
    missing = []
    for src in srcs:
        if src.startswith("http") or src.startswith("//"):
            continue
        path = src.split("?", 1)[0]
        resolved = SITE_ROOT / path
        if not resolved.exists():
            missing.append(path)
    assert not missing, f"Missing portal scripts: {missing}"
