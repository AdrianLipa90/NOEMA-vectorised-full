# CIELingo phase-sense output triad

This layer adds a runtime path for live text samples:

```text
surface words
  -> phase-sense parser
  -> comprehension lane
  -> inference lane
  -> expression lane
  -> 72D output vector
```

The 72D output vector consists of three 24D lanes so it remains compatible with
CIELingo vector surface contracts while preserving output-specific state.

## Lanes

- `comprehension`: token/card coverage, confidence, scalar-context density,
  viscosity, saturation, semantic time resistance/thinning and dominant phase.
- `inference`: mean CIELingo 24D vector over matched language cards; this is
  the CQCL/HTRI/NOEMA/OrchORbital-compatible semantic transport surface.
- `expression`: output readiness under tensor-scalar drag; it mixes
  comprehension and inference while accounting for semantic time resistance.

## Phase sense

Each token receives a `PhaseSenseToken`. Known words are bound to own
CIELingo/NOEMA language cards. Unknown words become supervised candidates with
low confidence and explicit repair policy. No source card is overwritten.

## Epistemic boundary

"On-vivo" here means a live local text sample in the current runtime. It does
not mean direct access to a phone, external NOEMA SoT, physical HTRI, live Mongo
or psychological affect measurement.
