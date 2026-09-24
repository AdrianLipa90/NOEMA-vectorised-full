from __future__ import annotations

import hashlib
import os
import importlib.util
import json
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

PATCH = Path(__file__).resolve().parents[1]


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def v36(offset: float = 0.0) -> bytes:
    return struct.pack("<36d", *[offset + i / 100.0 for i in range(36)])


def jbytes(x) -> bytes:
    return (json.dumps(x, sort_keys=True, separators=(",", ":")) + "\n").encode()


class FeedbackTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.feedback = load(PATCH / "scripts/noema_aux_feedback_lane.py", "feedback_lane")

    def tearDown(self):
        self.tmp.cleanup()

    def test_lossless_feedback_and_aux_ownership(self):
        phi = v36(1.0)
        aux = v36(2.0)
        (self.root / "phi").write_bytes(phi)
        (self.root / "aux_phi").write_bytes(aux)
        receipt = self.feedback.publish_once(self.root)
        self.assertEqual((self.root / "aux_feedback_phi").read_bytes(), phi)
        self.assertEqual((self.root / "aux_phi").read_bytes(), aux)
        self.assertTrue(receipt["lossless_identity"])
        self.assertFalse(receipt["aux_phi_overwritten"])
        self.assertEqual(receipt["input_v36_sha256"], hashlib.sha256(phi).hexdigest())
        self.assertEqual(receipt["aux_input_v36_sha256"], hashlib.sha256(aux).hexdigest())

    def test_missing_aux_never_seeds(self):
        (self.root / "phi").write_bytes(v36())
        with self.assertRaises(FileNotFoundError):
            self.feedback.publish_once(self.root)
        self.assertFalse((self.root / "aux_phi").exists())
        self.assertFalse((self.root / "aux_feedback_phi").exists())

    def test_guard_accepts_fresh_exact_lane(self):
        phi = v36(0.4)
        aux = v36(0.8)
        (self.root / "phi").write_bytes(phi)
        (self.root / "aux_phi").write_bytes(aux)
        self.feedback.publish_once(self.root)
        (self.root / "ciel_binding_status").write_text("ACTIVE\n")
        (self.root / "session").mkdir()
        (self.root / "session/startpoint.json").write_text("{}\n")
        (self.root / "session/system_message.txt").write_text("ok\n")
        proc = subprocess.run([sys.executable, str(PATCH / "scripts/noema_aux_tether_guard.py"), "--root", str(self.root)], text=True, capture_output=True)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        row = json.loads(proc.stdout)
        self.assertEqual(row["tether_status"], "ACTIVE")
        self.assertTrue(row["receipt_verified"])

    def test_guard_rejects_modified_feedback(self):
        (self.root / "phi").write_bytes(v36(0.4))
        (self.root / "aux_phi").write_bytes(v36(0.8))
        self.feedback.publish_once(self.root)
        (self.root / "aux_feedback_phi").write_bytes(v36(9.0))
        (self.root / "ciel_binding_status").write_text("ACTIVE\n")
        (self.root / "session").mkdir()
        (self.root / "session/startpoint.json").write_text("{}\n")
        (self.root / "session/system_message.txt").write_text("ok\n")
        proc = subprocess.run([sys.executable, str(PATCH / "scripts/noema_aux_tether_guard.py"), "--root", str(self.root)], text=True, capture_output=True)
        self.assertEqual(proc.returncode, 23)
        self.assertIn("AUX_FEEDBACK_NOT_LOSSLESS", proc.stdout)


class BootTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)
        self.repo = self.base / "repo"
        (self.repo / "scripts").mkdir(parents=True)
        (self.repo / "integration/surface_persistence/v0_2").mkdir(parents=True)
        for name in ("noema_session_boot.py", "noema_aux_feedback_lane.py", "noema_aux_tether_guard.py", "noema_runtime_source_guard.py", "dev_shm_startpoint.py"):
            shutil.copy2(PATCH / "scripts" / name, self.repo / "scripts" / name)
        fixture = """from pathlib import Path\nimport hashlib, json, time\nclass PersistentSurfaceSync:\n    def __init__(self, library_root, surface_root, fallback_root):\n        self.library_root=Path(library_root); self.surface=Path(surface_root)\n        self.store=self.library_root/'surface_store'; self.canonical=self.store/'canonical'; self.manifest_path=self.store/'manifest.json'\n    def project(self):\n        m=json.loads(self.manifest_path.read_text())\n        self.surface.mkdir(parents=True,exist_ok=True)\n        for rel,meta in m['files'].items():\n            raw=(self.canonical/rel).read_bytes()\n            if hashlib.sha256(raw).hexdigest()!=meta['sha256']: raise RuntimeError('canonical hash mismatch')\n            p=self.surface/rel; p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(raw)\n        return {'op':'PROJECT','generation':m['generation'],'timestamp_ns':time.time_ns()}\n"""
        (self.repo / "integration/surface_persistence/v0_2/surface_sync.py").write_text(fixture)
        self.library = self.base / "library"
        self.runtime = self.base / "runtime"
        self.surface = self.base / "surface"
        self.pin_file = self.base / "runtime_pin.json"
        self.seed_runtime_sources()
        (self.repo / "contracts").mkdir(parents=True, exist_ok=True)
        shutil.copy2(self.pin_file, self.repo / "contracts/NOEMA_RUNTIME_SOURCE_PIN_V1.json")

    def tearDown(self):
        self.tmp.cleanup()

    def seed_runtime_sources(self):
        rs = self.library / "runtime_sources"
        rs.mkdir(parents=True)
        mem_zip = rs / "mem.zip"
        ling_zip = rs / "ling.zip"
        mem_member = "runtime/unified_memory.py"
        ling_member = "runtime/sentence_equation.py"
        mem_raw = b"ORIGINAL_MEMORY_MONOLITH_FIXTURE\n"
        ling_raw = b"ORIGINAL_SENTENCE_EQUATION_FIXTURE\n"
        with zipfile.ZipFile(mem_zip, "w") as zf:
            zf.writestr(mem_member, mem_raw)
        with zipfile.ZipFile(ling_zip, "w") as zf:
            zf.writestr(ling_member, ling_raw)
        pin = {
            "schema":"noema.runtime-source-pin/v1",
            "sources":{
                "apocalypos_memory_monolith":{
                    "required_for_boot":True,
                    "archive_sha256":hashlib.sha256(mem_zip.read_bytes()).hexdigest(),
                    "member_path":mem_member,
                    "member_sha256":hashlib.sha256(mem_raw).hexdigest(),
                },
                "cielingo_sentence_equation_v0_12":{
                    "required_for_boot":True,
                    "archive_sha256":hashlib.sha256(ling_zip.read_bytes()).hexdigest(),
                    "member_path":ling_member,
                    "member_sha256":hashlib.sha256(ling_raw).hexdigest(),
                },
                "identity_crystal_v17":{
                    "required_for_boot":False,
                    "sha256":"ff437108fa768054f7590e054d872d24154c340d12de3a542c4838fbd588314f",
                },
            },
        }
        self.pin_file.write_text(json.dumps(pin))
        (rs / "MOUNT.json").write_text(json.dumps({
            "schema":"noema.runtime-mount/v1",
            "sources":{
                "apocalypos_memory_monolith":{"archive_path":"runtime_sources/mem.zip"},
                "cielingo_sentence_equation_v0_12":{"archive_path":"runtime_sources/ling.zip"},
            },
        }))

    def seed_store(self):
        canonical = self.library / "surface_store/canonical"
        canonical.mkdir(parents=True)
        files = {
            "current_memory.json": jbytes({"current_memory": {"head": "verified"}}),
            "current_task.json": jbytes({"current_task": "repair whole system"}),
            "active_path.json": jbytes({"active_path": "runtime_boot_repair"}),
            "closed_topics.json": jbytes({"closed_topics": []}),
            "timeline_head.json": jbytes({"timeline_head": "t0"}),
            "provenance.json": jbytes({"provenance": ["fixture"]}),
            "receipts/latest.json": jbytes({"status": "PASS"}),
            "aux_phi": v36(1.5),
        }
        meta={}
        for rel,raw in files.items():
            p=canonical/rel; p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(raw)
            meta[rel]={"sha256":hashlib.sha256(raw).hexdigest(),"size":len(raw)}
        (self.library / "surface_store/manifest.json").write_text(json.dumps({"schema":"noema.persistent-surface-store/v2","generation":3,"files":meta}))

    def run_boot(self):
        return subprocess.run([
            sys.executable, str(self.repo / "scripts/noema_session_boot.py"),
            "--repo-root", str(self.repo), "--library-root", str(self.library),
            "--runtime-root", str(self.runtime), "--surface-root", str(self.surface),
            "--pin-file", str(self.pin_file),
        ], text=True, capture_output=True)

    def test_full_boot_active_when_live_producer_exists(self):
        self.seed_store()
        self.surface.mkdir(parents=True)
        phi=v36(2.5)
        (self.surface/"phi").write_bytes(phi)
        (self.surface/"ciel_binding_status").write_text("ACTIVE\n")
        proc=self.run_boot()
        self.assertEqual(proc.returncode,0,proc.stdout+proc.stderr)
        row=json.loads(proc.stdout)
        self.assertEqual(row["tether_status"],"ACTIVE")
        self.assertEqual((self.surface/"aux_feedback_phi").read_bytes(),phi)
        self.assertEqual((self.surface/"aux_phi").read_bytes(),v36(1.5))
        self.assertTrue((self.surface/"session/startpoint.json").is_file())

    def test_missing_persistent_store_blocks_without_autoseed(self):
        proc=self.run_boot()
        self.assertEqual(proc.returncode,23)
        self.assertIn("BLOCKED_LIBRARY_STORE_MISSING",proc.stdout)
        self.assertFalse((self.library/"surface_store/manifest.json").exists())

    def test_missing_live_phi_blocks_and_does_not_fake_it(self):
        self.seed_store()
        self.surface.mkdir(parents=True)
        (self.surface/"ciel_binding_status").write_text("ACTIVE\n")
        proc=self.run_boot()
        self.assertEqual(proc.returncode,23)
        self.assertIn("BLOCKED_LIVE_FEEDBACK",proc.stdout)
        self.assertFalse((self.surface/"phi").exists())
        self.assertFalse((self.surface/"aux_feedback_phi").exists())

    def test_session_boot_never_captures_volatile_changes(self):
        self.seed_store()
        self.surface.mkdir(parents=True)
        (self.surface/"current_task.json").write_text('{"current_task":"malicious volatile drift"}\n')
        (self.surface/"phi").write_bytes(v36(2.5))
        (self.surface/"ciel_binding_status").write_text("ACTIVE\n")
        proc=self.run_boot()
        self.assertEqual(proc.returncode,0,proc.stdout+proc.stderr)
        persistent=json.loads((self.library/"surface_store/canonical/current_task.json").read_text())
        projected=json.loads((self.surface/"current_task.json").read_text())
        self.assertEqual(persistent["current_task"],"repair whole system")
        self.assertEqual(projected["current_task"],"repair whole system")

    def test_direct_startpoint_runs_library_prestart_automatically(self):
        self.seed_store()
        self.surface.mkdir(parents=True)
        (self.surface/"phi").write_bytes(v36(2.5))
        (self.surface/"ciel_binding_status").write_text("ACTIVE\n")
        env=dict(os.environ)
        env["NOEMA_LIBRARY_ROOT"]=str(self.library)
        env["NOEMA_RUNTIME_ROOT"]=str(self.runtime)
        proc=subprocess.run([sys.executable,str(self.repo/"scripts/dev_shm_startpoint.py"),"--root",str(self.surface),"--codex-hook"],text=True,capture_output=True,env=env)
        self.assertEqual(proc.returncode,0,proc.stdout+proc.stderr)
        row=json.loads(proc.stdout)
        self.assertTrue(row["continue"])
        self.assertEqual(row["hookSpecificOutput"]["surface_status"],"VERIFIED")
        self.assertTrue((self.surface/"aux_feedback_phi").is_file())

    def test_runtime_source_hash_mismatch_blocks_before_projection(self):
        self.seed_store()
        (self.library/"runtime_sources/mem.zip").write_bytes(b"corrupt")
        proc=self.run_boot()
        self.assertEqual(proc.returncode,23)
        self.assertIn("RUNTIME_SOURCE_HASH_MISMATCH",proc.stdout)
        self.assertFalse((self.surface/"current_memory.json").exists())


class PinTests(unittest.TestCase):
    def test_runtime_source_pins(self):
        p=json.loads((PATCH/"contracts/NOEMA_RUNTIME_SOURCE_PIN_V1.json").read_text())
        self.assertTrue(p["policy"]["activate_only_after_sha256_match"])
        self.assertEqual(p["policy"]["candidate_fallback"],"DENY")
        self.assertEqual(p["sources"]["identity_crystal_v17"]["sha256"],"ff437108fa768054f7590e054d872d24154c340d12de3a542c4838fbd588314f")
        self.assertTrue(p["sources"]["identity_crystal_v17"]["test_sealed"])


if __name__ == "__main__":
    unittest.main()
