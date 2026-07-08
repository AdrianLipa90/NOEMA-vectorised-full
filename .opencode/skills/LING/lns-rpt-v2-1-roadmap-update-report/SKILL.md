---
name: v2-1-roadmap-update-report
priority: 5
description: >
  >
---
# v2.1 Roadmap and Learning Policy Patch Report

## Contents

- **Summary**: This patch updates the repository-level plan. The previous roadmap was an early v0.7 plan and no lon
- **Added / updated**: - Updated `docs/11_IMPLEMENTATION_ROADMAP.md` - Added `docs/41_NOEMA_GGUF_TEACHER_VALIDATOR_ROADMAP.md` - Added `data/ro
- **Key policy changes**: 1. NOEMA retrieval and local validation come before GGUF/LLM calls. 2. GGUF/LLM verdicts are advisory teacher-validator 
- **Status**: - Data status: planning metadata only, no external dictionary import. - Blockers: none. - Expected test count after this

## Key Points

- Updated `docs/11_IMPLEMENTATION_ROADMAP.md`
- Added `docs/41_NOEMA_GGUF_TEACHER_VALIDATOR_ROADMAP.md`
- Added `data/roadmap/cielingo_stage_plan_v2_1.{json,yaml,csv}`
- Added `data/roadmap/gguf_teacher_validator_policy_v2_1.{json,yaml}`
- Added `data/roadmap/noema_inference_gate_policy_v2_1.{json,yaml}`
- Added `schemas/ciel_lns_roadmap.schema.json`
- Added `src/lingophysics/roadmap.py`
- Added `tests/test_roadmap.py`
- Data status: planning metadata only, no external dictionary import.
- Expected test count after this patch: previous tests + roadmap tests.

---
*Extracted from: `src/ciel_lingophysics_lns_repo_v2_3/reports/v2_1_roadmap_update_report.md` (30 lines, 1321B)*