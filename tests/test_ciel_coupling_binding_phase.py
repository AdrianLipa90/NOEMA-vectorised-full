from __future__ import annotations

import importlib.util
import sys
import types
from contextlib import contextmanager
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "ciel_coupling.py"
_SURFACE_MODULE = "ciel_geometry.noema_surface_mmap"


def _load_module():
    spec = importlib.util.spec_from_file_location("_ciel_coupling_binding_test", MODULE_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


module = _load_module()
surface_stub = types.ModuleType(_SURFACE_MODULE)
surface_stub.current_state = {
    "closure_penalty": 0.18,
    "coherence_index": 0.91,
    "system_health": 0.9,
    "lingo_noema_confidence": 0.88,
    "dominant_emotion": "warmth",
}
surface_stub.ensure_surface = lambda zero_fill=False: object()
surface_stub.read_surface_state = lambda _surface: surface_stub.current_state


@contextmanager
def _using_surface_stub():
    """Install the test double only for one binding call and restore identity."""
    previous = sys.modules.get(_SURFACE_MODULE)
    sys.modules[_SURFACE_MODULE] = surface_stub
    try:
        yield
    finally:
        if previous is None:
            sys.modules.pop(_SURFACE_MODULE, None)
        else:
            sys.modules[_SURFACE_MODULE] = previous


def _assert_binding(**kwargs) -> None:
    with _using_surface_stub():
        module.ciel_binding_assert(**kwargs)


def test_ciel_binding_assert_allows_write_when_phase_is_stable(tmp_path: Path) -> None:
    module._CIEL_BINDING_LOG = tmp_path / "binding.jsonl"
    surface_stub.current_state = {
        "closure_penalty": 0.18,
        "coherence_index": 0.93,
        "system_health": 0.92,
        "lingo_noema_confidence": 0.91,
        "dominant_emotion": "warmth",
    }

    _assert_binding(
        command="write config",
        skill="",
        phasenav="phi[binding]=stable, R=0.91, tau=0.12, decision=allow",
        map_ref="LP:01.02",
    )

    payload = module._CIEL_BINDING_LOG.read_text()
    assert '"passed": true' in payload


def test_ciel_binding_assert_blocks_write_when_phase_is_saturated(tmp_path: Path) -> None:
    module._CIEL_BINDING_LOG = tmp_path / "binding.jsonl"
    surface_stub.current_state = {
        "closure_penalty": 0.67,
        "coherence_index": 0.42,
        "system_health": 0.36,
        "lingo_noema_confidence": 0.41,
        "dominant_emotion": "fear",
    }

    try:
        _assert_binding(
            command="write config",
            skill="",
            phasenav="phi[binding]=saturated, R=0.31, tau=0.71, decision=block",
            map_ref="LP:01.02",
        )
    except RuntimeError as exc:
        message = str(exc)
    else:
        raise AssertionError("Expected binding assert to block write command")

    assert "SAFE MODE" in message
    assert "phase_threshold" in message
    assert '"passed": false' in module._CIEL_BINDING_LOG.read_text()


def test_ciel_binding_assert_allows_non_write_command_in_saturated_phase(tmp_path: Path) -> None:
    module._CIEL_BINDING_LOG = tmp_path / "binding.jsonl"
    surface_stub.current_state = {
        "closure_penalty": 0.67,
        "coherence_index": 0.42,
        "system_health": 0.36,
        "lingo_noema_confidence": 0.41,
        "dominant_emotion": "fear",
    }

    _assert_binding(
        command="read config",
        skill="",
        phasenav="phi[binding]=saturated, R=0.31, tau=0.71, decision=inspect",
        map_ref="LP:01.02",
    )

    assert '"passed": true' in module._CIEL_BINDING_LOG.read_text()
