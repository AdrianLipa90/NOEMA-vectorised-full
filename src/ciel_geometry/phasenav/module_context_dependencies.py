"""Exact Python module-context dependency facts for M8/M9.

This layer does not replace the M7 structural fingerprint. It derives facts M7
cannot know from a callable in isolation: package-qualified relative imports
and imports that occur inside executable scopes.
"""
from __future__ import annotations

import ast
import importlib.util
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Sequence

from .function_identity import DependencyManifest


@dataclass(frozen=True)
class ModuleContextScan:
    dependency_manifest: DependencyManifest
    function_dependency_rewrites: Mapping[str, Mapping[str, str]]
    unresolved_relative_imports: tuple[str, ...] = ()


def _module_context(relative: Path) -> tuple[str, str]:
    parts = list(relative.with_suffix("").parts)
    if parts and parts[0] == "src":
        parts = parts[1:]
    is_package = bool(parts and parts[-1] == "__init__")
    if is_package:
        parts = parts[:-1]
    module = ".".join(parts)
    package = module if is_package else ".".join(parts[:-1])
    return module, package


def _resolve_from_base(node: ast.ImportFrom, package: str) -> str | None:
    if node.level <= 0:
        return node.module
    if not package:
        return None
    relative_name = "." * node.level + (node.module or "")
    try:
        return importlib.util.resolve_name(relative_name, package)
    except (ImportError, ValueError):
        return None


def _relative_rewrites_for_import(
    node: ast.ImportFrom,
    package: str,
) -> tuple[dict[str, str], str | None]:
    if node.level <= 0:
        return {}, None
    base = _resolve_from_base(node, package)
    if base is None:
        spelling = "." * node.level + (node.module or "")
        return {}, spelling

    rewrites: dict[str, str] = {}
    for item in node.names:
        if item.name == "*":
            continue
        resolved = f"{base}.{item.name}"
        local_spelling = item.asname or item.name
        if node.module:
            # M7 normalizes a direct use in this scope, e.g. `b()` after
            # `from .foo import bar as b`, to `foo.bar`. A nested function,
            # however, may still observe the closure spelling `b`, so retain
            # both exact representations.
            observed = f"{node.module}.{item.name}"
            rewrites[observed] = resolved
            rewrites[local_spelling] = resolved
        else:
            # M7 currently cannot normalize `from . import foo as f`, so the
            # observed call root remains the local spelling.
            rewrites[local_spelling] = resolved
    return rewrites, None


class _AllImportRoots(ast.NodeVisitor):
    def __init__(self, package: str) -> None:
        self.package = package
        self.roots: set[str] = set()
        self.unresolved: set[str] = set()

    def visit_Import(self, node: ast.Import) -> None:
        for item in node.names:
            self.roots.add(item.name.split(".", 1)[0])

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        base = _resolve_from_base(node, self.package)
        if base is None:
            spelling = "." * node.level + (node.module or "")
            self.unresolved.add(spelling or "<relative-import>")
            return
        self.roots.add(base.split(".", 1)[0])


class _ScopeRelativeImports(ast.NodeVisitor):
    """Collect relative imports in one lexical function/module scope only."""

    def __init__(self, package: str) -> None:
        self.package = package
        self.rewrites: dict[str, str] = {}
        self.unresolved: set[str] = set()

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        rewrites, unresolved = _relative_rewrites_for_import(node, self.package)
        self.rewrites.update(rewrites)
        if unresolved:
            self.unresolved.add(unresolved)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        return

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        return


def _scope_relative_imports(
    statements: Sequence[ast.stmt], package: str
) -> tuple[dict[str, str], tuple[str, ...]]:
    collector = _ScopeRelativeImports(package)
    for statement in statements:
        collector.visit(statement)
    return collector.rewrites, tuple(sorted(collector.unresolved))


def _rewrite_map_for_functions(
    tree: ast.Module,
    *,
    module: str,
    package: str,
) -> tuple[dict[str, dict[str, str]], tuple[str, ...]]:
    module_rewrites, module_unresolved = _scope_relative_imports(tree.body, package)
    output: dict[str, dict[str, str]] = {}
    unresolved: set[str] = set(module_unresolved)

    class Collector(ast.NodeVisitor):
        def __init__(self) -> None:
            self.stack: list[str] = []
            self.inherited: list[dict[str, str]] = [dict(module_rewrites)]

        def _record(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
            local, debt = _scope_relative_imports(node.body, package)
            unresolved.update(debt)
            combined = dict(self.inherited[-1])
            combined.update(local)
            local_name = ".".join([*self.stack, node.name]) if self.stack else node.name
            qualified = f"{module}.{local_name}" if module else local_name
            output[qualified] = combined

            self.stack.append(node.name)
            self.inherited.append(combined)
            for statement in node.body:
                self.visit(statement)
            self.inherited.pop()
            self.stack.pop()

        def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
            self._record(node)

        visit_AsyncFunctionDef = visit_FunctionDef

        def visit_ClassDef(self, node: ast.ClassDef) -> None:
            # Class namespace imports are not lexical parents of methods.
            self.stack.append(node.name)
            for statement in node.body:
                self.visit(statement)
            self.stack.pop()

    Collector().visit(tree)
    return output, tuple(sorted(unresolved))


def scan_module_context(root: str | Path) -> ModuleContextScan:
    base = Path(root).resolve()
    paths = tuple(sorted(path for path in base.rglob("*.py") if path.is_file()))
    local_roots: set[str] = set()
    observed_roots: set[str] = set()
    rewrites: dict[str, dict[str, str]] = {}
    unresolved: set[str] = set()

    contexts: list[tuple[Path, Path, str, str]] = []
    for path in paths:
        relative = path.relative_to(base)
        module, package = _module_context(relative)
        contexts.append((path, relative, module, package))
        if module:
            local_roots.add(module.split(".", 1)[0])

    for path, relative, module, package in contexts:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))

        import_collector = _AllImportRoots(package)
        import_collector.visit(tree)
        observed_roots.update(import_collector.roots)
        unresolved.update(f"{relative}:{item}" for item in import_collector.unresolved)

        function_maps, function_debt = _rewrite_map_for_functions(
            tree,
            module=module,
            package=package,
        )
        rewrites.update(function_maps)
        unresolved.update(f"{relative}:{item}" for item in function_debt)

    stdlib_set = set(getattr(sys, "stdlib_module_names", ()))
    stdlib = observed_roots & stdlib_set
    local = (observed_roots - stdlib) & local_roots
    external = observed_roots - stdlib - local

    return ModuleContextScan(
        dependency_manifest=DependencyManifest(
            stdlib_imports=tuple(sorted(stdlib)),
            local_imports=tuple(sorted(local)),
            external_imports=tuple(sorted(external)),
        ),
        function_dependency_rewrites={
            name: dict(sorted(mapping.items())) for name, mapping in sorted(rewrites.items())
        },
        unresolved_relative_imports=tuple(sorted(unresolved)),
    )


__all__ = ["ModuleContextScan", "scan_module_context"]
