---
name: v2-2-noema-retrieval-inference-gate-report
priority: 5
description: >
  >
---
# v2.2 NOEMA Retrieval and Inference Gate Patch Report

## Contents

- **Summary**: v2.2 introduces the first executable NOEMA routing layer for CIELingo. It adds an index schema, a seed index, routing po
- **Key rules**: - NOEMA routes first. - CIELingo validates structurally. - GGUF verdict is advisory, not canonical. - Dense GGUF partial
- **Added modules**: ```text src/lingophysics/noema_index.py src/lingophysics/noema_router.py src/lingophysics/inference_gate.py src/lingophy
- **Added test files**: ```text tests/test_noema_router.py tests/test_inference_gate.py ```
- **Next recommended patch**: v2.3 GGUF Teacher-Validator Learning Loop.
- **Local test adjustment**: Inflected Polish glass forms (`szklance`, `szklankę`, `szklanki`) are included in the seed labels so

## Key Points

- NOEMA routes first.
- CIELingo validates structurally.
- GGUF verdict is advisory, not canonical.
- Dense GGUF partial execution is not claimed.
- Unresolved high-impact issues route to human review.

---
*Extracted from: `src/ciel_lingophysics_lns_repo_v2_3/reports/v2_2_noema_retrieval_inference_gate_report.md` (42 lines, 1096B)*