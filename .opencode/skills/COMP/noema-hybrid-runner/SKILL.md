---
name: noema-hybrid-runner
priority: 1
description: >
  >
---
# Hybrid Runner

## Build

```bash
python3 scripts/build_cielingo.py   # build CIELingo package
python3 scripts/build_noema_packages.py
python3 scripts/build_sot_agent.py
```

## Run

```bash
.venv/bin/python3 scripts/noema_daemon.py
.venv/bin/python3 scripts/noema_codegen.py
.venv/bin/python3 scripts/run_cielyngo_example.py
```

## Test

```bash
.venv/bin/python3 -m pytest tests/
```
