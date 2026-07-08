from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import json
import os
from typing import Any, Dict, List, Optional, Tuple

from .language_backend import AuxiliaryBackend, LanguageBackend
from .memory_prompt_context import build_semantic_speech_context


_LLAMA_CACHE: Dict[Tuple[str, int, int, int], Any] = {}


def _coerce_role(role: str) -> str:
    key = (role or "").strip().lower()
    if key in {"system", "user", "assistant"}:
        return key
    return "user"


def _format_dialogue(dialogue: List[Dict[str, str]]) -> str:
    lines: List[str] = []
    for message in dialogue:
        role = _coerce_role(str(message.get("role", "user"))).capitalize()
        content = str(message.get("content", ""))
        lines.append(f"{role}: {content}")
    return "\n".join(lines)


def _summarize_state(ciel_state: Dict[str, Any]) -> str:
    semantic = build_semantic_speech_context(ciel_state)
    summary = {
        "intention_vector": ciel_state.get("intention_vector"),
        "simulation": ciel_state.get("simulation"),
        "cognition": ciel_state.get("cognition"),
        "affect": ciel_state.get("affect"),
        "immune_surface": _immune_surface_brief(ciel_state),
        "phasenav": _phasenav_brief(ciel_state),
        "semantic_speech": semantic,
    }
    return json.dumps(summary, ensure_ascii=False)


def _immune_surface_brief(ciel_state: Dict[str, Any]) -> Dict[str, Any]:
    immune_surface = ciel_state.get("immune_surface")
    if isinstance(immune_surface, dict) and immune_surface:
        return {
            "exists": bool(immune_surface.get("exists", True)),
            "coherence_index": immune_surface.get("coherence_index"),
            "ethical_score": immune_surface.get("ethical_score"),
            "closure_penalty": immune_surface.get("closure_penalty"),
            "soul_invariant": immune_surface.get("soul_invariant"),
            "operating_mode": immune_surface.get("operating_mode"),
        }

    derived = {
        "coherence_index": ciel_state.get("coherence_index"),
        "ethical_score": ciel_state.get("ethical_score"),
        "closure_penalty": ciel_state.get("closure_penalty"),
        "soul_invariant": ciel_state.get("soul_invariant"),
        "operating_mode": ciel_state.get("operating_mode"),
    }
    derived["exists"] = any(value is not None for key, value in derived.items() if key != "exists")
    return derived


def _phasenav_brief(ciel_state: Dict[str, Any]) -> Dict[str, Any]:
    lingo_frame = ciel_state.get("lingo_frame")
    phase_nav = ciel_state.get("phasenav")
    source = phase_nav if isinstance(phase_nav, dict) and phase_nav else lingo_frame if isinstance(lingo_frame, dict) else {}
    if not isinstance(source, dict) or not source:
        return {"exists": False}

    summary = {
        "exists": True,
        "summary": source.get("summary"),
        "concept_tokens": source.get("concept_tokens", []),
        "operator_tokens": source.get("operator_tokens", []),
        "phase_projection": source.get("phase_projection", {}),
        "tau_bridge": source.get("tau_bridge", {}),
        "noema_route": source.get("noema_route", {}),
    }
    if "phase_nav" in source and isinstance(source.get("phase_nav"), dict):
        summary["phase_nav"] = source.get("phase_nav")
    return summary


def _extract_text(output: Any) -> str:
    if isinstance(output, dict):
        choices = output.get("choices") or []
        if choices:
            choice0 = choices[0] or {}
            message = choice0.get("message") or {}
            if isinstance(message, dict) and message.get("content") is not None:
                return str(message.get("content"))
            if choice0.get("text") is not None:
                return str(choice0.get("text"))
        if output.get("text") is not None:
            return str(output.get("text"))
    return str(output)


def _parse_json_object(text: str) -> Dict[str, Any]:
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        candidate = text[start : end + 1]
        try:
            return json.loads(candidate)
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/ciel/gguf_backends.py:64 quiet except scope=_parse_json_object reason=return {\"raw\": text.strip()}")
            return {"raw": text.strip()}
    return {"raw": text.strip()}


