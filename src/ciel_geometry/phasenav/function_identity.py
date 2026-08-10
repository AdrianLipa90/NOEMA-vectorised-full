"""Static, threshold-free function identity for CIELPC/NOEMA.

Only exact relations derivable from Python syntax are promoted. General program
semantic equivalence is not claimed; missing proof remains UNKNOWN.
"""
from __future__ import annotations

import ast
import copy
import hashlib
import json
import sys
from dataclasses import asdict, dataclass
from enum import Enum
from pathlib import Path
from typing import Iterable, Mapping, Sequence


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


class _ImportCollector(ast.NodeVisitor):
    def __init__(self) -> None:
        self.aliases: dict[str, str] = {}
        self.roots: set[str] = set()

    def visit_Import(self, node: ast.Import) -> None:
        for item in node.names:
            root = item.name.split(".", 1)[0]
            self.roots.add(root)
            self.aliases[item.asname or root] = item.name

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if not node.module:
            return
        root = node.module.split(".", 1)[0]
        self.roots.add(root)
        for item in node.names:
            if item.name != "*":
                self.aliases[item.asname or item.name] = f"{node.module}.{item.name}"

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        return

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        return


def _scope_imports(statements: Sequence[ast.stmt]) -> tuple[dict[str, str], tuple[str, ...]]:
    collector = _ImportCollector()
    for statement in statements:
        collector.visit(statement)
    return collector.aliases, tuple(sorted(collector.roots))


