"""Static, threshold-free function identity for CIELPC/NOEMA.

This module proves only exact relations derivable from Python syntax. It does
not claim general semantic program equivalence. Missing proof stays UNKNOWN.
"""
from __future__ import annotations

import ast
import hashlib
import json
import sys
from dataclasses import asdict, dataclass
from enum import Enum
from pathlib import Path
from typing import Iterable, Mapping


class FunctionRelation(str, Enum):
    SAME_IDENTITY = "SAME_IDENTITY"
    ALIAS = "ALIAS"
    CONFLICT = "CONFLICT"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class SignatureShape:
    positional_only: int
    positional_or_keyword: int
    keyword_only: int
    has_vararg: bool
    has_varkw: bool
    positional_defaults: int
    keyword_default_mask: tuple[bool, ...]
    is_async: bool
    is_generator: bool


@dataclass(frozen=True)
class FunctionIdentity:
    source_path: str
    module: str
    qualified_name: str
    symbol_name: str
    signature: SignatureShape
    dependency_symbols: tuple[str, ...]
    import_roots: tuple[str, ...]
    normalized_ast_sha256: str
    invariant_sha256: str


@dataclass(frozen=True)
class FunctionComparison:
    relation: FunctionRelation
    left: str
    right: str
    reasons: tuple[str, ...]


@dataclass(frozen=True)
class DependencyManifest:
    stdlib_imports: tuple[str, ...]
    local_imports: tuple[str, ...]
    external_imports: tuple[str, ...]


