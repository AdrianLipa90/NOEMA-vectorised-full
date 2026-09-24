"""Local NOEMA Surface command-prompt layer.

This is a local execution surface. It is not NOEMA SoT, not packet ACK,
not memory writeback, and not CURRENT update.
"""

from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


from dataclasses import asdict, dataclass, field
from pathlib import Path
import ast
import fnmatch
import hashlib
import json
import os
import subprocess
import sys
import zipfile
from typing import Any, Iterable


@dataclass
class NoemaSurfaceResult:
    command: str
    ok: bool
    payload: dict[str, Any] = field(default_factory=dict)
    issues: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class NoemaSurface:
    """Local command-prompt-like surface over a repository root.

    Boundary note:
        This surface is a local bounded proxy shell. It may read/write files
        under its configured root and run explicitly exposed commands. It is
        not a NOEMA Source of Truth, not an ACK channel, and not a CURRENT
        pointer updater.
    """

    GLOBAL_GADGETS = (
        "ls",
        "read_text",
        "write_text",
        "read_json",
        "write_json",
        "sha256_file",
        "zip_paths",
        "zip_test",
        "compileall",
        "install_global_gadget",
        "list_global_gadgets",
        "audit_global_gadgets",
        "canonize_local_sot_agent",
        "discover_local_sot_agent",
        "verify_local_sot_agent",
        "install_local_sot_access_standard",
        "verify_local_sot_access_standard",
        "check_write_permission",
        "ast_imports",
        "assert_router_boundary",
        "run_pytest",
    )

    def __init__(self, root: str | Path):
        self.root = Path(root).resolve()

    def path(self, relative_path: str | Path) -> Path:
        target = (self.root / relative_path).resolve()
        if target != self.root and self.root not in target.parents:
            raise ValueError(f"path escapes NOEMA surface root: {relative_path}")
        return target

    def command_registry(self) -> NoemaSurfaceResult:
        return NoemaSurfaceResult(
            "command_registry",
            True,
            payload={
                "surface_root": str(self.root),
                "commands": list(self.GLOBAL_GADGETS),
                "outside_sot": True,
                "sot_available": False,
                "updates_current": False,
                "memory_writeback_performed": False,
            },
        )


    @property
    def global_gadget_registry_path(self) -> Path:
        return self.path("state/noema_surface/GLOBAL_GADGET_REGISTRY.json")

    def install_global_gadget(
        self,
        name: str,
        *,
        description: str,
        commands: Iterable[str] | None = None,
        version: str = "v0_1",
        scope: str = "repo_global_noema_surface",
    ) -> NoemaSurfaceResult:
        """Register a NOEMA Surface gadget for repo-global local use.

        Boundary: this writes a local registry entry only. It is not NOEMA SoT,
        not account-wide GPT infrastructure, not ACK, and not CURRENT update.
        """
        if not name or any(ch in name for ch in "/\\:"):
            return NoemaSurfaceResult("install_global_gadget", False, issues=[f"invalid gadget name: {name!r}"])
        registry_path = self.global_gadget_registry_path
        if registry_path.exists():
            try:
                registry = json.loads(registry_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/cielingo_core/noema_surface/command_prompt.py:115 quiet except scope=NoemaSurface.install_global_gadget reason=return NoemaSurfaceResult(\"install_global_gadget\", False, issues=[f\"invalid registry JSON: {exc}\"])")
                return NoemaSurfaceResult("install_global_gadget", False, issues=[f"invalid registry JSON: {exc}"])
        else:
            registry = {
                "schema": "NOEMA_SURFACE_GLOBAL_GADGET_REGISTRY_V0_1",
                "outside_sot": True,
                "sot_available": False,
                "updates_current": False,
                "memory_writeback_performed": False,
                "account_global_claimed": False,
                "gadgets": {},
            }
        entry = {
            "name": name,
            "description": description,
            "commands": sorted(set(commands or [name])),
            "version": version,
            "scope": scope,
            "outside_sot": True,
            "sot_available": False,
            "updates_current": False,
            "canon_allowed": False,
        }
        entry_text = json.dumps(entry, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        entry["entry_sha256"] = hashlib.sha256(entry_text.encode("utf-8")).hexdigest()
        registry.setdefault("gadgets", {})[name] = entry
        registry["gadget_count"] = len(registry["gadgets"])
        registry_text = json.dumps(
            {k: v for k, v in registry.items() if k != "registry_sha256"},
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        registry["registry_sha256"] = hashlib.sha256(registry_text.encode("utf-8")).hexdigest()
        registry_path.parent.mkdir(parents=True, exist_ok=True)
        registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        gadget_path = self.path(f"state/noema_surface/global_gadgets/{name}.json")
        gadget_path.parent.mkdir(parents=True, exist_ok=True)
        gadget_path.write_text(json.dumps(entry, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return NoemaSurfaceResult(
            "install_global_gadget",
            True,
            payload={
                "name": name,
                "registry": str(registry_path.relative_to(self.root)),
                "gadget_path": str(gadget_path.relative_to(self.root)),
                "entry_sha256": entry["entry_sha256"],
                "registry_sha256": registry["registry_sha256"],
                "outside_sot": True,
            },
        )

    def list_global_gadgets(self) -> NoemaSurfaceResult:
        registry_path = self.global_gadget_registry_path
        if not registry_path.exists():
            return NoemaSurfaceResult(
                "list_global_gadgets",
                True,
                payload={
                    "registry_exists": False,
                    "gadgets": [],
                    "outside_sot": True,
                    "updates_current": False,
                },
            )
        result = self.read_json(registry_path.relative_to(self.root))
        if not result.ok:
            return NoemaSurfaceResult("list_global_gadgets", False, issues=result.issues)
        registry = result.payload["data"]
        return NoemaSurfaceResult(
            "list_global_gadgets",
            True,
            payload={
                "registry_exists": True,
                "gadget_count": registry.get("gadget_count", len(registry.get("gadgets", {}))),
                "gadgets": sorted(registry.get("gadgets", {}).keys()),
                "registry_sha256": registry.get("registry_sha256"),
                "outside_sot": registry.get("outside_sot", True),
                "updates_current": registry.get("updates_current", False),
            },
        )

    def audit_global_gadgets(self) -> NoemaSurfaceResult:
        listed = self.list_global_gadgets()
        if not listed.ok:
            return NoemaSurfaceResult("audit_global_gadgets", False, issues=listed.issues)
        issues: list[str] = []
        registry_path = self.global_gadget_registry_path
        if not registry_path.exists():
            issues.append("missing GLOBAL_GADGET_REGISTRY.json")
            return NoemaSurfaceResult("audit_global_gadgets", False, payload=listed.payload, issues=issues)
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
        for key in ("outside_sot", "sot_available", "updates_current", "memory_writeback_performed", "account_global_claimed"):
            expected = False if key in {"sot_available", "updates_current", "memory_writeback_performed", "account_global_claimed"} else True
            if registry.get(key) is not expected:
                issues.append(f"registry boundary mismatch: {key}={registry.get(key)!r}, expected {expected!r}")
        for name, entry in registry.get("gadgets", {}).items():
            if entry.get("outside_sot") is not True:
                issues.append(f"gadget {name} is not marked outside_sot")
            if entry.get("updates_current") is not False:
                issues.append(f"gadget {name} may update CURRENT")
            if entry.get("canon_allowed") is not False:
                issues.append(f"gadget {name} may canonize")
            if not entry.get("entry_sha256"):
                issues.append(f"gadget {name} missing entry_sha256")
        return NoemaSurfaceResult(
            "audit_global_gadgets",
            not issues,
            payload={
                "gadget_count": len(registry.get("gadgets", {})),
                "gadgets": sorted(registry.get("gadgets", {}).keys()),
                "outside_sot": registry.get("outside_sot", True),
                "updates_current": registry.get("updates_current", False),
            },
            issues=issues,
        )


    def canonize_local_sot_agent(self, state: dict[str, Any]) -> NoemaSurfaceResult:
        """Canonize a local SOT_Agent_NoemaSurface state inside this repo only."""
        from cielingo_core.noema_local_sot_agent import LocalSOTAgentNoemaSurface, LocalSOTAgentState
        required = ["agent_id", "selected_branch_id", "selected_artifact_sha256", "validation_status", "pytest_summary", "compileall_ok", "surface_audit_ok", "pseudo_global_status"]
        missing = [key for key in required if key not in state]
        if missing:
            return NoemaSurfaceResult("canonize_local_sot_agent", False, issues=[f"missing fields: {missing}"])
        agent = LocalSOTAgentNoemaSurface(self.root)
        current = agent.canonize(LocalSOTAgentState(**{key: state[key] for key in required}))
        self.install_global_gadget(
            "local_sot_agent_noema_surface",
            description="Local artifact-only SOT_Agent bound to NoemaSurface; outside external SoT.",
            commands=["canonize_local_sot_agent", "discover_local_sot_agent", "verify_local_sot_agent"],
            version="v0_1",
            scope="repo_global_noema_surface_local_canon",
        )
        return NoemaSurfaceResult("canonize_local_sot_agent", True, payload=current)


    def install_local_sot_access_standard(self) -> NoemaSurfaceResult:
        """Install local SOT access standard and permission policy."""
        from cielingo_core.noema_local_sot_agent.access_control import build_default_access_standard
        standard = build_default_access_standard()
        result = self.write_json("state/noema_local_sot_agent/access/ACCESS_STANDARD.noema.json", standard)
        if not result.ok:
            return NoemaSurfaceResult("install_local_sot_access_standard", False, issues=result.issues)
        self.install_global_gadget(
            "local_sot_access_standard",
            description="Local SOT_Agent permission standard: CIELingo edits allowed; non-work-core edits require Adrian ALLOW.",
            commands=["install_local_sot_access_standard", "verify_local_sot_access_standard", "check_write_permission"],
            version="v0_1",
            scope="repo_global_noema_surface_local_permissions",
        )
        return NoemaSurfaceResult("install_local_sot_access_standard", True, payload=standard)

    def verify_local_sot_access_standard(self) -> NoemaSurfaceResult:
        result = self.read_json("state/noema_local_sot_agent/access/ACCESS_STANDARD.noema.json")
        if not result.ok:
            return NoemaSurfaceResult("verify_local_sot_access_standard", False, issues=result.issues)
        standard = result.payload["data"]
        issues: list[str] = []
        if standard.get("schema") != "NOEMA_LOCAL_SOT_AGENT_ACCESS_STANDARD_V0_1":
            issues.append("wrong access standard schema")
        auth = standard.get("authority", {})
        if auth.get("local_sot_write_permission_granted_by_user") is not True:
            issues.append("local SOT write permission is not granted")
        for key in ["external_sot_write_permission_claimed", "user007_disk_write_claimed", "account_global_gpt_claimed"]:
            if auth.get(key) is not False:
                issues.append(f"authority boundary violation: {key}={auth.get(key)!r}")
        rule = standard.get("operational_rule", {})
        if rule.get("non_work_core_edits_require_question") is not True:
            issues.append("non-work-core edits do not require question")
        if not standard.get("standard_sha256"):
            issues.append("missing standard_sha256")
        return NoemaSurfaceResult("verify_local_sot_access_standard", not issues, payload=standard, issues=issues)

    def check_write_permission(self, relative_path: str | Path, allow_grant: dict[str, Any] | None = None) -> NoemaSurfaceResult:
        from cielingo_core.noema_local_sot_agent.access_control import LocalSOTAccessController
        controller = LocalSOTAccessController(self.root)
        decision = controller.can_write(relative_path, allow_grant=allow_grant).to_dict()
        return NoemaSurfaceResult("check_write_permission", decision["ok"], payload=decision, issues=[] if decision["ok"] else [decision["reason"]])

    def discover_local_sot_agent(self) -> NoemaSurfaceResult:
        from cielingo_core.noema_local_sot_agent import LocalSOTAgentNoemaSurface
        agent = LocalSOTAgentNoemaSurface(self.root)
        return NoemaSurfaceResult("discover_local_sot_agent", True, payload=agent.discover())

    def verify_local_sot_agent(self) -> NoemaSurfaceResult:
        from cielingo_core.noema_local_sot_agent import LocalSOTAgentNoemaSurface
        agent = LocalSOTAgentNoemaSurface(self.root)
        verification = agent.verify_current()
        return NoemaSurfaceResult("verify_local_sot_agent", verification.get("ok", False), payload=verification, issues=verification.get("issues", []))

    def ls(self, relative_path: str | Path = ".", *, recursive: bool = False, pattern: str | None = None) -> NoemaSurfaceResult:
        path = self.path(relative_path)
        if not path.exists():
            return NoemaSurfaceResult("ls", False, issues=[f"missing: {relative_path}"])
        if not path.is_dir():
            return NoemaSurfaceResult("ls", False, issues=[f"not a directory: {relative_path}"])

        iterator = path.rglob(pattern or "*") if recursive else path.glob(pattern or "*")
        entries = []
        for item in sorted(iterator):
            entries.append({
                "path": str(item.relative_to(self.root)),
                "type": "dir" if item.is_dir() else "file",
                "size": item.stat().st_size if item.is_file() else None,
            })
        return NoemaSurfaceResult(
            "ls",
            True,
            payload={"root": str(relative_path), "recursive": recursive, "pattern": pattern, "entries": entries},
        )

    def read_text(self, relative_path: str | Path) -> NoemaSurfaceResult:
        path = self.path(relative_path)
        if not path.exists():
            return NoemaSurfaceResult("read_text", False, issues=[f"missing: {relative_path}"])
        return NoemaSurfaceResult("read_text", True, payload={"text": path.read_text(encoding="utf-8")})

    def write_text(self, relative_path: str | Path, text: str) -> NoemaSurfaceResult:
        path = self.path(relative_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return NoemaSurfaceResult("write_text", True, payload={"path": str(relative_path), "bytes": len(text.encode("utf-8"))})

    def read_json(self, relative_path: str | Path) -> NoemaSurfaceResult:
        result = self.read_text(relative_path)
        if not result.ok:
            return result
        try:
            data = json.loads(result.payload["text"])
        except json.JSONDecodeError as exc:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/cielingo_core/noema_surface/command_prompt.py:345 quiet except scope=NoemaSurface.read_json reason=return NoemaSurfaceResult(\"read_json\", False, issues=[f\"invalid JSON: {exc}\"])")
            return NoemaSurfaceResult("read_json", False, issues=[f"invalid JSON: {exc}"])
        return NoemaSurfaceResult("read_json", True, payload={"data": data})

    def write_json(self, relative_path: str | Path, data: Any, *, indent: int = 2) -> NoemaSurfaceResult:
        text = json.dumps(data, ensure_ascii=False, indent=indent, sort_keys=True) + "\n"
        result = self.write_text(relative_path, text)
        return NoemaSurfaceResult("write_json", result.ok, payload=result.payload, issues=result.issues)

    def sha256_file(self, relative_path: str | Path, *, chunk_size: int = 1024 * 1024) -> NoemaSurfaceResult:
        path = self.path(relative_path)
        if not path.exists():
            return NoemaSurfaceResult("sha256_file", False, issues=[f"missing: {relative_path}"])
        if not path.is_file():
            return NoemaSurfaceResult("sha256_file", False, issues=[f"not a file: {relative_path}"])
        digest = hashlib.sha256()
        size = 0
        with path.open("rb") as handle:
            while True:
                chunk = handle.read(chunk_size)
                if not chunk:
                    break
                size += len(chunk)
                digest.update(chunk)
        return NoemaSurfaceResult(
            "sha256_file",
            True,
            payload={"path": str(relative_path), "sha256": digest.hexdigest(), "size": size},
        )

    def zip_paths(
        self,
        output_zip: str | Path,
        paths: Iterable[str | Path],
        *,
        compression: int = zipfile.ZIP_DEFLATED,
        exclude_globs: Iterable[str] | None = None,
    ) -> NoemaSurfaceResult:
        output = self.path(output_zip)
        output.parent.mkdir(parents=True, exist_ok=True)
        excluded = tuple(exclude_globs or ("__pycache__/*", "*/__pycache__/*", ".pytest_cache/*", "*/.pytest_cache/*"))

        def is_excluded(arcname: str) -> bool:
            return any(fnmatch.fnmatch(arcname, pattern) for pattern in excluded)

        issues: list[str] = []
        entries: list[str] = []
        with zipfile.ZipFile(output, "w", compression=compression) as archive:
            for rel in paths:
                source = self.path(rel)
                if not source.exists():
                    issues.append(f"missing: {rel}")
                    continue
                if source.is_file():
                    arcname = str(source.relative_to(self.root))
                    if is_excluded(arcname):
                        continue
                    archive.write(source, arcname)
                    entries.append(arcname)
                else:
                    for item in sorted(source.rglob("*")):
                        if not item.is_file():
                            continue
                        if item.resolve() == output.resolve():
                            continue
                        arcname = str(item.relative_to(self.root))
                        if is_excluded(arcname):
                            continue
                        archive.write(item, arcname)
                        entries.append(arcname)
        if issues:
            return NoemaSurfaceResult("zip_paths", False, payload={"output_zip": str(output_zip), "entries": entries, "excluded_globs": list(excluded)}, issues=issues)
        sha = self.sha256_file(output_zip)
        payload = {"output_zip": str(output_zip), "entries": entries, "entry_count": len(entries), "excluded_globs": list(excluded)}
        if sha.ok:
            payload.update({"sha256": sha.payload["sha256"], "size": sha.payload["size"]})
        return NoemaSurfaceResult("zip_paths", True, payload=payload)

    def zip_test(self, relative_zip: str | Path) -> NoemaSurfaceResult:
        path = self.path(relative_zip)
        if not path.exists():
            return NoemaSurfaceResult("zip_test", False, issues=[f"missing: {relative_zip}"])
        try:
            with zipfile.ZipFile(path, "r") as archive:
                bad = archive.testzip()
                names = archive.namelist()
        except zipfile.BadZipFile as exc:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/cielingo_core/noema_surface/command_prompt.py:431 quiet except scope=NoemaSurface.zip_test reason=return NoemaSurfaceResult(\"zip_test\", False, issues=[f\"bad zip: {exc}\"])")
            return NoemaSurfaceResult("zip_test", False, issues=[f"bad zip: {exc}"])
        if bad is not None:
            return NoemaSurfaceResult("zip_test", False, payload={"bad_entry": bad}, issues=[f"bad entry: {bad}"])
        return NoemaSurfaceResult("zip_test", True, payload={"zip": str(relative_zip), "entry_count": len(names)})


    def compileall(self, relative_path: str | Path = ".", timeout_s: int = 60) -> NoemaSurfaceResult:
        target = self.path(relative_path)
        if not target.exists():
            return NoemaSurfaceResult("compileall", False, issues=[f"missing: {relative_path}"])
        proc = subprocess.run(
            [sys.executable, "-m", "compileall", "-q", str(target)],
            cwd=self.root,
            capture_output=True,
            text=True,
            timeout=timeout_s,
        )
        return NoemaSurfaceResult(
            "compileall",
            proc.returncode == 0,
            payload={"return_code": proc.returncode, "stdout": proc.stdout, "stderr": proc.stderr, "path": str(relative_path)},
        )

    def ast_imports(self, relative_path: str | Path) -> NoemaSurfaceResult:
        result = self.read_text(relative_path)
        if not result.ok:
            return result
        tree = ast.parse(result.payload["text"])
        imports: list[str] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                imports.append(node.module)
            elif isinstance(node, ast.Import):
                imports.extend(alias.name for alias in node.names)
        return NoemaSurfaceResult("ast_imports", True, payload={"imports": imports})

    def assert_router_boundary(self, relative_path: str | Path) -> NoemaSurfaceResult:
        result = self.ast_imports(relative_path)
        if not result.ok:
            return result
        imports = result.payload["imports"]
        issues: list[str] = []
        required = {
            "cielingo_core.language_spaces.pl.sentence_equation",
            "cielingo_core.language_spaces.en.sentence_equation",
            "cielingo_core.language_spaces.ja.sentence_equation",
        }
        missing = sorted(required - set(imports))
        if missing:
            issues.append(f"router missing endpoint imports: {missing}")
        for imp in imports:
            if imp.endswith(".solver") or imp.endswith(".grammar") or imp.endswith(".j_holonomy"):
                issues.append(f"router imports forbidden regional internals: {imp}")
        return NoemaSurfaceResult("assert_router_boundary", not issues, payload={"imports": imports}, issues=issues)

    def run_pytest(self, timeout_s: int = 60) -> NoemaSurfaceResult:
        env = os.environ.copy()
        env["PYTHONPATH"] = "src"
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", "-q"],
            cwd=self.root,
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout_s,
        )
        return NoemaSurfaceResult(
            "run_pytest",
            proc.returncode == 0,
            payload={"return_code": proc.returncode, "stdout": proc.stdout, "stderr": proc.stderr},
        )
