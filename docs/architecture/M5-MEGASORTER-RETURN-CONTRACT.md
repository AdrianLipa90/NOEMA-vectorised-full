# M5 — MegaSorter Return Contract

Status: **IMPLEMENTED ON FEATURE BRANCH / VALIDATION PENDING**

Branch: `arch/pnv-gate-fabric-consolidation`

## Objective

Close the return leg from MegaSorter to NOEMA without allowing an external planner to manufacture evidence or mutation authority.

```text
NOEMA_MEGASORTER_ENVELOPE_V1
  -> MegaSorter
  -> NOEMA_MEGASORTER_PROPOSALS_V1
  -> NOEMA transport validation
  -> originating-envelope evidence lookup
  -> candidate PhaseOperation
  -> Gate / Doctor / Return
```

## Accepted return contract

NOEMA accepts only a proposal batch with:

```text
schema            = NOEMA_MEGASORTER_PROPOSALS_V1
source            = MEGASORTER
mode              = ADVISORY_ONLY
mutation_allowed  = false
originating_batch = current envelope batch_id
proposal_batch_sha256 = valid canonical SHA-256
```

Optional metadata may declare:

```text
evidence_authority          = ORIGINATING_NOEMA_ENVELOPE
integrity_hash_is_authority = false
```

Any other evidence-authority claim is rejected.

## Integrity is not authority

NOEMA recomputes `proposal_batch_sha256` over canonical JSON after removing only the hash field itself.

A matching digest establishes transport integrity only.

It does not create:

- epistemic evidence;
- provenance;
- Doctor PASS;
- Gate OPEN;
- mutation permission;
- SoT promotion permission.

The hash is therefore an audit primitive, not a truth scalar.

## Replay and endpoint isolation

The proposal batch is bound to the `originating_batch` identifier.

NOEMA rejects:

- cross-batch replay;
- proposal source outside the envelope;
- proposal target outside the envelope;
- mismatched `evidence_lookup_key` endpoints.

Formal batches are stricter than the lower-level single-proposal helper. This is intentional: transport contracts should reject malformed topology before creating a candidate.

## Evidence recovery

Proposal confidence and proposal-supplied `evidence` fields are not authoritative.

NOEMA resolves the source/target pair against `MegaSorterEnvelope.relations` and uses only the evidence from the originating relation.

Invariant:

```text
PhaseOperation.evidence = evidence(originating NOEMA relation)
```

not:

```text
PhaseOperation.evidence = evidence claimed by MegaSorter proposal
```

If no originating relation exists, the lower-level candidate path carries no evidence and Gate Fabric holds it. A valid formal M5 batch is expected to bind endpoints to the originating envelope and preserve this lookup semantics.

## Candidate status

Every accepted proposal remains:

```text
candidate_only = true
mutation_allowed = false
mutation_class = READ_ONLY
return_required = true
```

No M5 path invokes the Actuator.

## Tests specified

`tests/test_pnv_megasorter_bridge.py` covers:

- formal proposal batch round-trip;
- self-supplied MegaSorter evidence ignored as authority;
- originating NOEMA relation evidence recovered;
- cross-batch replay rejection;
- mutation-authority rejection;
- candidate-only requirement;
- transport hash tampering rejection;
- target-outside-envelope rejection;
- evidence lookup mismatch rejection.

## Current status

```text
return transport         = IMPLEMENTED
integrity verification   = IMPLEMENTED
replay isolation         = IMPLEMENTED
endpoint binding         = IMPLEMENTED
evidence authority split = IMPLEMENTED
tests                    = TEST-SPECIFIED
runtime validation       = UNKNOWN UNTIL EXECUTED
Actuator                  = NOT INVOKED
promotion                 = HOLD
main merge                = NOT AUTHORIZED
```
