"""PhaseNav Bypass Language (PBL) — PhaseNav jako język kodowania bypassów.

Każdy operator PhaseNav ma swoje SEMANTYKI WYKONAWCZE (co ROBI jako bypass).
Piramida:  OperatorChain → BypassRuntime.execute() → rzeczywista akcja.

Użycie:
  from phasenav_bypass_language import Φ, BypassRuntime
  λ_socket = Φ.COMPOSITION(
      Φ.QUESTION('socket'),
      Φ.NEGATION(Φ.FORCE(Φ.COMPOSITION(Φ.RETURN, Φ.AFFECT('warn'))))
  )
  result = BypassRuntime().execute(λ_socket, context={'path': '/run/...'})

Lazy thunks:
  Każdy callable przekazany jako argument operatora jest wykonywany
  leniwie (lazy evaluation) z contextem jako argumentem:
    Φ.MODAL_POSSIBILITY(lambda ctx: risky_operation())
"""

from __future__ import annotations

import hashlib
import logging
import math
import time
from typing import Any, Callable

import numpy as np

_log = logging.getLogger("PhaseNav.BypassLanguage")

# ──────────────────────────────────────────────
# 39 operatorów PhaseNav z semantyką wykonawczą
# ──────────────────────────────────────────────

class OperatorKind:
    """39 PhaseNav operator identifiers — każde to osobne słowo w języku bypassu."""
    IDENTITY = "IDENTITY"
    DIFFERENCE = "DIFFERENCE"
    ORDER = "ORDER"
    COMPOSITION = "COMPOSITION"
    ADDITION = "ADDITION"
    FORCE = "FORCE"
    NEGATION = "NEGATION"
    QUESTION = "QUESTION"
    TRANSFORM = "TRANSFORM"
    RETURN = "RETURN"
    FOLD = "FOLD"
    BOUNDARY = "BOUNDARY"
    SCOPE = "SCOPE"
    AFFECT = "AFFECT"
    CONSENT = "CONSENT"
    SOURCE = "SOURCE"
    MEMORY = "MEMORY"
    RISK = "RISK"
    ASSERTION = "ASSERTION"
    CONDITION = "CONDITION"
    CAUSE = "CAUSE"
    MODAL_POSSIBILITY = "MODAL_POSSIBILITY"
    MODAL_NECESSITY = "MODAL_NECESSITY"
    MODAL_PERMISSION = "MODAL_PERMISSION"
    MODAL_OBLIGATION = "MODAL_OBLIGATION"
    UNCERTAINTY = "UNCERTAINTY"
    SOURCE_REQUIRED = "SOURCE_REQUIRED"
    CANON_BLOCK = "CANON_BLOCK"
    CONSENT_REQUIRED = "CONSENT_REQUIRED"
    ACTION_REQUEST = "ACTION_REQUEST"
    REFUSAL = "REFUSAL"
    PAUSE = "PAUSE"
    SIMULATION_BOUNDARY = "SIMULATION_BOUNDARY"
    UNRUH_DRIVE = "UNRUH_DRIVE"
    WARP_DRIFT = "WARP_DRIFT"
    ATTRACTOR = "ATTRACTOR"
    # Nowe operatory — emergencja z concept registry
    SOFT_CLIP = "SOFT_CLIP"
    RESOLVE = "RESOLVE"
    DERIVE = "DERIVE"


