# CIELingo tensor-scalar context field

This layer corrects the pure-vector interpretation of CIELingo.  The 24D vector
surface remains a compatibility contract for CQCL, HTRI, NOEMA and OrchORbital,
but language dynamics require a mixed field:

- **real / koto exchange**: information exchanged between words/cards is encoded
  as a rank-2 tensor-like 3x3 matrix;
- **imaginary / mono context**: context and affect are encoded as scalar medium
  parameters: density, viscosity, colour and saturation.

Affect labels such as sarcasm, excitement, tension, relief and fear are not
claimed as measured emotions.  They are local scalar-context proxies derived
from card text, lexical holonomy load, phase tension and knowledge-confidence
debt.  External lexical/affective evidence must be attached before canonical
promotion.

## Semantic time

The module exposes two temporal scalar proxies:

- `semantic_time_resistance`: increases with contextual density, viscosity,
  saturation, opposition/divergence and fear/tension/sarcasm load.  This models
  information that feels heavy and temporally slow.
- `semantic_time_thinning`: increases with relief, excitement, convergence and
  knowledge confidence.  This models fluent information flow.

## Integration

The tensor-scalar state exports payloads for:

- CQCL: tensor trace/determinant proxy and scalar context variables;
- HTRI: phase drag, density, viscosity and colour hue;
- NOEMA: field digest and real/imaginary field roles;
- OrchORbital: tensor-scalar field digest and scalar-context payload.

This is a deterministic local diagnostic surface.  It is not an external NOEMA
SoT write, live Mongo update, physical HTRI proof, or psychological assessment.
