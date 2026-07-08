---
name: native-product-architecture
priority: 4
description: >
  >
---
# Native Product Architecture

## Contents

- **Product goal**: A self-contained native desktop product with: - local state engine - geometry engine - native renderer - autonomy routin
- **Proposed top-level packages**: - `ciel_orbital/kernel/` - `ciel_orbital/registry/` - `ciel_orbital/memory/` - `ciel_orbital/autonomy/` - `ciel_orbital/
- **Native UI stack**: Recommended first implementation: - Python - Qt / PySide6 - QML only where needed for motion-rich orbital views
- **Inference policy**: Use: 1. own memory 2. own evidence / local retrieval 3. own operators 4. external LLM only if still necessary Track: `al
- **MVP scope**: - native startup - orbital field view - entity inspector - session panel - memory panel - provenance view - reduction di
- **Hardening scope**: - packaging - crash handling - state snapshot and recovery - release bundles - smoke tests - offline mode

## Key Points

- local state engine
- autonomy routing
- optional model integration
- no web server as the UI substrate
- `ciel_orbital/kernel/`
- `ciel_orbital/registry/`
- `ciel_orbital/memory/`
- `ciel_orbital/autonomy/`
- `ciel_orbital/geometry/`
- `ciel_orbital/simulator/`
- `ciel_orbital/app/`
- `ciel_orbital/config/`

---
*Extracted from: `src/CIEL_Orbital_Foundation_Packk/09_NATIVE_PRODUCT_ARCHITECTURE.md` (66 lines, 1150B)*