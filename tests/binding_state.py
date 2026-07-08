from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path


BINDING_DIR = Path("/dev/shm/ciel_noema")
BINDING_STATUS = BINDING_DIR / "ciel_binding_status"


def ensure_active_binding() -> None:
    BINDING_DIR.mkdir(parents=True, exist_ok=True)
    BINDING_STATUS.write_text("ACTIVE", encoding="utf-8")


def set_binding_status(value: str) -> None:
    BINDING_DIR.mkdir(parents=True, exist_ok=True)
    BINDING_STATUS.write_text(value, encoding="utf-8")


def clear_binding_status() -> None:
    if BINDING_STATUS.exists():
        BINDING_STATUS.unlink()


@contextmanager
def temporarily_set_binding(value: str):
    previous = BINDING_STATUS.read_text(encoding="utf-8") if BINDING_STATUS.exists() else None
    set_binding_status(value)
    try:
        yield
    finally:
        if previous is None:
            clear_binding_status()
        else:
            BINDING_STATUS.write_text(previous, encoding="utf-8")
