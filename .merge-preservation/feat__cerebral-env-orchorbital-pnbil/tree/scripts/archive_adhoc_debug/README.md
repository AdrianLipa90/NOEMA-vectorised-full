# Ad-hoc debug/scratch scripts — archived 2026-07-18

These 91 scripts were found untracked in `scripts/` (never committed, never documented)
during a documentation-currency audit. Naming pattern (`noema_check_*`, `noema_debug_*`,
`noema_probe_*`, `noema_test_*`, `noema_find_*`, `noema_diagnose_*`, `noema_investigate_*`,
`noema_stop_pid.py`, `noema_restart_*`, etc.) and content indicate they were one-off
diagnostic/debugging scripts written during past interactive sessions (Claude CLI and/or
other agents) to answer a specific question in the moment — not ongoing infrastructure.

**Verification performed:** none of these 91 filenames appear as `ExecStart=` in any of the
21 `noema-*.service`/`.path`/`.timer` systemd user units (checked 2026-07-18). That is the
only verification done — content of each script was not individually reviewed.

**Why archived, not deleted:** they may still have diagnostic value or reveal historical
debugging context. If you need to run a one-off check like this again, look here first
before writing a new one — several near-duplicates already exist (e.g. three separate
`noema_check_llama*.py` variants, several `noema_headless_log*.py` tailing scripts).

**Do not treat anything in this directory as documented, current, or safe to run without
re-reading it first** — none of it was verified against current system state.
