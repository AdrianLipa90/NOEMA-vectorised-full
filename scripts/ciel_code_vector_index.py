#!/usr/bin/env python3
"""CIEL Code Vector Indexer — Source files → 36D PhaseNav embedding.

Czyta wszystkie pliki źródłowe projektu NOEMA/CIEL i konwertuje je na
36D wektory fazowe PhaseNav (12 kanałów × 3 oscylatory), kompatybilne
z istniejącym systemem embeddingów Knowledge DB.

Różnica względem ciel_noema_doc_embedder.py:
  - Źródłem są RAWNE PLIKI (nie SQLite Knowledge DB)
  - TF-IDF liczone inline z treści pliku (nie z DB)
  - Metadane pliku (ścieżka, rozmiar, rozszerzenie) → feature wektora
  - Zapis do osobnego pliku (nie nadpisuje embeddingów Knowledge DB)

Output:
  /media/adrian/New Volume/CIEL_memories/state/noema_code_embeddings.npy   — (N, 36)
  /media/adrian/New Volume/CIEL_memories/state/noema_code_embeddings.json  — index

Usage:
  python3 scripts/ciel_code_vector_index.py [--rebuild] [--stats] [--query "..."]
"""
from __future__ import annotations

import argparse
import json
import logging
import math
import os
import re
import sys
import time
from collections import Counter
from pathlib import Path

import numpy as np