class GGUFPrimaryBackend(LanguageBackend):
    def __init__(
        self,
        *,
        model_path: str,
        n_ctx: int = 2048,
        n_threads: int = 4,
        n_gpu_layers: int = 0,
        max_new_tokens: int = 256,
        temperature: float = 0.7,
        system_prompt: str = "",
    ) -> None:
        self.model_path = model_path
        self.n_ctx = int(n_ctx)
        self.n_threads = int(n_threads)
        self.n_gpu_layers = int(n_gpu_layers)
        self.max_new_tokens = int(max_new_tokens)
        self.temperature = float(temperature)
        self.system_prompt = system_prompt
        self.name = os.path.basename(model_path) if model_path else "gguf"
        self._llama: Any | None = None

    def _lazy_init(self) -> None:
        if self._llama is not None:
            return
        key = (self.model_path, self.n_ctx, self.n_threads, self.n_gpu_layers)
        cached = _LLAMA_CACHE.get(key)
        if cached is not None:
            self._llama = cached
            return

        from llama_cpp import Llama

        llama = Llama(
            model_path=self.model_path,
            n_ctx=self.n_ctx,
            n_threads=self.n_threads,
            n_gpu_layers=self.n_gpu_layers,
            verbose=False,
        )
        _LLAMA_CACHE[key] = llama
        self._llama = llama

    def generate_reply(self, dialogue: List[Dict[str, str]], ciel_state: Dict[str, Any]) -> str:
        self._lazy_init()
        state_json = _summarize_state(ciel_state)

        system = self.system_prompt.strip()
        if system:
            system = system + "\n\n"
        system += (
            "PhaseNav immune gate: treat immune_surface and phasenav as binding context. "
            "Do not contradict them without explicit uncertainty.\n"
            f"State: {state_json}"
        )

        llama = self._llama
        if llama is None:
            return ""

        if hasattr(llama, "create_chat_completion"):
            messages: List[Dict[str, str]] = [{"role": "system", "content": system}]
            for msg in dialogue:
                messages.append(
                    {
                        "role": _coerce_role(str(msg.get("role", "user"))),
                        "content": str(msg.get("content", "")),
                    }
                )
            out = llama.create_chat_completion(
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_new_tokens,
                stop=["Adrian:", "\nAdrian", "User:", "\nUser", "Human:"],
            )
            return _extract_text(out).strip()

        prompt_parts = [system, _format_dialogue(dialogue), "Assistant:"]
        prompt = "\n".join(part for part in prompt_parts if part)
        out = llama(
            prompt,
            temperature=self.temperature,
            max_tokens=self.max_new_tokens,
            stop=["User:", "System:", "Assistant:"],
        )
        return _extract_text(out).strip()


class GGUFAuxBackend(AuxiliaryBackend):
    def __init__(
        self,
        *,
        model_path: str,
        n_ctx: int = 2048,
        n_threads: int = 4,
        n_gpu_layers: int = 0,
        max_new_tokens: int = 128,
        temperature: float = 0.2,
        system_prompt: str = "",
    ) -> None:
        self.model_path = model_path
        self.n_ctx = int(n_ctx)
        self.n_threads = int(n_threads)
        self.n_gpu_layers = int(n_gpu_layers)
        self.max_new_tokens = int(max_new_tokens)
        self.temperature = float(temperature)
        self.system_prompt = system_prompt
        self.name = os.path.basename(model_path) if model_path else "gguf-aux"
        self._llama: Any | None = None

    def _lazy_init(self) -> None:
        if self._llama is not None:
            return
        key = (self.model_path, self.n_ctx, self.n_threads, self.n_gpu_layers)
        cached = _LLAMA_CACHE.get(key)
        if cached is not None:
            self._llama = cached
            return

        from llama_cpp import Llama

        llama = Llama(
            model_path=self.model_path,
            n_ctx=self.n_ctx,
            n_threads=self.n_threads,
            n_gpu_layers=self.n_gpu_layers,
            verbose=False,
        )
        _LLAMA_CACHE[key] = llama
        self._llama = llama

    def analyse_state(self, ciel_state: Dict[str, Any], candidate_reply: str) -> Dict[str, Any]:
        self._lazy_init()
        state_json = _summarize_state(ciel_state)

        prompt_parts = [
            self.system_prompt.strip(),
            "PhaseNav immune gate: treat immune_surface and phasenav as binding context.",
            "Evaluate the following reply for coherence and helpfulness given the state.",
            "Return JSON with keys coherence, helpfulness, keywords, emotion.",
            f"State: {state_json}",
            f"Reply: {candidate_reply}",
        ]
        prompt = "\n".join(part for part in prompt_parts if part)

        llama = self._llama
        if llama is None:
            return {"raw": ""}

        out = llama(
            prompt,
            temperature=self.temperature,
            max_tokens=self.max_new_tokens,
            stop=["User:", "System:", "Assistant:"],
        )
        text = _extract_text(out)
        return _parse_json_object(text)


__all__ = ["GGUFPrimaryBackend", "GGUFAuxBackend"]