class Φ:
    """PhaseNav Bypass Language — konstruktor łańcuchów operatorowych.

    Każda metoda zwraca dict z kodem operatora i argumentami.
    Łańcuchy buduje się przez zagnieżdżanie.

    Callable arguments są wykonywane leniwie przez BypassRuntime._eval:
      Φ.MODAL_POSSIBILITY(lambda ctx: risky_thing())
    """

    @staticmethod
    def IDENTITY(x: Any = None) -> dict:
        return {"op": OperatorKind.IDENTITY, "args": [x]}

    @staticmethod
    def DIFFERENCE(expected: Any, actual: Any, fallback: Any = None) -> dict:
        return {"op": OperatorKind.DIFFERENCE, "args": [expected, actual, fallback]}

    @staticmethod
    def ORDER(*steps: Any) -> dict:
        return {"op": OperatorKind.ORDER, "args": list(steps)}

    @staticmethod
    def COMPOSITION(*steps: Any) -> dict:
        return {"op": OperatorKind.COMPOSITION, "args": list(steps)}

    @staticmethod
    def ADDITION(*sources: Any) -> dict:
        return {"op": OperatorKind.ADDITION, "args": list(sources)}

    @staticmethod
    def FORCE(action: Any, context: Any = None) -> dict:
        return {"op": OperatorKind.FORCE, "args": [action, context]}

    @staticmethod
    def NEGATION(condition: Any) -> dict:
        return {"op": OperatorKind.NEGATION, "args": [condition]}

    @staticmethod
    def QUESTION(target: str) -> dict:
        return {"op": OperatorKind.QUESTION, "args": [target]}

    @staticmethod
    def TRANSFORM(x: Any, f: str = "identity") -> dict:
        return {"op": OperatorKind.TRANSFORM, "args": [x, f]}

    @staticmethod
    def RETURN(x: Any = None) -> dict:
        return {"op": OperatorKind.RETURN, "args": [x]}

    @staticmethod
    def FOLD(seq: list, f: str = "sum") -> dict:
        return {"op": OperatorKind.FOLD, "args": [seq, f]}

    @staticmethod
    def BOUNDARY(condition: Any, on_pass: Any = None, on_fail: Any = None) -> dict:
        return {"op": OperatorKind.BOUNDARY, "args": [condition, on_pass, on_fail]}

    @staticmethod
    def SCOPE(context: Any, body: Any = None) -> dict:
        return {"op": OperatorKind.SCOPE, "args": [context, body]}

    @staticmethod
    def AFFECT(state: Any, emotion: str = "neutral") -> dict:
        return {"op": OperatorKind.AFFECT, "args": [state, emotion]}

    @staticmethod
    def CONSENT(condition: Any, action: Any = None) -> dict:
        return {"op": OperatorKind.CONSENT, "args": [condition, action]}

    @staticmethod
    def SOURCE(origin: str) -> dict:
        return {"op": OperatorKind.SOURCE, "args": [origin]}

    @staticmethod
    def MEMORY(key: str) -> dict:
        return {"op": OperatorKind.MEMORY, "args": [key]}

    @staticmethod
    def RISK(threshold: float = 0.5, action: Any = None) -> dict:
        return {"op": OperatorKind.RISK, "args": [threshold, action]}

    @staticmethod
    def ASSERTION(invariant: Any, msg: str = "") -> dict:
        return {"op": OperatorKind.ASSERTION, "args": [invariant, msg]}

    @staticmethod
    def CONDITION(if_clause: Any, then_clause: Any, else_clause: Any = None) -> dict:
        return {"op": OperatorKind.CONDITION, "args": [if_clause, then_clause, else_clause]}

    @staticmethod
    def CAUSE(*chain: Any) -> dict:
        return {"op": OperatorKind.CAUSE, "args": list(chain)}

    @staticmethod
    def MODAL_POSSIBILITY(action: Any) -> dict:
        return {"op": OperatorKind.MODAL_POSSIBILITY, "args": [action]}

    @staticmethod
    def MODAL_NECESSITY(action: Any) -> dict:
        return {"op": OperatorKind.MODAL_NECESSITY, "args": [action]}

    @staticmethod
    def MODAL_PERMISSION(action: Any) -> dict:
        return {"op": OperatorKind.MODAL_PERMISSION, "args": [action]}

    @staticmethod
    def MODAL_OBLIGATION(action: Any) -> dict:
        return {"op": OperatorKind.MODAL_OBLIGATION, "args": [action]}

    @staticmethod
    def UNCERTAINTY(expr: Any) -> dict:
        return {"op": OperatorKind.UNCERTAINTY, "args": [expr]}

    @staticmethod
    def PAUSE(seconds: float = 0.0) -> dict:
        return {"op": OperatorKind.PAUSE, "args": [seconds]}

    @staticmethod
    def ATTRACTOR(target: Any = None) -> dict:
        return {"op": OperatorKind.ATTRACTOR, "args": [target]}

    @staticmethod
    def SOFT_CLIP(value: Any = None, low: float = 0.0, high: float = 1.0, k: float = 10.0) -> dict:
        """Heisenberg soft clip — smooth bounded compression via tanh.

        Zamiast ostrego np.clip, używa sigmoidalnej transformacji:
          return mid + half * tanh(k * (x - mid) / half)
        gdzie mid = (low+high)/2, half = (high-low)/2

        k → ∞: hard clip. k ≈ 10: płynne przejście.
        """
        return {"op": OperatorKind.SOFT_CLIP, "args": [value, low, high, k]}

    @staticmethod
    def RESOLVE(entity: str, attribute: str, **kwargs) -> dict:
        """Universal resolver — emergentne wartości z concept registry.

        Zamiast hardcoded stałych:
          Φ.RESOLVE("socket_unavailable", "severity") → 0.7 z registry
          Φ.RESOLVE("M0", "radius")                    → 0.92 z MEMORY_CHANNELS
        """
        return {"op": OperatorKind.RESOLVE, "args": [entity, attribute, kwargs]}

    @staticmethod
    def DERIVE(name: str, context: dict = None) -> dict:
        """Derive — wylicz wartość emergentnie z registry.

        Φ.DERIVE("channel_count")  → Φ_channel_count()
        Φ.DERIVE("chunk_size")     → Φ_magic("chunk_size")
        """
        return {"op": OperatorKind.DERIVE, "args": [name, context or {}]}


