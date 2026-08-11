# M8 Validation Receipt — Relational Function Identity Closure

## Scope

Validation target: `feat/relational-function-closure` against `master` after M7 merge.

## Implemented

- structural identity explicitly separated from relational identity;
- concrete callable occurrence keys;
- exact internal binding resolution without first-match selection;
- versioned imported environment anchors;
- bare global/builtin names fail closed without a global binding table;
- occurrence call graph;
- exact SCC derivation and condensation DAG;
- acyclic relational hash closure;
- recursive SCCs remain OPEN debt;
- NOEMA structural/relational bridges;
- existing function-identity CLI extended with a threshold-free relational-closure section.

## Regression cases specified

1. structurally identical callers of different module-local helpers must **not** become aliases;
2. true copies with relationally identical helpers must become CLOSED aliases;
3. bare `len()` remains OPEN until global-shadowing absence can be derived;
4. explicit stdlib import may close through runtime identity;
5. pinned external distribution may close through distribution identity;
6. unversioned external distribution remains OPEN;
7. dynamic/local callable parameter remains OPEN;
8. recursive SCC remains OPEN with cycle debt;
9. same qualified symbol with different CLOSED relational identity is CONFLICT;
10. NOEMA structural bridge cannot claim relational closure;
11. CLOSED relational aliases share NOEMA relational identity without fabricated PNV36;
12. OPEN relational identities remain occurrence-specific;
13. CLI payload exposes exact bindings, components, condensation edges, and `thresholds=[]`.

## Current verdict

- implementation: **IMPLEMENTED CANDIDATE**
- tests: **TEST-SPECIFIED**
- isolated execution: **NOT YET ESTABLISHED IN THIS RECEIPT**
- repository CI: **PENDING / UNKNOWN**
- CANON promotion: **NO**
- NOEMA CURRENT update: **NO**
- Actuator: **NO**
- automatic module/package rewrite: **NO**

A later append/update to this receipt must record the concrete workflow/job evidence. A workflow status without executable step evidence must not be interpreted as a code PASS or code FAIL.
