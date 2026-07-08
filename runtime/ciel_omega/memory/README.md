# memory

## Identity
Retention, path dependence, and consolidation layer.

## Database Modules
Persistent stores are exposed as explicit memory modules in
[`database_modules.py`](database_modules.py):

- SQLite ledgers and caches are inspectable as read-only memory modules.
- HDF5 archives are surfaced as memory modules when available.
- The canonical catalog currently includes the TSM ledger, WPM archive,
  nonlocal graph cache, and the local CIEL state DB.

## Berry Phase
The canonical Berry-phase interface lives in
[`berry_phase.py`](berry_phase.py) and is shared by memory, orbital metrics,
and book analysis.

## Sleep Consolidation
Idle-time corpus digestion and holonomy-based promotion live in
[`sleep_consolidation.py`](sleep_consolidation.py). It is the explicit
sleep-mode wrapper around book analysis for low-activity consolidation.
The cadence layer lives in [`sleep_scheduler.py`](sleep_scheduler.py) and
drives the daemon/job entrypoints in `scripts/sleep_mode_daemon.py` and
`scripts/sleep_mode_book_consolidation.py`.

## Layered Memory
The layered facade lives in [`layered_memory.py`](layered_memory.py). It
exposes a read-only snapshot over the live channels with metatime-normalized
scalar flow and `W_ij` transport.

## Parent
- [ciel_omega](../README.md)

## Navigation
Up:
- [ciel_omega](../README.md)

Side:
- [runtime](../runtime/README.md)
- [bridge](../bridge/README.md)
- [constraints](../constraints/README.md)
- [vocabulary](../vocabulary/README.md)

## Action / Spin
- dominant spin: `stabilize`

## Coherence Impact
High for local orbital geometry and sector-level transport.
