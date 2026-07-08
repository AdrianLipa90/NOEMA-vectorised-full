---
name: omega-cockpit-1-0
priority: 5
description: >
  >
---
# Omega Cockpit 1.0

## Contents

- **Purpose**: This document defines the first architectural refactor of the current `ciel-omega-demo` UI. The goal is **not** to repla
- **Core principle**: Omega Cockpit is organized around an **Identity Attractor**. The center is not chat, kernel, files, or settings. The cen
- **Orbit 0 — Identity Attractor**: Central system state. Fields: - identity_state - coherence_scalar - resonance_scalar - ethics_gate - active_contract - a
- **Orbit 1 — Constitutive layers**: What defines what Omega is. Modules: - Theory - Operators - Constants - Constraints - Memory Topology Each object in thi
- **Orbit 2 — Dynamic layers**: What executes motion. Modules: - Kernel - Execution - Planner - Session Dynamics - Command Routing Execution chain must 
- **Orbit 3 — Interaction layers**: What touches the user and the outside world. Modules: - Agent - Chat - Dialogue - Tool Interface - User Input - Session 
- **Orbit 4 — Observational layers**: What observes, measures, and audits the system. Modules: - Observability - Logs - Tests - Audit - Provenance - Crossrefs
- **Orbit 5 — Boundary layers**: What separates internal state from external release. Modules: - Publication Boundary - Public/Private Separation - Expor

## Key Points

- tools are exposed as peer tabs,
- runtime concerns dominate the surface,
- the relation between theory, execution, evidence, and publication boundaries is not shown explicitly,
- epistemic status is not treated as a first-class UI signal.
- active identity profile,
- coherence / resonance,
- active canon/export package,
- active operator set,
- active constraints,
- ethics gate state,
- current session phase,
- memory/provenance load,

---
*Extracted from: `src/ciel-omega-demo-main/docs/OMEGA_COCKPIT_1_0.md` (328 lines, 6307B)*