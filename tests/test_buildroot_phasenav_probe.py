from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from src.ciel_sot_agent import buildroot_phasenav_probe as probe


def _make_buildroot_tree(root: Path) -> None:
    for rel in [
        "boot",
        "linux",
        "toolchain",
        "system",
        "fs",
        "package/alpha",
        "package/beta",
    ]:
        (root / rel).mkdir(parents=True, exist_ok=True)
    (root / "Config.in").write_text("# root\n", encoding="utf-8")
    (root / "package" / "Config.in").write_text(
        "\n".join(
            [
                'menu "Target packages"',
                'source "package/alpha/Config.in"',
                'source "package/beta/Config.in"',
                'endmenu',
            ]
        ),
        encoding="utf-8",
    )
    (root / "package" / "alpha" / "Config.in").write_text("config BR2_ALPHA\n", encoding="utf-8")
    (root / "package" / "beta" / "Config.in").write_text("config BR2_BETA\n", encoding="utf-8")
    (root / "toolchain" / "Config.in").write_text("# toolchain\n", encoding="utf-8")
    (root / "linux" / "README").write_text("linux readme\n", encoding="utf-8")
    (root / "system" / "defconfig").write_text("CONFIG_RT=y\n", encoding="utf-8")


def test_summarize_buildroot_reports_counts(tmp_path: Path) -> None:
    _make_buildroot_tree(tmp_path)

    snapshot = probe.summarize_buildroot(tmp_path)

    assert snapshot["root"] == str(tmp_path)
    assert snapshot["package_dir_count"] == 2
    assert "boot" in snapshot["top_level_dirs"]
    assert snapshot["counts"]["config_in"] >= 3
    assert snapshot["counts"]["defconfig"] >= 1
    assert snapshot["menu_tree"]["menu_count"] >= 1
    assert snapshot["menu_tree"]["source_count"] >= 2
    assert snapshot["semantic_subtrees"]
    assert snapshot["rt_surface"]["boot"] == "present"
    assert snapshot["rt_surface"]["kernel"] == "present"


