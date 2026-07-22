#!/usr/bin/env python3
"""NOEMA Knowledge Graph — maps PhaseNav operators ↔ PDF topics ↔ relational ontology.

Builds a directed graph from:
  - PhaseNav operators (35 total)
  - Library topics (432 from catalog)
  - Author entities
  - Relational edges (influence, describes, defines, references, implements)

Output: PHASE_INDEX/knowledge_graph.json (nodes + edges + adjacency)

Usage:
    .venv/bin/python3 scripts/noema_knowledge_graph.py --build
    .venv/bin/python3 scripts/noema_knowledge_graph.py --query "operator MEMORY"
    .venv/bin/python3 scripts/noema_knowledge_graph.py --operators   # list all PhaseNav operators
    .venv/bin/python3 scripts/noema_knowledge_graph.py --paths MEMORY CONDITION  # find connection path
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from collections import defaultdict, deque
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

PHASE_DATA = Path(os.environ.get(
    "NOEMA_PHASE_DATA",
    "/media/adrian/New Volume/NOEMA_PHASE_DATA",
))
PHASE_INDEX = PHASE_DATA / "PHASE_INDEX"

# ── PhaseNav operators — LEGACY/DIVERGENT catalog, NOT the canonical one ──
# CANONICAL SOURCE OF TRUTH: src/ciel_geometry/phasenav/operator_algebra.py
# ::ALL_OPERATOR_IDS (36 operators, asserted length, matches live runtime
# output). This dict below was developed independently for the knowledge
# graph builder and only overlaps 13/36 names with the canonical catalog
# (AFFECT, MEMORY, CONDITION, SCOPE, MODAL_PERMISSION, NEGATION, TRANSFORM,
# CAUSE, IDENTITY, DIFFERENCE, ADDITION, UNRUH_DRIVE, WARP_DRIFT) — the
# other 23 entries here (INTENTION, MULTIPLICATION, TEMPORAL_*, SPATIAL_*,
# CAUSAL_*, AGENT, PATIENT, BELIEF, etc.) do not exist in the canonical
# catalog, and 23 canonical operators (ORDER, COMPOSITION, FORCE, QUESTION,
# RETURN, FOLD, BOUNDARY, CONSENT, SOURCE, RISK, ASSERTION, MODAL_*,
# UNCERTAINTY, SOURCE_REQUIRED, CANON_BLOCK, CONSENT_REQUIRED,
# ACTION_REQUEST, REFUSAL, PAUSE, SIMULATION_BOUNDARY, ATTRACTOR) are
# missing here. Flagged 2026-07-08 — do not build new concept-tagging
# logic on this dict; use operator_algebra.ALL_OPERATOR_IDS instead. This
# knowledge-graph builder is left as-is (working script, own node labels)
# pending a decision on whether to reconcile or retire it.

PHASENAV_OPERATORS = {
    # Core (0-23)
    "AFFECT": "emotional valence — sadness/happiness/love/fear/anger/surprise",
    "MEMORY": "episodic recall — past surface states",
    "CONDITION": "if-then logic gates over phase",
    "SCOPE": "existential/universal quantifier",
    "MODAL_PERMISSION": "may, can, allowed — possibility operator",
    "NEGATION": "logical not — phase inversion",
    "TRANSFORM": "morphism — maps one phase pattern to another",
    "CAUSE": "causal implication — φ₁ → φ₂",
    "INTENTION": "future-directed phase gradient",
    "IDENTITY": "self-sameness over time",
    "DIFFERENCE": "phase distance — dissimilarity measure",
    "ADDITION": "phase superposition — sum of vectors",
    "MULTIPLICATION": "phase convolution — product of vectors",
    "COMPARISON": "relational operator — greater/less/equal",
    "EVALUATION": "value judgement on phase state",
    "TEMPORAL_BEFORE": "temporal precedence",
    "TEMPORAL_AFTER": "temporal succession",
    "TEMPORAL_DURING": "temporal overlap",
    "SPATIAL_IN": "containment relation",
    "SPATIAL_ON": "surface contact relation",
    "SPATIAL_UNDER": "subordination relation",
    "CAUSAL_ENABLE": "enabling condition",
    "CAUSAL_PREVENT": "preventing condition",
    "CAUSAL_CONTRIBUTE": "partial causal influence",
    # Extended (24-33)
    "POSSESSION": "belonging — X has Y",
    "EXPERIENCER": "phenomenal subject — X feels Y",
    "AGENT": "volitional actor — X does Y",
    "PATIENT": "undergoer — Y is done to X",
    "INSTRUMENT": "tool — X uses Y to Z",
    "BENEFICIARY": "for whom — X does Y for Z",
    "PURPOSE": "telos — X does Y in order to Z",
    "BELIEF": "epistemic attitude — X believes Y",
    "DESIRE": "wanting — X wants Y",
    "OBLIGATION": "deontic — X must Y",
    # Derived (34-35)
    "UNRUH_DRIVE": "extracts energy from temporal friction — E = mean(dω²)",
    "WARP_DRIFT": "injects travelling wave bias when unruh_power > threshold",
}

# ── Operator-to-topic affinity (hand-curated from catalog analysis) ─────

OPERATOR_TOPIC_AFFINITY = {
    "MEMORY": ["Adrian Lipa", "Nieznany_Autor", "Fractal_Field"],
    "AFFECT": ["Adrian Lipa", "Emotional", "Social Media"],
    "CONDITION": ["Logic", "Ramka Badawcza CIEL", "Mathematical Formulation"],
    "IDENTITY": ["Adrian Lipa", "UNITY Alignment Bundle", "Johnathan Surmont"],
    "INTENTION": ["Adrian Lipa", "Intention Lab", "Danail Valov"],
    "DIFFERENCE": ["Fractal Dissociative Field", "Primordial Black Hole", "Difference"],
    "TRANSFORM": ["Fractal", "Transform", "Recursive"],
    "CAUSE": ["Causal", "Physics Letters", "Loop Quantum Gravity"],
    "TEMPORAL_BEFORE": ["Metaczas", "Temporal", "History"],
    "TEMPORAL_AFTER": ["Future", "Prediction", "Simulation"],
    "BELIEF": ["Adrian Lipa", "Belief", "Philosophy"],
    "DESIRE": ["Adrian Lipa", "Intention", "Purpose"],
    "OBLIGATION": ["Adrian Lipa", "Law", "Contract", "Ethics"],
    "SCOPE": ["Universal", "Mathematical", "Quantum"],
    "NEGATION": ["Logic", "Paradox", "Negation"],
    "UNRUH_DRIVE": ["Metaczas", "Gravity", "Unruh"],
    "WARP_DRIFT": ["Metaczas", "Gravity", "Warp"],
    "AGENT": ["Adrian Lipa", "Johnathan Surmont", "Danail Valov"],
    "METATIME": ["Metatime_Formula_Ledger", "Standard Model", "Adrian Lipa"],
    "OI": ["Metatime_Formula_Ledger", "Information", "Mathematical Formulation"],
    "TRANSFORM": ["Metatime_Formula_Ledger", "Transformation", "Standard Model"],
    "PURPOSE": ["Intention Lab", "CIEL", "Sustainability"],
    "EVALUATION": ["Ethics", "Law", "Evaluation"],
}

# ── Knowledge Graph ────────────────────────────────────────────────

class KnowledgeGraph:
    """Directed weighted graph with typed edges."""

    def __init__(self):
        self.nodes: dict[str, dict] = {}  # id → {label, type, metadata}
        self.edges: list[dict] = []        # {source, target, weight, type}
        self._adj: dict[str, list[tuple[str, float, str]]] = defaultdict(list)

    def add_node(self, node_id: str, label: str, node_type: str = "concept",
                 metadata: dict | None = None) -> None:
        if node_id not in self.nodes:
            self.nodes[node_id] = {
                "id": node_id,
                "label": label,
                "type": node_type,
                "metadata": metadata or {},
            }

    def add_edge(self, source: str, target: str, weight: float = 1.0,
                 edge_type: str = "related") -> None:
        self.edges.append({
            "source": source, "target": target,
            "weight": weight, "type": edge_type,
        })
        self._adj[source].append((target, weight, edge_type))
        self._adj[target].append((source, weight, edge_type))  # undirected for paths

    def get(self, node_id: str) -> dict | None:
        return self.nodes.get(node_id)

    def neighbors(self, node_id: str) -> list[tuple[str, float, str]]:
        return self._adj.get(node_id, [])

    def find_path(self, source: str, target: str) -> list[str]:
        """BFS shortest path between two nodes."""
        if source not in self.nodes or target not in self.nodes:
            return []
        queue = deque([source])
        visited = {source: None}
        while queue:
            curr = queue.popleft()
            if curr == target:
                path = []
                while curr is not None:
                    path.append(curr)
                    curr = visited[curr]
                return list(reversed(path))
            for neighbor, _, _ in self._adj.get(curr, []):
                if neighbor not in visited:
                    visited[neighbor] = curr
                    queue.append(neighbor)
        return []

    def to_dict(self) -> dict:
        return {
            "nodes": list(self.nodes.values()),
            "edges": self.edges,
            "stats": {
                "n_nodes": len(self.nodes),
                "n_edges": len(self.edges),
                "n_operators": sum(1 for n in self.nodes.values() if n["type"] == "operator"),
                "n_topics": sum(1 for n in self.nodes.values() if n["type"] == "topic"),
                "n_authors": sum(1 for n in self.nodes.values() if n["type"] == "author"),
            },
        }

    def save(self, path: Path | str) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)


def build_graph() -> KnowledgeGraph:
    """Build the knowledge graph from catalog + operator definitions."""
    kg = KnowledgeGraph()

    # Load catalog
    catalog_path = ROOT / "NOEMA" / "pdf_catalog.noema.json"
    catalog = {}
    if catalog_path.exists():
        with open(catalog_path) as f:
            catalog = json.load(f)

    # 1. Add PhaseNav operators
    for op_name, op_desc in PHASENAV_OPERATORS.items():
        kg.add_node(
            node_id=f"operator:{op_name}",
            label=op_name,
            node_type="operator",
            metadata={"description": op_desc, "arity": 2},
        )

    # 2. Add topics from catalog
    topic_set = set()
    for f in catalog.get("files", []):
        topic = f.get("topic", "unknown")
        if topic:
            topic_set.add(topic)
    for topic in sorted(topic_set):
        kg.add_node(
            node_id=f"topic:{topic}",
            label=topic,
            node_type="topic",
            metadata={"count": sum(1 for f in catalog.get("files", []) if f.get("topic") == topic)},
        )
        # Auto-link to "AGENT" operator if contains person name indicators
        if any(indicator in topic.lower() for indicator in ["lipa", "surmont", "valov", "kamecka", "ahmad"]):
            kg.add_edge(f"operator:AGENT", f"topic:{topic}", weight=0.8, edge_type="describes")

    # 3. Add authors as entities
    for author, count in catalog.get("authors", {}).items():
        kg.add_node(
            node_id=f"author:{author}",
            label=author,
            node_type="author",
            metadata={"count": count},
        )
        # Link author to their topics
        for f in catalog.get("files", []):
            if author in f.get("author", ""):
                topic = f.get("topic", "unknown")
                kg.add_edge(
                    f"author:{author}",
                    f"topic:{topic}",
                    weight=min(1.0, count / 550.0),
                    edge_type="authored",
                )

    # 4. Apply operator–topic affinity edges
    for op_name, topics in OPERATOR_TOPIC_AFFINITY.items():
        op_id = f"operator:{op_name}"
        for topic_name in topics:
            topic_id = f"topic:{topic_name}"
            if kg.get(topic_id):
                kg.add_edge(op_id, topic_id, weight=0.85, edge_type="resonates")
            else:
                # Try partial match
                for full_topic_id in list(kg.nodes.keys()):
                    if full_topic_id.startswith("topic:") and topic_name.lower() in full_topic_id.lower():
                        kg.add_edge(op_id, full_topic_id, weight=0.75, edge_type="resonates_partial")

    # 5. Operator–operator edges (semantic proximity)
    op_names = list(PHASENAV_OPERATORS.keys())
    for i, a in enumerate(op_names):
        for b in op_names[i + 1:]:
            # Shared characters in description → edge
            desc_a = set(PHASENAV_OPERATORS[a].lower().split())
            desc_b = set(PHASENAV_OPERATORS[b].lower().split())
            shared = desc_a & desc_b
            # Shared affinity topics → edge
            aff_a = set(OPERATOR_TOPIC_AFFINITY.get(a, []))
            aff_b = set(OPERATOR_TOPIC_AFFINITY.get(b, []))
            shared_topics = aff_a & aff_b
            weight = (len(shared) * 0.05 + len(shared_topics) * 0.1)
            if weight > 0.05:
                kg.add_edge(
                    f"operator:{a}", f"operator:{b}",
                    weight=min(1.0, weight),
                    edge_type="semantic_proximity",
                )

    # 6. Add Metatime Formula Ledger as a first-class node
    kg.add_node(
        node_id="topic:Metatime_Formula_Ledger",
        label="Metatime Formula Ledger v8.2.1",
        node_type="topic",
        metadata={
            "description": "Low-parameter arithmetic-geometric ansatz for SM mass and mixing patterns",
            "constants": "κ=ln(2)/(24π), L3=7, L4=2, L5=5, quark primes",
            "claim_level": "L0-L1 (formula ledger / phenomenological fit)",
            "structural_choices": 58,
            "status": "ANSATZ_ONLY with TENSION in strong CP, gauge bosons, CKM phase",
            "package": "metatime_v8_2_1_consistency_patch.zip",
        },
    )
    # Link metatime → relevant operators beyond affinity
    for op in ["TRANSFORM", "CAUSE", "INTENTION", "IDENTITY", "DIFFERENCE", "EVALUATION"]:
        kg.add_edge(f"operator:{op}", "topic:Metatime_Formula_Ledger", weight=0.90, edge_type="describes")
    # Link metatime → Adrian Lipa
    if kg.get("author:Adrian Lipa"):
        kg.add_edge("author:Adrian Lipa", "topic:Metatime_Formula_Ledger", weight=1.0, edge_type="authored")
    # Link metatime → SM topics
    for sm_topic in ["Standard Model", "Particle Physics", "Mathematical Formulation", "Quantum"]:
        tid = f"topic:{sm_topic}"
        if kg.get(tid):
            kg.add_edge(f"topic:Metatime_Formula_Ledger", tid, weight=0.85, edge_type="references")

    # 7. Derive top-3 holonomic paths from operator algebra
    # These are the highest-curvature paths from the live surface holonomy
    high_curvature_paths = [
        ["MEMORY", "CONDITION", "AFFECT"],
        ["SCOPE", "MODAL_PERMISSION", "NEGATION"],
        ["DIFFERENCE", "TRANSFORM", "ADDITION"],
        ["NEGATION", "TRANSFORM", "DIFFERENCE"],
        ["CAUSE", "INTENTION", "IDENTITY"],
    ]
    for path in high_curvature_paths:
        for i in range(len(path) - 1):
            a, b = path[i], path[i + 1]
            kg.add_edge(
                f"operator:{a}", f"operator:{b}",
                weight=0.95, edge_type="holonomic_path",
            )

    return kg


# ── CLI ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    kg = build_graph()

    if "--build" in sys.argv:
        kg.save(PHASE_INDEX / "knowledge_graph.json")
        data = kg.to_dict()
        print(f"Knowledge Graph: {data['stats']}")
        print(f"  Saved to {PHASE_INDEX / 'knowledge_graph.json'}")

    elif "--query" in sys.argv:
        idx = sys.argv.index("--query")
        q = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else ""

        # Find matching node
        matches = [n for nid, n in kg.nodes.items() if q.lower() in n["label"].lower()]
        if not matches:
            print(f"No nodes matching '{q}'")
        else:
            for m in matches[:10]:
                print(f"● {m['id']}")
                print(f"  label: {m['label']}")
                print(f"  type: {m['type']}")
                neighbors = kg.neighbors(m["id"])
                if neighbors:
                    print(f"  connections ({len(neighbors)}):")
                    for nbr, w, t in sorted(neighbors, key=lambda x: -x[1])[:8]:
                        nbr_label = kg.get(nbr)["label"] if kg.get(nbr) else nbr
                        print(f"    └─ {nbr_label}  (γ={w:.2f}, {t})")
                print()

    elif "--paths" in sys.argv:
        idx = sys.argv.index("--paths")
        args = sys.argv[idx + 1:]
        if len(args) >= 2:
            src = f"operator:{args[0]}" if not args[0].startswith("operator:") else args[0]
            tgt = f"operator:{args[1]}" if not args[1].startswith("operator:") else args[1]
            # Also try topic:
            for prefix in ["operator:", "topic:", "author:"]:
                if kg.get(f"{prefix}{args[0]}"):
                    src = f"{prefix}{args[0]}"
                if kg.get(f"{prefix}{args[1]}"):
                    tgt = f"{prefix}{args[1]}"
            path = kg.find_path(src, tgt)
            if path:
                print(f"Path: {' → '.join(kg.get(n)['label'] for n in path)}")
            else:
                print(f"No path between {src} and {tgt}")

            # Also show direct neighbors
            for nid in [src, tgt]:
                node = kg.get(nid)
                if not node:
                    continue
                nbrs = kg.neighbors(nid)
                print(f"\n{node['label']} neighbors ({len(nbrs)}):")
                for nbr, w, t in sorted(nbrs, key=lambda x: -x[1])[:6]:
                    nbr_label = kg.get(nbr)["label"] if kg.get(nbr) else nbr
                    print(f"  {nbr_label}  γ={w:.2f} [{t}]")

    elif "--operators" in sys.argv:
        print("PhaseNav Operators (35):")
        for i, (name, desc) in enumerate(PHASENAV_OPERATORS.items()):
            neighbors = kg.neighbors(f"operator:{name}")
            n_links = len(neighbors)
            print(f"  {i:2d}. {name:20s}  {desc[:50]:55s}  ({n_links} links)")

    elif "--stats" in sys.argv:
        data = kg.to_dict()
        print(json.dumps(data["stats"], indent=2))
        # Show top connected nodes
        degrees = {nid: len(kg.neighbors(nid)) for nid in kg.nodes}
        top = sorted(degrees.items(), key=lambda x: -x[1])[:10]
        print("\nMost connected nodes:")
        for nid, deg in top:
            label = kg.nodes[nid]["label"]
            print(f"  {deg:3d}  {label}")

    else:
        print(__doc__)
