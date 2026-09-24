"""Card Tag Algebra — every tag on every NOEMA card as an algebraic subset
of the card universe.

Origin: Adrian's insight (2026-07-10) mid-session — "każdy tag każdej karty
jest nowym zbiorem/podzbiorem algebraicznym!! to są klastry sensu w
temacie" (every tag of every card is a new algebraic set/subset, these are
clusters of meaning in the topic). Not built from scratch: the core math
(tag as a set of records, pairwise coupling via set intersection weighted
by a semantic-mass-like quantity, clustering from that coupling graph)
already exists in consolidation_resonator.py — but scoped narrowly to
~400 recent session-consolidation records in consolidator.db. This module
applies the same algebraic shape to the actual NOEMA card corpus
(cards/**/*.noema.card.json, 264 cards as of 2026-07-10), which is a
different, larger, more structurally significant universe.

Core objects:
  - CARD_UNIVERSE: the set of all card ids.
  - Each tag t defines a SUBSET: cards(t) = {c in CARD_UNIVERSE : t in tags(c)}.
  - Two tags' relationship is their subset overlap: intersection (shared
    cards — direct semantic correlation) and union (combined coverage).
    Jaccard(t1, t2) = |cards(t1) ∩ cards(t2)| / |cards(t1) ∪ cards(t2)|
    is the natural [0,1] coupling strength between two tags-as-sets.
  - A CLUSTER is a connected component of the tag graph where edges are
    Jaccard(t1, t2) >= threshold — a group of tags whose card-subsets
    overlap enough to represent one cluster of meaning, exactly Adrian's
    framing ("to są klastry sensu w temacie").
"""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)

import json
import math
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

_ROOT = Path(__file__).resolve().parents[2]
_CARDS_DIR = _ROOT / "cards"
_CLUSTERS_OUT = _ROOT / "docs" / "object_cards" / "db" / "tag_clusters"
# Compact machine-readable cache — phasenav_learning_gate.py reads this
# (not the markdown cards, not a live recompute) so a per-candidate gate
# call doesn't re-scan 264 card files every time. Refreshed by whatever
# periodic mechanism runs this module (see OPEN_ISSUES
# 'card-tag-algebra-new-capability' for the on-demand-vs-daemon decision).
_CLUSTERS_CACHE = Path("/media/adrian/New Volume/CIEL_memories/state/tag_clusters_cache.json")
# Verified live 2026-07-10 against the real 264-card corpus: 0.12 chains
# via transitive overlap into one giant 132-card/200+-tag blob (classic
# connected-components-at-low-threshold failure — any two tags sharing
# even one card in a small-world graph end up in the same component).
# 0.35 breaks that apart into ~40 small, high-cohesion (0.4-1.0), legible
# clusters (e.g. {autotask, learned, lessons, rule-15, self-improvement}
# cohesion=0.67; {keyinject, trigger, x11} cohesion=0.57) — real clusters
# of meaning, not one blob.
_DEFAULT_JACCARD_THRESHOLD = 0.35


@dataclass
class TagSubset:
    """One tag as an algebraic subset of the card universe."""
    tag: str
    card_ids: set[str] = field(default_factory=set)

    @property
    def count(self) -> int:
        return len(self.card_ids)


@dataclass
class TagCluster:
    """A connected component of tags whose card-subsets overlap enough to
    represent one cluster of meaning."""
    tags: set[str]
    card_ids: set[str]  # union of every member tag's subset
    cohesion: float  # mean pairwise Jaccard among member tags

    @property
    def size(self) -> int:
        return len(self.tags)


