---
name: geometry-engine-and-ui-surface
priority: 4
description: >
  >
---
# Geometry Engine and UI Surface

## Contents

- **Principle**: The geometry engine maps formal state into an operational chart. The renderer displays the chart. Do not mix them.
- **Geometry engine responsibilities**: - compute orbital positions - compute geodesic dependencies - compute activity overlays - compute tension/conflict overl
- **Poincaré disk responsibilities**: Use the disk for: - distance-to-attractor reading - conflict clustering - geodesic edge placement - transition continuit
- **Bloch local views**: Use Bloch-like views only as local inspectors: - local phase relations - spin orientation - reduced triadic or qubit-lik
- **UI surface responsibilities**: The native UI must: - open instantly - show the orbital field - support entity inspection - support session inspection -
- **Non-goals**: Do not implement: - classic tabbed admin panel as the primary experience - fake orbital visuals without state backing - 

## Key Points

- compute orbital positions
- compute geodesic dependencies
- compute activity overlays
- compute tension/conflict overlays
- compute focus transitions
- compute orbit precession and stability diagnostics
- distance-to-attractor reading
- conflict clustering
- geodesic edge placement
- transition continuity
- orbital shell differentiation
- local phase relations

---
*Extracted from: `src/CIEL_Orbital_Foundation_Packk/08_GEOMETRY_ENGINE_AND_UI_SURFACE.md` (50 lines, 1202B)*