def test_probe_uses_system_map_and_immune_surface(tmp_path: Path, monkeypatch) -> None:
    _make_buildroot_tree(tmp_path)

    system_map_path = tmp_path / "system_map_v2.json"
    system_map_path.write_text(
        json.dumps(
            {
                "schema": "ciel-test/system-map/v1",
                "systems": [
                    {
                        "id": "noema:nonlocal_db:000_ROOT",
                        "name": "NOEMA root card",
                        "ordinal": "990",
                        "ordinal_name": "NOEMA root card",
                        "type": "data",
                        "satellites": [{"id": "sat:boot"}],
                    },
                    {
                        "id": "daemon:linux_sensor",
                        "name": "Linux Sensor daemon",
                        "ordinal": "009",
                        "ordinal_name": "Linux Sensor daemon",
                        "type": "daemon",
                    },
                    {
                        "id": "noema:workben:37:workben-system",
                        "name": "Workben SYSTEM",
                        "ordinal": "028",
                        "ordinal_name": "Workben SYSTEM",
                        "type": "meta_skill",
                    },
                    {
                        "id": "noema:workben:43:workben-linux",
                        "name": "Workben LINUX",
                        "ordinal": "034",
                        "ordinal_name": "workben-linux",
                        "type": "meta_skill",
                    },
                    {
                        "id": "noema:workben:46:workben-dev",
                        "name": "Workben DEV",
                        "ordinal": "037",
                        "ordinal_name": "workben-dev",
                        "type": "meta_skill",
                    },
                ],
            }
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(probe, "DEFAULT_SYSTEM_MAP_CANDIDATES", (system_map_path,))
    monkeypatch.setattr(
        probe,
        "_read_immune_surface_state",
        lambda: {
            "exists": True,
            "root": "/dev/shm/ciel_noema",
            "coherence_index": 0.83,
            "soul_invariant": 0.72,
            "ethical_score": 0.91,
            "closure_penalty": 0.18,
            "operating_mode": "safe",
            "noema_tick": 123,
        },
    )

    report = probe.run_buildroot_probe(tmp_path, use_gguf=False)

    assert report["backend_mode"] == "deterministic"
    assert report["buildroot_snapshot"]["system_map"]["path"] == str(system_map_path)
    assert report["buildroot_snapshot"]["immune_surface"]["exists"] is True
    assert "IMMUNE SURFACE" in report["prompt"]
    assert "SYSTEM MAP" in report["prompt"]
    assert report["parsed_ir"]["system_map_alignment"]["record_count"] == 5
    assert report["parsed_ir"]["system_map_alignment"]["anchor_count"] >= 2
    assert report["parsed_ir"]["buildroot_characterization"]["menu_count"] >= 1
    assert report["parsed_ir"]["buildroot_characterization"]["semantic_subtree_count"] >= 1
    assert report["parsed_ir"]["buildroot_characterization"]["workben_alignment_count"] >= 3
    assert report["quality_breakdown"]["surface_mode"] == "safe"

    linux_nodes = [entry for entry in report["parsed_ir"]["subsystems"] if entry["name"] == "linux"]
    assert linux_nodes and linux_nodes[0]["system_map_matches"], "linux should align to the system map"
    package_nodes = [entry for entry in report["parsed_ir"]["subsystems"] if entry["kind"] == "menu"]
    assert package_nodes, "menu subtree entries should be present"
    workben_alignment = report["parsed_ir"]["system_map_alignment"]["workben_alignment"]
    assert {entry["target"] for entry in workben_alignment} == {
        "workben-system",
        "workben-linux",
        "workben-dev",
    }
    assert all(entry["matched"] for entry in workben_alignment)


def test_probe_uses_gguf_backend_when_available(tmp_path: Path) -> None:
    _make_buildroot_tree(tmp_path)
    model_path = tmp_path / "probe.gguf"
    model_path.write_bytes(b"fake-gguf-model")

    class FakeBackend:
        def generate_reply(self, messages, context):
            assert messages[0]["role"] == "user"
            assert "Buildroot" in messages[0]["content"]
            assert "buildroot_snapshot" in context
            return json.dumps(
                {
                    "system_name": "ResEnta RT",
                    "translation_mode": "PhaseNav",
                    "buildroot_characterization": {"package_dir_count": 2},
                    "subsystems": [{"name": "linux"}],
                    "boot_chain": ["boot", "linux"],
                    "continuity_plan": ["keep continuity"],
                    "rt_constraints": ["bound latency"],
                    "memory_plan": ["budget memory"],
                    "ipc_plan": ["structured messages"],
                    "risks": ["packaging drift"],
                    "next_steps": ["generate skeleton"],
                    "confidence": 0.94,
                }
            )

    report = probe.run_buildroot_probe(
        tmp_path,
        model_path=model_path,
        use_gguf=True,
        backend_factory=lambda **kwargs: FakeBackend(),
    )

    assert report["backend_mode"] == "gguf"
    assert report["model_path"] == str(model_path)
    assert report["parsed_ir"]["system_name"] == "ResEnta RT"
    assert report["quality_breakdown"]["model_confidence"] == 0.94


def test_phase_benchmark_compares_deterministic_and_gguf(tmp_path: Path) -> None:
    _make_buildroot_tree(tmp_path)
    model_path = tmp_path / "benchmark.gguf"
    model_path.write_bytes(b"benchmark-gguf-model")

    class FakeBackend:
        def generate_reply(self, messages, context):
            return json.dumps(
                {
                    "system_name": "ResEnta RT",
                    "translation_mode": "PhaseNav",
                    "buildroot_characterization": {
                        "package_dir_count": 2,
                        "menu_count": 1,
                    },
                    "subsystems": [{"name": "linux", "kind": "dir"}],
                    "boot_chain": ["boot", "linux"],
                    "continuity_plan": ["keep continuity"],
                    "rt_constraints": ["bound latency"],
                    "memory_plan": ["budget memory"],
                    "ipc_plan": ["structured messages"],
                    "risks": ["packaging drift"],
                    "next_steps": ["generate skeleton"],
                    "confidence": 0.96,
                }
            )

    report = probe.run_buildroot_phase_benchmark(
        tmp_path,
        model_path=model_path,
        use_gguf=True,
        runs=3,
        backend_factory=lambda **kwargs: FakeBackend(),
    )

    assert report["schema"] == probe.BENCH_SCHEMA_V01
    assert report["deterministic"]["backend_mode"] == "deterministic"
    assert report["deterministic"]["runs"] == 3
    assert report["gguf"]["runs"] == 3
    assert report["gguf"]["samples"]
    assert report["gguf"]["median_elapsed_ms"] >= 0.0
    assert report["gguf"]["p95_elapsed_ms"] >= report["gguf"]["median_elapsed_ms"]
    assert report["gguf"]["mean_quality_score"] >= report["deterministic"]["mean_quality_score"]
    assert report["winner"] == "gguf"
    assert report["quality_delta"] is not None


def test_probe_help_includes_benchmark_flag() -> None:
    src = str(Path(__file__).resolve().parents[1] / "src")
    env = {**os.environ, "PYTHONPATH": src}
    result = subprocess.run(
        [sys.executable, "-m", "ciel_sot_agent", "buildroot-phase-probe", "--help"],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )
    assert result.returncode == 0
    assert "--benchmark" in result.stdout
    assert "--benchmark-runs" in result.stdout
