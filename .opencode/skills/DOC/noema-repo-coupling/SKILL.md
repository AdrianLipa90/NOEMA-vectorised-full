---
name: noema-repo-coupling
priority: 1
description: >
  >
---
# Repo Coupling

## Scripts

```bash
.venv/bin/python3 scripts/run_gh_repo_coupling.py
.venv/bin/python3 scripts/run_gh_repo_coupling_v2.py
.venv/bin/python3 scripts/run_repo_phase_sync.py
.venv/bin/python3 scripts/run_repo_sync_v2.py
```

## Flow

1. Clone/read repo
2. Extract coupling patterns
3. Phase encode → surface injection
4. TSM write
