---
name: interpretation
priority: 5
description: >
  >
---
# Toy-Model White-Thread Matrix F_ij on S²

## Contents

- **Model Specification**: | Fermion | Generation | Cycle θ_i (rad) | |---------|------------|-----------------| | e       | 1          | π/6 ≈ 0.5
- **Summary Statistics**: | Variant      | Min     | Max     | Mean   | Std     | |--------------|---------|---------|--------|---------| | Direct
- **Inter-Generation Block Averages (Directional)**: | Gen i → Gen j | Mean F_ij | |---------------|-----------| | 1 → 1         | 1.000001 | | 1 → 2         | 1.004553 | | 
- **Sample Pairwise Values**: | Pair     | F_dir   | F_abs   | F_cos   | |----------|---------|---------|---------| | e → μ    | 1.0024  | 1.0024  | 1
- **Top Deviations from 1 (|F_ij - 1| > 0, excluding diagonal)**: **Directional** (largest): t→d (0.9790, Δ=-0.0214), d→t (1.0214, Δ=+0.0214), b→ν₁ (0.9805), ... **Sym Abs** (largest): t
- **Physical Interpretation**: 1. **Directional**: Models **oriented transport** (holonomy-like). Generations 1→3 amplified (1.01), 2. **Sym Abs**: Pur
- **Files Generated**: | File | Description | |------|-------------| | `analysis_F_directional_full.csv` | Full 12×12 F_dir [code_file:77] | | 

## Key Points

- Calibrate β to match PDG F_i (u/d/s/neutrinos).
- Add monopole Berry A on S² for true holonomy.
- Extend to full SM (baryons/mesons via quark F_ij).

## Tables

| e       | 1          | π/6 ≈ 0.5236   |
| μ       | 2          | π/4 ≈ 0.7854   |
| τ       | 3          | π/3 ≈ 1.0472   |
| u       | 1          | π/8 ≈ 0.3927   |
| d       | 1          | π/10 ≈ 0.3142  |
| s       | 2          | π/5 ≈ 0.6283   |
| c       | 2          | π/2 ≈ 1.5708   |
| b       | 3          | 2π/3 ≈ 2.0944  |

| Directional | 0.9790 | 1.0214 | ~1.000 | 0.0065 |
| Sym Abs     | 1.0000 | 1.0214 | 1.0032 | 0.0048 |
| Sym Cos     | 0.9937 | 1.0090 | 1.0000 | 0.0037 |

| 1 → 1         | 1.000001 |
| 1 → 2         | 1.004553 |
| 1 → 3         | 1.011457 |
| 2 → 1         | 0.995482 |
| 2 → 2         | 1.000014 |
| 2 → 3         | 1.006903 |
| 3 → 1         | 0.988589 |
| 3 → 2         | 0.993133 |

---
*Extracted from: `src/ciel-omega-demo-main/docs/Studies/Metatime-main/data/2026/01/Standard Model/interpretation.md` (100 lines, 4248B)*