def _digest(value: object) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def _dotted(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        parent = _dotted(node.value)
        return f"{parent}.{node.attr}" if parent else None
    return None


def _imports(tree: ast.AST) -> tuple[dict[str, str], tuple[str, ...]]:
    aliases: dict[str, str] = {}
    roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for item in node.names:
                root = item.name.split(".", 1)[0]
                roots.add(root)
                aliases[item.asname or root] = item.name
        elif isinstance(node, ast.ImportFrom) and node.module:
            root = node.module.split(".", 1)[0]
            roots.add(root)
            for item in node.names:
                if item.name != "*":
                    aliases[item.asname or item.name] = f"{node.module}.{item.name}"
    return aliases, tuple(sorted(roots))


class _Bindings(ast.NodeVisitor):
    def __init__(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        self.names: list[str] = []
        self._seen: set[str] = set()
        args = [*node.args.posonlyargs, *node.args.args, *node.args.kwonlyargs]
        for arg in args:
            self.add(arg.arg)
        if node.args.vararg:
            self.add(node.args.vararg.arg)
        if node.args.kwarg:
            self.add(node.args.kwarg.arg)
        for statement in node.body:
            self.visit(statement)

    def add(self, name: str) -> None:
        if name not in self._seen:
            self._seen.add(name)
            self.names.append(name)

    def target(self, node: ast.AST) -> None:
        if isinstance(node, ast.Name):
            self.add(node.id)
        elif isinstance(node, (ast.Tuple, ast.List)):
            for item in node.elts:
                self.target(item)

    def visit_Assign(self, node: ast.Assign) -> None:
        for target in node.targets:
            self.target(target)
        self.visit(node.value)

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        self.target(node.target)
        if node.value:
            self.visit(node.value)

    def visit_For(self, node: ast.For) -> None:
        self.target(node.target)
        self.generic_visit(node)

    visit_AsyncFor = visit_For


class _Normalize(ast.NodeTransformer):
    def __init__(self, local: Mapping[str, str], aliases: Mapping[str, str]) -> None:
        self.local = dict(local)
        self.aliases = dict(aliases)

    def visit_Name(self, node: ast.Name) -> ast.AST:
        value = self.aliases.get(node.id, self.local.get(node.id, node.id))
        return ast.copy_location(ast.Name(id=value, ctx=node.ctx), node)

    def visit_arg(self, node: ast.arg) -> ast.AST:
        return ast.copy_location(ast.arg(arg=self.local.get(node.arg, node.arg), annotation=node.annotation), node)


class _Calls(ast.NodeVisitor):
    def __init__(self, local: Mapping[str, str], aliases: Mapping[str, str]) -> None:
        self.local = dict(local)
        self.aliases = dict(aliases)
        self.items: set[str] = set()

    def visit_Call(self, node: ast.Call) -> None:
        name = _dotted(node.func)
        if name:
            root, dot, rest = name.partition(".")
            root = self.aliases.get(root, self.local.get(root, root))
            self.items.add(f"{root}.{rest}" if dot else root)
        else:
            self.items.add("<dynamic-call>")
        self.generic_visit(node)


def _shape(node: ast.FunctionDef | ast.AsyncFunctionDef) -> SignatureShape:
    args = node.args
    return SignatureShape(
        positional_only=len(args.posonlyargs),
        positional_or_keyword=len(args.args),
        keyword_only=len(args.kwonlyargs),
        has_vararg=args.vararg is not None,
        has_varkw=args.kwarg is not None,
        positional_defaults=len(args.defaults),
        keyword_default_mask=tuple(item is not None for item in args.kw_defaults),
        is_async=isinstance(node, ast.AsyncFunctionDef),
        is_generator=any(isinstance(item, (ast.Yield, ast.YieldFrom)) for item in ast.walk(node)),
    )


def _body(node: ast.FunctionDef | ast.AsyncFunctionDef) -> list[ast.stmt]:
    body = list(node.body)
    if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant):
        if isinstance(body[0].value.value, str):
            body = body[1:]
    return body


def identities_from_source(source: str, *, module: str = "", source_path: str = "<memory>") -> tuple[FunctionIdentity, ...]:
    tree = ast.parse(source, filename=source_path)
    aliases, module_imports = _imports(tree)
    output: list[FunctionIdentity] = []

    class Collector(ast.NodeVisitor):
        def __init__(self) -> None:
            self.stack: list[str] = []

        def record(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
            local_map = {name: f"v{i}" for i, name in enumerate(_Bindings(node).names)}
            normalizer = _Normalize(local_map, aliases)
            normalized = [normalizer.visit(ast.fix_missing_locations(ast.parse(ast.unparse(item))).body[0]) for item in _body(node)]
            body_dump = [ast.dump(item, include_attributes=False) for item in normalized]
            calls = _Calls(local_map, aliases)
            for item in node.body:
                calls.visit(item)
            local_imports = _imports(node)[1]
            signature = _shape(node)
            ast_sha = _digest(body_dump)
            invariant = {
                "signature": asdict(signature),
                "dependency_symbols": sorted(calls.items),
                "import_roots": list(local_imports),
                "normalized_ast_sha256": ast_sha,
            }
            local_name = ".".join([*self.stack, node.name]) if self.stack else node.name
            qualified = f"{module}.{local_name}" if module else local_name
            output.append(FunctionIdentity(
                source_path=source_path,
                module=module,
                qualified_name=qualified,
                symbol_name=node.name,
                signature=signature,
                dependency_symbols=tuple(sorted(calls.items)),
                import_roots=local_imports,
                normalized_ast_sha256=ast_sha,
                invariant_sha256=_digest(invariant),
            ))

        def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
            self.record(node)
            self.stack.append(node.name)
            for item in node.body:
                self.visit(item)
            self.stack.pop()

        visit_AsyncFunctionDef = visit_FunctionDef

        def visit_ClassDef(self, node: ast.ClassDef) -> None:
            self.stack.append(node.name)
            for item in node.body:
                self.visit(item)
            self.stack.pop()

    Collector().visit(tree)
    return tuple(output)


def compare_functions(left: FunctionIdentity, right: FunctionIdentity) -> FunctionComparison:
    same_invariant = left.invariant_sha256 == right.invariant_sha256
    same_symbol = left.qualified_name == right.qualified_name
    if same_symbol and same_invariant:
        relation = FunctionRelation.SAME_IDENTITY
        reason = "same qualified symbol and invariant"
    elif same_invariant:
        relation = FunctionRelation.ALIAS
        reason = "different qualified symbols share one invariant"
    elif same_symbol:
        relation = FunctionRelation.CONFLICT
        reason = "same qualified symbol has different invariants"
    else:
        relation = FunctionRelation.UNKNOWN
        reason = "no exact proof"
    return FunctionComparison(relation, left.qualified_name, right.qualified_name, (reason,))


def derive_dependency_manifest(import_roots: Iterable[str], *, local_roots: Iterable[str] = ()) -> DependencyManifest:
    observed = {str(item) for item in import_roots if item}
    stdlib_set = set(getattr(sys, "stdlib_module_names", ()))
    local_set = set(local_roots)
    stdlib = observed & stdlib_set
    local = (observed - stdlib) & local_set
    external = observed - stdlib - local
    return DependencyManifest(tuple(sorted(stdlib)), tuple(sorted(local)), tuple(sorted(external)))


def scan_python_tree(root: str | Path) -> tuple[tuple[FunctionIdentity, ...], DependencyManifest]:
    base = Path(root).resolve()
    paths = tuple(sorted(path for path in base.rglob("*.py") if path.is_file()))
    identities: list[FunctionIdentity] = []
    imports: set[str] = set()
    local_roots: set[str] = set()
    for path in paths:
        relative = path.relative_to(base)
        parts = list(relative.parts)
        if parts and parts[0] == "src":
            parts = parts[1:]
        if parts:
            local_roots.add(Path(parts[0]).stem)
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
        imports.update(_imports(tree)[1])
        module_parts = list(relative.with_suffix("").parts)
        if module_parts and module_parts[0] == "src":
            module_parts = module_parts[1:]
        if module_parts and module_parts[-1] == "__init__":
            module_parts = module_parts[:-1]
        identities.extend(identities_from_source(source, module=".".join(module_parts), source_path=str(relative)))
    return tuple(identities), derive_dependency_manifest(imports, local_roots=local_roots)


__all__ = [
    "DependencyManifest",
    "FunctionComparison",
    "FunctionIdentity",
    "FunctionRelation",
    "SignatureShape",
    "compare_functions",
    "derive_dependency_manifest",
    "identities_from_source",
    "scan_python_tree",
]
