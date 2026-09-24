from __future__ import annotations

import base64
import hashlib
from pathlib import Path

from .schema import CanonicalArtifact

MAX_READ_BYTES = 256 * 1024 * 1024  # defensive cap for prototype use


class ArtifactTooLargeError(ValueError):
    pass


def read_binary(path: str | Path, max_bytes: int = MAX_READ_BYTES) -> bytes:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(str(p))
    if not p.is_file():
        raise ValueError(f"not a regular file: {p}")
    size = p.stat().st_size
    if size > max_bytes:
        raise ArtifactTooLargeError(
            f"artifact is {size} bytes; cap is {max_bytes} bytes in this prototype"
        )
    return p.read_bytes()


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_base64(data: bytes) -> str:
    """Return canonical RFC 4648 Base64 ASCII without line wrapping."""
    return base64.b64encode(data).decode("ascii")


def canonicalize(path: str | Path) -> tuple[CanonicalArtifact, bytes, str]:
    p = Path(path)
    data = read_binary(p)
    b64 = canonical_base64(data)
    artifact = CanonicalArtifact(
        path=str(p),
        size_bytes=len(data),
        sha256=sha256_hex(data),
        base64_sha256=sha256_hex(b64.encode("ascii")),
        base64_length=len(b64),
        sample_base64_prefix=b64[:96],
    )
    return artifact, data, b64
