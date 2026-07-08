"""Orbital hierarchy helpers for star -> planet -> satellite loading.

This module formalizes the recursive orbital interpretation already used by
``system_map_v2.json`` and ``OrbitalTree``:

* depth 0 is the attractor/star,
* depth 1 is the planet/system orbit,
* depth 2 is the satellite orbit,
* depth 3+ are sub-satellites.

The same ordering is useful for memory layers: load the attractor first, then
the next orbital shell, then the next, and so on.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .orbital_tree import OrbitalTree


def layer_name_for_depth(depth: int) -> str:
    """Return the canonical layer label for an orbital depth."""
    depth = max(0, int(depth))
    if depth == 0:
        return "attractor"
    if depth == 1:
        return "planet"
    if depth == 2:
        return "satellite"
    if depth == 3:
        return "sub-satellite"
    return f"sub-satellite-{depth - 2}"


def orbit_load_mode_for_depth(depth: int) -> str:
    """All layers in the canonical hierarchy are loaded orbitally."""
    _ = max(0, int(depth))
    return "orbital"


def _degrees(tree: OrbitalTree, connection_type: str = "depends_on") -> tuple[dict[str, int], dict[str, int]]:
    outgoing: dict[str, int] = {}
    incoming: dict[str, int] = {}
    for connection in tree.connections:
        if connection.get("type") != connection_type:
            continue
        source = str(connection.get("from") or "")
        target = str(connection.get("to") or "")
        if source:
            outgoing[source] = outgoing.get(source, 0) + 1
        if target:
            incoming[target] = incoming.get(target, 0) + 1
    return outgoing, incoming


def choose_root_id(tree: OrbitalTree, connection_type: str = "depends_on") -> str | None:
    """Pick the most central root, preferring nodes with no incoming edges."""
    outgoing, incoming = _degrees(tree, connection_type=connection_type)
    nodes = list(tree.systems)
    if not nodes:
        return None

    roots = [node for node in nodes if incoming.get(node.get("id", ""), 0) == 0 and outgoing.get(node.get("id", ""), 0) > 0]
    candidates = roots or nodes

    def _score(node: dict[str, Any]) -> tuple[int, int, str]:
        node_id = str(node.get("id") or "")
        return (
            -(outgoing.get(node_id, 0) + incoming.get(node_id, 0)),
            -outgoing.get(node_id, 0),
            str(node.get("ordinal") or node.get("lp") or node_id),
        )

    candidates.sort(key=_score)
    return str(candidates[0].get("id") or "") or None


@dataclass(frozen=True)
class OrbitalHierarchyNode:
    """Single node in the canonical orbital hierarchy."""

    id: str
    name: str
    ordinal: str
    depth: int
    layer: str
    parent_id: str | None
    child_count: int
    load_mode: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "ordinal": self.ordinal,
            "depth": self.depth,
            "layer": self.layer,
            "parent_id": self.parent_id,
            "child_count": self.child_count,
            "load_mode": self.load_mode,
        }


class OrbitalHierarchy:
    """Build and render the orbital loading hierarchy from ``system_map_v2.json``."""

    def __init__(
        self,
        map_path: str | Path | None = None,
        *,
        tree: OrbitalTree | None = None,
        root_id: str | None = None,
        max_depth: int = 16,
        connection_type: str = "depends_on",
    ) -> None:
        self.tree = tree or OrbitalTree(Path(map_path) if map_path is not None else None)
        self.connection_type = connection_type
        self.root_id = root_id or choose_root_id(self.tree, connection_type=connection_type)
        self.max_depth = max(1, int(max_depth))
        self.nodes = self._build_nodes()
        self.edges = self._build_edges()

    def _children_of(self, node_id: str) -> list[dict[str, Any]]:
        children: list[dict[str, Any]] = []
        for connection in self.tree.outgoing.get(node_id, []):
            if connection.get("type") != self.connection_type:
                continue
            target_id = str(connection.get("to") or "")
            child = self.tree.by_id.get(target_id)
            if child is not None:
                children.append(child)
        children.sort(
            key=lambda item: (
                str(item.get("ordinal") or item.get("lp") or ""),
                str(item.get("name") or item.get("id") or ""),
            )
        )
        return children

    def _build_nodes(self) -> list[OrbitalHierarchyNode]:
        if not self.root_id:
            return []

        nodes: list[OrbitalHierarchyNode] = []
        best_depth: dict[str, int] = {self.root_id: 0}
        parent: dict[str, str | None] = {self.root_id: None}
        queue: list[tuple[str, int]] = [(self.root_id, 0)]

        while queue:
            current_id, depth = queue.pop(0)
            if depth > self.max_depth:
                continue
            node = self.tree.by_id.get(current_id)
            if node is None:
                continue
            nodes.append(
                OrbitalHierarchyNode(
                    id=current_id,
                    name=str(node.get("name") or current_id),
                    ordinal=str(node.get("ordinal") or node.get("lp") or ""),
                    depth=depth,
                    layer=layer_name_for_depth(depth),
                    parent_id=parent.get(current_id),
                    child_count=len(self._children_of(current_id)),
                    load_mode=orbit_load_mode_for_depth(depth),
                )
            )

            for child in self._children_of(current_id):
                child_id = str(child.get("id") or "")
                if not child_id:
                    continue
                next_depth = depth + 1
                prev_depth = best_depth.get(child_id)
                if prev_depth is not None and prev_depth <= next_depth:
                    continue
                best_depth[child_id] = next_depth
                parent[child_id] = current_id
                queue.append((child_id, next_depth))

        return nodes

    def _build_edges(self) -> list[dict[str, str]]:
        edges: list[dict[str, str]] = []
        for node in self.nodes:
            if node.parent_id:
                edges.append({"from": node.parent_id, "to": node.id})
        return edges

    def load_order(self) -> list[dict[str, Any]]:
        """Return nodes ordered by orbital depth for memory-like loading."""
        return [node.to_dict() for node in sorted(self.nodes, key=lambda item: (item.depth, item.ordinal, item.name))]

    def to_dict(self) -> dict[str, Any]:
        return {
            "root_id": self.root_id,
            "max_depth": self.max_depth,
            "connection_type": self.connection_type,
            "levels": {
                "0": "attractor",
                "1": "planet",
                "2": "satellite",
                "3": "sub-satellite",
            },
            "nodes": [node.to_dict() for node in self.nodes],
            "edges": list(self.edges),
            "load_order": self.load_order(),
        }

    def validate(self) -> list[dict[str, Any]]:
        """Return a list of validation issues, if any."""
        issues: list[dict[str, Any]] = []
        if not self.root_id:
            issues.append({"kind": "missing_root", "detail": "No root node could be selected."})
        if not self.nodes:
            issues.append({"kind": "empty_hierarchy", "detail": "Hierarchy contains no nodes."})
            return issues

        if self.nodes[0].depth != 0:
            issues.append({"kind": "bad_root_depth", "detail": f"Root depth is {self.nodes[0].depth}, expected 0."})

        depths = [node.depth for node in self.nodes]
        if any(depth < 0 for depth in depths):
            issues.append({"kind": "negative_depth", "detail": "Negative depth found in hierarchy."})

        for node in self.nodes:
            if node.depth > self.max_depth:
                issues.append(
                    {
                        "kind": "depth_overflow",
                        "detail": f"{node.id} exceeds max_depth={self.max_depth}",
                    }
                )

        return issues

    def render_mermaid(self) -> str:
        """Render the hierarchy as Mermaid flowchart syntax."""
        lines = ["flowchart TB"]
        for node in self.nodes:
            label = f"{node.name}\\n{node.layer} · d={node.depth}"
            lines.append(f'    "{node.id}"["{label}"]')
        for edge in self.edges:
            lines.append(f'    "{edge["from"]}" --> "{edge["to"]}"')
        return "\n".join(lines)


def build_orbital_hierarchy(
    map_path: str | Path | None = None,
    *,
    root_id: str | None = None,
    max_depth: int = 16,
    connection_type: str = "depends_on",
) -> dict[str, Any]:
    """Convenience wrapper that returns the hierarchy as a JSON-friendly dict."""
    return OrbitalHierarchy(
        map_path=map_path,
        root_id=root_id,
        max_depth=max_depth,
        connection_type=connection_type,
    ).to_dict()


def render_orbital_mermaid(
    map_path: str | Path | None = None,
    *,
    root_id: str | None = None,
    max_depth: int = 16,
    connection_type: str = "depends_on",
) -> str:
    """Convenience wrapper for Mermaid rendering."""
    return OrbitalHierarchy(
        map_path=map_path,
        root_id=root_id,
        max_depth=max_depth,
        connection_type=connection_type,
    ).render_mermaid()


def orbit_load_order(
    map_path: str | Path | None = None,
    *,
    root_id: str | None = None,
    max_depth: int = 16,
    connection_type: str = "depends_on",
) -> list[dict[str, Any]]:
    """Return the canonical orbital load order for memory-like layers."""
    return OrbitalHierarchy(
        map_path=map_path,
        root_id=root_id,
        max_depth=max_depth,
        connection_type=connection_type,
    ).load_order()

