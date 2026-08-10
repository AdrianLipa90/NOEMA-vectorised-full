# M6 — Cross-Repo Transport Conformance

Status: **IMPLEMENTED ON FEATURE BRANCH / VALIDATION PENDING**

Branch: `arch/pnv-gate-fabric-consolidation`

Canonical authority: `NOEMA`

## Objective

Bind the M4/M5 NOEMA ↔ MegaSorter round-trip to one machine-readable transport contract without transferring authority to the planner.

```text
NOEMA
  -> NOEMA_MEGASORTER_ENVELOPE_V1
  -> transport fingerprint check
  -> MegaSorter M4 PLAN_ONLY
  -> NOEMA_MEGASORTER_PROPOSALS_V1
  -> transport fingerprint + batch integrity checks
  -> NOEMA M5 evidence recovery
  -> candidate PhaseOperation
```

## Canonical transport descriptor

Artifact:

`contracts/noema_megasorter_transport_v1.json`

Contract id:

`NOEMA_MEGASORTER_TRANSPORT_V1`

Descriptor SHA-256:

`b490f9ec27879db1fd7ab83473a670a8e49190ca8bf6bc8d1595da2195654f7b`

The descriptor binds:

- envelope schema `NOEMA_MEGASORTER_ENVELOPE_V1`;
- proposal schema `NOEMA_MEGASORTER_PROPOSALS_V1`;
- outbound `source=NOEMA`, `mode=PLAN_ONLY`;
- inbound `source=MEGASORTER`, `mode=ADVISORY_ONLY`;
- `mutation_allowed=false`;
- `pnv_precise_phase_36`;
- `PHASENAV_PNV_RUNTIME_CANON_PRECISE_V1`;
- 36 dimensions;
- `evidence_authority=ORIGINATING_NOEMA_ENVELOPE`;
- `integrity_hash_is_authority=false`.

A code-side hard-coded expected descriptor digest makes silent descriptor drift fail at import time unless the contract is deliberately versioned.

## NOEMA transport wrapper

Module:

`src/ciel_sot_agent/pnv_megasorter_transport.py`

It provides:

- `build_transport_envelope()` — normal M5 envelope plus contract id/fingerprint;
- `envelope_from_transport_dict()` — typed reconstruction for round-trip transport material;
- `proposal_batch_to_transport_candidates()` — requires the M6 fingerprint before delegating to the M5 evidence-authority split;
- `contract_artifact()` — machine-readable runtime descriptor.

M6 does not replace M4/M5 semantics. It constrains their transport seam.

## Exact shared fixture

Artifact:

`contracts/fixtures/noema_megasorter_roundtrip_v1.json`

The fixture is mirrored byte-for-byte in the MegaSorter feature branch and contains:

- one query node at phase `0` on all 36 axes;
- one retrieved observation at phase `π` on all 36 axes;
- one evidence-backed `retrieved_for` relation;
- no holonomic cycle;
- the exact expected `NOEMA_MEGASORTER_PROPOSALS_V1` batch;
- the exact expected NOEMA candidate evidence.

Expected proposal batch SHA-256:

`e74866ad8acc4b4457cef1821e224c446d73bef61c6415c792bf5c0373aef37b`

The expected planner output is exactly one `PHASE_ALIGNMENT_GATE` candidate with confidence `0.65` and no mutation authority.

## Authority invariants

```text
contract fingerprint != evidence
contract fingerprint != provenance
contract fingerprint != Doctor PASS
contract fingerprint != Gate OPEN
contract fingerprint != mutation permission
contract fingerprint != SoT promotion
```

The fingerprint proves only that both transport endpoints claim the same versioned structural contract.

M5 still determines proposal-batch payload integrity separately with `proposal_batch_sha256`.

Evidence is still recovered only from the originating NOEMA relation.

## Tests specified

`tests/test_pnv_megasorter_transport.py` checks:

- canonical contract artifact equals runtime descriptor;
- descriptor SHA is exact;
- exact shared fixture reconstructs a valid typed envelope;
- exact shared proposal batch recovers only originating NOEMA evidence;
- outbound runtime envelope carries the contract fingerprint;
- envelope fingerprint drift is rejected;
- return-batch fingerprint drift is rejected before M5 candidate conversion.

## Current epistemic status

```text
contract artifact          = IMPLEMENTED
runtime fingerprint        = IMPLEMENTED
shared golden fixture      = IMPLEMENTED
NOEMA transport wrapper    = IMPLEMENTED
cross-batch M5 isolation   = IMPLEMENTED
Actuator                    = NOT INVOKED
promotion                   = HOLD
tests                       = TEST-SPECIFIED
runtime validation          = UNKNOWN UNTIL EXECUTED
master merge                = NOT AUTHORIZED
```
