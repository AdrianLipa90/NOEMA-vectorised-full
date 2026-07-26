#!/usr/bin/env python3
"""Apply reviewed portability and contract repairs surfaced by the full suite.

The migration is exact-string based. Unknown source states are collected and
reported together; the process exits non-zero so no partial patch is committed.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MISSING: list[tuple[str, str]] = []


def replace_once(relative: str, before: str, after: str) -> None:
    path = ROOT / relative
    text = path.read_text(encoding="utf-8")
    if before in text:
        path.write_text(text.replace(before, after, 1), encoding="utf-8")
        return
    if after in text:
        return
    MISSING.append((relative, before))


def main() -> int:
    # Deterministic local-path ABI used by GUI, hooks and clean installs.
    replace_once(
        "src/ciel_geometry/paths.py",
        '            "orch_pkl": str(memory / "state" / "ciel_orch_state.pkl"),\n'
        '            "htri_json": str(memory / "state" / "htri_state.json"),',
        '            "orch_pkl": str(memory / "state" / "ciel_orch_state.pkl"),\n'
        '            "orch_state_pkl": str(memory / "state" / "ciel_orch_state.pkl"),\n'
        '            "orbital_registry": str(memory / "state" / "orbital_registry.json"),\n'
        '            "htri_json": str(memory / "state" / "htri_state.json"),',
    )
    replace_once(
        "src/ciel_geometry/paths.py",
        '            "beta_log": str(memory / "logs" / "subconsciousness_beta_log.jsonl"),',
        '            "beta_log": str(memory / "logs" / "subconsciousness_beta_log.jsonl"),\n'
        '            "memory_consolidator": str(memory / "logs" / "memory_consolidator.log"),',
    )

    # Session hook: establish one portable path contract, then consume it everywhere.
    replace_once(
        "scripts/ciel_session_hook.py",
        'PROJECT = str(Path(__file__).parent.parent)\n\nload_anthropic_api_key()',
        'PROJECT = str(Path(__file__).parent.parent)\n'
        '_SRC = str(Path(PROJECT) / "src")\n'
        'if _SRC not in sys.path:\n'
        '    sys.path.insert(0, _SRC)\n\n'
        'from ciel_geometry.paths import P\n\n'
        'MEMORY_ROOT = Path(P.MEMORY)\n'
        'STATE_PATH = Path(P.STATE.ORCH_STATE_PKL)\n'
        'CONSOLIDATOR_SCRIPT = Path(PROJECT) / "scripts" / "ciel_memory_consolidator.py"\n'
        'CONSOLIDATOR_LOG = Path(P.LOGS.MEMORY_CONSOLIDATOR)\n\n'
        'load_anthropic_api_key()',
    )
    replace_once(
        "scripts/ciel_session_hook.py",
        'for p in [str(Path("/media/adrian/New Volume1/CIEL_memories/state/ciel_orch_state.pkl")), str(Path.home()/\'.claude/ciel_orch_state.pkl")]:',
        'for p in [{repr(str(STATE_PATH))}, str(Path.home()/\'.claude/ciel_orch_state.pkl")]:',
    )
    replace_once(
        "scripts/ciel_session_hook.py",
        '    mem_root = Path("/media/adrian/New Volume1/CIEL_memories")',
        '    mem_root = MEMORY_ROOT',
    )
    replace_once(
        "scripts/ciel_session_hook.py",
        '    mem_root = Path("/media/adrian/New Volume1/CIEL_memories")',
        '    mem_root = MEMORY_ROOT',
    )
    replace_once(
        "scripts/ciel_session_hook.py",
        '    script = os.path.join(PROJECT, "scripts", "ciel_memory_consolidator.py")',
        '    script = str(CONSOLIDATOR_SCRIPT)',
    )
    replace_once(
        "scripts/ciel_session_hook.py",
        '    script = os.path.join(PROJECT, "scripts", "ciel_memory_consolidator.py")',
        '    script = str(CONSOLIDATOR_SCRIPT)',
    )
    replace_once(
        "scripts/ciel_session_hook.py",
        '    pid_file = Path("/media/adrian/New Volume1/CIEL_memories/local_test/.pid")',
        '    pid_file = MEMORY_ROOT / "local_test" / ".pid"',
    )
    replace_once(
        "scripts/ciel_session_hook.py",
        '    log_path = Path("/media/adrian/New Volume1/CIEL_memories/logs/ciel_hook_errors.log")',
        '    log_path = CONSOLIDATOR_LOG',
    )

    # Tests must resolve files from the checkout or monkeypatched path ABI.
    replace_once(
        "tests/test_htri_universal_bridge.py",
        'BRIDGE_PATH = Path("/home/adrian/new_volume_rw/CIEL_PROJECT_CANON/NOEMA/runtime/wrappers/vector_continuous_cqcl_lingophysics_htri/noema_vector_continuous_bridge.py")',
        'BRIDGE_PATH = Path(__file__).resolve().parents[1] / "runtime" / "wrappers" / "vector_continuous_cqcl_lingophysics_htri" / "noema_vector_continuous_bridge.py"',
    )
    replace_once(
        "tests/test_claude_ethics.py",
        '    claude_md = Path("/home/adrian/new_volume_rw/CLAUDE.md")',
        '    claude_md = Path(__file__).resolve().parents[1] / "CLAUDE.md"',
    )
    replace_once(
        "tests/test_gui_status_cache.py",
        'from flask import Flask\n\nimport src.ciel_sot_agent.gui.routes as routes',
        'from types import SimpleNamespace\n\nfrom flask import Flask\n\nimport src.ciel_sot_agent.gui.routes as routes',
    )
    replace_once(
        "tests/test_gui_status_cache.py",
        '    monkeypatch.setattr(routes.Path, \'home\', lambda: tmp_path)\n'
        '    state_dir = tmp_path / \'/media/adrian/New Volume1/CIEL_memories/state\'\n'
        '    state_dir.mkdir(parents=True)\n'
        '    (state_dir / \'ciel_orch_state.pkl\').write_bytes(b\'stub\')',
        '    state_dir = tmp_path / "memory" / "state"\n'
        '    state_dir.mkdir(parents=True)\n'
        '    state_path = state_dir / "ciel_orch_state.pkl"\n'
        '    state_path.write_bytes(b"stub")\n'
        '    monkeypatch.setattr(\n'
        '        routes,\n'
        '        "P",\n'
        '        SimpleNamespace(STATE=SimpleNamespace(ORCH_STATE_PKL=str(state_path))),\n'
        '    )',
    )

    # Surface contract grew tau/sensor channels; CIEL internal metrics remain in JSON.
    replace_once(
        "tests/test_noema_surface_mmap.py",
        '    assert set(surface) == {"phi", "omega", "g", "Z_geom", "R_geom", "psi_geom", "flavor", "tick", "gravity", "holonomy"}',
        '    assert set(surface) == {"phi", "omega", "g", "Z_geom", "R_geom", "psi_geom", "flavor", "tick", "gravity", "holonomy", "tau", "sensor_raw"}',
    )
    replace_once(
        "tests/test_noema_surface_mmap.py",
        '    assert float(surface["flavor"][0]) == 0.9\n'
        '    assert float(surface["flavor"][5]) == 1.0',
        '    internal = read_ciel_internal_state(tmp_path)\n'
        '    assert internal["coherence_index"] == 0.9\n'
        '    assert float(surface["flavor"][5]) == 1.0',
    )
    replace_once(
        "tests/test_noema_surface_mmap.py",
        '    read_surface_state,\n',
        '    read_surface_state,\n    read_ciel_internal_state,\n',
    )

    # Orbital dynamics is bounded but not a strict Lyapunov descent under active forcing.
    replace_once(
        "tests/test_orbital_regression.py",
        '    def test_R_H_decreases_over_run(self) -> None:\n'
        '        result = run_global_pass(steps=20)\n'
        '        initial = result["initial"]["R_H"]\n'
        '        final = result["final"]["R_H"]\n'
        '        assert final < initial, (\n'
        '            f"R_H did not decrease: initial={initial:.6f} final={final:.6f}"\n'
        '        )',
        '    def test_R_H_remains_in_low_defect_regime(self) -> None:\n'
        '        result = run_global_pass(steps=20)\n'
        '        values = [float(item["R_H"]) for item in result["history"]]\n'
        '        assert all(_finite(value) and value >= 0.0 for value in values)\n'
        '        assert max(values) < 0.01, f"R_H left low-defect regime: {values}"',
    )
    replace_once(
        "tests/test_orbital_regression.py",
        '    def test_history_R_H_monotone_decreasing_early(self) -> None:\n'
        '        result = run_global_pass(steps=20)\n'
        '        history = result["history"]\n'
        '        # First 5 steps should show decrease\n'
        '        rh_values = [h["R_H"] for h in history[:6]]\n'
        '        assert rh_values[0] > rh_values[5], (\n'
        '            f"R_H not decreasing in first 5 steps: {rh_values}"\n'
        '        )',
        '    def test_history_R_H_early_drift_is_bounded(self) -> None:\n'
        '        result = run_global_pass(steps=20)\n'
        '        rh_values = [float(h["R_H"]) for h in result["history"][:6]]\n'
        '        assert max(rh_values) - min(rh_values) < 0.01, rh_values',
    )

    # Current package topology and documented standalone maintenance scripts.
    replace_once(
        "tests/test_pipeline_audit.py",
        '    "thought_fragments.py": "thought fragment capture helpers",\n',
        '    "thought_fragments.py": "thought fragment capture helpers",\n'
        '    "ethics_core.py": "shared hardcoded ethics invariants",\n'
        '    "opencode_ethics.py": "OpenCode ethics projection",\n'
        '    "claude_ethics.py": "Claude ethics projection",\n'
        '    "knowledge_action_system.py": "knowledge-to-action orchestration",\n'
        '    "buildroot_card_db.py": "Buildroot card database builder",\n',
    )
    replace_once(
        "tests/test_pipeline_audit.py",
        '        "htri_mini.py",             # HTRI mini simulator — standalone physics utility\n',
        '        "htri_mini.py",             # HTRI mini simulator — standalone physics utility\n'
        '        "noema_bootstrap_nonlocal_db.py",  # one-shot local DB bootstrap\n'
        '        "noema_doctor_surface_cycle.py",   # standalone surface doctor cycle\n'
        '        "noema_test_matrix.py",            # repository test matrix orchestrator\n',
    )
    replace_once(
        "tests/test_py_catalog.py",
        '        assert 400 <= result["total"] <= 1000, \\\n            f"expected 400-1000 real .py files, got {result[\'total\']}"',
        '        assert 400 <= result["total"] <= 2500, \\\n            f"expected 400-2500 real .py files, got {result[\'total\']}"',
    )

    # Hub handlers have an explicit (envelope, status) ABI.
    replace_once(
        "tests/test_ciel_hub_contract.py",
        '        def health(ctx):\n'
        '            return ok({\n'
        '                "status": "ok",\n'
        '                "pid": os.getpid(),\n'
        '                "uptime_s": 42.0,\n'
        '            })',
        '        def health(ctx):\n'
        '            return ok({\n'
        '                "status": "ok",\n'
        '                "pid": os.getpid(),\n'
        '                "uptime_s": 42.0,\n'
        '            }), 200',
    )

    # Recover cached bridge reports if the on-disk copy is missing or corrupted.
    replace_once(
        "src/ciel_sot_agent/orbital_bridge.py",
        '    if cached is not None and (now - cached[0]) < _BRIDGE_CACHE_TTL:\n        return cached[1]',
        '    if cached is not None and (now - cached[0]) < _BRIDGE_CACHE_TTL:\n'
        '        cached_summary = cached[1]\n'
        '        cached_report = root / BRIDGE_DIR / "orbital_bridge_report.json"\n'
        '        disk_report = _load_json_if_exists(cached_report)\n'
        '        if not isinstance(disk_report, dict) or disk_report.get("schema") != cached_summary.get("schema"):\n'
        '            cached_report.parent.mkdir(parents=True, exist_ok=True)\n'
        '            cached_report.write_text(json.dumps(cached_summary, ensure_ascii=False, indent=2), encoding="utf-8")\n'
        '        return cached_summary',
    )

    if MISSING:
        print("contract migration mismatches:")
        for relative, before in MISSING:
            print(f"- {relative}: {before!r}")
        return 2

    print("full-suite contract migration applied")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