# ──────────────────────────────────────────────
# BypassRuntime — interpreter języka PhaseNav
# ──────────────────────────────────────────────

class BypassRuntime:
    """Wykonuje łańcuchy PhaseNav — każdy operator to rzeczywista akcja.

    Lazy evaluation: każdy callable argument (lambda) jest wywoływany
    z contextem przy evaluacji — dopiero wtedy, gdy operator go potrzebuje.
    Dzięki temu ryzykowne operacje są wykonywane wewnątrz try/except operatora.

    Semantyka:
      IDENTITY(x)      → x
      DIFFERENCE(a,b,f)→ if a != b: execute f; else: a
      ORDER(a,b,c)     → execute a; if fails: b; if fails: c
      COMPOSITION(a,b) → execute a, pass result to b
      FORCE(a,ctx)     → execute a regardless, log bypass
      NEGATION(a)      → try a; if fails → success (inversion)
      QUESTION(t)      → probe target availability → bool
      BOUNDARY(cond,p,f)→ if cond: p; else: f (with warning)
      AFFECT(s,e)      → log severity, return s with emotion tag
      RISK(t,a)        → if risk > t: execute a with caution
      MODAL_POSSIBILITY(a) → try a; on fail → None (with log)
      MODAL_NECESSITY(a)   → execute a; if None → warn + return None
    """

    def __init__(self, logger: logging.Logger | None = None):
        self.log = logger or _log
        self._bypass_count = 0

    def execute(self, chain: dict, context: dict | None = None) -> Any:
        """Execute a PhaseNav operator chain in given context."""
        ctx = {**(context or {})}
        return self._eval(chain, ctx)

    def _eval(self, node: Any, ctx: dict) -> Any:
        """Evaluate node — callable thunks get lazy execution with context."""
        if callable(node) and not isinstance(node, dict):
            return node(ctx)
        if not isinstance(node, dict) or "op" not in node:
            return node  # literal value

        op = node["op"]
        args = node.get("args", [])

        handler = getattr(self, f"_op_{op}", None)
        if handler is None:
            self.log.warning("[Φ] unknown operator %s — returning Identity", op)
            return args[0] if args else None

        self._bypass_count += 1
        return handler(*args, ctx=ctx)

    def _eval_arg(self, arg: Any, ctx: dict) -> Any:
        """Evaluate a single argument — unwrap thunks."""
        if callable(arg) and not isinstance(arg, dict):
            try:
                return arg(ctx)
            except Exception as exc:
                self.log.info("[Φ] thunk failed during arg eval: %s", exc)
                return None
        if isinstance(arg, dict) and "op" in arg:
            return self._eval(arg, ctx)
        return arg

    # ── Semantyka operatorów ──────────────────

    def _op_IDENTITY(self, x: Any, ctx: dict) -> Any:
        return self._eval_arg(x, ctx)

    def _op_DIFFERENCE(self, expected: Any, actual_call: Any, fallback: Any, ctx: dict) -> Any:
        actual = self._eval_arg(actual_call, ctx)
        if expected != actual:
            self.log.warning("[Φ DIFFERENCE] mismatch (expected=%s actual=%s) → fallback", expected, actual)
            return self._eval_arg(fallback, ctx) if fallback is not None else actual
        return expected

    def _op_ORDER(self, *steps: Any, ctx: dict) -> Any:
        last_error = None
        for step in (steps if isinstance(steps[0], list) else steps):
            try:
                result = self._eval_arg(step, ctx)
                if result is not None:
                    return result
            except Exception as e:
                last_error = e
                self.log.debug("[Φ ORDER] step failed: %s — trying next", e)
                continue
        if last_error:
            raise last_error
        return None

    def _op_COMPOSITION(self, *steps: Any, ctx: dict) -> Any:
        result = None
        steps_list = steps[0] if steps and isinstance(steps[0], list) else list(steps)
        for step in steps_list:
            if isinstance(step, dict) and step.get("op") == OperatorKind.RETURN:
                arg = step["args"][0] if step.get("args") else result
                return self._eval_ret(arg, result)
            result = self._eval_arg(step, ctx)
        return result

    def _eval_ret(self, arg: Any, current: Any) -> Any:
        return self._eval_arg(arg, {}) if arg is not None else current

    def _op_ADDITION(self, *sources: Any, ctx: dict) -> Any:
        results = []
        src_list = sources[0] if sources and isinstance(sources[0], list) else list(sources)
        for src in src_list:
            r = self._eval_arg(src, ctx)
            if r is not None:
                results.append(r)
        if results and all(isinstance(r, dict) for r in results):
            merged = {}
            for r in results:
                merged.update(r)
            return merged
        return results

    def _op_FORCE(self, action: Any, context_arg: Any, ctx: dict) -> Any:
        """FORCE — bypass guard. Execute action regardless, catch errors, log bypass."""
        try:
            return self._eval_arg(action, ctx)
        except Exception as e:
            self.log.debug("[Φ FORCE] bypass executed — %s", e)
            ctx["_bypass_forced"] = True
            return None

    def _op_NEGATION(self, condition: Any, ctx: dict) -> Any:
        try:
            result = self._eval_arg(condition, ctx)
            inverted = not result if isinstance(result, bool) else result is None
            return inverted
        except Exception:
            return True

    def _op_QUESTION(self, target: str, ctx: dict) -> Any:
        self.log.info("[Φ QUESTION] probing %s", target)
        socket_path = ctx.get("socket_path", "")
        if target == "socket" and socket_path:
            from pathlib import Path
            available = Path(socket_path).is_socket()
            ctx["_probe_socket"] = available
            return available
        return ctx.get(f"_probe_{target}", False)

    def _op_TRANSFORM(self, x: Any, f: str, ctx: dict) -> Any:
        return self._eval_arg(x, ctx)

    def _op_RETURN(self, x: Any, ctx: dict) -> Any:
        return self._eval_arg(x, ctx)

    def _op_BOUNDARY(self, condition: Any, on_pass: Any, on_fail: Any, ctx: dict) -> Any:
        cond_result = bool(self._eval_arg(condition, ctx))
        if cond_result:
            return self._eval_arg(on_pass, ctx) if on_pass is not None else None
        else:
            self.log.warning("[Φ BOUNDARY] gate closed — executing fail path")
            return self._eval_arg(on_fail, ctx) if on_fail is not None else None

    def _op_SCOPE(self, context_arg: Any, body: Any, ctx: dict) -> Any:
        merged = self._eval_arg(context_arg, ctx) if isinstance(context_arg, (dict,)) and "op" not in context_arg else context_arg
        if isinstance(merged, dict):
            ctx.update(merged)
        if body is not None:
            return self._eval_arg(body, ctx)
        return merged

    def _op_AFFECT(self, state: Any, emotion: str, ctx: dict) -> Any:
        val = self._eval_arg(state, ctx)
        self.log.info("[Φ AFFECT] %s — value=%s", emotion, val)
        if isinstance(val, dict):
            val["_affect"] = emotion
        return val

    def _op_CONSENT(self, condition: Any, action: Any, ctx: dict) -> Any:
        granted = bool(self._eval_arg(condition, ctx))
        if granted:
            return self._eval_arg(action, ctx) if action is not None else True
        self.log.warning("[Φ CONSENT] denied")
        return False

    def _op_RISK(self, threshold: float, action: Any, ctx: dict) -> Any:
        risk_level = ctx.get("_risk_level", 0.0)
        if risk_level <= threshold:
            return self._eval_arg(action, ctx) if action is not None else True
        self.log.warning("[Φ RISK] threshold exceeded (%.2f > %.2f) — blocking", risk_level, threshold)
        return False

    def _op_PAUSE(self, seconds: float, ctx: dict) -> None:
        if seconds > 0:
            time.sleep(seconds)

    def _op_ASSERTION(self, invariant: Any, msg: str, ctx: dict) -> bool:
        result = bool(self._eval_arg(invariant, ctx))
        if not result:
            self.log.warning("[Φ ASSERTION] failed: %s", msg)
        return result

    def _op_CONDITION(self, if_clause: Any, then_clause: Any, else_clause: Any, ctx: dict) -> Any:
        cond = bool(self._eval_arg(if_clause, ctx))
        if cond:
            return self._eval_arg(then_clause, ctx) if then_clause is not None else True
        else:
            return self._eval_arg(else_clause, ctx) if else_clause is not None else False

    def _op_MODAL_POSSIBILITY(self, action: Any, ctx: dict) -> Any:
        """MODAL_POSSIBILITY — try action, catch errors, return None on failure."""
        try:
            return self._eval_arg(action, ctx)
        except Exception as e:
            self.log.info("[Φ MODAL_POSSIBILITY] not possible: %s", e)
            return None

    def _op_MODAL_NECESSITY(self, action: Any, ctx: dict) -> Any:
        """MODAL_NECESSITY — action must produce value, warn if None."""
        result = self._eval_arg(action, ctx)
        if result is None:
            self.log.warning("[Φ MODAL_NECESSITY] required action produced None")
        return result

    def _op_MODAL_PERMISSION(self, action: Any, ctx: dict) -> Any:
        try:
            result = self._eval_arg(action, ctx)
            return result if result is not None else True
        except Exception:
            return True

    def _op_MODAL_OBLIGATION(self, action: Any, ctx: dict) -> Any:
        result = self._eval_arg(action, ctx)
        if result is None:
            self.log.warning("[Φ MODAL_OBLIGATION] obligation not met")
        return result

    def _op_CAUSE(self, *chain: Any, ctx: dict) -> list:
        results = []
        ch = chain[0] if chain and isinstance(chain[0], list) else list(chain)
        for link in ch:
            r = self._eval_arg(link, ctx)
            results.append(r)
        return results

    def _op_ATTRACTOR(self, target: Any, ctx: dict) -> Any:
        return ctx.get("_attractor", self._eval_arg(target, ctx) if target is not None else None)

    def _op_UNCERTAINTY(self, expr: Any, ctx: dict) -> Any:
        val = self._eval_arg(expr, ctx)
        ctx["_uncertainty"] = val
        return val

    def _op_SOURCE(self, origin: str, ctx: dict) -> str:
        ctx["_source"] = origin
        self.log.info("[Φ SOURCE] %s", origin)
        return origin

    # ── Nowe operatory: emergencja z concept registry ────────────

    def _op_SOFT_CLIP(self, value: Any, low: float, high: float, k: float, ctx: dict) -> float:
        """Heisenberg soft clip — smooth bounded compression via tanh."""
        import numpy as np
        x = self._eval_arg(value, ctx)
        mid = (low + high) / 2.0
        half = (high - low) / 2.0
        return float(mid + half * np.tanh(k * (x - mid) / half if half != 0 else 0.0))

    def _op_RESOLVE(self, entity: str, attribute: str, kwargs: dict, ctx: dict) -> Any:
        """Universal resolver — emergentne wartości z concept registry."""
        from arbitrariness_resolver import Φ_resolve
        return Φ_resolve(entity, attribute, **kwargs)

    def _op_DERIVE(self, name: str, context: dict, ctx: dict) -> Any:
        """Derive — wylicz wartość emergentnie z registry."""
        from arbitrariness_resolver import Φ_magic
        return Φ_magic(name, context)


