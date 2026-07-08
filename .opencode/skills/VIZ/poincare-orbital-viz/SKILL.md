---
name: poincare-orbital-viz
priority: 1
description: >
  >
---
# Orbital Visualization

## Layout

```python
from ciel_geometry.layout import compute_orbital_layout, apply_layout
centers = compute_orbital_layout(surface_state)
edges = infer_edges(entities, centers)
```

## Renderers

| Renderer | Output | Use case |
|----------|--------|----------|
| `renderer_ascii.py` | Terminal (60×20) | Debug bez X11 |
| `renderer_mpl.py` | Matplotlib window | Interactive |
| `orbital.html` | HTML + JS | Browser |

## Pliki

- `src/ciel_geometry/layout.py`
- `src/ciel_geometry/renderer_ascii.py`
- `src/ciel_geometry/renderer_mpl.py`
- `opencode_research/orbital.html`
