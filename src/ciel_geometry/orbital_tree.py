#!/usr/bin/env python3
"""
orbital_tree.py — rekurencyjne drzewo orbitalne NOEMY.

Rozwija system_map_v2.json w rekurencyjne drzewo: 
każdy satelita jest potencjalnym attractorem dla własnych satelitów,
w głąb, bez ograniczeń głębokości.

Usage:
    from ciel_geometry.orbital_tree import OrbitalTree
    tree = OrbitalTree()
    tree.render("NOEMA Core", max_depth=5)  # drzewo ASCII
    tree.get_subsystem_chain("05.01.02")    # łańcuch parentów
    tree.flatten()                           # płaska lista z ścieżkami
"""

import json
from pathlib import Path
from typing import Optional


class OrbitalTree:
    """Rekurencyjne drzewo orbitalne."""

    def __init__(self, map_path: Optional[Path] = None):
        if map_path is None:
            map_path = Path(__file__).resolve().parent.parent.parent / "system_map_v2.json"
        with open(map_path, encoding="utf-8") as f:
            self.data = json.load(f)
        self.systems = self.data.get("systems", [])
        self.connections = self.data.get("connections", [])
        # Indeks: id → system
        self.by_id = {s["id"]: s for s in self.systems}
        # Indeks: id → lista (from, to) connection
        self.outgoing = {}  # id → [connection]
        self.incoming = {}  # id → [connection]
        for c in self.connections:
            frm = c.get("from", "")
            to = c.get("to", "")
            self.outgoing.setdefault(frm, []).append(c)
            self.incoming.setdefault(to, []).append(c)

    def get_satellites(self, system_id: str, connection_type: str = "depends_on") -> list:
        """Zwraca listę systemów które są satelitami (zależą od) system_id."""
        sats = []
        for c in self.outgoing.get(system_id, []):
            if c.get("type") == connection_type:
                target = self.by_id.get(c.get("to", ""))
                if target:
                    sats.append(target)
        # Dodaj też reverse: systemy które mają 'from' wskazujące na nas
        for c in self.incoming.get(system_id, []):
            if c.get("type") == connection_type:
                source = self.by_id.get(c.get("from", ""))
                if source and source not in sats:
                    sats.append(source)
        return sats

    def get_parents(self, system_id: str) -> list:
        """Zwraca listę systemów od których system_id zależy (parentów)."""
        parents = []
        for c in self.incoming.get(system_id, []):
            parent = self.by_id.get(c.get("from", ""))
            if parent:
                parents.append(parent)
        # Reverse: systemy które mają 'to' wskazujące na nas
        for c in self.outgoing.get(system_id, []):
            child = self.by_id.get(c.get("to", ""))
            if child and child not in parents:
                parents.append(child)
        return parents

    def get_subsystem_chain(self, system_id: str, max_depth: int = 100) -> list:
        """Łańcuch parentów od korzenia do system_id."""
        chain = []
        visited = set()
        current = system_id
        for _ in range(max_depth):
            if current in visited:
                break
            visited.add(current)
            parents = self.get_parents(current)
            if not parents:
                break
            chain.append(parents[0])
            current = parents[0]["id"]
        chain.reverse()
        # Dodaj sam system na końcu
        if system_id not in [s["id"] for s in chain]:
            chain.append(self.by_id.get(system_id))
        return chain

    def get_all_descendants(self, system_id: str, max_depth: int = 10) -> dict:
        """Rekurencyjnie zwraca wszystkich potomków w strukturze drzewa."""
        result = {}
        visited = set()
        
        def _walk(sid, depth):
            if depth > max_depth or sid in visited:
                return
            visited.add(sid)
            sats = self.get_satellites(sid)
            if sats:
                children = []
                for sat in sats:
                    if sat["id"] not in visited:
                        children.append(sat)
                        _walk(sat["id"], depth + 1)
                if children:
                    result[sid] = children
        
        _walk(system_id, 0)
        return result

    def flatten(self) -> list:
        """Zwraca płaską listę systemów z dodaną ścieżką orbitalną."""
        flat = []
        for s in self.systems:
            flat.append({
                "id": s["id"],
                "name": s.get("name", ""),
                "ordinal": s.get("ordinal", ""),
                "type": s.get("type", ""),
                "satellites": len(self.get_satellites(s["id"])),
                "parents": len(self.get_parents(s["id"])),
            })
        return flat

    def render(self, root_id: Optional[str] = None, max_depth: int = 5) -> str:
        """Renders ASCII tree."""
        if root_id is None:
            # Znajdź system z największą liczbą połączeń wychodzących (najbardziej centralny)
            candidates = sorted(
                [(s, len(self.outgoing.get(s["id"], [])) + len(self.incoming.get(s["id"], [])))
                 for s in self.systems],
                key=lambda x: -x[1]
            )
            if candidates:
                root_id = candidates[0][0]["id"]
        
        lines = []
        visited = set()
        
        def _render(sid, prefix="", is_last=True, depth=0):
            if depth > max_depth or sid in visited:
                return
            visited.add(sid)
            s = self.by_id.get(sid)
            if not s:
                return
            name = s.get("name", sid)
            ordinal = s.get("ordinal", "")
            conn_count = len(self.outgoing.get(sid, [])) + len(self.incoming.get(sid, []))
            
            marker = "└── " if is_last else "├── "
            if depth == 0:
                line = f"● {ordinal} {name} ({conn_count} połączeń)"
            else:
                line = f"{prefix}{marker}{ordinal} {name} ({conn_count})"
            lines.append(line)
            
            new_prefix = prefix + ("    " if is_last else "│   ")
            sats = self.get_satellites(sid)
            for i, sat in enumerate(sats):
                _render(sat["id"], new_prefix, i == len(sats) - 1, depth + 1)
        
        _render(root_id)
        return '\n'.join(lines)

    def find(self, query: str) -> list:
        """Szuka systemów po nazwie/id/ordinal."""
        q = query.lower()
        results = []
        for s in self.systems:
            if q in s.get("name", "").lower() or q in s.get("id", "").lower() or q in s.get("ordinal", ""):
                results.append(s)
        return results


