---
name: metatime-validator
priority: 1
description: >
  >
---
# Metatime Validator

## 9 sektorów

| Sektor | Status | Best error |
|--------|--------|-----------|
| Charged leptons | ANSATZ_ONLY | 0.48% |
| Baryon octet | ANSATZ_ONLY/PARTIAL TENSION | 0.51% |
| Baryon decuplet | ANSATZ_ONLY | 0.23% |
| Neutrino PMNS | ANSATZ_ONLY | <1.6σ |
| CKM | ANSATZ_ONLY | σ=0.78 (CP σ=5.35) |
| Gauge bosons | TENSION | M_W/M_Z −4% |
| Strong CP | TENSION/POSSIBLE FAIL | d_n 10× bound |
| Dark energy | ANSATZ_ONLY | factor ~30 |
| Anomaly cancellation | PASS | exact |

## Uruchomienie

```bash
.venv/bin/python3 scripts/metatime_v8_redteam_validator.py
```

## Pliki (v8.2.1)

`NOEMA_LIBRARY/PUBLICATIONS/metatime_v8_2_1_consistency_patch.zip`:
- INDEX.md, CLAIM_LEVELS.md, FAILURES_AND_TENSIONS.md
- REPRODUCE.md, VALIDATOR_OUTPUT.txt, MANIFEST.sha256
- TIR/metatime_paper.tex