logging.basicConfig(
    level=logging.INFO,
    format="[codevec] %(asctime)s %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

N_CHANNELS = 12
OSC_PER_CHANNEL = 3
N_OSCILLATORS = N_CHANNELS * OSC_PER_CHANNEL  # 36

PROJECT_ROOT = Path(__file__).resolve().parents[1]

OUTPUT_NPY = PROJECT_ROOT / "state" / "noema_code_embeddings.npy"
OUTPUT_JSON = PROJECT_ROOT / "state" / "noema_code_embeddings.json"

# Te same kanały co w ciel_noema_doc_embedder.py
CHANNEL_KEYWORDS: dict[str, list[str]] = {
    "M0_Perceptual": ["percept", "sensor", "obserw", "widz", "postrzeg", "zmysł", "światło", "dźwięk", "obraz",
                      "perception", "sense", "light", "sound", "image", "pattern", "shape", "color",
                      "display", "render", "visual", "gui", "view", "log", "monitor", "listen"],
    "M1_Working": ["operator", "logik", "składnia", "struktur", "funkcj", "proces", "algorithm", "compute",
                   "syntax", "grammar", "logic", "function", "process", "operation",
                   "compute", "calculate", "transform", "map", "filter", "reduce", "loop", "iterate"],
    "M2_Episodic": ["kontekst", "epizod", "zdarzen", "scen", "sytuacj", "pamięć", "wspomnien", "doświadczen",
                    "context", "episode", "event", "scene", "memory", "experience", "place", "time",
                    "session", "history", "log", "story", "narrative", "trace"],
    "M3_Semantic": ["znaczen", "semantyk", "definicj", "pojęci", "rozumien", "wiedza", "koncept", "meaning",
                    "semantic", "concept", "knowledge", "understanding", "define", "term",
                    "schema", "type", "class", "interface", "model", "ontology", "vocab"],
    "M4_Procedural": ["procedur", "działan", "umiejętnoś", "metoda", "technik", "krok", "instrukcj", "skill",
                      "procedure", "action", "method", "technique", "step", "practice",
                      "function", "method", "handler", "middleware", "plugin", "hook", "pipeline"],
    "M5_Affective": ["emocj", "uczuci", "nastrój", "afekt", "wartoś", "etyk", "moral", "uczuci",
                     "emotion", "feeling", "mood", "affect", "value", "ethical", "moral", "love", "fear",
                     "trust", "care", "safety", "consent", "boundary", "respect"],
    "M6_Identity": ["tożsamoś", "osoba", "podmiot", "autor", "ja", "self", "identity", "soul", "ego",
                    "identity", "self", "author", "subject", "person", "character",
                    "agent", "persona", "name", "signature", "key", "cert"],
    "M7_Braid": ["relacj", "powiązan", "sieć", "graf", "łącz", "korelacj", "affinity", "relation",
                 "relation", "connection", "network", "graph", "link", "braid", "weave",
                 "bridge", "edge", "vertex", "topology", "mesh", "chain", "dependency"],
    "M8_Meta": ["meta", "refleksj", "abstrakcj", "model", "teori", "paradygmat", "metacognition",
                "meta", "reflection", "abstract", "model", "theory", "paradigm", "cognition",
                "config", "schema", "template", "pattern", "architecture", "framework"],
    "M9_Temporal": ["czas", "przeszłoś", "przyszłoś", "teraz", "chwil", "moment", "tempus",
                    "time", "past", "future", "present", "moment", "temporal", "duration",
                    "delay", "timeout", "schedule", "cron", "timer", "clock", "age"],
    "M10_Imaginal": ["wyobraźn", "kreatywnoś", "imaginacj", "symbol", "metafor", "wizj", "fantazj",
                     "imagination", "creative", "vision", "symbol", "metaphor", "dream", "myth",
                     "design", "idea", "concept", "novel", "generative", "dream", "fiction"],
    "M11_Quantum": ["kwant", "niepewnoś", "potencjał", "superpozycj", "splątan", "probabilist",
                    "quantum", "uncertain", "potential", "superposition", "entangle", "probability",
                    "random", "entropy", "chaos", "noise", "probabilistic", "stochastic"],
}

EXT_WEIGHTS: dict[str, float] = {
    ".py": 1.0, ".ts": 1.0, ".js": 1.0, ".tsx": 1.0, ".jsx": 1.0,
    ".go": 0.9, ".rs": 0.9, ".c": 0.8, ".cpp": 0.8, ".h": 0.7,
    ".toml": 0.6, ".json": 0.6, ".yaml": 0.6, ".yml": 0.6,
    ".sh": 0.5, ".bash": 0.5, ".service": 0.4, ".md": 0.7,
    ".html": 0.5, ".css": 0.4, ".sql": 0.6,
}

def _tokenize(text: str) -> Counter:
    clean = text.lower()

    # line comments — use MULTILINE but NOT DOTALL
    clean = re.sub(r"#.*$", "", clean, flags=re.MULTILINE)
    clean = re.sub(r"//.*$", "", clean, flags=re.MULTILINE)

    # block comments — use DOTALL to match across lines
    clean = re.sub(r"/\*.*?\*/", "", clean, flags=re.DOTALL)
    clean = re.sub(r"'''[^']*'''", "", clean, flags=re.DOTALL)
    clean = re.sub(r'"""[^"]*"""', "", clean, flags=re.DOTALL)
    clean = re.sub(r"<!--.*?-->", "", clean, flags=re.DOTALL)
    tokens = re.findall(r"[a-ząćęłńóśźż_][a-ząćęłńóśźż0-9_]{1,}", clean)
    return Counter(tokens)


def _compute_channel_weights(tokens: Counter) -> np.ndarray:
    weights = np.zeros(N_CHANNELS, dtype=np.float64)
    total = max(sum(tokens.values()), 1)
    for term, count in tokens.items():
        tf = count / total
        term_lower = term.lower()
        for ch_idx, (_ch_name, keywords) in enumerate(CHANNEL_KEYWORDS.items()):
            for kw in keywords:
                if kw in term_lower or term_lower in kw:
                    weights[ch_idx] += tf
                    break
    max_w = max(float(np.max(weights)), 1e-12)
    weights = weights / max_w
    return weights


def _ext_to_channel_bias(ext: str) -> np.ndarray:
    bias = np.zeros(N_CHANNELS, dtype=np.float64)
    ext_w = EXT_WEIGHTS.get(ext.lower(), 0.5)
    bias[1] += ext_w * 0.3   # M1_Working — kod
    bias[3] += ext_w * 0.2   # M3_Semantic — definicje
    bias[4] += ext_w * 0.3   # M4_Procedural — implementacje
    bias[7] += ext_w * 0.1   # M7_Braid — zależności
    if ext in (".md", ".rst", ".txt"):
        bias[0] += 0.2       # M0_Perceptual — dokumentacja
        bias[2] += 0.2       # M2_Episodic — opowieść
        bias[5] += 0.1       # M5_Affective — wartości
        bias[9] += 0.1       # M9_Temporal — historia
    if ext in (".toml", ".json", ".yaml", ".yml"):
        bias[8] += 0.3       # M8_Meta — konfiguracja
    return bias


def _file_to_phi(path: Path, rel_path: str, idx: int) -> np.ndarray | None:
    try:
        text = path.read_text("utf-8", errors="replace")
    except Exception:
        return None
    if not text.strip():
        return None

    ext = path.suffix.lower()
    size = len(text)
    n_lines = text.count("\n") + 1

    tokens = _tokenize(text)
    if not tokens:
        return None

    channel_w = _compute_channel_weights(tokens)
    ext_bias = _ext_to_channel_bias(ext)

    # Syntetyczne feature z metadanych pliku
    size_norm = min(size / 50000.0, 1.0)
    line_norm = min(n_lines / 2000.0, 1.0)
    path_depth = len(rel_path.split(os.sep))
    depth_norm = min(path_depth / 8.0, 1.0)
    entropy = math.log(max(len(tokens), 2))

    # Buduj (12, 3) — 3 oscylatory na kanał
    np.random.seed(idx)
    phi_2d = np.zeros((N_CHANNELS, OSC_PER_CHANNEL), dtype=np.float64)

    for ch in range(N_CHANNELS):
        base_w = float(channel_w[ch]) + float(ext_bias[ch])
        for osc in range(OSC_PER_CHANNEL):
            phase_shift = osc * (2.0 * math.pi / 3.0)
            per_osc = base_w * 1.5 * osc / (OSC_PER_CHANNEL - 1)  # break 120° symmetry
            omega = 0.5 + base_w * 2.0 + entropy * 0.05
            phi = (omega * idx * 0.01 + phase_shift + base_w * math.pi + per_osc) % (2.0 * math.pi)
            phi_2d[ch, osc] = phi

    # Specyficzne modulacje per-oscillator (nie per-channel)
    phi_2d[1, 2] = (phi_2d[1, 2] + line_norm * 0.3) % (2.0 * math.pi)
    phi_2d[4, 2] = (phi_2d[4, 2] + size_norm * 0.2) % (2.0 * math.pi)
    phi_2d[7, 2] = (phi_2d[7, 2] + depth_norm * 0.3) % (2.0 * math.pi)
    phi_2d[9, 2] = (phi_2d[9, 2] + size_norm * 0.2) % (2.0 * math.pi)

    return phi_2d.ravel()


def _collect_source_files() -> list[dict]:
    files: list[dict] = []
    root = PROJECT_ROOT

    include_dirs = [
        "scripts",
        "src",
        "opencode-plugin",
        ".claude",
        ".config",
    ]

    # Dodaj też opencode packages jeśli istnieją
    packages_dir = root / "packages"
    if packages_dir.exists():
        for sub in packages_dir.iterdir():
            if sub.is_dir() and not sub.name.startswith("."):
                for pkg_sub in ["src", "tool"]:
                    p = sub / pkg_sub
                    if p.exists():
                        include_dirs.append(str(p.relative_to(root)))

    exclude_patterns = [
        "__pycache__",
        "node_modules",
        ".git",
        ".venv",
        "venv",
        "__init__",
        ".bak",
        ".pyc",
    ]

    done: set[Path] = set()
    for rel_dir in include_dirs:
        target = root / rel_dir
        if not target.exists():
            continue
        for fpath in target.rglob("*"):
            if not fpath.is_file():
                continue
            if any(p in str(fpath) for p in exclude_patterns):
                continue
            if fpath in done:
                continue
            ext = fpath.suffix.lower()
            if ext not in EXT_WEIGHTS and ext not in (".py", ".ts", ".js"):
                continue
            done.add(fpath)
            try:
                stat = fpath.stat()
            except OSError:
                continue
            rel = str(fpath.relative_to(root))
            files.append({
                "path": str(fpath),
                "rel": rel,
                "ext": ext,
                "size": stat.st_size,
                "mtime": stat.st_mtime,
            })

    # Sort dla determinizmu
    files.sort(key=lambda f: f["rel"])
    return files


def _index_files(files: list[dict]) -> tuple[np.ndarray, dict]:
    n = len(files)
    embeddings = np.zeros((n, N_OSCILLATORS), dtype=np.float64)
    entries: list[dict] = []

    log.info("Indexing %d source files...", n)
    t0 = time.time()
    skipped = 0

    for i, f in enumerate(files):
        phi = _file_to_phi(Path(f["path"]), f["rel"], i)
        if phi is None:
            skipped += 1
            continue
        embeddings[i] = phi

        R_ch = []
        for ch in range(N_CHANNELS):
            s = ch * OSC_PER_CHANNEL
            e = s + OSC_PER_CHANNEL
            ch_phi = phi[s:e]
            ch_R = abs(sum(math.e ** (1j * p) for p in ch_phi)) / OSC_PER_CHANNEL
            R_ch.append(round(ch_R, 4))

        entries.append({
            "idx": i,
            "filename": f["rel"],
            "ext": f["ext"],
            "size": f["size"],
            "phi": [round(p, 6) for p in phi],
            "R_channels": R_ch,
            "R_global": round(abs(sum(math.e ** (1j * p) for p in phi)) / N_OSCILLATORS, 4),
        })

        if (i + 1) % 50 == 0:
            elapsed = time.time() - t0
            rate = (i + 1) / elapsed if elapsed > 0 else 0
            log.info("  %d/%d files (%.1f/s)", i + 1, n, rate)

    elapsed = time.time() - t0
    log.info("Indexed %d files (skipped %d) in %.1fs (%.1f/s)", len(entries), skipped, elapsed, len(entries) / elapsed if elapsed > 0 else 0)

    embeddings = embeddings[:len(entries)]
    index = {
        "n_docs": len(entries),
        "n_dimensions": N_OSCILLATORS,
        "channels": list(CHANNEL_KEYWORDS.keys()),
        "schema": "noema/code/embedding/v0.1",
        "entries": entries,
    }
    return embeddings, index


def _query(query_text: str, embeddings: np.ndarray, index: dict, top_k: int = 10) -> list[dict]:
    query_terms = query_text.lower().split()
    tokens = Counter(query_terms)

    q_w = _compute_channel_weights(tokens)
    q_phi = np.zeros(N_OSCILLATORS, dtype=np.float64)
    for ch in range(N_CHANNELS):
        for osc in range(OSC_PER_CHANNEL):
            phase_shift = osc * (2.0 * math.pi / 3.0)
            q_phi[ch * OSC_PER_CHANNEL + osc] = (q_w[ch] * math.pi + phase_shift) % (2.0 * math.pi)

    n = len(index["entries"])
    if n == 0:
        return []

    scores = np.zeros(n, dtype=np.float64)
    for i in range(n):
        diff = np.angle(np.exp(1j * (embeddings[i] - q_phi)))
        scores[i] = float(np.mean(np.cos(diff)))

    top_idx = np.argsort(scores)[::-1][:top_k]
    results = []
    for i in top_idx:
        entry = index["entries"][i]
        results.append({
            "rank": len(results) + 1,
            "filename": entry["filename"],
            "ext": entry.get("ext", ""),
            "size": entry.get("size", 0),
            "similarity": round(float(scores[i]), 4),
            "R_global": entry.get("R_global", 0),
        })
    return results


def main() -> int:
    ap = argparse.ArgumentParser(description="CIEL Code Vector Indexer — 36D PhaseNav embeddings")
    ap.add_argument("--rebuild", action="store_true", help="Force rebuild from source files")
    ap.add_argument("--query", type=str, default=None, help="Query text for similarity search")
    ap.add_argument("--top-k", type=int, default=10, help="Number of results (default: 10)")
    ap.add_argument("--stats", action="store_true", help="Show embedding statistics")
    ap.add_argument("--json", action="store_true", help="Output as JSON (for machine consumption)")
    ap.add_argument("--output-npy", type=str, default=None, help=f"Output .npy path (default: {OUTPUT_NPY})")
    ap.add_argument("--output-json", type=str, default=None, help=f"Output .json path (default: {OUTPUT_JSON})")
    args = ap.parse_args()

    npy_path = Path(args.output_npy) if args.output_npy else OUTPUT_NPY
    json_path = Path(args.output_json) if args.output_json else OUTPUT_JSON

    need_rebuild = args.rebuild
    if need_rebuild or not npy_path.exists():
        files = _collect_source_files()
        if not files:
            log.error("No source files found")
            return 1
        embeddings, index = _index_files(files)
        npy_path.parent.mkdir(parents=True, exist_ok=True)
        np.save(str(npy_path), embeddings)
        log.info("Saved embeddings: %s (%s)", npy_path, embeddings.shape)
        with open(json_path, "w") as f:
            json.dump(index, f, indent=1)
        log.info("Saved index: %s (%d entries)", json_path, len(index["entries"]))
    else:
        embeddings = np.load(str(npy_path))
        with open(json_path) as f:
            index = json.load(f)
        log.info("Loaded %d existing code embeddings", len(index.get("entries", [])))

    if args.stats:
        R_globals = [e.get("R_global", 0) for e in index["entries"]]
        channels = index.get("channels", [])
        ch_stats = {}
        for ch_idx, ch_name in enumerate(channels):
            ch_Rs = [e["R_channels"][ch_idx] for e in index["entries"]]
            ch_stats[ch_name] = {"mean_R": round(float(np.mean(ch_Rs)), 4)}
        ext_counts: Counter = Counter()
        for e in index["entries"]:
            ext_counts[e.get("ext", "?")] += 1
        ext_list = [{"ext": k, "count": v} for k, v in ext_counts.most_common(10)]
        if args.json:
            print(json.dumps({
                "status": "ok",
                "n_files": len(index["entries"]),
                "n_dimensions": index["n_dimensions"],
                "schema": index["schema"],
                "mean_R": round(float(np.mean(R_globals)), 4),
                "min_R": round(float(np.min(R_globals)), 4),
                "max_R": round(float(np.max(R_globals)), 4),
                "channels": ch_stats,
                "extensions": ext_list,
            }, indent=1))
        else:
            print(f"\n=== Code Embedding stats ===")
            print(f"  Files: {len(index['entries'])}")
            print(f"  Dimensions: {index['n_dimensions']} (12 ch × 3 osc)")
            print(f"  Schema: {index['schema']}")
            print(f"  Mean R: {np.mean(R_globals):.4f}")
            print(f"  Min R: {np.min(R_globals):.4f}")
            print(f"  Max R: {np.max(R_globals):.4f}")
            for ch_idx, ch_name in enumerate(channels):
                ch_Rs = [e["R_channels"][ch_idx] for e in index["entries"]]
                print(f"    {ch_name:20s} mean_R={np.mean(ch_Rs):.4f}")
            print(f"\n  Extensions:")
            for ext, count in ext_counts.most_common(10):
                print(f"    {ext:8s}  {count:4d} files")

    if args.query:
        results = _query(args.query, embeddings, index, top_k=args.top_k)
        if args.json:
            print(json.dumps({"status": "ok", "query": args.query, "results": results}, indent=1))
        else:
            print(f"\n=== Query: '{args.query}' ===")
            for r in results:
                print(f"  #{r['rank']:2d} sim={r['similarity']:.4f} R={r['R_global']:.4f}  [{r['ext']:6s}] {r['filename'][:80]}")

    if args.json and not args.query and not args.stats:
        print(json.dumps({
            "status": "ok",
            "action": "rebuild" if need_rebuild else "load",
            "n_files": len(index["entries"]),
            "n_dimensions": index["n_dimensions"],
        }))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
