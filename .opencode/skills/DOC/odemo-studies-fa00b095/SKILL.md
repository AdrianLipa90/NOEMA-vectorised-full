---
name: fa00b095
priority: 5
description: >
  >
---
# Neutrino Mass-Splitting Scaling Convention: Full Summary

## Contents

- **Executive Summary**: After analyzing multiple Metatime documents, **we adopt the atmospheric-anchor convention** as the s - **Global scale \(
- **Question Posed**: **Q: "Który lepiej skalować?"** (Which is better to scale on?) Two concrete options were evaluated: 1. **Scale on \(\Del
- **Scaling on \(\Delta m^2_{31}\) — Pros**: - **Canonical in current notes**: *Formal_SM.pdf*, *Coherence_law_application.pdf*, *Collatz_emergen - **Simplest calibr
- **Scaling on \(\Delta m^2_{31}\) — Cons**: - **Solar splits are undershoot**: By definition, \(\Delta m^2_{21}\) comes out as \(\sim 4.09 \time - **Requires explic
- **Scaling on \(\Delta m^2_{32}\) — Pros**: - **Decouples from mass-1 baseline**: \(\Delta m^2_{32} = \Delta m^2_{31} - \Delta m^2_{21}\) isolat - **Directly releva
- **Scaling on \(\Delta m^2_{32}\) — Cons**: - **Not used in current pipeline**: None of the primary calibration documents (*Formal_SM.pdf*, *Coh - **Requires more a
- **Official Convention**: **Global scale \(s\) is fixed by atmospheric splitting:** $$ s = \sqrt{\frac{\Delta m^2_{31,\text{exp}}}{\Delta m^2_{31,
- **Solar Splitting Recovery**: **The observed \(\Delta m^2_{21} = 7.53 \times 10^{-5}\,\text{eV}^2\) is recovered via pairwise topo $$ \Delta m^2_{21,\

## Formulas

- `s = \sqrt{\frac{\Delta m^2_{31,\text{exp}}}{\Delta m^2_{31,\text{model}}}} = \sqrt{\frac{2.524 \times 10^{-3}}{3.0604 \times 10^{-6}}} = 28.7198 \,\text{eV per model unit}`
- `m_i^{\text{phys}} = s \cdot m_i^{\text{model}}`
- `\Delta m^2_{21,\text{corrected}} = s^2 (\tau_2^2 - \tau_1^2) (F_{21})^2`
- `(F_{21})^2 = \frac{\Delta m^2_{21,\text{exp}}}{\Delta m^2_{21,\text{model}}} = \frac{7.53 \times 10^{-5}}{4.0937 \times 10^{-5}} \approx 1.841`
- `F_{21} \approx 1.357`
- `F_{ij} = 1 + \varepsilon_\nu \tanh(\Omega_{ij} - \Omega_{\text{crit}}) / \Delta\Omega`

## Definitions

- **where:**: \(\Delta m^2_{31,\text{exp}} = 2.524 \times 10^{-3}\,\text{eV}^2\) is the PDG 2024 global-fit value (normal ordering).
- **Resulting mass-squared splittings:**: \(\Delta m^2_{31} = 2.524 \times 10^{-3}\,\text{eV}^2\) (by calibration, exact).

## Key Points

- **Global scale \(s\) is fixed by atmospheric splitting \(\Delta m^2_{31} = 2.524 \times 10^{-3}\,\text{eV}^2\)** (PDG 2024 global fit, normal ordering).
- **Solar splitting \(\Delta m^2_{21}\)** is subsequently recovered via pairwise topological correction factor \(F_{21}\).
- **Future alternative scalings** (solar-anchor, \(\Delta m^2_{32}\)-anchor) can be derived by recomputing scale factors and correction hierarchies.
- **Canonical in current notes**: *Formal_SM.pdf*, *Coherence_law_application.pdf*, *Collatz_emergence1.pdf* all use this convention explicitly.
- **Simplest calibration pipeline**: Single scale factor \(s = \sqrt{\Delta m^2_{31,\text{exp}} / \Delta m^2_{31,\text{model}}}\) directly determines all physical masses.
- **Atmospheric anchor is robust**: \(\Delta m^2_{31}\) is the primary atmospheric parameter measured in long-baseline experiments (T2K, NOvA, DUNE).
- **Explicit numerical reference**: \(s = 28.7198\,\text{eV}\) per model unit is hardcoded in the pipeline.
- **Solar splits are undershoot**: By definition, \(\Delta m^2_{21}\) comes out as \(\sim 4.09 \times 10^{-5}\,\text{eV}^2\), a factor ~1.84 too small compared to PDG (\(7.53 \times 10^{-5}\,\text{eV}^2
- **Requires explicit \(F_{21}\) correction**: Must introduce pairwise topology factor \(F_{21} \approx 1.357\) (or \((F_{21})^2 \approx 1.841\)) to recover solar splitting.
- **Coupling to mass-1 introduces sensitivity**: If the mass-1 baseline or \(\Delta\epsilon_1\) eigenvalue definition changes, the entire atmospheric calibration shifts.
- **Decouples from mass-1 baseline**: \(\Delta m^2_{32} = \Delta m^2_{31} - \Delta m^2_{21}\) isolates the heaviest two states, reducing entanglement with solar sector.
- **Directly relevant for resonance physics**: DUNE CP-resonance condition depends explicitly on \(m^2_{32}L / 4E\); scaling on \(\Delta m^2_{32}\) makes resonance predictions more transparent.

## Tables

| *Formal_SM.pdf* | \(\Delta m^2_{31}\) → \(s\) | 28.7198 eV | \(\Delta m^2_{21}\) undershoot factor 2; requires \(F_{21}\) |
| *Coherence_law_application.pdf* | Same, with pairwise coherence \(\Omega_{ij}\) | 28.72 eV | \(F_{21}=1.357\), \(\Omega_{21}=0.931\) |
| *Collatz_emergence1.pdf* | Explicit numeric steps | 28.7198 eV | Mass hierarchy reproduced; \(\Delta m^2_{21}\) acknowledged as undershoot |
| *Calabi_Yau.pdf* | Same pipeline + geometric moduli | 28.72 eV | Discusses \(\rho_0\)-modulation as alternative to \(F_{ij}\) |

| \(\nu_1\) | 0.02 | \(1.4687 \times 10^{-5}\) | \(4.218 \times 10^{-4}\) | By definition \(m_1 < m_2 < m_3\) (NO) |
| \(\nu_2\) | 0.05 | \(2.2326 \times 10^{-4}\) | \(6.412 \times 10^{-3}\) | |
| \(\nu_3\) | 0.10 | \(1.7494 \times 10^{-3}\) | \(5.024 \times 10^{-2}\) | Heaviest mass-eigenstate |

| \(\Delta m^2_{31}\) | By calibration: \(2.524 \times 10^{-3}\) | \(2.524 \times 10^{-3}\) | ✓ Exact match |
| \(\Delta m^2_{21}\) | \(4.0937 \times 10^{-5}\) | \(7.53 \times 10^{-5}\) | Factor 1.84 short → requires \(F_{21}\) |
| \(\Delta m^2_{32}\) | \(2.449 \times 10^{-3}\) | \(2.449 \times 10^{-3}\) | ✓ Derived from difference, consistent |

---
*Extracted from: `src/ciel-omega-demo-main/docs/Studies/Metatime-main/documents/fa00b095.md` (271 lines, 13126B)*