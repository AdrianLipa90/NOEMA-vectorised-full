# NOEMA ↔ PhaseNav TIR × ½ Dependency Contract v0.7

This directory is the NOEMA-side dependency/provenance boundary for the PhaseNav
TIR × Secret-of-a-Half canon.

## Authority

NOEMA stores:

- the exact PhaseNav canonical commit;
- upstream TIR and Secret-of-a-Half source commits;
- routing and intrinsic dimensions;
- typed epistemic statuses;
- firewall rules;
- append-only integration receipts.

NOEMA does **not** duplicate the PhaseNav engine and does not acquire authority to
promote a mathematical or physical claim.

The canonical PhaseNav parent for this integration is:

`54f65f2ca7d35cdd98f0ab8984cc1a8d74444a96`

with hard-canon version `1.2.0` and dependency layer `0.7.0`.

## State-space boundary

The recovered coefficient state remains intrinsic 4D:

`(h,a,b,c)`.

PhaseNav transport/routing remains `T^36`.

These spaces are related by an executable routing projection; they are not
identified.

## Epistemic boundary

The contract preserves, rather than flattens, the current scientific states:

- role routing: structural PASS;
- orbital direction: implemented project rule;
- relational gradient: implemented source operator, TIR binding still candidate;
- TIR coefficient-slot binding: OPEN;
- Collatz stopping orientation: retrospective candidate requiring prospective test;
- SOH-C004: OPEN;
- SOH-C005: OPEN;
- TIR common likelihood: OPEN;
- current TIR neutron EDM relation: PHYSICAL_FAIL.

A memory write, vectorization, PhaseNav route, holonomy receipt, or NOEMA recall
cannot promote any of those labels.

## Validation

Run the stdlib-only validator directly with Python:

`python integration/phasenav_dependencies/v0_7/validate_contract.py`

It performs no memory mutation. Its output is a deterministic validation receipt
containing the canonicalized contract SHA-256.

## Writeback sequence

This first contract binds PhaseNav to the current upstream TIR/½ source heads.
After the corresponding v0.7 TIR and Secret-of-a-Half integrations are merged,
NOEMA receives a second append-only cross-repository closure receipt containing
their final merge SHAs. The first receipt is not overwritten.
