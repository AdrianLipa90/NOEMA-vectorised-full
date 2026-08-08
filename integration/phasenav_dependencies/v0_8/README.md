# NOEMA PhaseNav / TIR / Secret-of-a-Half Closure v0.8

This directory is an append-only successor to `integration/phasenav_dependencies/v0_7/`.

It records the final merged software/provenance closure of the v0.7 integration trajectory. It does not replace the earlier contract or initial binding receipt.

## Canonical anchors

- PhaseNav runtime parent: `54f65f2ca7d35cdd98f0ab8984cc1a8d74444a96`
- PhaseNav closure canon merge: `b3f31a0cad78f6c7c9e908434b98d5e3132b2a0a`
- NOEMA predecessor: `42a0a8916e81ca27f2213bf0f28538f046c2e89a`
- TIR merge: `df8a6e1321ecf2e2c8819f4e9d5ec7d4f997d170`
- Secret-of-a-Half merge: `a1b0aeba192766163893fab1468b8f9cd9b8853b`

PhaseNav canon is `1.3.0`, distribution `0.6.0`, closure schema `v0.8`.

## Vector closure

The PhaseNav closure vectorizes three distinct routing layers through the existing native `T^36` runtime:

1. four exact repository/commit source anchors;
2. eleven typed dependency nodes inherited from the v0.7 graph;
3. seven dependency paths, with path vectors explicitly carrying routing identity only.

Focused vector validation produced:

- source-state SHA-256: `d0c624dffcbc889309ebab418d48e16d9c172cf902590f90883b8e34c88c4638`
- closure SHA-256: `1619fa17f609baf1fc4db12dac7b3a166b26b44c84f9ffb80fc7533fb3767361`
- 22 vectors total;
- 22 finite 36D vectors;
- 22 unique vector hashes.

The intrinsic TIR coefficient state remains four-dimensional. The 36D envelope is routing state and is not a source of coefficients.

## Scientific boundary

No scientific status was promoted by the closure.

In particular:

- `KAPPA` remains `PROJECT_DERIVED_EXACT_ALGEBRA`;
- `TIR_SLOT_BINDING` remains `OPEN`;
- `SOH_C004` remains `OPEN`;
- `SOH_C005` remains `OPEN`;
- `TIR_COMMON_LIKELIHOOD` remains `OPEN`;
- `TIR_NEUTRON_EDM` remains `PHYSICAL_FAIL`;
- `COLLATZ_STOPPING_ORIENTATION` remains retrospective and blocked pending prospective validation.

NOEMA stores this state as provenance/dependency memory. It does not duplicate the PhaseNav engine and has no authority to convert a vector or receipt into scientific proof.

## Validation

Run with Python only:

```text
python integration/phasenav_dependencies/v0_8/validate_closure.py
```

The validator performs no memory mutation and verifies the exact source SHA pins, closure digests, vector counts, epistemic firewalls, append-only boundary, and receipt hash.
