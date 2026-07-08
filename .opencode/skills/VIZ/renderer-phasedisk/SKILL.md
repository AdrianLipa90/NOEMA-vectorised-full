---
name: renderer-phasedisk
priority: 1
description: >
  >
---
# Renderer: Poincaré Disk

## ASCII renderer

```python
from ciel_geometry.renderer_ascii import render_ascii
print(render_ascii(entities, edges, width=60, height=20))
```

Terminalowy Poincaré disk — entities jako kropki, edges jako linie.
Do debugowania bez X11.

## Matplotlib renderer

```bash
python -m ciel_geometry.renderer_mpl
```

Interaktywny orbital cockpit — entity circles z coupling labels,
geodesic arcs, zoom/pan.

## Pliki

- `src/ciel_geometry/renderer_ascii.py`
- `src/ciel_geometry/renderer_mpl.py`
