---
name: loader-edges
priority: 1
description: >
  >
---
# Loader & Edges

## Loader

```python
# Ładuje geometry data z CIEL integration layer
from ciel_geometry.loader import load_entities, load_relations
entities = load_entities("path/to/data.json")  # nazwa, coupling, phase
relations = load_relations("path/to/edges.json")  # src, dst, weight
```

## Edges

Geodesic arcs między entity na Poincaré disk:

```python
from ciel_geometry.edges import GeodesicEdge, build_edges
edges = build_edges(entities, relations, min_weight=0.05)
# edge.arc_points → lista (x,y) do rysowania
```

## Pliki

- `src/ciel_geometry/loader.py`
- `src/ciel_geometry/edges.py`
- `src/ciel_geometry/layout.py`
