---
name: noema-build-system
priority: 1
description: >
  >
---
# Build System

## Konfiguracja

| Plik | Rola |
|------|------|
| `pyproject.toml` | PEP 517/518 build config + entry points |
| `setup.py` | Legacy setup |
| `requirements.txt` | Core deps |
| `requirements-dev.txt` | Dev deps |
| `requirements-cuda.txt` | CUDA/cupy deps |
| `requirements-htri.txt` | HTRI hardware deps |
| `conftest.py` | Pytest fixtures |
| `sitecustomize.py` | Python site init |
| `VERSION` | Semver tag |
| `.env.example` | Environment template |
