"""Read-only, content-addressed manifests for exact M11 bundle groups."""
from __future__ import annotations

import hashlib
import json
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from .bundle_identity import BundleIdentityGroup


@dataclass(frozen=True)
class DerivedBundleManifest:
    bundle_id: str
    bundle_invariant: str
    manifest_invariant: str
    manifest_id: str
    entrypoints: tuple[str, ...]
    requirements: tuple[str, ...]
    requires_python: str | None
    requirements_sha256: str
    requirements_text: str
    authority: str = "DERIVED_READ_ONLY_NO_INSTALL_AUTHORITY"


def _digest(value: object) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def render_requirements(requirements: Sequence[str]) -> str:
    values = tuple(sorted(set(str(item).strip() for item in requirements if str(item).strip())))
    return "" if not values else "\n".join(values) + "\n"


def load_project_requires_python(pyproject: str | Path) -> str | None:
    payload = tomllib.loads(Path(pyproject).read_text(encoding="utf-8"))
    project = payload.get("project", {})
    value = project.get("requires-python") if isinstance(project, dict) else None
    return str(value).strip() if isinstance(value, str) and value.strip() else None


def derive_bundle_manifest(
    group: BundleIdentityGroup,
    *,
    requires_python: str | None = None,
) -> DerivedBundleManifest:
    requirements = tuple(sorted(set(group.requirements)))
    requirements_text = render_requirements(requirements)
    requirements_sha = hashlib.sha256(requirements_text.encode()).hexdigest()
    payload = {
        "schema": "CIELPC_DERIVED_BUNDLE_MANIFEST_V1",
        "bundle_id": group.bundle_id,
        "bundle_invariant": group.bundle_invariant,
        "requires_python": requires_python,
        "requirements": requirements,
        "requirements_sha256": requirements_sha,
    }
    invariant = _digest(payload)
    return DerivedBundleManifest(
        bundle_id=group.bundle_id,
        bundle_invariant=group.bundle_invariant,
        manifest_invariant=invariant,
        manifest_id=f"manifest:{invariant}",
        entrypoints=tuple(sorted(group.entrypoints)),
        requirements=requirements,
        requires_python=requires_python,
        requirements_sha256=requirements_sha,
        requirements_text=requirements_text,
    )


def derive_bundle_manifests(
    groups: Sequence[BundleIdentityGroup],
    *,
    requires_python: str | None = None,
) -> tuple[DerivedBundleManifest, ...]:
    return tuple(
        sorted(
            (derive_bundle_manifest(group, requires_python=requires_python) for group in groups),
            key=lambda item: item.bundle_id,
        )
    )


__all__ = [
    "DerivedBundleManifest",
    "derive_bundle_manifest",
    "derive_bundle_manifests",
    "load_project_requires_python",
    "render_requirements",
]
