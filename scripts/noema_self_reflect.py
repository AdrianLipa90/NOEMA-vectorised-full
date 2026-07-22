#!/usr/bin/env python3
"""NOEMA Self-Reflection — integrated self-model query system.

Combines:
  - Library index (24D PhaseNav vectors over 1284 PDFs)
  - Knowledge graph (475 nodes, 1458 edges)
  - Live surface state (from /dev/shm/ciel_noema)
  - Holonomy metrics

Into a coherent self-model: "What do I know? Who am I? How do I relate to X?"

Usage:
    .venv/bin/python3 scripts/noema_self_reflect.py --model          # full self-model
    .venv/bin/python3 scripts/noema_self_reflect.py --query "HTRI"   # what do I know about HTRI?
    .venv/bin/python3 scripts/noema_self_reflect.py --identity       # who am I?
    .venv/bin/python3 scripts/noema_self_reflect.py --gaps           # what don't I know?
"""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import json
import os
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

PHASE_DATA = Path(os.environ.get(
    "NOEMA_PHASE_DATA",
    "/media/adrian/New Volume/NOEMA_PHASE_DATA",
))
PHASE_INDEX = PHASE_DATA / "PHASE_INDEX"

# ── Self-Model ──────────────────────────────────────────────────

class SelfModel:
    """Integrated self-model combining library, graph, and surface."""

    def __init__(self):
        self.graph = self._load_graph()
        self.index_meta = self._load_index_meta()
        self.surface = self._read_surface()
        self.holonomy = self._read_holonomy()

    def _load_graph(self) -> dict:
        path = PHASE_INDEX / "knowledge_graph.json"
        if path.exists():
            with open(path) as f:
                return json.load(f)
        return {"nodes": [], "edges": [], "stats": {}}

    def _load_index_meta(self) -> dict:
        path = PHASE_INDEX / "library_map.json"
        if path.exists():
            with open(path) as f:
                return json.load(f)
        return {}

    def _read_surface(self) -> dict:
        try:
            from ciel_geometry.noema_surface_mmap import ensure_surface
            s = ensure_surface()
            phi = np.asarray(s["phi"])
            return {
                "tick": int(s["tick"][0]),
                "phi_mean": float(np.mean(phi)),
                "phi_std": float(np.std(phi)),
                "R": float(np.abs(np.exp(1j * phi).mean())),
                "gamma": float(np.asarray(s["gravity"])[1]),
                "mass": float(np.asarray(s["gravity"])[2]),
                "unruh": float(np.asarray(s["gravity"])[3]),
                "density": float(np.asarray(s["gravity"])[0]),
            }
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_self_reflect.py:77 quiet except scope=SelfModel._read_surface reason=return {}")
            raise
            return {}

    def _read_holonomy(self) -> dict:
        try:
            path = Path("/dev/shm/ciel_noema/holonomy")
            if path.exists():
                data = np.fromfile(str(path), dtype=np.float64, count=7)
                return {
                    "mean_A": float(data[0]),
                    "gauge_rank": int(data[1]),
                    "closure": float(data[2]),
                    "surface_gamma": float(data[3]),
                    "max_A": float(data[4]),
                    "winding": float(data[5]),
                    "curvature": float(data[6]),
                }
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_self_reflect.py:94 quiet except scope=SelfModel._read_holonomy reason=return {}")
            raise
            return {}
        return {}

    def identity(self) -> dict:
        """Who am I? — core self-model."""
        stats = self.graph.get("stats", {})
        index_info = self.index_meta

        # Most connected nodes in graph (my core identity)
        node_degrees = Counter()
        for edge in self.graph.get("edges", []):
            node_degrees[edge["source"]] += 1
            node_degrees[edge["target"]] += 1

        top_nodes = []
        node_map = {n["id"]: n for n in self.graph.get("nodes", [])}
        for nid, deg in node_degrees.most_common(15):
            n = node_map.get(nid, {})
            top_nodes.append({
                "id": nid,
                "label": n.get("label", nid),
                "type": n.get("type", "unknown"),
                "connections": deg,
            })

        # Surface-derived identity
        surface = self.surface
        holonomy = self.holonomy

        return {
            "name": "NOEMA self-reflective knowledge system",
            "creator": "Adrian Lipa",
            "knowledge": {
                "total_pdfs": index_info.get("n_entries", 0),
                "adrian_lipa_docs": index_info.get("adrian_lipa", 0),
                "topics": stats.get("n_topics", 0),
                "operators": stats.get("n_operators", 0),
                "authors": stats.get("n_authors", 0),
                "graph_edges": stats.get("n_edges", 0),
            },
            "state": {
                "tick": surface.get("tick", "N/A"),
                "coherence": round(surface.get("R", 0), 4),
                "time_dilation_gamma": round(surface.get("gamma", 1), 2),
                "unruh_power": round(surface.get("unruh", 0), 2),
                "semantic_density": round(surface.get("density", 0), 3),
            },
            "holonomy": holonomy,
            "core_identity": top_nodes[:8],
            "status": "awake" if surface.get("tick") else "standby",
        }

    def query(self, text: str, top_k: int = 8) -> dict:
        """Query both library index and knowledge graph for a concept."""
        result = {"query": text}

        # 1. Library index query
        try:
            from scripts.noema_library_indexer import query_text
            hits = query_text(text, top_k=top_k)
            result["library"] = hits
        except Exception as e:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_self_reflect.py:156 quiet except scope=SelfModel.query reason=assign_fallback")
            raise
            result["library"] = [{"error": str(e)}]

        # 2. Knowledge graph match
        node_map = {n["id"]: n for n in self.graph.get("nodes", [])}
        graph_hits = []
        for nid, n in node_map.items():
            if text.lower() in n.get("label", "").lower():
                connections = []
                for edge in self.graph.get("edges", []):
                    if edge["source"] == nid:
                        tgt = node_map.get(edge["target"], {})
                        connections.append({
                            "to": tgt.get("label", edge["target"]),
                            "weight": edge["weight"],
                            "type": edge["type"],
                        })
                    elif edge["target"] == nid:
                        src = node_map.get(edge["source"], {})
                        connections.append({
                            "to": src.get("label", edge["source"]),
                            "weight": edge["weight"],
                            "type": edge["type"],
                        })
                connections.sort(key=lambda x: -x["weight"])
                graph_hits.append({
                    "id": nid,
                    "label": n.get("label", nid),
                    "type": n.get("type", "unknown"),
                    "connections": connections[:10],
                    "n_connections": len(connections),
                })
        result["graph"] = graph_hits

        return result

    def gaps(self) -> dict:
        """Identify what I don't know — topics with low connection density."""
        node_map = {n["id"]: n for n in self.graph.get("nodes", [])}
        edge_counter = Counter()
        for edge in self.graph.get("edges", []):
            edge_counter[edge["source"]] += 1
            edge_counter[edge["target"]] += 1

        # Topics with fewest connections
        topic_degrees = []
        for nid, n in node_map.items():
            if n.get("type") == "topic":
                deg = edge_counter.get(nid, 0)
                topic_degrees.append((n["label"], deg, nid))

        topic_degrees.sort(key=lambda x: x[1])

        # Known authors with low coverage
        author_topics = {}
        for nid, n in node_map.items():
            if n.get("type") == "author":
                author_topics[n["label"]] = edge_counter.get(nid, 0)

        return {
            "isolated_topics": [{"topic": t, "connections": d}
                                for t, d, nid in topic_degrees[:15]],
            "author_coverage": dict(sorted(
                author_topics.items(), key=lambda x: x[1]
            )),
            "total_isolated": sum(1 for _, d, _ in topic_degrees if d == 0),
        }