class _Bindings(ast.NodeVisitor):
    def __init__(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        self.names: list[str] = []
        self._seen: set[str] = set()
        self._excluded: set[str] = set()
        for arg in [*node.args.posonlyargs, *node.args.args, *node.args.kwonlyargs]:
            self._add(arg.arg)
        if node.args.vararg:
            self._add(node.args.vararg.arg)
        if node.args.kwarg:
            self._add(node.args.kwarg.arg)
        for statement in node.body:
            self.visit(statement)
        self.names = [item for item in self.names if item not in self._excluded]

    def _add(self, name: str | None) -> None:
        if name and name not in self._seen:
            self._seen.add(name)
            self.names.append(name)

    def _target(self, node: ast.AST) -> None:
        if isinstance(node, ast.Name):
            self._add(node.id)
        elif isinstance(node, (ast.Tuple, ast.List)):
            for item in node.elts:
                self._target(item)
        elif isinstance(node, ast.Starred):
            self._target(node.value)

    def visit_Global(self, node: ast.Global) -> None:
        self._excluded.update(node.names)

    def visit_Nonlocal(self, node: ast.Nonlocal) -> None:
        self._excluded.update(node.names)

    def visit_Assign(self, node: ast.Assign) -> None:
        for target in node.targets:
            self._target(target)
        self.visit(node.value)

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        self._target(node.target)
        if node.value:
            self.visit(node.value)

    def visit_AugAssign(self, node: ast.AugAssign) -> None:
        self._target(node.target)
        self.visit(node.value)

    def visit_For(self, node: ast.For) -> None:
        self._target(node.target)
        self.generic_visit(node)

    visit_AsyncFor = visit_For

    def visit_With(self, node: ast.With) -> None:
        for item in node.items:
            if item.optional_vars:
                self._target(item.optional_vars)
        self.generic_visit(node)

    visit_AsyncWith = visit_With

    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        self._add(node.name)
        self.generic_visit(node)

    def visit_NamedExpr(self, node: ast.NamedExpr) -> None:
        self._target(node.target)
        self.visit(node.value)

    def visit_comprehension(self, node: ast.comprehension) -> None:
        # Python 3 comprehension targets have a separate scope. Keeping their
        # spelling can cause false UNKNOWN but cannot create a false ALIAS.
        self.visit(node.iter)
        for item in node.ifs:
            self.visit(item)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._add(node.name)

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self._add(node.name)


class _AliasNormalizer(ast.NodeTransformer):
    """Normalize imported names without applying callable-local bindings."""

    def __init__(self, aliases: Mapping[str, str]) -> None:
        self.aliases = dict(aliases)

    def visit_Name(self, node: ast.Name) -> ast.AST:
        value = self.aliases.get(node.id, node.id)
        return ast.copy_location(ast.Name(id=value, ctx=node.ctx), node)


class _BodyNormalizer(ast.NodeTransformer):
    """Normalize only the current callable body scope.

    Nested function/class bodies are kept verbatim. This is conservative: M7
    may miss an alias across renamed nested scopes, but cannot invent one.
    """

    def __init__(self, local: Mapping[str, str], aliases: Mapping[str, str]) -> None:
        self.local = dict(local)
        self.aliases = dict(aliases)

    def visit_Name(self, node: ast.Name) -> ast.AST:
        value = self.aliases.get(node.id, self.local.get(node.id, node.id))
        return ast.copy_location(ast.Name(id=value, ctx=node.ctx), node)

    def visit_alias(self, node: ast.alias) -> ast.AST:
        result = copy.deepcopy(node)
        result.asname = None
        return result

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.AST:
        result = copy.deepcopy(node)
        result.name = self.local.get(node.name, node.name)
        return result

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> ast.AST:
        result = copy.deepcopy(node)
        result.name = self.local.get(node.name, node.name)
        return result

    def visit_ClassDef(self, node: ast.ClassDef) -> ast.AST:
        result = copy.deepcopy(node)
        result.name = self.local.get(node.name, node.name)
        return result


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

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        return

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        return


class _YieldProbe(ast.NodeVisitor):
    def __init__(self) -> None:
        self.found = False

    def visit_Yield(self, node: ast.Yield) -> None:
        self.found = True

    def visit_YieldFrom(self, node: ast.YieldFrom) -> None:
        self.found = True

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        return

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        return


def _is_generator(node: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    probe = _YieldProbe()
    for statement in node.body:
        probe.visit(statement)
    return probe.found


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
        is_generator=_is_generator(node),
    )


def _normalized_arguments(
    args: ast.arguments,
    local: Mapping[str, str],
    module_aliases: Mapping[str, str],
) -> ast.arguments:
    result = copy.deepcopy(args)
    outer = _AliasNormalizer(module_aliases)
    all_args = [*result.posonlyargs, *result.args, *result.kwonlyargs]
    for arg in all_args:
        arg.arg = local.get(arg.arg, arg.arg)
        if arg.annotation:
            arg.annotation = outer.visit(arg.annotation)
    if result.vararg:
        result.vararg.arg = local.get(result.vararg.arg, result.vararg.arg)
        if result.vararg.annotation:
            result.vararg.annotation = outer.visit(result.vararg.annotation)
    if result.kwarg:
        result.kwarg.arg = local.get(result.kwarg.arg, result.kwarg.arg)
        if result.kwarg.annotation:
            result.kwarg.annotation = outer.visit(result.kwarg.annotation)
    result.defaults = [outer.visit(item) for item in result.defaults]
    result.kw_defaults = [outer.visit(item) if item is not None else None for item in result.kw_defaults]
    return result


def _normalized_function(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    module_aliases: Mapping[str, str],
) -> tuple[str, tuple[str, ...], tuple[str, ...]]:
    local = {name: f"v{i}" for i, name in enumerate(_Bindings(node).names)}
    local_aliases, local_imports = _scope_imports(node.body)
    body_aliases = {**module_aliases, **local_aliases}
    body_normalizer = _BodyNormalizer(local, body_aliases)
    outer = _AliasNormalizer(module_aliases)

    normalized = copy.deepcopy(node)
    normalized.name = "<function>"
    normalized.args = _normalized_arguments(node.args, local, module_aliases)
    normalized.decorator_list = [outer.visit(copy.deepcopy(item)) for item in node.decorator_list]
    normalized.returns = outer.visit(copy.deepcopy(node.returns)) if node.returns else None
    normalized.body = [body_normalizer.visit(copy.deepcopy(item)) for item in node.body]
    if normalized.body and isinstance(normalized.body[0], ast.Expr):
        value = normalized.body[0].value
        if isinstance(value, ast.Constant) and isinstance(value.value, str):
            normalized.body = normalized.body[1:]
    ast.fix_missing_locations(normalized)

    calls = _Calls(local, body_aliases)
    for statement in node.body:
        calls.visit(statement)
    return ast.dump(normalized, include_attributes=False), tuple(sorted(calls.items)), local_imports


def identities_from_source(
    source: str,
    *,
    module: str = "",
    source_path: str = "<memory>",
) -> tuple[FunctionIdentity, ...]:
    tree = ast.parse(source, filename=source_path)
    module_aliases, _ = _scope_imports(tree.body)
    output: list[FunctionIdentity] = []

    class Collector(ast.NodeVisitor):
        def __init__(self) -> None:
            self.stack: list[str] = []

        def record(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
            normalized, calls, local_imports = _normalized_function(node, module_aliases)
            signature = _shape(node)
            ast_sha = _digest(normalized)
            invariant = {
                "signature": asdict(signature),
                "dependency_symbols": list(calls),
                "import_roots": list(local_imports),
                "normalized_ast_sha256": ast_sha,
            }
            local_name = ".".join([*self.stack, node.name]) if self.stack else node.name
            qualified = f"{module}.{local_name}" if module else local_name
            output.append(
                FunctionIdentity(
                    source_path=source_path,
                    module=module,
                    qualified_name=qualified,
                    symbol_name=node.name,
                    signature=signature,
                    dependency_symbols=calls,
                    import_roots=local_imports,
                    normalized_ast_sha256=ast_sha,
                    invariant_sha256=_digest(invariant),
                )
            )

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
        return FunctionComparison(
            FunctionRelation.SAME_IDENTITY,
            left.qualified_name,
            right.qualified_name,
            ("same qualified symbol and invariant",),
        )
    if same_invariant:
        return FunctionComparison(
            FunctionRelation.ALIAS,
            left.qualified_name,
            right.qualified_name,
            ("different qualified symbols share one invariant",),
        )
    if same_symbol:
        return FunctionComparison(
            FunctionRelation.CONFLICT,
            left.qualified_name,
            right.qualified_name,
            ("same qualified symbol has different invariants",),
        )
    return FunctionComparison(
        FunctionRelation.UNKNOWN,
        left.qualified_name,
        right.qualified_name,
        ("no exact proof",),
    )


def derive_dependency_manifest(
    import_roots: Iterable[str],
    *,
    local_roots: Iterable[str] = (),
) -> DependencyManifest:
    observed = {str(item) for item in import_roots if item}
    stdlib_set = set(getattr(sys, "stdlib_module_names", ()))
    local_set = set(local_roots)
    stdlib = observed & stdlib_set
    local = (observed - stdlib) & local_set
    external = observed - stdlib - local
    return DependencyManifest(
        tuple(sorted(stdlib)),
        tuple(sorted(local)),
        tuple(sorted(external)),
    )


def scan_python_tree(
    root: str | Path,
) -> tuple[tuple[FunctionIdentity, ...], DependencyManifest]:
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
        imports.update(_scope_imports(tree.body)[1])
        module_parts = list(relative.with_suffix("").parts)
        if module_parts and module_parts[0] == "src":
            module_parts = module_parts[1:]
        if module_parts and module_parts[-1] == "__init__":
            module_parts = module_parts[:-1]
        identities.extend(
            identities_from_source(
                source,
                module=".".join(module_parts),
                source_path=str(relative),
            )
        )
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
