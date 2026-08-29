from __future__ import annotations

import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from ciel_geometry.phasenav.bundle_identity import BundleIdentityGroup
from ciel_geometry.phasenav.bundle_manifest import (
    derive_bundle_manifest,
    derive_bundle_manifests,
    load_project_requires_python,
    render_requirements,
)


def _group(entrypoints=("a", "b"), requirements=("numpy==2.0.0",)):
    invariant = "a" * 64
    return BundleIdentityGroup(
        bundle_invariant=invariant,
        bundle_id=f"bundle:{invariant}",
        entrypoints=tuple(entrypoints),
        requirements=tuple(requirements),
    )


def test_manifest_is_one_per_bundle_group_and_keeps_entrypoints_as_provenance():
    manifests = derive_bundle_manifests((_group(),), requires_python=">=3.11")
    assert len(manifests) == 1
    manifest = manifests[0]
    assert manifest.entrypoints == ("a", "b")
    assert manifest.requirements == ("numpy==2.0.0",)
    assert manifest.requirements_text == "numpy==2.0.0\n"
    assert manifest.authority == "DERIVED_READ_ONLY_NO_INSTALL_AUTHORITY"


def test_entrypoint_rename_does_not_change_manifest_identity():
    left = derive_bundle_manifest(_group(entrypoints=("old-name",)), requires_python=">=3.11")
    right = derive_bundle_manifest(_group(entrypoints=("new-name",)), requires_python=">=3.11")
    assert left.manifest_invariant == right.manifest_invariant
    assert left.manifest_id == right.manifest_id


def test_requires_python_is_manifest_identity_bearing():
    left = derive_bundle_manifest(_group(), requires_python=">=3.11")
    right = derive_bundle_manifest(_group(), requires_python=">=3.12")
    assert left.manifest_invariant != right.manifest_invariant
    assert left.manifest_id != right.manifest_id


def test_requirements_render_is_deterministic_and_deduplicated():
    text = render_requirements(("scipy==1.14.0", "numpy==2.0.0", "numpy==2.0.0"))
    assert text == "numpy==2.0.0\nscipy==1.14.0\n"
    manifest = derive_bundle_manifest(
        _group(requirements=("scipy==1.14.0", "numpy==2.0.0", "numpy==2.0.0"))
    )
    assert manifest.requirements == ("numpy==2.0.0", "scipy==1.14.0")
    assert manifest.requirements_sha256 == hashlib.sha256(text.encode()).hexdigest()


def test_empty_requirements_render_to_empty_content():
    manifest = derive_bundle_manifest(_group(requirements=()), requires_python=">=3.11")
    assert manifest.requirements_text == ""
    assert manifest.requirements_sha256 == hashlib.sha256(b"").hexdigest()


def test_load_project_requires_python_is_exact_declared_constraint(tmp_path: Path):
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text(
        "[project]\nname='demo'\nversion='0'\nrequires-python='>=3.11'\n",
        encoding="utf-8",
    )
    assert load_project_requires_python(pyproject) == ">=3.11"
