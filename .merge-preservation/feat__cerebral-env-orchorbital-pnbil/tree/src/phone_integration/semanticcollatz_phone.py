#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CIEL/0 – Semantic Computation Language (SCL)
Compact, production-ready semantic language and interpreter

Design goals:
- Human-first syntax focused on intention and meaning
- Deterministic core with optional stochastic/creative operators  
- Modular execution pipeline: INTENT → ANALYZE → PLAN → EXECUTE → VERIFY
- Extensible: new operators, rules, backends can be registered at runtime
- No external dependencies beyond Python stdlib + numpy (optional, graceful fallback)
"""
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import argparse
import dataclasses
import json
import math
import re
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

try:
    import numpy as _np
    _HAVE_NUMPY = True
except Exception:
    _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/phone_integration/semanticcollatz_phone.py:28 quiet except scope=<module> reason=no_log_no_raise")
    _HAVE_NUMPY = False
    _np = None

# =============================
# Core data structures
# =============================

@dataclass
class Emotions:
    """Emotional state representation"""
    love: float = 0.0
    joy: float = 0.0
    fear: float = 0.0
    anger: float = 0.0
    sadness: float = 0.0
    peace: float = 0.0
    
    def normalized(self) -> "Emotions":
        """Return normalized emotional state"""
        vals = [self.love, self.joy, self.fear, self.anger, self.sadness, self.peace]
        total = sum(max(0.0, v) for v in vals)
        if total <= 1e-12:
            return Emotions()
        scale = 1.0 / total
        return Emotions(*(max(0.0, v) * scale for v in vals))
    
    def as_dict(self) -> Dict[str, float]:
        return dataclasses.asdict(self)
    
    def copy(self) -> "Emotions":
        return Emotions(**self.as_dict())
    
    def amplify(self, which: str, delta: float) -> None:
        """Amplify specific emotion"""
        if hasattr(self, which):
            setattr(self, which, max(0.0, getattr(self, which)) + float(delta))
    
    def intensity(self) -> float:
        """Calculate emotional intensity"""
        vals = list(self.as_dict().values())
        return sum(vals) / (len(vals) or 1)

@dataclass
class SemanticConfig:
    """Semantic computation configuration"""
    coherence: float = 0.6
    superposition: float = 0.5
    entanglement: float = 0.4
    resonance: float = 0.0

@dataclass
class SemanticProgram:
    """Complete semantic program"""
    intent: str
    emotions: Emotions = field(default_factory=Emotions)
    input_value: complex = complex(1.0, 0.0)
    rules: List[str] = field(default_factory=list)
    pipeline: List[Tuple[str, Dict[str, Any]]] = field(default_factory=list)
    config: SemanticConfig = field(default_factory=SemanticConfig)
    
    def summary(self) -> str:
        return (
            f"Intent: {self.intent}\n"
            f"Emotions: {self.emotions.as_dict()}\n"
            f"Input: {self.input_value}\n"
            f"Rules: {self.rules}\n"
            f"Pipeline: {[name for name,_ in self.pipeline]}\n"
        )

@dataclass
class ExecutionTrace:
    """Execution trace for debugging and analysis"""
    steps: List[Dict[str, Any]] = field(default_factory=list)
    
    def log(self, **kwargs: Any) -> None:
        self.steps.append({"t": time.time(), **kwargs})
    
    def to_json(self) -> str:
        return json.dumps(self.steps, ensure_ascii=False, indent=2)

@dataclass
class ExecutionResult:
    """Final execution result"""
    final_state: complex
    metrics: Dict[str, float]
    trace: ExecutionTrace
    
    def summary(self) -> str:
        lines = [
            f"final_state = {self.final_state}",
            "metrics:",
        ]
        for k, v in self.metrics.items():
            lines.append(f"  - {k}: {v:.4f}")
        return "\n".join(lines)

# =============================
# Parser for SCL
# =============================

class SCLParser:
    """Parser for Semantic Computation Language"""
    
    kv_re = re.compile(r"^\s*([A-Za-z][A-Za-z0-9_-]*)\s*[:=]\s*(.+?)\s*$")
    
    def parse(self, text: str) -> SemanticProgram:
        """Parse SCL text into SemanticProgram"""
        sections = self._split_sections(text)
        intent = self._parse_intent(sections.get("INTENT", "").strip())
        emotions = self._parse_emotions(sections.get("EMOTIONS", ""))
        input_value = self._parse_input(sections.get("INPUT", ""))
        rules = self._parse_rules(sections.get("RULES", ""))
        pipeline = self._parse_pipeline(sections.get("PIPELINE", ""))
        cfg = SemanticConfig()
        
        # Initial resonance
        cfg.resonance = (_phi() if any("resonance=phi" in x[1].get("_raw", "") 
                                     for x in pipeline) else 0.0)
        
        return SemanticProgram(intent, emotions.normalized(), input_value, 
                             rules, pipeline, cfg)
    
    def _split_sections(self, text: str) -> Dict[str, str]:
        """Split text into sections"""
        out: Dict[str, List[str]] = {}
        current = None
        
        for raw in text.splitlines():
            line = raw.rstrip()
            if not line.strip():
                continue
                
            m = re.match(r"^([A-Z][A-Z0-9_ ]+):\s*$", line)
            if m:
                current = m.group(1).strip()
                out[current] = []
            elif current is not None:
                out[current].append(line)
                
        return {k: "\n".join(v) for k, v in out.items()}
    
    def _parse_intent(self, block: str) -> str:
        """Parse intent section"""
        if not block:
            return ""
        if block.startswith('"') and block.endswith('"'):
            return block.strip()[1:-1]
            
        m = self.kv_re.match(block)
        if m and m.group(1).lower() in ("intent", "value"):
            v = m.group(2).strip()
            return v.strip('"')
            
        return block.strip('"')
    
    def _parse_emotions(self, block: str) -> Emotions:
        """Parse emotions section"""
        e = Emotions()
        for line in block.splitlines():
            m = self.kv_re.match(line)
            if not m:
                continue
            key, val = m.group(1).lower(), m.group(2)
            try:
                setattr(e, key, float(val))
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/phone_integration/semanticcollatz_phone.py:194 quiet except scope=SCLParser._parse_emotions reason=pass")
                pass
        return e
    
    def _parse_input(self, block: str) -> complex:
        """Parse input section"""
        for line in block.splitlines():
            m = self.kv_re.match(line)
            if not m:
                continue
            if m.group(1).lower() == "value":
                raw = m.group(2).strip()
                try:
                    if raw.startswith("complex(") and raw.endswith(")"):
                        inside = raw[len("complex("):-1]
                        a, b = inside.split(",")
                        return complex(float(a), float(b))
                    if "j" in raw:
                        return complex(raw.replace(" ", ""))
                    return complex(float(raw), 0.0)
                except Exception:
                    _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/phone_integration/semanticcollatz_phone.py:214 quiet except scope=SCLParser._parse_input reason=pass")
                    pass
        return complex(1.0, 0.0)
    
    def _parse_rules(self, block: str) -> List[str]:
        """Parse rules section"""
        rules: List[str] = []
        for line in block.splitlines():
            s = line.strip()
            if s and not s.startswith("#"):
                rules.append(s)
        return rules
    
    def _parse_pipeline(self, block: str) -> List[Tuple[str, Dict[str, Any]]]:
        """Parse pipeline section"""
        stages: List[Tuple[str, Dict[str, Any]]] = []
        for line in block.splitlines():
            s = line.strip()
            if not s or s.startswith("#"):
                continue
                
            m = re.match(r"^([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.*)\)\s*$", s)
            if not m:
                continue
                
            name, argstr = m.group(1), m.group(2).strip()
            args = self._parse_args(argstr)
            args["_raw"] = s
            stages.append((name.lower(), args))
        return stages
    
    def _parse_args(self, argstr: str) -> Dict[str, Any]:
        """Parse pipeline arguments"""
        if not argstr:
            return {}
        out: Dict[str, Any] = {}
        parts = [p.strip() for p in argstr.split(",") if p.strip()]
        
        for p in parts:
            if "=" in p:
                k, v = p.split("=", 1)
                out[k.strip()] = _auto_cast(v.strip())
            else:
                out[p] = True
        return out

# =============================
# Virtual machine / Execution
# =============================

class SemanticVM:
    """Small, deterministic interpreter for SCL programs"""
    
    def __init__(self) -> None:
        self.ops: Dict[str, Callable] = {
            "collatz": self._op_collatz,
            "quantum": self._op_quantum,
            "ramanujan": self._op_ramanujan,
            "verify": self._op_verify,
        }
    
    def run(self, program: SemanticProgram) -> ExecutionResult:
        """Execute semantic program"""
        trace = ExecutionTrace()
        state = program.input_value

        # Apply rules
        self._apply_rules(program, trace)

        # Execute pipeline
        for name, args in program.pipeline:
            op = self.ops.get(name)
            if op is None:
                trace.log(stage=name, event="skip", reason="unknown_op")
                continue
            trace.log(stage=name, event="start", args=args)
            op(program, args, trace)
            trace.log(stage=name, event="done")

        # Aggregate metrics
        metrics = self._collect_metrics(program, trace)
        final_state = _trace_last_complex(trace) or state
        
        return ExecutionResult(final_state=final_state, metrics=metrics, trace=trace)
    
    def register(self, name: str, fn: Callable) -> None:
        """Register custom operator"""
        self.ops[name] = fn
    
    # ---- operators ----
    def _op_collatz(self, program: SemanticProgram, args: Dict[str, Any], trace: ExecutionTrace) -> None:
        """Collatz computation with emotional modulation"""
        seed = args.get("seed", "auto")
        if seed == "auto":
            seed = (abs(hash(program.intent)) % 10_000) + 1
        seed = int(seed)
        max_steps = int(args.get("max_steps", 120))

        n = seed
        path: List[int] = []
        for i in range(max_steps):
            path.append(n)
            if n == 1:
                break
            if n % 2 == 0:
                n //= 2
            else:
                n = 3 * n + 1
            
            # Emotional modulation
            emo = program.emotions.normalized()
            modulation = 1.0 + 0.05 * (emo.love + emo.joy) - 0.03 * (emo.fear + emo.sadness + emo.anger)
            n = max(1, int(n * max(0.9, min(1.1, modulation))))
        
        path.append(1)
        trace.log(stage="collatz", path_len=len(path), seed=seed, last=n)
        
        # Store as complex state
        c = complex(float(len(path)), float(max(path) if path else 1))
        trace.log(stage="collatz", complex_state=str(c))
    
    def _op_quantum(self, program: SemanticProgram, args: Dict[str, Any], trace: ExecutionTrace) -> None:
        """Quantum-inspired computation"""
        cfg = program.config
        emo = program.emotions.normalized()
        
        def auto_or(name: str, default: float) -> float:
            v = args.get(name, "auto")
            if v == "auto":
                if name == "coherence":
                    return max(0.3, min(1.0, 0.5 + 0.5 * (emo.love + emo.joy - emo.fear)))
                if name == "superposition":
                    return max(0.2, min(1.0, 0.3 + 0.7 * _lexical_diversity(program.intent)))
                if name == "entanglement":
                    return max(0.2, min(1.0, 0.4 + 0.3 * emo.intensity()))
            try:
                return float(v)
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/phone_integration/semanticcollatz_phone.py:351 quiet except scope=SemanticVM._op_quantum.auto_or reason=return default")
                return default
        
        cfg.coherence = auto_or("coherence", cfg.coherence)
        cfg.superposition = auto_or("superposition", cfg.superposition)
        cfg.entanglement = auto_or("entanglement", cfg.entanglement)
        
        trace.log(stage="quantum", coherence=cfg.coherence, superposition=cfg.superposition, 
                 entanglement=cfg.entanglement)
        
        # Produce complex state
        amp = cfg.coherence * (0.7 + 0.3 * cfg.superposition)
        phase = 2 * math.pi * (cfg.entanglement * 0.25)
        c = amp * complex(math.cos(phase), math.sin(phase))
        trace.log(stage="quantum", complex_state=str(c))
    
    def _op_ramanujan(self, program: SemanticProgram, args: Dict[str, Any], trace: ExecutionTrace) -> None:
        """Ramanujan mathematical resonance"""
        resonance = args.get("resonance", program.config.resonance)
        if resonance == "phi":
            resonance = _phi()
        try:
            resonance = float(resonance)
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/phone_integration/semanticcollatz_phone.py:374 quiet except scope=SemanticVM._op_ramanujan reason=assign_fallback")
            resonance = 1.0
            
        gain = float(args.get("gain", 1.0))
        
        # Combine with intent hash for stable-but-unique phase
        h = (abs(hash(program.intent)) % 10_000) / 10_000.0
        phase = 2 * math.pi * (resonance % 1.0) * (0.5 + 0.5 * h)
        amp = gain * (0.9 + 0.1 * _sentiment(program.intent))
        c = amp * complex(math.cos(phase), math.sin(phase))
        
        trace.log(stage="ramanujan", resonance=resonance, gain=gain, complex_state=str(c))
    
    def _op_verify(self, program: SemanticProgram, args: Dict[str, Any], trace: ExecutionTrace) -> None:
        """Truth-lock verification"""
        cfg = program.config
        emo = program.emotions.normalized()
        
        # Internal evidence scoring
        evidence = (0.5 * cfg.coherence + 
                   0.3 * (1.0 - abs(emo.fear - emo.love)) + 
                   0.2 * (0.6 + 0.4 * _sentiment(program.intent)))
        contradictions = max(0.0, 0.4 * (emo.anger - emo.peace))
        completeness = max(0.0, min(1.0, evidence - contradictions))
        
        state = "evidence_verified" if completeness >= float(args.get("threshold", 0.7)) else "insufficient_evidence"
        
        trace.log(stage="verify", completeness=completeness, state=state)
        
        # Store decision as complex flag
        c = complex(completeness, 1.0 if state == "evidence_verified" else 0.0)
        trace.log(stage="verify", complex_state=str(c))
    
    # ---- utilities ----
    def _apply_rules(self, program: SemanticProgram, trace: ExecutionTrace) -> None:
        """Apply semantic rules"""
        for rule in program.rules:
            s = rule.strip()
            
            # Rule: if contains("word") then amplify emotion X by +Y
            m = re.match(r'^if\s+contains\("(.+?)"\)\s+then\s+amplify\s+emotion\s+([a-z]+)\s+by\s*([+\-]?[0-9.]+)', s, re.IGNORECASE)
            if m:
                word, emo, delta = m.group(1), m.group(2).lower(), float(m.group(3))
                if word.lower() in program.intent.lower():
                    program.emotions.amplify(emo, delta)
                    trace.log(stage="rules", rule="contains→amplify", matched=word, emotion=emo, delta=delta)
                    continue
            
            # Rule: if sentiment >= X then set coherence to Y
            m2 = re.match(r'^if\s+sentiment\s*([><=]{1,2})\s*([0-9.]+)\s+then\s+set\s+coherence\s+to\s*([0-9.]+)$', s, re.IGNORECASE)
            if m2:
                op, thr, val = m2.group(1), float(m2.group(2)), float(m2.group(3))
                sent = _sentiment(program.intent)
                ok = (sent >= thr) if op in (">=", ">") else (sent <= thr) if op in ("<=", "<") else (abs(sent - thr) < 1e-9)
                if ok:
                    program.config.coherence = val
                    trace.log(stage="rules", rule="sentiment→coherence", op=op, thr=thr, coherence=val)
    
    def _collect_metrics(self, program: SemanticProgram, trace: ExecutionTrace) -> Dict[str, float]:
        """Collect execution metrics"""
        emo = program.emotions.normalized()
        coherence = program.config.coherence
        
        collatz_len = _trace_pick(trace, "collatz", "path_len") or 0
        verify_state = _trace_pick(trace, "verify", "state") or "insufficient_evidence"
        completeness = float(_trace_pick(trace, "verify", "completeness") or 0.0)
        
        return {
            "emotional_balance": 1.0 - abs(emo.love - emo.fear),
            "emotional_diversity": sum(1 for v in emo.as_dict().values() if v > 0.05) / 6.0,
            "coherence": coherence,
            "collatz_path_length": float(collatz_len),
            "truth_completeness": completeness,
            "truth_verified": 1.0 if verify_state == "evidence_verified" else 0.0,
        }

# =============================
# Helpers
# =============================

def _phi() -> float:
    """Golden ratio"""
    return (1 + math.sqrt(5.0)) / 2.0

def _lexical_diversity(text: str) -> float:
    """Calculate lexical diversity"""
    ws = [w.lower() for w in re.findall(r"[A-Za-zÀ-ž0-9]+", text)]
    return (len(set(ws)) / max(1, len(ws))) if ws else 0.0

def _sentiment(text: str) -> float:
    """Simple sentiment analysis"""
    pos = {"love", "peace", "harmony", "cooperation", "joy", "trust", "compassion", 
           "sprawczości", "współpracy"}
    neg = {"fear", "anger", "war", "conflict", "hate", "despair"}
    
    t = text.lower()
    p = sum(t.count(w) for w in pos)
    n = sum(t.count(w) for w in neg)
    tot = p + n
    return p / tot if tot else 0.5

def _auto_cast(v: str) -> Any:
    """Auto-cast string values"""
    v = v.strip()
    if v.lower() in ("true", "false"):
        return v.lower() == "true"
    try:
        if re.match(r"^[+-]?[0-9]+$", v):
            return int(v)
        if re.match(r"^[+-]?[0-9]*\.[0-9]+$", v):
            return float(v)
        if v.startswith('"') and v.endswith('"'):
            return v[1:-1]
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/phone_integration/semanticcollatz_phone.py:487 quiet except scope=_auto_cast reason=pass")
        pass
    return v

def _trace_pick(trace: ExecutionTrace, stage: str, key: str) -> Optional[Any]:
    """Pick value from trace"""
    for rec in reversed(trace.steps):
        if rec.get("stage") == stage and key in rec:
            return rec[key]
    return None

def _trace_last_complex(trace: ExecutionTrace) -> Optional[complex]:
    """Get last complex state from trace"""
    for rec in reversed(trace.steps):
        s = rec.get("complex_state")
        if isinstance(s, str) and s.startswith("("):
            try:
                return complex(s)
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/phone_integration/semanticcollatz_phone.py:505 quiet except scope=_trace_last_complex reason=continue")
                continue
    return None

# =============================
# Python API (builder)
# =============================

class ProgramBuilder:
    """Programmatic SCL builder"""
    
    def __init__(self, intent: str) -> None:
        self._intent = intent
        self._emotions = Emotions()
        self._rules: List[str] = []
        self._pipeline: List[Tuple[str, Dict[str, Any]]] = []
        self._input = complex(1.0, 0.0)
    
    def emotions(self, **kwargs: float) -> "ProgramBuilder":
        for k, v in kwargs.items():
            if hasattr(self._emotions, k):
                setattr(self._emotions, k, float(v))
        return self
    
    def rule(self, text: str) -> "ProgramBuilder":
        self._rules.append(text)
        return self
    
    def input(self, value: Union[float, complex]) -> "ProgramBuilder":
        self._input = complex(value)
        return self
    
    def stage(self, name: str, **kwargs: Any) -> "ProgramBuilder":
        self._pipeline.append((name.lower(), {**kwargs}))
        return self
    
    def build(self) -> SemanticProgram:
        return SemanticProgram(
            intent=self._intent,
            emotions=self._emotions.normalized(),
            input_value=self._input,
            rules=list(self._rules),
            pipeline=list(self._pipeline),
        )

# =============================
# CLI
# =============================

def _run_cli(args: argparse.Namespace) -> int:
    """Run CLI interface"""
    if args.file:
        text = open(args.file, "r", encoding="utf-8").read()
        program = SCLParser().parse(text)
    else:
        # Default demo program
        demo = (
            'INTENT: "Zharmonizuj system poprzez współpracę i zaufanie."\n\n'
            "EMOTIONS:\n  love=0.6\n  joy=0.2\n  fear=0.05\n\n"
            "RULES:\n  if contains(\"współpracę\") then amplify emotion love by +0.10\n"
            "PIPELINE:\n  collatz(seed=auto, max_steps=90)\n  quantum(coherence=auto, superposition=auto, entanglement=auto)\n  ramanujan(resonance=phi, gain=1.0)\n  verify(truth_lock=true, threshold=0.7)\n"
        )
        program = SCLParser().parse(demo)
    
    vm = SemanticVM()
    result = vm.run(program)
    
    if args.pretty:
        print(program.summary())
        print("-" * 60)
        print(result.summary())
    else:
        print(json.dumps({
            "program": dataclasses.asdict(program),
            "result": {
                "final_state": str(result.final_state),
                "metrics": result.metrics,
                "trace": result.trace.steps if args.trace else []
            }
        }, ensure_ascii=False, indent=2))
    
    return 0

def main(argv: Optional[List[str]] = None) -> int:
    """Main CLI entry point"""
    p = argparse.ArgumentParser(description="CIEL/0 – Semantic Computation Language (SCL)")
    p.add_argument("--file", type=str, default=None, help="Path to .scl program file")
    p.add_argument("--pretty", action="store_true", help="Pretty human-readable output")
    p.add_argument("--trace", action="store_true", help="Include full execution trace in JSON output")
    args = p.parse_args(argv)
    return _run_cli(args)

if __name__ == "__main__":
    raise SystemExit(main())
#
# NOEMA_QUARANTINED_APPENDIX:     #!/usr/bin/env python3
#
# NOEMA_QUARANTINED_APPENDIX: -- coding: utf-8 --
#
# NOEMA_QUARANTINED_APPENDIX: """ CIEL/0 Unified Bridge (SCL ↔ Core)
#
# NOEMA_QUARANTINED_APPENDIX: Bridges the Semantic Computation Language (SCL) with the physical/mathematical CIEL0Core simulation. SCL intentions/emotions/rules modulate core parameters and drive time evolution; core metrics can be fed back into the SCL trace.
#
# NOEMA_QUARANTINED_APPENDIX: Requirements
#
# NOEMA_QUARANTINED_APPENDIX: ciel_semantic_language.py providing: SCLParser, SemanticVM, ProgramBuilder, SemanticProgram, ExecutionTrace, ExecutionResult, Emotions.
#
# NOEMA_QUARANTINED_APPENDIX: A CIEL0Core implementation providing fields and methods used below (see placeholders in try/except import).
#
#
# NOEMA_QUARANTINED_APPENDIX: Usage
#
# NOEMA_QUARANTINED_APPENDIX: python ciel0_bridge.py --file plan.scl --steps 24 --dt 0.05 --pretty
#
# NOEMA_QUARANTINED_APPENDIX: SCL operator extension
#
# NOEMA_QUARANTINED_APPENDIX: This bridge registers a new SCL pipeline stage: link_to_core(steps=20, dt=0.05, visualize=false) which runs the CIEL0Core for the given number of steps and logs metrics into the SCL trace. If visualize=true, figures are shown at the end.
#
# NOEMA_QUARANTINED_APPENDIX: Mapping (default heuristics)
#
# NOEMA_QUARANTINED_APPENDIX: Emotions → Core couplings (bounded, smooth): lambda_1  ← 0.05 + 0.25*(love + joy) - 0.15*(fear + anger) lambda_3  ← 0.05 + 0.20*(peace + love) - 0.10*(sadness) lambda_2  ← 0.03 + 0.15*diversity(emotions)
#
# NOEMA_QUARANTINED_APPENDIX: SCL quantum config → simulation step size and nonlinearity: dt        ← base_dt * clamp(0.75, 1.25, 1.2 - coherence/2 + superposition/4) nonlin_gain (internal) ← 0.8 + 0.4*entanglement
#
# NOEMA_QUARANTINED_APPENDIX: Ramanujan resonance: If SCL ramanujan(resonance=phi), we increase phase coupling by ~10%.
#
# NOEMA_QUARANTINED_APPENDIX: Rules can also tweak starting fields (e.g., boost I_field magnitude or seed phase) via simple text triggers.
#
# NOEMA_QUARANTINED_APPENDIX: All heuristics are deterministic and bounded; adjust freely. """ from future import annotations
#
# NOEMA_QUARANTINED_APPENDIX: import argparse import math from dataclasses import dataclass from typing import Any, Dict, Optional, Tuple, List
#
# NOEMA_QUARANTINED_APPENDIX: -------------------------
#
# NOEMA_QUARANTINED_APPENDIX: Imports with fallbacks
#
# NOEMA_QUARANTINED_APPENDIX: -------------------------
#
# NOEMA_QUARANTINED_APPENDIX: try: # Preferred names from the provided files from ciel_semantic_language import ( SCLParser, SemanticVM, ProgramBuilder, SemanticProgram, ExecutionTrace, ) except Exception as _e:  # pragma: no cover raise ImportError( "Missing ciel_semantic_language.py with SCLParser/SemanticVM. " "Place it next to this file." ) from _e
#
# NOEMA_QUARANTINED_APPENDIX: try: # Expect a CIEL0Core class with fields/methods used below from main import CIEL0Core  # when run inside a monolithic file except Exception: try: from ciel_unified_core import CIEL0Core  # optional module name except Exception as _e: # Minimal placeholder error to guide the user clearly raise ImportError( "CIEL0Core not found. Ensure your CIEL/0 core class is importable " "as CIEL0Core (either in main or a module)." ) from _e
#
# NOEMA_QUARANTINED_APPENDIX: -------------------------
#
# NOEMA_QUARANTINED_APPENDIX: Utility helpers
#
# NOEMA_QUARANTINED_APPENDIX: -------------------------
#
# NOEMA_QUARANTINED_APPENDIX: def _clamp(v: float, lo: float, hi: float) -> float: return max(lo, min(hi, v))
#
# NOEMA_QUARANTINED_APPENDIX: def _emo_diversity(emodict: Dict[str, float]) -> float: """Fraction of emotions with noticeable (>0.05) intensity.""" if not emodict: return 0.0 k = sum(1 for x in emodict.values() if x > 0.05) return k / float(len(emodict))
#
# NOEMA_QUARANTINED_APPENDIX: def _intent_hash_phase(text: str) -> float: """Stable phase in [0, 2π) derived from intent hash.""" h = (abs(hash(text)) % 10_000) / 10_000.0 return 2.0 * math.pi * h
#
# NOEMA_QUARANTINED_APPENDIX: -------------------------
#
# NOEMA_QUARANTINED_APPENDIX: Bridge
#
# NOEMA_QUARANTINED_APPENDIX: -------------------------
#
# NOEMA_QUARANTINED_APPENDIX: @dataclass class BridgeConfig: base_dt: float = 0.05 verbose: bool = True visualize: bool = False
#
# NOEMA_QUARANTINED_APPENDIX: class CIEL0Bridge: """Connects SCL programs to a CIEL0Core instance and drives co-evolution."""
#
# NOEMA_QUARANTINED_APPENDIX: def __init__(self, core: Optional[CIEL0Core] = None, vm: Optional[SemanticVM] = None,
# NOEMA_QUARANTINED_APPENDIX:              cfg: Optional[BridgeConfig] = None) -> None:
# NOEMA_QUARANTINED_APPENDIX:     self.core = core or CIEL0Core(grid_size=32)
# NOEMA_QUARANTINED_APPENDIX:     self.vm = vm or SemanticVM()
# NOEMA_QUARANTINED_APPENDIX:     self.cfg = cfg or BridgeConfig()
#
# NOEMA_QUARANTINED_APPENDIX:     # Register extended SCL operator
# NOEMA_QUARANTINED_APPENDIX:     self.vm.register("link_to_core", self._op_link_to_core)
#
# NOEMA_QUARANTINED_APPENDIX:     # internal state used by the extended operator
# NOEMA_QUARANTINED_APPENDIX:     self._last_metrics: Dict[str, float] = {}
#
# NOEMA_QUARANTINED_APPENDIX: # ------------------
# NOEMA_QUARANTINED_APPENDIX: # Public API
# NOEMA_QUARANTINED_APPENDIX: # ------------------
# NOEMA_QUARANTINED_APPENDIX: def run_scl(self, program: SemanticProgram) -> Tuple[SemanticProgram, Dict[str, Any]]:
# NOEMA_QUARANTINED_APPENDIX:     """Execute the SCL program (with the bridge op available)."""
# NOEMA_QUARANTINED_APPENDIX:     result = self.vm.run(program)
# NOEMA_QUARANTINED_APPENDIX:     return program, {"metrics": result.metrics, "trace": result.trace}
#
# NOEMA_QUARANTINED_APPENDIX: def run_file(self, path: str) -> Tuple[SemanticProgram, Dict[str, Any]]:
# NOEMA_QUARANTINED_APPENDIX:     prog = SCLParser().parse(open(path, "r", encoding="utf-8").read())
# NOEMA_QUARANTINED_APPENDIX:     self._prime_core_from_program(prog)
# NOEMA_QUARANTINED_APPENDIX:     return self.run_scl(prog)
#
# NOEMA_QUARANTINED_APPENDIX: # ------------------
# NOEMA_QUARANTINED_APPENDIX: # SCL extended operator
# NOEMA_QUARANTINED_APPENDIX: # ------------------
# NOEMA_QUARANTINED_APPENDIX: def _op_link_to_core(self, program: SemanticProgram, args: Dict[str, Any], trace: ExecutionTrace) -> None:
# NOEMA_QUARANTINED_APPENDIX:     """SCL stage that runs the physical core for N steps with current mapping."""
# NOEMA_QUARANTINED_APPENDIX:     steps = int(args.get("steps", 20))
# NOEMA_QUARANTINED_APPENDIX:     visualize = bool(args.get("visualize", self.cfg.visualize))
#
# NOEMA_QUARANTINED_APPENDIX:     # Derive simulation dt from SCL config
# NOEMA_QUARANTINED_APPENDIX:     dt = float(args.get("dt", self.cfg.base_dt))
# NOEMA_QUARANTINED_APPENDIX:     dt = self._derive_dt_from_scl(program, dt)
#
# NOEMA_QUARANTINED_APPENDIX:     # Update core params from SCL intent/emotions before running
# NOEMA_QUARANTINED_APPENDIX:     self._apply_emotion_mapping(program)
# NOEMA_QUARANTINED_APPENDIX:     self._apply_rule_seeding(program)
# NOEMA_QUARANTINED_APPENDIX:     self._apply_resonance_mapping(program)
#
# NOEMA_QUARANTINED_APPENDIX:     # Run the core
# NOEMA_QUARANTINED_APPENDIX:     metrics_history = {"resonance_mean": [], "mass_mean": [], "intention_strength": [], "coherence": []}
# NOEMA_QUARANTINED_APPENDIX:     if self.cfg.verbose:
# NOEMA_QUARANTINED_APPENDIX:         print(f"[bridge] Running core: steps={steps}, dt≈{dt:.4f}")
# NOEMA_QUARANTINED_APPENDIX:     for _ in range(steps):
# NOEMA_QUARANTINED_APPENDIX:         self.core.evolution_step(dt=dt)
# NOEMA_QUARANTINED_APPENDIX:         # collect compatible metrics (names assumed from a typical core impl)
# NOEMA_QUARANTINED_APPENDIX:         metrics_history["resonance_mean"].append(float((self.core.R_field).mean()))
# NOEMA_QUARANTINED_APPENDIX:         metrics_history["mass_mean"].append(float((self.core.mass_field).mean()))
# NOEMA_QUARANTINED_APPENDIX:         metrics_history["intention_strength"].append(float(abs(self.core.I_field).mean()))
# NOEMA_QUARANTINED_APPENDIX:         metrics_history["coherence"].append(float((self.core.R_field).sum()))
#
# NOEMA_QUARANTINED_APPENDIX:     # Persist last metrics for follow-up operators
# NOEMA_QUARANTINED_APPENDIX:     self._last_metrics = {k: (v[-1] if v else 0.0) for k, v in metrics_history.items()}
#
# NOEMA_QUARANTINED_APPENDIX:     # Log into SCL trace
# NOEMA_QUARANTINED_APPENDIX:     trace.log(stage="link_to_core", **{f"core_{k}": v[-1] for k, v in metrics_history.items()})
#
# NOEMA_QUARANTINED_APPENDIX:     # Visualize if requested and available
# NOEMA_QUARANTINED_APPENDIX:     if visualize:
# NOEMA_QUARANTINED_APPENDIX:         try:
# NOEMA_QUARANTINED_APPENDIX:             fig1 = self.core.visualize_fields()
# NOEMA_QUARANTINED_APPENDIX:             fig2 = self.core.plot_evolution(metrics_history)
# NOEMA_QUARANTINED_APPENDIX:             for fig in (fig1, fig2):
# NOEMA_QUARANTINED_APPENDIX:                 fig.show()
# NOEMA_QUARANTINED_APPENDIX:         except Exception:
# NOEMA_QUARANTINED_APPENDIX:             pass
#
# NOEMA_QUARANTINED_APPENDIX: # ------------------
# NOEMA_QUARANTINED_APPENDIX: # Mappings (SCL → Core)
# NOEMA_QUARANTINED_APPENDIX: # ------------------
# NOEMA_QUARANTINED_APPENDIX: def _prime_core_from_program(self, program: SemanticProgram) -> None:
# NOEMA_QUARANTINED_APPENDIX:     """Apply one-time initialization mapping from SCL before any run()."""
# NOEMA_QUARANTINED_APPENDIX:     self._apply_emotion_mapping(program)
# NOEMA_QUARANTINED_APPENDIX:     self._apply_rule_seeding(program)
# NOEMA_QUARANTINED_APPENDIX:     self._apply_resonance_mapping(program)
#
# NOEMA_QUARANTINED_APPENDIX: def _apply_emotion_mapping(self, program: SemanticProgram) -> None:
# NOEMA_QUARANTINED_APPENDIX:     e = program.emotions.normalized().as_dict()
# NOEMA_QUARANTINED_APPENDIX:     div = _emo_diversity(e)
# NOEMA_QUARANTINED_APPENDIX:     p = self.core.params
#
# NOEMA_QUARANTINED_APPENDIX:     lam1 = 0.05 + 0.25 * (e.get("love", 0.0) + e.get("joy", 0.0)) - 0.15 * (e.get("fear", 0.0) + e.get("anger", 0.0))
# NOEMA_QUARANTINED_APPENDIX:     lam3 = 0.05 + 0.20 * (e.get("peace", 0.0) + e.get("love", 0.0)) - 0.10 * (e.get("sadness", 0.0))
# NOEMA_QUARANTINED_APPENDIX:     lam2 = 0.03 + 0.15 * div
#
# NOEMA_QUARANTINED_APPENDIX:     p.lambda_1 = _clamp(lam1, 0.01, 0.6)
# NOEMA_QUARANTINED_APPENDIX:     p.lambda_3 = _clamp(lam3, 0.01, 0.5)
# NOEMA_QUARANTINED_APPENDIX:     p.lambda_2 = _clamp(lam2, 0.01, 0.5)
#
# NOEMA_QUARANTINED_APPENDIX: def _apply_rule_seeding(self, program: SemanticProgram) -> None:
# NOEMA_QUARANTINED_APPENDIX:     # Simple text triggers to alter initial fields gently
# NOEMA_QUARANTINED_APPENDIX:     intent = program.intent.lower()
# NOEMA_QUARANTINED_APPENDIX:     phase = _intent_hash_phase(program.intent)
#
# NOEMA_QUARANTINED_APPENDIX:     # Phase imprint on I_field
# NOEMA_QUARANTINED_APPENDIX:     self.core.I_field *= complex(math.cos(phase), math.sin(phase))
#
# NOEMA_QUARANTINED_APPENDIX:     # If intent mentions cooperation/harmony → strengthen central Gaussian
# NOEMA_QUARANTINED_APPENDIX:     if any(w in intent for w in ("współpr", "cooperat", "harmony", "harmonia")):
# NOEMA_QUARANTINED_APPENDIX:         self.core.I_field *= 1.05
# NOEMA_QUARANTINED_APPENDIX:         self.core.tau_field *= 0.95  # slightly reduce phase lag
#
# NOEMA_QUARANTINED_APPENDIX:     # If intent mentions conflict/fear → increase temporal damping a bit
# NOEMA_QUARANTINED_APPENDIX:     if any(w in intent for w in ("conflict", "wojna", "fear", "lęk")):
# NOEMA_QUARANTINED_APPENDIX:         self.core.tau_field *= 0.9
#
# NOEMA_QUARANTINED_APPENDIX: def _apply_resonance_mapping(self, program: SemanticProgram) -> None:
# NOEMA_QUARANTINED_APPENDIX:     # If any ramanujan-stage with phi resonance was declared, reinforce lambda_3 a bit
# NOEMA_QUARANTINED_APPENDIX:     for name, args in program.pipeline:
# NOEMA_QUARANTINED_APPENDIX:         if name == "ramanujan":
# NOEMA_QUARANTINED_APPENDIX:             res = args.get("resonance")
# NOEMA_QUARANTINED_APPENDIX:             if isinstance(res, str) and res.lower() == "phi":
# NOEMA_QUARANTINED_APPENDIX:                 self.core.params.lambda_3 = _clamp(self.core.params.lambda_3 * 1.1, 0.01, 0.6)
#
# NOEMA_QUARANTINED_APPENDIX: def _derive_dt_from_scl(self, program: SemanticProgram, base_dt: float) -> float:
# NOEMA_QUARANTINED_APPENDIX:     cfg = program.config
# NOEMA_QUARANTINED_APPENDIX:     # scale dt by coherence/superposition; more coherence → smaller dt (stabler, finer steps)
# NOEMA_QUARANTINED_APPENDIX:     scale = 1.2 - 0.5 * _clamp(cfg.coherence, 0.0, 1.0) + 0.25 * _clamp(cfg.superposition, 0.0, 1.0)
# NOEMA_QUARANTINED_APPENDIX:     return _clamp(base_dt * scale, 0.01, 0.25)
#
# NOEMA_QUARANTINED_APPENDIX: -------------------------
#
# NOEMA_QUARANTINED_APPENDIX: CLI
#
# NOEMA_QUARANTINED_APPENDIX: -------------------------
#
# NOEMA_QUARANTINED_APPENDIX: def _run_cli(args: argparse.Namespace) -> int: bridge = CIEL0Bridge() if args.file: program = SCLParser().parse(open(args.file, "r", encoding="utf-8").read()) else: # Minimal embedded demo demo = ( 'INTENT: "Synchronizuj świadomość i materię przez rezonans złotej proporcji."\n\n' 'EMOTIONS:\n  love=0.55\n  joy=0.20\n  fear=0.05\n  peace=0.15\n\n' 'RULES:\n  if contains("rezonans") then amplify emotion love by +0.05\n\n' 'PIPELINE:\n' '  collatz(seed=auto, max_steps=60)\n' '  quantum(coherence=auto, superposition=auto, entanglement=auto)\n' '  ramanujan(resonance=phi, gain=1.0)\n' '  link_to_core(steps=20, dt=0.05, visualize=false)\n' ) program = SCLParser().parse(demo)
#
# NOEMA_QUARANTINED_APPENDIX: # Prime core (initial mapping) and run the SCL program, which will in turn run the core
# NOEMA_QUARANTINED_APPENDIX: bridge._prime_core_from_program(program)
# NOEMA_QUARANTINED_APPENDIX: prog, out = bridge.run_scl(program)
#
# NOEMA_QUARANTINED_APPENDIX: # Pretty print
# NOEMA_QUARANTINED_APPENDIX: if args.pretty:
# NOEMA_QUARANTINED_APPENDIX:     print("\n=== SCL Metrics ===")
# NOEMA_QUARANTINED_APPENDIX:     for k, v in out["metrics"].items():
# NOEMA_QUARANTINED_APPENDIX:         print(f"  {k:24s}: {v:.4f}")
# NOEMA_QUARANTINED_APPENDIX:     print("\n=== Last Core Metrics ===")
# NOEMA_QUARANTINED_APPENDIX:     if bridge._last_metrics:
# NOEMA_QUARANTINED_APPENDIX:         for k, v in bridge._last_metrics.items():
# NOEMA_QUARANTINED_APPENDIX:             print(f"  {k:24s}: {v:.6f}")
# NOEMA_QUARANTINED_APPENDIX: else:
# NOEMA_QUARANTINED_APPENDIX:     import json
# NOEMA_QUARANTINED_APPENDIX:     print(json.dumps({
# NOEMA_QUARANTINED_APPENDIX:         "scl_metrics": out["metrics"],
# NOEMA_QUARANTINED_APPENDIX:         "core_metrics": bridge._last_metrics,
# NOEMA_QUARANTINED_APPENDIX:     }, ensure_ascii=False, indent=2))
#
# NOEMA_QUARANTINED_APPENDIX: return 0
#
# NOEMA_QUARANTINED_APPENDIX: def main(argv: Optional[List[str]] = None) -> int: p = argparse.ArgumentParser(description="CIEL/0 Unified Bridge (SCL ↔ Core)") p.add_argument("--file", type=str, default=None, help="Path to .scl program file") p.add_argument("--steps", type=int, default=20, help="Default steps for link_to_core when omitted") p.add_argument("--dt", type=float, default=0.05, help="Base dt (scaled by coherence/superposition)") p.add_argument("--pretty", action="store_true", help="Pretty console output") args = p.parse_args(argv) return _run_cli(args)
#
# NOEMA_QUARANTINED_APPENDIX: if name == "main":  # pragma: no cover raise SystemExit(main())
#
# NOEMA_QUARANTINED_APPENDIX: #!/usr/bin/env python3
#
# NOEMA_QUARANTINED_APPENDIX: -- coding: utf-8 --
#
# NOEMA_QUARANTINED_APPENDIX: """ CIEL/0 – Semantic Computation Language (SCL)
#
# NOEMA_QUARANTINED_APPENDIX: A compact, production-ready semantic language and interpreter in Python.
#
# NOEMA_QUARANTINED_APPENDIX: Design goals
#
# NOEMA_QUARANTINED_APPENDIX: Human-first syntax focused on intention and meaning.
#
# NOEMA_QUARANTINED_APPENDIX: Deterministic core with optional stochastic/creative operators.
#
# NOEMA_QUARANTINED_APPENDIX: Modular execution pipeline: INTENT → ANALYZE → PLAN → EXECUTE → VERIFY.
#
# NOEMA_QUARANTINED_APPENDIX: Extensible: new operators, rules, backends can be registered at runtime.
#
# NOEMA_QUARANTINED_APPENDIX: No external dependencies beyond the Python stdlib + numpy (optional, graceful fallback).
#
#
# NOEMA_QUARANTINED_APPENDIX: This module exposes two layers:
#
# NOEMA_QUARANTINED_APPENDIX: 1. High-level DSL (text) parsed by SCLParser → SemanticProgram → executed by SemanticVM.
#
#
# NOEMA_QUARANTINED_APPENDIX: 2. Python API for programmatic construction (ProgramBuilder).
#
#
#
# NOEMA_QUARANTINED_APPENDIX: Example (DSL)
#
# NOEMA_QUARANTINED_APPENDIX: SCL programs are whitespace-insensitive, INI-like with blocks.
#
# NOEMA_QUARANTINED_APPENDIX: INTENT: "Zharmonizuj system ekonomiczny na bazie współpracy i sprawczości."
#
# NOEMA_QUARANTINED_APPENDIX: EMOTIONS:
# NOEMA_QUARANTINED_APPENDIX:   love = 0.55
# NOEMA_QUARANTINED_APPENDIX:   joy  = 0.25
# NOEMA_QUARANTINED_APPENDIX:   fear = 0.05
#
# NOEMA_QUARANTINED_APPENDIX: INPUT:
# NOEMA_QUARANTINED_APPENDIX:   value = 1.0
#
# NOEMA_QUARANTINED_APPENDIX: RULES:
# NOEMA_QUARANTINED_APPENDIX:   if contains("współpracy") then amplify emotion love by +0.10
# NOEMA_QUARANTINED_APPENDIX:   if sentiment >= 0.6 then set coherence to 0.85
#
# NOEMA_QUARANTINED_APPENDIX: PIPELINE:
# NOEMA_QUARANTINED_APPENDIX:   collatz(seed=auto, max_steps=120)
# NOEMA_QUARANTINED_APPENDIX:   quantum(coherence=auto, superposition=auto, entanglement=auto)
# NOEMA_QUARANTINED_APPENDIX:   ramanujan(resonance=phi)
# NOEMA_QUARANTINED_APPENDIX:   verify(truth_lock=true)
#
# NOEMA_QUARANTINED_APPENDIX: Run from Python:
#
# NOEMA_QUARANTINED_APPENDIX: from ciel_semantic_language import SCLParser, SemanticVM
# NOEMA_QUARANTINED_APPENDIX: program = SCLParser().parse(open('plan.scl').read())
# NOEMA_QUARANTINED_APPENDIX: result = SemanticVM().run(program)
# NOEMA_QUARANTINED_APPENDIX: print(result.summary())
#
# NOEMA_QUARANTINED_APPENDIX: Run from CLI:
#
# NOEMA_QUARANTINED_APPENDIX: python ciel_semantic_language.py --file plan.scl --pretty
#
# NOEMA_QUARANTINED_APPENDIX: """ from future import annotations
#
# NOEMA_QUARANTINED_APPENDIX: import argparse import dataclasses import json import math import re import time from dataclasses import dataclass, field from typing import Any, Callable, Dict, List, Optional, Tuple, Union
#
# NOEMA_QUARANTINED_APPENDIX: try: import numpy as _np  # optional; used for small numerics _HAVE_NUMPY = True except Exception:  # pragma: no cover _HAVE_NUMPY = False _np = None  # type: ignore
#
# NOEMA_QUARANTINED_APPENDIX: -----------------------------
#
# NOEMA_QUARANTINED_APPENDIX: Core data structures
#
# NOEMA_QUARANTINED_APPENDIX: -----------------------------
#
# NOEMA_QUARANTINED_APPENDIX: @dataclass class Emotions: love: float = 0.0 joy: float = 0.0 fear: float = 0.0 anger: float = 0.0 sadness: float = 0.0 peace: float = 0.0
#
# NOEMA_QUARANTINED_APPENDIX: def normalized(self) -> "Emotions":
# NOEMA_QUARANTINED_APPENDIX:     vals = [self.love, self.joy, self.fear, self.anger, self.sadness, self.peace]
# NOEMA_QUARANTINED_APPENDIX:     total = sum(max(0.0, v) for v in vals)
# NOEMA_QUARANTINED_APPENDIX:     if total <= 1e-12:
# NOEMA_QUARANTINED_APPENDIX:         return Emotions()
# NOEMA_QUARANTINED_APPENDIX:     scale = 1.0 / total
# NOEMA_QUARANTINED_APPENDIX:     return Emotions(*(max(0.0, v) * scale for v in vals))  # type: ignore[arg-type]
#
# NOEMA_QUARANTINED_APPENDIX: def as_dict(self) -> Dict[str, float]:
# NOEMA_QUARANTINED_APPENDIX:     return dataclasses.asdict(self)
#
# NOEMA_QUARANTINED_APPENDIX: def copy(self) -> "Emotions":
# NOEMA_QUARANTINED_APPENDIX:     return Emotions(**self.as_dict())
#
# NOEMA_QUARANTINED_APPENDIX: def amplify(self, which: str, delta: float) -> None:
# NOEMA_QUARANTINED_APPENDIX:     if hasattr(self, which):
# NOEMA_QUARANTINED_APPENDIX:         setattr(self, which, max(0.0, getattr(self, which)) + float(delta))
#
# NOEMA_QUARANTINED_APPENDIX: def intensity(self) -> float:
# NOEMA_QUARANTINED_APPENDIX:     # simple scalar summary
# NOEMA_QUARANTINED_APPENDIX:     vals = list(self.as_dict().values())
# NOEMA_QUARANTINED_APPENDIX:     return sum(vals) / (len(vals) or 1)
#
# NOEMA_QUARANTINED_APPENDIX: @dataclass class SemanticConfig: coherence: float = 0.6 superposition: float = 0.5 entanglement: float = 0.4 resonance: float = 0.0  # will be set to phi if requested
#
# NOEMA_QUARANTINED_APPENDIX: @dataclass class SemanticProgram: intent: str emotions: Emotions = field(default_factory=Emotions) input_value: complex = complex(1.0, 0.0) rules: List[str] = field(default_factory=list) pipeline: List[Tuple[str, Dict[str, Any]]] = field(default_factory=list) config: SemanticConfig = field(default_factory=SemanticConfig)
#
# NOEMA_QUARANTINED_APPENDIX: def summary(self) -> str:
# NOEMA_QUARANTINED_APPENDIX:     return (
# NOEMA_QUARANTINED_APPENDIX:         f"Intent: {self.intent}\n"
# NOEMA_QUARANTINED_APPENDIX:         f"Emotions: {self.emotions.as_dict()}\n"
# NOEMA_QUARANTINED_APPENDIX:         f"Input: {self.input_value}\n"
# NOEMA_QUARANTINED_APPENDIX:         f"Rules: {self.rules}\n"
# NOEMA_QUARANTINED_APPENDIX:         f"Pipeline: {[name for name,_ in self.pipeline]}\n"
# NOEMA_QUARANTINED_APPENDIX:     )
#
# NOEMA_QUARANTINED_APPENDIX: @dataclass class ExecutionTrace: steps: List[Dict[str, Any]] = field(default_factory=list)
#
# NOEMA_QUARANTINED_APPENDIX: def log(self, **kwargs: Any) -> None:
# NOEMA_QUARANTINED_APPENDIX:     self.steps.append({"t": time.time(), **kwargs})
#
# NOEMA_QUARANTINED_APPENDIX: def to_json(self) -> str:
# NOEMA_QUARANTINED_APPENDIX:     return json.dumps(self.steps, ensure_ascii=False, indent=2)
#
# NOEMA_QUARANTINED_APPENDIX: @dataclass class ExecutionResult: final_state: complex metrics: Dict[str, float] trace: ExecutionTrace
#
# NOEMA_QUARANTINED_APPENDIX: def summary(self) -> str:
# NOEMA_QUARANTINED_APPENDIX:     lines = [
# NOEMA_QUARANTINED_APPENDIX:         f"final_state = {self.final_state}",
# NOEMA_QUARANTINED_APPENDIX:         "metrics:" ,
# NOEMA_QUARANTINED_APPENDIX:     ]
# NOEMA_QUARANTINED_APPENDIX:     for k, v in self.metrics.items():
# NOEMA_QUARANTINED_APPENDIX:         lines.append(f"  - {k}: {v:.4f}")
# NOEMA_QUARANTINED_APPENDIX:     return "\n".join(lines)
#
# NOEMA_QUARANTINED_APPENDIX: -----------------------------
#
# NOEMA_QUARANTINED_APPENDIX: Parser for SCL (simple, robust)
#
# NOEMA_QUARANTINED_APPENDIX: -----------------------------
#
# NOEMA_QUARANTINED_APPENDIX: class SCLParser: kv_re = re.compile(r"^\s*([A-Za-z][A-Za-z0-9_-])\s[:=]\s*(.+?)\s*$")
#
# NOEMA_QUARANTINED_APPENDIX: def parse(self, text: str) -> SemanticProgram:
# NOEMA_QUARANTINED_APPENDIX:     sections = self._split_sections(text)
# NOEMA_QUARANTINED_APPENDIX:     intent = self._parse_intent(sections.get("INTENT", "").strip())
# NOEMA_QUARANTINED_APPENDIX:     emotions = self._parse_emotions(sections.get("EMOTIONS", ""))
# NOEMA_QUARANTINED_APPENDIX:     input_value = self._parse_input(sections.get("INPUT", ""))
# NOEMA_QUARANTINED_APPENDIX:     rules = self._parse_rules(sections.get("RULES", ""))
# NOEMA_QUARANTINED_APPENDIX:     pipeline = self._parse_pipeline(sections.get("PIPELINE", ""))
# NOEMA_QUARANTINED_APPENDIX:     cfg = SemanticConfig()
# NOEMA_QUARANTINED_APPENDIX:     # Initial resonance
# NOEMA_QUARANTINED_APPENDIX:     cfg.resonance = (_phi() if any("resonance=phi" in x[1].get("_raw", "") for x in pipeline) else 0.0)
# NOEMA_QUARANTINED_APPENDIX:     return SemanticProgram(intent, emotions.normalized(), input_value, rules, pipeline, cfg)
#
# NOEMA_QUARANTINED_APPENDIX: def _split_sections(self, text: str) -> Dict[str, str]:
# NOEMA_QUARANTINED_APPENDIX:     out: Dict[str, List[str]] = {}
# NOEMA_QUARANTINED_APPENDIX:     current = None
# NOEMA_QUARANTINED_APPENDIX:     for raw in text.splitlines():
# NOEMA_QUARANTINED_APPENDIX:         line = raw.rstrip()
# NOEMA_QUARANTINED_APPENDIX:         if not line.strip():
# NOEMA_QUARANTINED_APPENDIX:             continue
# NOEMA_QUARANTINED_APPENDIX:         m = re.match(r"^([A-Z][A-Z0-9_ ]+):\s*$", line)
# NOEMA_QUARANTINED_APPENDIX:         if m:
# NOEMA_QUARANTINED_APPENDIX:             current = m.group(1).strip()
# NOEMA_QUARANTINED_APPENDIX:             out[current] = []
# NOEMA_QUARANTINED_APPENDIX:         elif current is not None:
# NOEMA_QUARANTINED_APPENDIX:             out[current].append(line)
# NOEMA_QUARANTINED_APPENDIX:     return {k: "\n".join(v) for k, v in out.items()}
#
# NOEMA_QUARANTINED_APPENDIX: def _parse_intent(self, block: str) -> str:
# NOEMA_QUARANTINED_APPENDIX:     # Accept either raw line or key/value
# NOEMA_QUARANTINED_APPENDIX:     if not block:
# NOEMA_QUARANTINED_APPENDIX:         return ""
# NOEMA_QUARANTINED_APPENDIX:     if block.startswith('"') and block.endswith('"'):
# NOEMA_QUARANTINED_APPENDIX:         return block.strip()[1:-1]
# NOEMA_QUARANTINED_APPENDIX:     m = self._kv_re.match(block)
# NOEMA_QUARANTINED_APPENDIX:     if m and m.group(1).lower() in ("intent", "value"):
# NOEMA_QUARANTINED_APPENDIX:         v = m.group(2).strip()
# NOEMA_QUARANTINED_APPENDIX:         return v.strip('"')
# NOEMA_QUARANTINED_APPENDIX:     return block.strip('"')
#
# NOEMA_QUARANTINED_APPENDIX: def _parse_emotions(self, block: str) -> Emotions:
# NOEMA_QUARANTINED_APPENDIX:     e = Emotions()
# NOEMA_QUARANTINED_APPENDIX:     for line in block.splitlines():
# NOEMA_QUARANTINED_APPENDIX:         m = self._kv_re.match(line)
# NOEMA_QUARANTINED_APPENDIX:         if not m:
# NOEMA_QUARANTINED_APPENDIX:             continue
# NOEMA_QUARANTINED_APPENDIX:         key, val = m.group(1).lower(), m.group(2)
# NOEMA_QUARANTINED_APPENDIX:         try:
# NOEMA_QUARANTINED_APPENDIX:             setattr(e, key, float(val))
# NOEMA_QUARANTINED_APPENDIX:         except Exception:
# NOEMA_QUARANTINED_APPENDIX:             pass
# NOEMA_QUARANTINED_APPENDIX:     return e
#
# NOEMA_QUARANTINED_APPENDIX: def _parse_input(self, block: str) -> complex:
# NOEMA_QUARANTINED_APPENDIX:     # Supports: value=1.23 ; value=1+2j ; value=complex(a,b)
# NOEMA_QUARANTINED_APPENDIX:     for line in block.splitlines():
# NOEMA_QUARANTINED_APPENDIX:         m = self._kv_re.match(line)
# NOEMA_QUARANTINED_APPENDIX:         if not m:
# NOEMA_QUARANTINED_APPENDIX:             continue
# NOEMA_QUARANTINED_APPENDIX:         if m.group(1).lower() == "value":
# NOEMA_QUARANTINED_APPENDIX:             raw = m.group(2).strip()
# NOEMA_QUARANTINED_APPENDIX:             try:
# NOEMA_QUARANTINED_APPENDIX:                 if raw.startswith("complex(") and raw.endswith(")"):
# NOEMA_QUARANTINED_APPENDIX:                     inside = raw[len("complex("):-1]
# NOEMA_QUARANTINED_APPENDIX:                     a, b = inside.split(",")
# NOEMA_QUARANTINED_APPENDIX:                     return complex(float(a), float(b))
# NOEMA_QUARANTINED_APPENDIX:                 if "j" in raw:
# NOEMA_QUARANTINED_APPENDIX:                     return complex(raw.replace(" ",""))
# NOEMA_QUARANTINED_APPENDIX:                 return complex(float(raw), 0.0)
# NOEMA_QUARANTINED_APPENDIX:             except Exception:
# NOEMA_QUARANTINED_APPENDIX:                 pass
# NOEMA_QUARANTINED_APPENDIX:     return complex(1.0, 0.0)
#
# NOEMA_QUARANTINED_APPENDIX: def _parse_rules(self, block: str) -> List[str]:
# NOEMA_QUARANTINED_APPENDIX:     rules: List[str] = []
# NOEMA_QUARANTINED_APPENDIX:     for line in block.splitlines():
# NOEMA_QUARANTINED_APPENDIX:         s = line.strip()
# NOEMA_QUARANTINED_APPENDIX:         if s and not s.startswith("#"):
# NOEMA_QUARANTINED_APPENDIX:             rules.append(s)
# NOEMA_QUARANTINED_APPENDIX:     return rules
#
# NOEMA_QUARANTINED_APPENDIX: def _parse_pipeline(self, block: str) -> List[Tuple[str, Dict[str, Any]]]:
# NOEMA_QUARANTINED_APPENDIX:     stages: List[Tuple[str, Dict[str, Any]]] = []
# NOEMA_QUARANTINED_APPENDIX:     for line in block.splitlines():
# NOEMA_QUARANTINED_APPENDIX:         s = line.strip()
# NOEMA_QUARANTINED_APPENDIX:         if not s or s.startswith("#"):
# NOEMA_QUARANTINED_APPENDIX:             continue
# NOEMA_QUARANTINED_APPENDIX:         m = re.match(r"^([a-zA-Z_][a-zA-Z0-9_]*)\s*(.*)\s*$", s)
# NOEMA_QUARANTINED_APPENDIX:         if not m:
# NOEMA_QUARANTINED_APPENDIX:             continue
# NOEMA_QUARANTINED_APPENDIX:         name, argstr = m.group(1), m.group(2).strip()
# NOEMA_QUARANTINED_APPENDIX:         args = self._parse_args(argstr)
# NOEMA_QUARANTINED_APPENDIX:         args["_raw"] = s
# NOEMA_QUARANTINED_APPENDIX:         stages.append((name.lower(), args))
# NOEMA_QUARANTINED_APPENDIX:     return stages
#
# NOEMA_QUARANTINED_APPENDIX: def _parse_args(self, argstr: str) -> Dict[str, Any]:
# NOEMA_QUARANTINED_APPENDIX:     if not argstr:
# NOEMA_QUARANTINED_APPENDIX:         return {}
# NOEMA_QUARANTINED_APPENDIX:     out: Dict[str, Any] = {}
# NOEMA_QUARANTINED_APPENDIX:     parts = [p.strip() for p in argstr.split(",") if p.strip()]
# NOEMA_QUARANTINED_APPENDIX:     for p in parts:
# NOEMA_QUARANTINED_APPENDIX:         if "=" in p:
# NOEMA_QUARANTINED_APPENDIX:             k, v = p.split("=", 1)
# NOEMA_QUARANTINED_APPENDIX:             out[k.strip()] = _auto_cast(v.strip())
# NOEMA_QUARANTINED_APPENDIX:         else:
# NOEMA_QUARANTINED_APPENDIX:             out[p] = True
# NOEMA_QUARANTINED_APPENDIX:     return out
#
# NOEMA_QUARANTINED_APPENDIX: -----------------------------
#
# NOEMA_QUARANTINED_APPENDIX: Virtual machine / Execution
#
# NOEMA_QUARANTINED_APPENDIX: -----------------------------
#
# NOEMA_QUARANTINED_APPENDIX: class SemanticVM: """Small, deterministic interpreter for SCL programs."""
#
# NOEMA_QUARANTINED_APPENDIX: def __init__(self) -> None:
# NOEMA_QUARANTINED_APPENDIX:     self.ops: Dict[str, Callable[[SemanticProgram, Dict[str, Any], ExecutionTrace], None]] = {
# NOEMA_QUARANTINED_APPENDIX:         "collatz": self._op_collatz,
# NOEMA_QUARANTINED_APPENDIX:         "quantum": self._op_quantum,
# NOEMA_QUARANTINED_APPENDIX:         "ramanujan": self._op_ramanujan,
# NOEMA_QUARANTINED_APPENDIX:         "verify": self._op_verify,
# NOEMA_QUARANTINED_APPENDIX:     }
#
# NOEMA_QUARANTINED_APPENDIX: # ---- public API ----
# NOEMA_QUARANTINED_APPENDIX: def run(self, program: SemanticProgram) -> ExecutionResult:
# NOEMA_QUARANTINED_APPENDIX:     trace = ExecutionTrace()
# NOEMA_QUARANTINED_APPENDIX:     state = program.input_value
#
# NOEMA_QUARANTINED_APPENDIX:     # Apply rules (simple built-ins)
# NOEMA_QUARANTINED_APPENDIX:     self._apply_rules(program, trace)
#
# NOEMA_QUARANTINED_APPENDIX:     for name, args in program.pipeline:
# NOEMA_QUARANTINED_APPENDIX:         op = self.ops.get(name)
# NOEMA_QUARANTINED_APPENDIX:         if op is None:
# NOEMA_QUARANTINED_APPENDIX:             trace.log(stage=name, event="skip", reason="unknown_op")
# NOEMA_QUARANTINED_APPENDIX:             continue
# NOEMA_QUARANTINED_APPENDIX:         trace.log(stage=name, event="start", args=args)
# NOEMA_QUARANTINED_APPENDIX:         op(program, args, trace)  # may modify program.config or store aux state
# NOEMA_QUARANTINED_APPENDIX:         trace.log(stage=name, event="done")
#
# NOEMA_QUARANTINED_APPENDIX:     # Aggregate metrics
# NOEMA_QUARANTINED_APPENDIX:     metrics = self._collect_metrics(program, trace)
# NOEMA_QUARANTINED_APPENDIX:     # Final state is whatever last numeric accumulator was (store in trace if produced)
# NOEMA_QUARANTINED_APPENDIX:     final_state = _trace_last_complex(trace) or state
# NOEMA_QUARANTINED_APPENDIX:     return ExecutionResult(final_state=final_state, metrics=metrics, trace=trace)
#
# NOEMA_QUARANTINED_APPENDIX: def register(self, name: str, fn: Callable[[SemanticProgram, Dict[str, Any], ExecutionTrace], None]) -> None:
# NOEMA_QUARANTINED_APPENDIX:     self.ops[name] = fn
#
# NOEMA_QUARANTINED_APPENDIX: # ---- operators ----
# NOEMA_QUARANTINED_APPENDIX: def _op_collatz(self, program: SemanticProgram, args: Dict[str, Any], trace: ExecutionTrace) -> None:
# NOEMA_QUARANTINED_APPENDIX:     # Seed selection
# NOEMA_QUARANTINED_APPENDIX:     seed = args.get("seed", "auto")
# NOEMA_QUARANTINED_APPENDIX:     if seed == "auto":
# NOEMA_QUARANTINED_APPENDIX:         seed = (abs(hash(program.intent)) % 10_000) + 1
# NOEMA_QUARANTINED_APPENDIX:     seed = int(seed)
# NOEMA_QUARANTINED_APPENDIX:     max_steps = int(args.get("max_steps", 120))
#
# NOEMA_QUARANTINED_APPENDIX:     n = seed
# NOEMA_QUARANTINED_APPENDIX:     path: List[int] = []
# NOEMA_QUARANTINED_APPENDIX:     for i in range(max_steps):
# NOEMA_QUARANTINED_APPENDIX:         path.append(n)
# NOEMA_QUARANTINED_APPENDIX:         if n == 1:
# NOEMA_QUARANTINED_APPENDIX:             break
# NOEMA_QUARANTINED_APPENDIX:         if n % 2 == 0:
# NOEMA_QUARANTINED_APPENDIX:             n //= 2
# NOEMA_QUARANTINED_APPENDIX:         else:
# NOEMA_QUARANTINED_APPENDIX:             n = 3 * n + 1
# NOEMA_QUARANTINED_APPENDIX:         # gentle emotional modulation (bounded)
# NOEMA_QUARANTINED_APPENDIX:         emo = program.emotions.normalized()
# NOEMA_QUARANTINED_APPENDIX:         modulation = 1.0 + 0.05 * (emo.love + emo.joy) - 0.03 * (emo.fear + emo.sadness + emo.anger)
# NOEMA_QUARANTINED_APPENDIX:         n = max(1, int(n * max(0.9, min(1.1, modulation))))
# NOEMA_QUARANTINED_APPENDIX:     path.append(1)
# NOEMA_QUARANTINED_APPENDIX:     trace.log(stage="collatz", path_len=len(path), seed=seed, last=n)
# NOEMA_QUARANTINED_APPENDIX:     # store as last complex value (for downstream)
# NOEMA_QUARANTINED_APPENDIX:     c = complex(float(len(path)), float(max(path) if path else 1))
# NOEMA_QUARANTINED_APPENDIX:     trace.log(stage="collatz", complex_state=str(c))
#
# NOEMA_QUARANTINED_APPENDIX: def _op_quantum(self, program: SemanticProgram, args: Dict[str, Any], trace: ExecutionTrace) -> None:
# NOEMA_QUARANTINED_APPENDIX:     # Resolve config (auto → derive from emotions)
# NOEMA_QUARANTINED_APPENDIX:     cfg = program.config
# NOEMA_QUARANTINED_APPENDIX:     emo = program.emotions.normalized()
# NOEMA_QUARANTINED_APPENDIX:     def auto_or(name: str, default: float) -> float:
# NOEMA_QUARANTINED_APPENDIX:         v = args.get(name, "auto")
# NOEMA_QUARANTINED_APPENDIX:         if v == "auto":
# NOEMA_QUARANTINED_APPENDIX:             if name == "coherence":
# NOEMA_QUARANTINED_APPENDIX:                 return max(0.3, min(1.0, 0.5 + 0.5 * (emo.love + emo.joy - emo.fear)))
# NOEMA_QUARANTINED_APPENDIX:             if name == "superposition":
# NOEMA_QUARANTINED_APPENDIX:                 return max(0.2, min(1.0, 0.3 + 0.7 * _lexical_diversity(program.intent)))
# NOEMA_QUARANTINED_APPENDIX:             if name == "entanglement":
# NOEMA_QUARANTINED_APPENDIX:                 return max(0.2, min(1.0, 0.4 + 0.3 * emo.intensity()))
# NOEMA_QUARANTINED_APPENDIX:         try:
# NOEMA_QUARANTINED_APPENDIX:             return float(v)
# NOEMA_QUARANTINED_APPENDIX:         except Exception:
# NOEMA_QUARANTINED_APPENDIX:             return default
# NOEMA_QUARANTINED_APPENDIX:     cfg.coherence = auto_or("coherence", cfg.coherence)
# NOEMA_QUARANTINED_APPENDIX:     cfg.superposition = auto_or("superposition", cfg.superposition)
# NOEMA_QUARANTINED_APPENDIX:     cfg.entanglement = auto_or("entanglement", cfg.entanglement)
# NOEMA_QUARANTINED_APPENDIX:     trace.log(stage="quantum", coherence=cfg.coherence, superposition=cfg.superposition, entanglement=cfg.entanglement)
# NOEMA_QUARANTINED_APPENDIX:     # produce a complex state based on these params
# NOEMA_QUARANTINED_APPENDIX:     amp = cfg.coherence * (0.7 + 0.3 * cfg.superposition)
# NOEMA_QUARANTINED_APPENDIX:     phase = 2 * math.pi * (cfg.entanglement * 0.25)
# NOEMA_QUARANTINED_APPENDIX:     c = amp * complex(math.cos(phase), math.sin(phase))
# NOEMA_QUARANTINED_APPENDIX:     trace.log(stage="quantum", complex_state=str(c))
#
# NOEMA_QUARANTINED_APPENDIX: def _op_ramanujan(self, program: SemanticProgram, args: Dict[str, Any], trace: ExecutionTrace) -> None:
# NOEMA_QUARANTINED_APPENDIX:     # resonance=phi|value, gain=...
# NOEMA_QUARANTINED_APPENDIX:     resonance = args.get("resonance", program.config.resonance)
# NOEMA_QUARANTINED_APPENDIX:     if resonance == "phi":
# NOEMA_QUARANTINED_APPENDIX:         resonance = _phi()
# NOEMA_QUARANTINED_APPENDIX:     try:
# NOEMA_QUARANTINED_APPENDIX:         resonance = float(resonance)
# NOEMA_QUARANTINED_APPENDIX:     except Exception:
# NOEMA_QUARANTINED_APPENDIX:         resonance = 1.0
# NOEMA_QUARANTINED_APPENDIX:     gain = float(args.get("gain", 1.0))
# NOEMA_QUARANTINED_APPENDIX:     # combine with intent hash for a stable-but-unique phase
# NOEMA_QUARANTINED_APPENDIX:     h = (abs(hash(program.intent)) % 10_000) / 10_000.0
# NOEMA_QUARANTINED_APPENDIX:     phase = 2 * math.pi * (resonance % 1.0) * (0.5 + 0.5 * h)
# NOEMA_QUARANTINED_APPENDIX:     amp = gain * (0.9 + 0.1 * _sentiment(program.intent))
# NOEMA_QUARANTINED_APPENDIX:     c = amp * complex(math.cos(phase), math.sin(phase))
# NOEMA_QUARANTINED_APPENDIX:     trace.log(stage="ramanujan", resonance=resonance, gain=gain, complex_state=str(c))
#
# NOEMA_QUARANTINED_APPENDIX: def _op_verify(self, program: SemanticProgram, args: Dict[str, Any], trace: ExecutionTrace) -> None:
# NOEMA_QUARANTINED_APPENDIX:     # tiny truth-lock-like check using internal coherence
# NOEMA_QUARANTINED_APPENDIX:     cfg = program.config
# NOEMA_QUARANTINED_APPENDIX:     emo = program.emotions.normalized()
# NOEMA_QUARANTINED_APPENDIX:     # internal scores
# NOEMA_QUARANTINED_APPENDIX:     evidence = 0.5 * cfg.coherence + 0.3 * (1.0 - abs(emo.fear - emo.love)) + 0.2 * (0.6 + 0.4 * _sentiment(program.intent))
# NOEMA_QUARANTINED_APPENDIX:     contradictions = max(0.0, 0.4 * (emo.anger - emo.peace))
# NOEMA_QUARANTINED_APPENDIX:     completeness = max(0.0, min(1.0, evidence - contradictions))
# NOEMA_QUARANTINED_APPENDIX:     state = "evidence_verified" if completeness >= float(args.get("threshold", 0.7)) else "insufficient_evidence"
# NOEMA_QUARANTINED_APPENDIX:     trace.log(stage="verify", completeness=completeness, state=state)
# NOEMA_QUARANTINED_APPENDIX:     # store decision as a complex flag
# NOEMA_QUARANTINED_APPENDIX:     c = complex(completeness, 1.0 if state == "evidence_verified" else 0.0)
# NOEMA_QUARANTINED_APPENDIX:     trace.log(stage="verify", complex_state=str(c))
#
# NOEMA_QUARANTINED_APPENDIX: # ---- utilities ----
# NOEMA_QUARANTINED_APPENDIX: def _apply_rules(self, program: SemanticProgram, trace: ExecutionTrace) -> None:
# NOEMA_QUARANTINED_APPENDIX:     # Very small rule engine: two primitives implemented
# NOEMA_QUARANTINED_APPENDIX:     for rule in program.rules:
# NOEMA_QUARANTINED_APPENDIX:         s = rule.strip()
# NOEMA_QUARANTINED_APPENDIX:         # 1) if contains("word") then amplify emotion X by +Y
# NOEMA_QUARANTINED_APPENDIX:         m = re.match(r'^if\s+contains"(.+?)"\s+then\s+amplify\s+emotion\s+([a-z]+)\s+by\s*([+\-]?[0-9.]+)', s, re.IGNORECASE)
# NOEMA_QUARANTINED_APPENDIX:         if m:
# NOEMA_QUARANTINED_APPENDIX:             word, emo, delta = m.group(1), m.group(2).lower(), float(m.group(3))
# NOEMA_QUARANTINED_APPENDIX:             if word.lower() in program.intent.lower():
# NOEMA_QUARANTINED_APPENDIX:                 program.emotions.amplify(emo, delta)
# NOEMA_QUARANTINED_APPENDIX:                 trace.log(stage="rules", rule="contains→amplify", matched=word, emotion=emo, delta=delta)
# NOEMA_QUARANTINED_APPENDIX:                 continue
# NOEMA_QUARANTINED_APPENDIX:         # 2) if sentiment >= X then set coherence to Y
# NOEMA_QUARANTINED_APPENDIX:         m2 = re.match(r'^if\s+sentiment\s*([><=]{1,2})\s*([0-9.]+)\s+then\s+set\s+coherence\s+to\s*([0-9.]+)$', s, re.IGNORECASE)
# NOEMA_QUARANTINED_APPENDIX:         if m2:
# NOEMA_QUARANTINED_APPENDIX:             op, thr, val = m2.group(1), float(m2.group(2)), float(m2.group(3))
# NOEMA_QUARANTINED_APPENDIX:             sent = _sentiment(program.intent)
# NOEMA_QUARANTINED_APPENDIX:             ok = (sent >= thr) if op in (">=", ">=") else (sent <= thr) if op in ("<=", "<=") else (abs(sent - thr) < 1e-9)
# NOEMA_QUARANTINED_APPENDIX:             if ok:
# NOEMA_QUARANTINED_APPENDIX:                 program.config.coherence = val
# NOEMA_QUARANTINED_APPENDIX:                 trace.log(stage="rules", rule="sentiment→coherence", op=op, thr=thr, coherence=val)
#
# NOEMA_QUARANTINED_APPENDIX: def _collect_metrics(self, program: SemanticProgram, trace: ExecutionTrace) -> Dict[str, float]:
# NOEMA_QUARANTINED_APPENDIX:     emo = program.emotions.normalized()
# NOEMA_QUARANTINED_APPENDIX:     coherence = program.config.coherence
# NOEMA_QUARANTINED_APPENDIX:     # derive simple summaries from trace
# NOEMA_QUARANTINED_APPENDIX:     collatz_len = _trace_pick(trace, "collatz", "path_len") or 0
# NOEMA_QUARANTINED_APPENDIX:     verify_state = _trace_pick(trace, "verify", "state") or "insufficient_evidence"
# NOEMA_QUARANTINED_APPENDIX:     completeness = float(_trace_pick(trace, "verify", "completeness") or 0.0)
# NOEMA_QUARANTINED_APPENDIX:     return {
# NOEMA_QUARANTINED_APPENDIX:         "emotional_balance": 1.0 - abs(emo.love - emo.fear),
# NOEMA_QUARANTINED_APPENDIX:         "emotional_diversity": sum(1 for v in emo.as_dict().values() if v > 0.05) / 6.0,
# NOEMA_QUARANTINED_APPENDIX:         "coherence": coherence,
# NOEMA_QUARANTINED_APPENDIX:         "collatz_path_length": float(collatz_len),
# NOEMA_QUARANTINED_APPENDIX:         "truth_completeness": completeness,
# NOEMA_QUARANTINED_APPENDIX:         "truth_verified": 1.0 if verify_state == "evidence_verified" else 0.0,
# NOEMA_QUARANTINED_APPENDIX:     }
#
# NOEMA_QUARANTINED_APPENDIX: -----------------------------
#
# NOEMA_QUARANTINED_APPENDIX: Helpers
#
# NOEMA_QUARANTINED_APPENDIX: -----------------------------
#
# NOEMA_QUARANTINED_APPENDIX: def _phi() -> float: return (1 + math.sqrt(5.0)) / 2.0
#
# NOEMA_QUARANTINED_APPENDIX: def lexical_diversity(text: str) -> float: ws = [w.lower() for w in re.findall(r"[A-Za-zÀ-ž0-9]+", text)] return (len(set(ws)) / max(1, len(ws))) if ws else 0.0
#
# NOEMA_QUARANTINED_APPENDIX: def _sentiment(text: str) -> float: # ultra-simple lexicon (placeholder; deterministic) pos = {"love", "peace", "harmony", "cooperation", "joy", "trust", "compassion", "sprawczości", "współpracy"} neg = {"fear", "anger", "war", "conflict", "hate", "despair"} t = text.lower() p = sum(t.count(w) for w in pos) n = sum(t.count(w) for w in neg) tot = p + n return p / tot if tot else 0.5
#
# NOEMA_QUARANTINED_APPENDIX: def _auto_cast(v: str) -> Any: v = v.strip() if v.lower() in ("true", "false"): return v.lower() == "true" try: if re.match(r"^[+-]?[0-9]+$", v): return int(v) if re.match(r"^[+-]?[0-9]*.[0-9]+$", v): return float(v) if v.startswith('"') and v.endswith('"'): return v[1:-1] except Exception: pass return v
#
# NOEMA_QUARANTINED_APPENDIX: def _trace_pick(trace: ExecutionTrace, stage: str, key: str) -> Optional[Any]: for rec in reversed(trace.steps): if rec.get("stage") == stage and key in rec: return rec[key] return None
#
# NOEMA_QUARANTINED_APPENDIX: def _trace_last_complex(trace: ExecutionTrace) -> Optional[complex]: for rec in reversed(trace.steps): s = rec.get("complex_state") if isinstance(s, str) and s.startswith("("): try: return complex(s) except Exception: continue return None
#
# NOEMA_QUARANTINED_APPENDIX: -----------------------------
#
# NOEMA_QUARANTINED_APPENDIX: Python API (builder)
#
# NOEMA_QUARANTINED_APPENDIX: -----------------------------
#
# NOEMA_QUARANTINED_APPENDIX: class ProgramBuilder: def init(self, intent: str) -> None: self._intent = intent self._emotions = Emotions() self._rules: List[str] = [] self._pipeline: List[Tuple[str, Dict[str, Any]]] = [] self._input = complex(1.0, 0.0)
#
# NOEMA_QUARANTINED_APPENDIX: def emotions(self, **kwargs: float) -> "ProgramBuilder":
# NOEMA_QUARANTINED_APPENDIX:     for k, v in kwargs.items():
# NOEMA_QUARANTINED_APPENDIX:         if hasattr(self._emotions, k):
# NOEMA_QUARANTINED_APPENDIX:             setattr(self._emotions, k, float(v))
# NOEMA_QUARANTINED_APPENDIX:     return self
#
# NOEMA_QUARANTINED_APPENDIX: def rule(self, text: str) -> "ProgramBuilder":
# NOEMA_QUARANTINED_APPENDIX:     self._rules.append(text)
# NOEMA_QUARANTINED_APPENDIX:     return self
#
# NOEMA_QUARANTINED_APPENDIX: def input(self, value: Union[float, complex]) -> "ProgramBuilder":
# NOEMA_QUARANTINED_APPENDIX:     self._input = complex(value)
# NOEMA_QUARANTINED_APPENDIX:     return self
#
# NOEMA_QUARANTINED_APPENDIX: def stage(self, name: str, **kwargs: Any) -> "ProgramBuilder":
# NOEMA_QUARANTINED_APPENDIX:     self._pipeline.append((name.lower(), {**kwargs}))
# NOEMA_QUARANTINED_APPENDIX:     return self
#
# NOEMA_QUARANTINED_APPENDIX: def build(self) -> SemanticProgram:
# NOEMA_QUARANTINED_APPENDIX:     return SemanticProgram(
# NOEMA_QUARANTINED_APPENDIX:         intent=self._intent,
# NOEMA_QUARANTINED_APPENDIX:         emotions=self._emotions.normalized(),
# NOEMA_QUARANTINED_APPENDIX:         input_value=self._input,
# NOEMA_QUARANTINED_APPENDIX:         rules=list(self._rules),
# NOEMA_QUARANTINED_APPENDIX:         pipeline=list(self._pipeline),
# NOEMA_QUARANTINED_APPENDIX:     )
#
# NOEMA_QUARANTINED_APPENDIX: -----------------------------
#
# NOEMA_QUARANTINED_APPENDIX: CLI
#
# NOEMA_QUARANTINED_APPENDIX: -----------------------------
#
# NOEMA_QUARANTINED_APPENDIX: def _run_cli(args: argparse.Namespace) -> int: if args.file: text = open(args.file, "r", encoding="utf-8").read() program = SCLParser().parse(text) else: # minimal default demo demo = ( 'INTENT: "Zharmonizuj system poprzez współpracę i zaufanie."\n\n' "EMOTIONS:\n  love=0.6\n  joy=0.2\n  fear=0.05\n\n" "RULES:\n  if contains("współpracę") then amplify emotion love by +0.10\n" "PIPELINE:\n  collatz(seed=auto, max_steps=90)\n  quantum(coherence=auto, superposition=auto, entanglement=auto)\n  ramanujan(resonance=phi, gain=1.0)\n  verify(truth_lock=true, threshold=0.7)\n" ) program = SCLParser().parse(demo) vm = SemanticVM() result = vm.run(program) if args.pretty: print(program.summary()) print("-" * 60) print(result.summary()) else: print(json.dumps({ "program": dataclasses.asdict(program), "result": { "final_state": str(result.final_state), "metrics": result.metrics, "trace": result.trace.steps if args.trace else [] } }, ensure_ascii=False, indent=2)) return 0
#
# NOEMA_QUARANTINED_APPENDIX: def main(argv: Optional[List[str]] = None) -> int: p = argparse.ArgumentParser(description="CIEL/0 – Semantic Computation Language (SCL)") p.add_argument("--file", type=str, default=None, help="Path to .scl program file") p.add_argument("--pretty", action="store_true", help="Pretty human-readable output") p.add_argument("--trace", action="store_true", help="Include full execution trace in JSON output") args = p.parse_args(argv) return _run_cli(args)
#
# NOEMA_QUARANTINED_APPENDIX: if name == "main":  # pragma: no cover raise SystemExit(main())
#
