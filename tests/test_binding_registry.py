from __future__ import annotations

import pytest

from binding_state import temporarily_set_binding
from src.ciel_geometry.noema_registry import NoemaRegistry, _ciel_binding_check


def test_binding_check_reports_degraded_state() -> None:
    with temporarily_set_binding("DEGRADED"):
        assert _ciel_binding_check() == "ciel_binding_status NOT ACTIVE: DEGRADED"


def test_registry_refuses_register_when_binding_is_broken(tmp_path) -> None:
    registry = NoemaRegistry(root=tmp_path / "registry")

    with temporarily_set_binding("DEGRADED"):
        with pytest.raises(RuntimeError, match="CIEL BINDING BROKEN"):
            registry.register("phasenav")