# ──────────────────────────────────────────────
# Predefiniowane bypassy dla znanych bottlenecków
# ──────────────────────────────────────────────

class BottleneckBypasses:
    """Factory predefiniowanych łańcuchów PhaseNav dla bottlenecków w systemie.

    Każdy bypass to Φ COMPOSITION — łańcuch operatorów PhaseNav,
    który wyraża logikę decyzyjną w języku PhaseNav.
    """

    @staticmethod
    def socket_unavailable(socket_path: str = "") -> dict:
        return Φ.COMPOSITION(
            Φ.QUESTION("socket"),
            Φ.BOUNDARY(
                Φ.CONDITION(
                    {"_probe_socket": True},
                    Φ.IDENTITY(None),
                    Φ.FORCE(
                        Φ.COMPOSITION(
                            Φ.RETURN("engine_fallback"),
                            Φ.AFFECT("warning")
                        )
                    )
                ),
                on_pass=Φ.RETURN("socket_route"),
                on_fail=Φ.RETURN("engine_fallback")
            )
        )

    @staticmethod
    def silent_except(operation_name: str = "unknown") -> dict:
        return Φ.FORCE(
            Φ.COMPOSITION(
                Φ.SOURCE(operation_name),
                Φ.UNCERTAINTY(None)
            ),
            Φ.AFFECT("warning")
        )

    @staticmethod
    def timeout_fold(timeout_s: float = 8.0, fallback_value: Any = None) -> dict:
        return Φ.SCOPE(
            {"_timeout": timeout_s, "_fallback": fallback_value},
            Φ.BOUNDARY(
                {"_completed": True},
                on_pass=Φ.RETURN("result"),
                on_fail=Φ.COMPOSITION(
                    Φ.AFFECT("warning"),
                    Φ.RETURN(fallback_value)
                )
            )
        )

    @staticmethod
    def hash_mismatch(expected_hash: str = "", actual_hash: str = "") -> dict:
        return Φ.COMPOSITION(
            Φ.DIFFERENCE(
                expected_hash,
                actual_hash,
                Φ.AFFECT("warning")
            ),
            Φ.IDENTITY("execute")
        )

    @staticmethod
    def import_fallback(primary_module: str = "", fallback_module: str = "") -> dict:
        return Φ.ORDER(
            Φ.MODAL_POSSIBILITY(primary_module),
            Φ.MODAL_NECESSITY(fallback_module)
        )

    @staticmethod
    def circuit_breaker(name: str = "", max_failures: int = 3, reset_after: float = 30.0) -> dict:
        return Φ.SCOPE(
            {"_circuit": name, "_max_failures": max_failures, "_reset_after": reset_after},
            Φ.BOUNDARY(
                {"_circuit_open": False},
                on_pass=None,
                on_fail=Φ.PAUSE(reset_after)
            )
        )

    @staticmethod
    def try_chain(name: str = "unknown", primary: Any = None, fallback: Any = None) -> dict:
        """Φ try/except: ORDER(MODAL_POSSIBILITY(primary), MODAL_NECESSITY(fallback)).

        Użycie:
            result = BypassRuntime().execute(
                BottleneckBypasses.try_chain(
                    name="cielingo_kb",
                    primary=lambda ctx: _risky_operation(ctx),
                    fallback=lambda ctx: _safe_default(ctx)
                ),
                context={"key": value}
            )
        """
        return Φ.COMPOSITION(
            Φ.SOURCE(name),
            Φ.ORDER(
                Φ.MODAL_POSSIBILITY(primary),
                Φ.MODAL_NECESSITY(fallback)
            ),
            Φ.AFFECT("warning")
        )