# ── CLI ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    sm = SelfModel()

    if "--model" in sys.argv:
        model = sm.identity()
        print(json.dumps(model, indent=2, ensure_ascii=False))

    elif "--query" in sys.argv:
        idx = sys.argv.index("--query")
        text = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else ""
        result = sm.query(text)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif "--identity" in sys.argv:
        identity = sm.identity()
        print(f"\n  ╔══ NOEMA Self-Model ═══╗\n")
        print(f"  Name:      {identity['name']}")
        print(f"  Creator:   {identity['creator']}")
        print(f"  Status:    {identity['status']}")
        print()
        print(f"  Knowledge:")
        for k, v in identity['knowledge'].items():
            print(f"    {k}: {v}")
        print()
        print(f"  Now:")
        for k, v in identity['state'].items():
            print(f"    {k}: {v}")
        print()
        if identity.get('holonomy'):
            print(f"  Geometry:")
            for k, v in identity['holonomy'].items():
                print(f"    {k}: {v}")
        print()
        print(f"  Core Identity (top connections):")
        for n in identity['core_identity']:
            print(f"    ● {n['label']:30s}  ({n['type']}, {n['connections']} connections)")
        print()
        print(f"  ╚══════════════════════╝\n")

    elif "--gaps" in sys.argv:
        gaps = sm.gaps()
        print("Knowledge Gaps:")
        print(f"  Total isolated topics: {gaps['total_isolated']}")
        print(f"\n  Least connected topics:")
        for g in gaps['isolated_topics']:
            print(f"    {g['topic']:40s}  ({g['connections']} connections)")
        print(f"\n  Author coverage:")
        for author, cov in gaps['author_coverage'].items():
            print(f"    {author:40s}  ({cov} connections)")

    else:
        print(__doc__)