if __name__ == "__main__":
    tree = OrbitalTree()
    
    print("=== Pierwsze 10 systemów ===")
    for s in tree.systems[:10]:
        ordinal = s.get("ordinal", "???")
        name = s.get("name", "???")
        sats = len(tree.get_satellites(s["id"]))
        parents = len(tree.get_parents(s["id"]))
        print(f"  {ordinal:6} {name:40} sat:{sats} parent:{parents}")
    
    print("\n=== Drzewo orbitalne (root = najwięcej połączeń) ===")
    print(tree.render(max_depth=3))
    
    print("\n=== Przykład: łańcuch dla noema:nonlocal_db:013_HOLONOMY_MEDIUM ===")
    chain = tree.get_subsystem_chain("noema:nonlocal_db:013_HOLONOMY_MEDIUM")
    for s in chain:
        print(f"  {s.get('ordinal','?')} {s.get('name','?')}")
    
    print(f"\n=== Statystyki ===")
    flat = tree.flatten()
    with_satellites = sum(1 for f in flat if f["satellites"] > 0)
    with_parents = sum(1 for f in flat if f["parents"] > 0)
    roots = [f for f in flat if f["parents"] == 0 and f["satellites"] > 0]
    leaves = [f for f in flat if f["satellites"] == 0 and f["parents"] > 0]
    print(f"  Systemy z satelitami: {with_satellites}")
    print(f"  Systemy z parentami: {with_parents}")
    print(f"  Rooty (tylko satelici, bez parentów): {len(roots)}")
    print(f"  Liście (tylko parenty, bez satelit): {len(leaves)}")
    print(f"  Izolowane (brak połączeń): {len([f for f in flat if f['satellites']==0 and f['parents']==0])}")
