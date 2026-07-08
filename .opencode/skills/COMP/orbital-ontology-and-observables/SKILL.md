---
name: ontology-and-observables
priority: 4
description: >
  >
---
# Ontology and Observables

## Contents

- **Purpose**: This document freezes the canonical vocabulary of the new project. Nothing else should be implemente
- **Entity**: A persistent system object with identity, location in the orbital model, provenance, and dynamic sta
- **State**: A structured snapshot of the system at a discrete step. A state is not a UI frame; it is the formal 
- **Observable**: A quantity that can be computed from the state and used for validation, routing, or reduction. Examp - closure defect - 
- **Attractor**: A structured basin of convergence that shapes state evolution. Required attractor classes: - AttractorEC - AttractorZS -
- **Orbit**: A stable or metastable trajectory class around an attractor inside a sphere.
- **Sphere**: A local state container embedded inside a larger state container. Every sphere has: - internal modes - leak / embedding 
- **Leak mode**: A non-local embedding channel that carries unresolved closure, surplus coherence, or structural resi

## Key Points

- global coherence
- subjective time scale
- AttractorLLMTemp
- leak / embedding mode
- parent sphere reference or null
- child sphere references
- parent_sphere_id
- winding_components
- epistemic_status
- provenance_links
- dependency_links
- subjective_time_scale

---
*Extracted from: `src/CIEL_Orbital_Foundation_Packk/02_ONTOLOGY_AND_OBSERVABLES.md` (108 lines, 2523B)*