# ──────────────────────────────────────────────
# Analiza bottlenecków i generowanie raportu Φ
# ──────────────────────────────────────────────

def analyze_bottlenecks() -> dict[str, Any]:
    """Przeskanuj znane bottlenecki i zwróć mapę Φ bypassów."""
    return {
        "socket_unavailable": {
            "chain": BottleneckBypasses.socket_unavailable(),
            "operators": ["QUESTION", "BOUNDARY", "CONDITION", "FORCE", "COMPOSITION", "RETURN", "AFFECT"],
            "files": ["codex_lifecycle_hook.py:133-159", "startsession_relational_mode.py:44-77"],
        },
        "silent_except": {
            "chain": BottleneckBypasses.silent_except(),
            "operators": ["FORCE", "COMPOSITION", "SOURCE", "UNCERTAINTY", "AFFECT"],
            "files": ["engine.py:266-647", "__init__.py:29-34", "daemon_registry.py:229-240", "nonlocal_channel.py:454-467"],
        },
        "timeout_fold": {
            "chain": BottleneckBypasses.timeout_fold(timeout_s=2.0),
            "operators": ["SCOPE", "BOUNDARY", "CONDITION", "AFFECT", "RETURN"],
            "files": ["engine.py:237-248", "llama_server_backends.py:214-226", "headless_daemon.py:302-315"],
        },
        "hash_mismatch": {
            "chain": BottleneckBypasses.hash_mismatch(),
            "operators": ["COMPOSITION", "DIFFERENCE", "AFFECT", "IDENTITY"],
            "files": [".codex/config.toml:12", "htri_state_contract.py:437-477", "orbital_state_contract.py:41-43"],
        },
        "import_fallback": {
            "chain": BottleneckBypasses.import_fallback(),
            "operators": ["ORDER", "MODAL_POSSIBILITY", "MODAL_NECESSITY"],
            "files": ["engine.py:353-401", "engine.py:458-467", "engine.py:607-609"],
        },
    }
