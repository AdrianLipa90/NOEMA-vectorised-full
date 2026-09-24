"""Binary-vector phase memory for Ciel over the NOEMA shared surface.

The adapter stores only deterministic hypervectors plus phase/flavor signatures,
not raw conversational text. Retrieval is driven by vector similarity and local
surface phase alignment rather than arbitrary string lookup.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Mapping
import re

import numpy as np

from .noema_surface_mmap import DEFAULT_SURFACE_ROOT, N_FLAVORS, open_surface
from .imaginal_memory_guard import (
    guard_imaginal_write,
    is_canonical_imaginal_path,
    phase_memory_bytes,
)

DEFAULT_MEMORY_ROOT = Path("/dev/shm/ciel_phase_memory")
DEFAULT_VECTOR_BITS = 256
DEFAULT_SLOTS = 512


@dataclass(frozen=True)
class PhaseMemoryRecord:
    slot: int
    score: float
    vector_similarity: float
    phase_similarity: float
    flavor_similarity: float
    coherence: float
    tick: int
    event_hash_hex: str
    # Deterministic per-slot binary hypervector (256 bits) already computed
    # for vector_similarity above, but previously dropped before reaching
    # callers — PhaseNav graphics fell back to np.roll(phi, slot % 36) for
    # node placement, which collapses every slot to nearly the same point
    # whenever the Kuramoto surface is synchronized (phi close to uniform).
    vector: np.ndarray


def _tokenize(text: str) -> list[str]:
    tokens = re.findall(r"\w+", text.lower(), flags=re.UNICODE)
    return tokens if tokens else [text.strip().lower() or "ciel"]


def encode_text_to_binary_vector(text: str, *, bits: int = DEFAULT_VECTOR_BITS) -> np.ndarray:
    if bits % 256 != 0:
        raise ValueError("bits must be a multiple of 256")
    acc = np.zeros(bits, dtype=np.int32)
    repeats = bits // 256
    for token in _tokenize(text):
        digest_bits = np.unpackbits(np.frombuffer(sha256(token.encode("utf-8")).digest(), dtype=np.uint8))
        tiled = np.tile(digest_bits, repeats)
        acc += np.where(tiled > 0, 1, -1)
    return (acc >= 0).astype(np.uint8)


def event_hash(text: str) -> np.ndarray:
    return np.frombuffer(sha256(text.encode("utf-8")).digest(), dtype=np.uint8).copy()


def _capture_surface_signature(surface: Mapping[str, np.ndarray]) -> tuple[float, float, np.ndarray, int]:
    phi = np.asarray(surface["phi"], dtype=np.float64)
    flavor = np.asarray(surface["flavor"], dtype=np.float64)
    z = np.exp(1j * phi).mean()
    phase = float(np.angle(z))
    coherence_raw = np.asarray(surface["R_geom"], dtype=np.float64)
    coherence = float(np.mean(np.abs(coherence_raw))) if np.any(coherence_raw) else float(np.abs(z))
    tick = int(np.asarray(surface["tick"], dtype=np.uint64)[0])
    return phase, coherence, flavor.copy(), tick


def _memory_paths(root: Path) -> dict[str, Path]:
    return {
        "vectors": root / "vectors",
        "occupied": root / "occupied",
        "phase": root / "phase",
        "coherence": root / "coherence",
        "tick": root / "tick",
        "flavor": root / "flavor",
        "event_hash": root / "event_hash",
        "write_head": root / "write_head",
    }


def _ensure_file(path: Path, nbytes: int) -> None:
    if not path.exists() or path.stat().st_size != nbytes:
        with path.open("wb") as handle:
            handle.truncate(nbytes)


def ensure_phase_memory(
    root: Path = DEFAULT_MEMORY_ROOT,
    *,
    slots: int = DEFAULT_SLOTS,
    bits: int = DEFAULT_VECTOR_BITS,
    zero_fill: bool = False,
) -> dict[str, np.memmap]:
    if is_canonical_imaginal_path(root):
        guard_imaginal_write(
            root,
            additional_bytes=phase_memory_bytes(
                slots=slots, bits=bits, n_flavors=N_FLAVORS
            ),
            slots=slots,
            bits=bits,
        )
    root.mkdir(parents=True, exist_ok=True)
    if bits % 256 != 0:
        raise ValueError("bits must be a multiple of 256")
    paths = _memory_paths(root)
    specs = {
        "vectors": (np.uint8, (slots, bits)),
        "occupied": (np.uint8, (slots,)),
        "phase": (np.float64, (slots,)),
        "coherence": (np.float64, (slots,)),
        "tick": (np.uint64, (slots,)),
        "flavor": (np.float64, (slots, N_FLAVORS)),
        "event_hash": (np.uint8, (slots, 32)),
        "write_head": (np.uint64, (1,)),
    }
    out: dict[str, np.memmap] = {}
    for name, (dtype, shape) in specs.items():
        dtype = np.dtype(dtype)
        nbytes = int(np.prod(shape, dtype=np.int64)) * dtype.itemsize
        _ensure_file(paths[name], nbytes)
        mem = np.memmap(paths[name], dtype=dtype, mode="r+", shape=shape)
        if zero_fill:
            mem[...] = 0
            mem.flush()
        out[name] = mem
    return out


def bind_phase_memory(
    text: str,
    *,
    surface_root: Path = DEFAULT_SURFACE_ROOT,
    memory_root: Path = DEFAULT_MEMORY_ROOT,
    bits: int = DEFAULT_VECTOR_BITS,
    slots: int = DEFAULT_SLOTS,
) -> int:
    surface = open_surface(surface_root)
    memory = ensure_phase_memory(memory_root, slots=slots, bits=bits)
    vector = encode_text_to_binary_vector(text, bits=bits)
    phase, coherence, flavor, tick = _capture_surface_signature(surface)
    digest = event_hash(text)

    write_head = int(memory["write_head"][0])
    slot = write_head % slots
    memory["vectors"][slot] = vector
    memory["occupied"][slot] = 1
    memory["phase"][slot] = phase
    memory["coherence"][slot] = coherence
    memory["tick"][slot] = tick
    memory["flavor"][slot] = flavor
    memory["event_hash"][slot] = digest
    memory["write_head"][0] = write_head + 1
    for mem in memory.values():
        mem.flush()
    return slot


def _cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    denom = float(np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0.0:
        return 0.5
    return float((np.dot(a, b) / denom + 1.0) / 2.0)


def query_phase_memory(
    text: str,
    *,
    top_k: int = 5,
    surface_root: Path = DEFAULT_SURFACE_ROOT,
    memory_root: Path = DEFAULT_MEMORY_ROOT,
    bits: int = DEFAULT_VECTOR_BITS,
    slots: int = DEFAULT_SLOTS,
) -> list[PhaseMemoryRecord]:
    surface = open_surface(surface_root)
    memory = ensure_phase_memory(memory_root, slots=slots, bits=bits)
    occupied = np.asarray(memory["occupied"], dtype=np.uint8) > 0
    if not np.any(occupied):
        return []

    query_vector = encode_text_to_binary_vector(text, bits=bits)
    phase, _, flavor, _ = _capture_surface_signature(surface)

    vectors = np.asarray(memory["vectors"][occupied], dtype=np.uint8)
    stored_phase = np.asarray(memory["phase"][occupied], dtype=np.float64)
    stored_flavor = np.asarray(memory["flavor"][occupied], dtype=np.float64)
    coherence = np.asarray(memory["coherence"][occupied], dtype=np.float64)
    tick = np.asarray(memory["tick"][occupied], dtype=np.uint64)
    hashes = np.asarray(memory["event_hash"][occupied], dtype=np.uint8)
    slots_idx = np.nonzero(occupied)[0]

    vector_similarity = 1.0 - np.mean(np.bitwise_xor(vectors, query_vector), axis=1)
    phase_similarity = (1.0 + np.cos(stored_phase - phase)) / 2.0
    # Wektorowo: flavor_similarity = (cosine_sim + 1) / 2
    flavor_norms = np.linalg.norm(stored_flavor, axis=1) * float(np.linalg.norm(flavor))
    flavor_dots = stored_flavor @ flavor
    flavor_similarity = np.where(
        flavor_norms > 1e-12,
        (flavor_dots / flavor_norms + 1.0) / 2.0,
        0.5,
    ).astype(np.float64)
    score = 0.6 * vector_similarity + 0.3 * phase_similarity + 0.1 * flavor_similarity

    order = np.argsort(score)[::-1][:top_k]
    out: list[PhaseMemoryRecord] = []
    for idx in order:
        out.append(
            PhaseMemoryRecord(
                slot=int(slots_idx[idx]),
                score=float(score[idx]),
                vector_similarity=float(vector_similarity[idx]),
                phase_similarity=float(phase_similarity[idx]),
                flavor_similarity=float(flavor_similarity[idx]),
                coherence=float(coherence[idx]),
                tick=int(tick[idx]),
                event_hash_hex=bytes(hashes[idx].tolist()).hex(),
                vector=vectors[idx].copy(),
            )
        )
    return out


if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Store or query binary-vector phase memory")
    parser.add_argument("text")
    parser.add_argument("--store", action="store_true")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--surface-root", type=Path, default=DEFAULT_SURFACE_ROOT)
    parser.add_argument("--memory-root", type=Path, default=DEFAULT_MEMORY_ROOT)
    args = parser.parse_args()

    if args.store:
        slot = bind_phase_memory(args.text, surface_root=args.surface_root, memory_root=args.memory_root)
        print(json.dumps({"stored": True, "slot": slot}, indent=2))
    else:
        rows = query_phase_memory(
            args.text,
            top_k=args.top_k,
            surface_root=args.surface_root,
            memory_root=args.memory_root,
        )
        print(json.dumps([row.__dict__ for row in rows], indent=2))