def load_card_tags() -> dict[str, set[str]]:
    """card_id -> set(tags). Cards without a 'tags' field or with an empty
    list are skipped — no tag, no subset membership, nothing to cluster."""
    result: dict[str, set[str]] = {}
    if not _CARDS_DIR.exists():
        return result
    for path in _CARDS_DIR.rglob("*.noema.card.json"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            _NOEMA_QUIET_EXCEPT_LOGGER.exception(
                "src/ciel_sot_agent/card_tag_algebra.py:load_card_tags quiet except scope=load_card_tags reason=skip_unreadable")
            continue
        card_id = data.get("id") or data.get("card_id") or str(path)
        raw_tags = data.get("tags")
        if not raw_tags:
            continue
        tags = {str(t).strip().lower() for t in raw_tags if str(t).strip()}
        if tags:
            result[card_id] = tags
    return result


def build_tag_subsets(card_tags: dict[str, set[str]]) -> dict[str, TagSubset]:
    """Invert card_id->tags into tag->TagSubset (tag as a set of card ids) —
    this IS the algebraic subset Adrian described: cards(tag)."""
    inverted: dict[str, set[str]] = defaultdict(set)
    for card_id, tags in card_tags.items():
        for tag in tags:
            inverted[tag].add(card_id)
    return {tag: TagSubset(tag=tag, card_ids=ids) for tag, ids in inverted.items()}


def jaccard(a: TagSubset, b: TagSubset) -> float:
    union = a.card_ids | b.card_ids
    if not union:
        return 0.0
    return len(a.card_ids & b.card_ids) / len(union)


def build_coupling_graph(
    subsets: dict[str, TagSubset],
    threshold: float = _DEFAULT_JACCARD_THRESHOLD,
) -> dict[str, dict[str, float]]:
    """Adjacency map tag -> {other_tag: jaccard} for pairs above threshold.
    O(n^2) over unique tags — fine for hundreds of tags, would need an
    inverted-index shortcut (only compare tags sharing >=1 card) well
    before this becomes a bottleneck at NOEMA's current card-corpus scale."""
    tags = list(subsets.keys())
    graph: dict[str, dict[str, float]] = {t: {} for t in tags}
    for i, t1 in enumerate(tags):
        s1 = subsets[t1]
        for t2 in tags[i + 1:]:
            s2 = subsets[t2]
            if not (s1.card_ids & s2.card_ids):
                continue  # zero intersection -> zero Jaccard, skip the divide
            j = jaccard(s1, s2)
            if j >= threshold:
                graph[t1][t2] = j
                graph[t2][t1] = j
    return graph


def cluster_tags(
    subsets: dict[str, TagSubset],
    threshold: float = _DEFAULT_JACCARD_THRESHOLD,
) -> list[TagCluster]:
    """Connected components of the tag coupling graph — each component is
    one cluster of meaning (Adrian: 'to są klastry sensu w temacie')."""
    graph = build_coupling_graph(subsets, threshold)
    visited: set[str] = set()
    clusters: list[TagCluster] = []

    for start in subsets:
        if start in visited:
            continue
        # BFS over the coupling graph
        component = {start}
        frontier = [start]
        visited.add(start)
        while frontier:
            node = frontier.pop()
            for neighbor in graph.get(node, {}):
                if neighbor not in visited:
                    visited.add(neighbor)
                    component.add(neighbor)
                    frontier.append(neighbor)

        member_card_ids: set[str] = set()
        for tag in component:
            member_card_ids |= subsets[tag].card_ids

        # Cohesion: mean Jaccard across the edges actually present within
        # this component (isolated single-tag "clusters" get cohesion 1.0
        # by convention — a lone tag is perfectly cohesive with itself).
        edges = [
            graph[t1][t2]
            for t1 in component
            for t2 in graph.get(t1, {})
            if t2 in component and t1 < t2
        ]
        cohesion = sum(edges) / len(edges) if edges else 1.0

        clusters.append(TagCluster(tags=component, card_ids=member_card_ids, cohesion=round(cohesion, 4)))

    clusters.sort(key=lambda c: -c.size)
    return clusters


def write_cluster_cards(clusters: list[TagCluster]) -> int:
    """Write one markdown card per multi-tag cluster + an INDEX.md — same
    shape/location pattern as consolidation_resonator.write_tag_cards(),
    applied to the card-tag clusters instead of consolidation-tag clusters.
    Singleton (size==1) clusters are skipped here — a lone unclustered tag
    isn't a 'cluster of meaning' worth a card of its own; it's still fully
    present in report()'s raw output for anyone inspecting the algebra
    directly."""
    import re
    from datetime import datetime, timezone

    multi = [c for c in clusters if c.size > 1]
    _CLUSTERS_OUT.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    written = 0

    for cluster in sorted(multi, key=lambda c: -c.cohesion):
        label = "_".join(sorted(cluster.tags)[:3])
        fname = re.sub(r"[^a-zA-Z0-9ąćęłńóśźżĄĆĘŁŃÓŚŹŻ_\-]", "_", label)[:60] + ".md"
        fpath = _CLUSTERS_OUT / fname
        tags_list = "\n".join(f"- `{t}`" for t in sorted(cluster.tags))
        md = f"""# TAG CLUSTER: {label}

## Identity
- **cluster_id:** `cluster:{label}`
- **source:** `cards/**/*.noema.card.json` (card_tag_algebra.py)
- **last_updated:** `{now}`

## Algebra
| param | value |
|---|---|
| **cohesion** | `{cluster.cohesion}` |
| n_tags | `{cluster.size}` |
| n_cards | `{len(cluster.card_ids)}` |

## Member tags (each an algebraic subset of the card universe)
{tags_list}
"""
        fpath.write_text(md, encoding="utf-8")
        written += 1

    lines = [
        "# Card Tag Clusters — Index",
        f"*Generated: {now} | {len(multi)} multi-tag clusters (threshold={_DEFAULT_JACCARD_THRESHOLD})*",
        "",
        "| cluster | cohesion | n_tags | n_cards |",
        "|---|---|---|---|",
    ]
    for cluster in sorted(multi, key=lambda c: -c.cohesion):
        label = ", ".join(sorted(cluster.tags)[:4]) + (", ..." if cluster.size > 4 else "")
        lines.append(f"| {label} | `{cluster.cohesion}` | {cluster.size} | {len(cluster.card_ids)} |")
    (_CLUSTERS_OUT / "INDEX.md").write_text("\n".join(lines), encoding="utf-8")
    return written


def write_clusters_cache(clusters: list[TagCluster]) -> None:
    """Compact JSON: [{tags: [...], cohesion: float}, ...] for multi-tag
    clusters only — the fast-loadable artifact phasenav_learning_gate.py's
    tag_cluster_relevance() reads instead of recomputing clustering per
    candidate."""
    multi = [c for c in clusters if c.size > 1]
    _CLUSTERS_CACHE.parent.mkdir(parents=True, exist_ok=True)
    payload = [
        {"tags": sorted(c.tags), "cohesion": c.cohesion}
        for c in sorted(multi, key=lambda c: -c.cohesion)
    ]
    _CLUSTERS_CACHE.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")


def report(threshold: float = _DEFAULT_JACCARD_THRESHOLD) -> dict[str, Any]:
    card_tags = load_card_tags()
    subsets = build_tag_subsets(card_tags)
    clusters = cluster_tags(subsets, threshold)

    multi_tag_clusters = [c for c in clusters if c.size > 1]
    return {
        "n_cards_with_tags": len(card_tags),
        "n_unique_tags": len(subsets),
        "n_clusters_total": len(clusters),
        "n_multi_tag_clusters": len(multi_tag_clusters),
        "threshold": threshold,
        "clusters": [
            {
                "tags": sorted(c.tags),
                "n_cards": len(c.card_ids),
                "cohesion": c.cohesion,
            }
            for c in multi_tag_clusters
        ],
    }


if __name__ == "__main__":
    import sys
    thr = float(sys.argv[1]) if len(sys.argv) > 1 else _DEFAULT_JACCARD_THRESHOLD
    write_cards = "--no-write" not in sys.argv
    rep = report(threshold=thr)
    print(json.dumps(rep, indent=2, ensure_ascii=False))
    if write_cards:
        card_tags = load_card_tags()
        subsets = build_tag_subsets(card_tags)
        clusters = cluster_tags(subsets, thr)
        n = write_cluster_cards(clusters)
        print(f"\nWritten {n} cluster cards to {_CLUSTERS_OUT}", file=sys.stderr)
        write_clusters_cache(clusters)
        print(f"Written clusters cache to {_CLUSTERS_CACHE}", file=sys.stderr)
