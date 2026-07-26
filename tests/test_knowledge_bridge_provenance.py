from __future__ import annotations

import ast
from pathlib import Path


def test_inactive_binding_warning_interpolates_module_name():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "src"
        / "cielingo_core"
        / "bridge"
        / "knowledge_bridge.py"
    )
    tree = ast.parse(module_path.read_text(encoding="utf-8"))

    warning_messages = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if not isinstance(node.func, ast.Attribute) or node.func.attr != "warn":
            continue
        if node.args:
            warning_messages.append(node.args[0])

    assert warning_messages
    message = warning_messages[0]
    assert isinstance(message, ast.JoinedStr)
    assert any(
        isinstance(part, ast.FormattedValue)
        and isinstance(part.value, ast.Name)
        and part.value.id == "__name__"
        for part in message.values
    )
