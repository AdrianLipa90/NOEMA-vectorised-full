from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class StructureSummary:
    """Small, safe, static structure summary for a binary artefact.

    This module deliberately avoids executing, unpacking, emulating, or using
    exploit-oriented parsing. It only inspects byte-level headers and marker
    patterns needed for defensive trust-signalling.
    """

    kind: str
    extension: str
    magic_hex: str
    has_nul_bytes: bool
    ascii_ratio: float
    printable_run_count: int
    marker_counts: dict[str, int]
    structural_notes: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))


def _count_printable_runs(data: bytes, min_len: int = 8) -> int:
    runs = 0
    current = 0
    for b in data:
        if 32 <= b <= 126 or b in {9, 10, 13}:
            current += 1
        else:
            if current >= min_len:
                runs += 1
            current = 0
    if current >= min_len:
        runs += 1
    return runs


def guess_kind(data: bytes, path: str | Path = "") -> tuple[str, list[str]]:
    notes: list[str] = []
    suffix = Path(path).suffix.lower() if path else ""

    if data.startswith(b"\x7fELF"):
        return "elf_executable_or_library", ["ELF magic detected"]
    if data.startswith(b"MZ"):
        return "pe_executable_or_library", ["MZ/PE DOS header magic detected"]
    if data.startswith((b"\xfe\xed\xfa\xce", b"\xce\xfa\xed\xfe", b"\xfe\xed\xfa\xcf", b"\xcf\xfa\xed\xfe")):
        return "macho_executable_or_library", ["Mach-O magic detected"]
    if data.startswith(b"PK\x03\x04"):
        return "zip_container", ["ZIP local-file header magic detected"]
    if data.startswith(b"%PDF"):
        return "pdf_document", ["PDF magic detected"]
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png_image", ["PNG magic detected"]
    if data.startswith(b"\xff\xd8\xff"):
        return "jpeg_image", ["JPEG magic detected"]
    if data.startswith(b"SQLite format 3\x00"):
        return "sqlite_database", ["SQLite database magic detected"]
    if data.startswith(b"#!"):
        return "script_with_shebang", ["shebang detected"]

    if suffix in {".so", ".dll", ".dylib"}:
        notes.append("library-like extension without recognised executable magic")
        return "library_like_unknown", notes
    if suffix in {".bin", ".dat", ".img", ".fw"}:
        notes.append("generic binary-like extension")
        return "generic_binary", notes
    if suffix in {".json", ".yaml", ".yml", ".toml", ".txt", ".md"}:
        notes.append("text/config-like extension")
        return "text_or_config", notes

    notes.append("no recognised magic; treating as unknown artefact")
    return "unknown", notes


def structure_summary(data: bytes, path: str | Path = "") -> StructureSummary:
    size = len(data) or 1
    kind, notes = guess_kind(data, path)
    printable = sum(1 for b in data if 32 <= b <= 126 or b in {9, 10, 13})
    ascii_ratio = _clamp01(printable / size)

    marker_specs = {
        "nul": b"\x00",
        "zip_local_header": b"PK\x03\x04",
        "zip_central_dir": b"PK\x01\x02",
        "pdf_object": b" obj",
        "elf_dynamic": b".dynamic",
        "elf_text": b".text",
        "pe_this_program": b"This program cannot be run in DOS mode",
        "url_http": b"http://",
        "url_https": b"https://",
    }
    marker_counts = {name: data.count(marker) for name, marker in marker_specs.items()}

    if marker_counts["url_http"] or marker_counts["url_https"]:
        notes.append("URL-like strings detected; inspect provenance if unexpected")
    if ascii_ratio > 0.85 and kind not in {"text_or_config", "script_with_shebang"}:
        notes.append("high printable ratio for non-text artefact")
    if ascii_ratio < 0.08 and len(data) > 256:
        notes.append("very low printable ratio; likely compressed, encrypted, or high-entropy payload")

    return StructureSummary(
        kind=kind,
        extension=Path(path).suffix.lower() if path else "",
        magic_hex=data[:16].hex(),
        has_nul_bytes=b"\x00" in data,
        ascii_ratio=ascii_ratio,
        printable_run_count=_count_printable_runs(data),
        marker_counts=marker_counts,
        structural_notes=notes,
    )
