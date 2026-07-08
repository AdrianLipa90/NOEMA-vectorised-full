from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


from typing import Any, Dict, List, Optional
import json

from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

from .language_backend import AuxiliaryBackend, LanguageBackend
from .memory_prompt_context import build_semantic_speech_context


class PrimaryLLMBackend(LanguageBackend):
    def __init__(
        self,
        model_name: str,
        device: Optional[str | int] = None,
        max_new_tokens: int = 256,
    ) -> None:
        self.name = model_name
        self.device = device
        self.max_new_tokens = max_new_tokens
        self._pipe = None

    def _lazy_init(self) -> None:
        if self._pipe is None:
            tokenizer = AutoTokenizer.from_pretrained(self.name)
            model = AutoModelForCausalLM.from_pretrained(self.name)
            self._pipe = pipeline(
                "text-generation",
                model=model,
                tokenizer=tokenizer,
                device=self.device,
            )

    def _format_dialogue(self, dialogue: List[Dict[str, str]]) -> str:
        lines: List[str] = []
        for message in dialogue:
            role = message.get("role", "user")
            content = message.get("content", "")
            lines.append(f"{role.capitalize()}: {content}")
        return "\n".join(lines)

    def _summarize_state(self, ciel_state: Dict[str, Any]) -> str:
        summary = {
            "intention_vector": ciel_state.get("intention_vector"),
            "simulation": ciel_state.get("simulation"),
            "cognition": ciel_state.get("cognition"),
            "affect": ciel_state.get("affect"),
            "semantic_speech": build_semantic_speech_context(ciel_state),
        }
        return json.dumps(summary, ensure_ascii=False)

    def generate_reply(
        self,
        dialogue: List[Dict[str, str]],
        ciel_state: Dict[str, Any],
    ) -> str:
        self._lazy_init()
        prompt_parts = [self._format_dialogue(dialogue), "State:", self._summarize_state(ciel_state)]
        prompt = "\n".join(part for part in prompt_parts if part)

        outputs = self._pipe(prompt, max_new_tokens=self.max_new_tokens)
        if not outputs:
            return ""
        generated = outputs[0].get("generated_text", "")
        if generated.startswith(prompt):
            generated = generated[len(prompt) :]
        return generated.strip()


class AuxLLMBackend(AuxiliaryBackend):
    def __init__(
        self,
        model_name: str,
        device: Optional[str | int] = None,
        max_new_tokens: int = 128,
    ) -> None:
        self.name = model_name
        self.device = device
        self.max_new_tokens = max_new_tokens
        self._pipe = None

    def _lazy_init(self) -> None:
        if self._pipe is None:
            tokenizer = AutoTokenizer.from_pretrained(self.name)
            model = AutoModelForCausalLM.from_pretrained(self.name)
            self._pipe = pipeline(
                "text-generation",
                model=model,
                tokenizer=tokenizer,
                device=self.device,
            )

    def _build_prompt(self, ciel_state: Dict[str, Any], candidate_reply: str) -> str:
        summary = {
            "intention_vector": ciel_state.get("intention_vector"),
            "simulation": ciel_state.get("simulation"),
            "cognition": ciel_state.get("cognition"),
            "affect": ciel_state.get("affect"),
        }
        state_json = json.dumps(summary, ensure_ascii=False)
        return (
            "Evaluate the following reply for coherence and helpfulness given the state. "
            "Provide JSON with keys coherence, helpfulness, keywords, emotion.\n"
            f"State: {state_json}\n"
            f"Reply: {candidate_reply}\n"
        )

    def _parse_output(self, text: str) -> Dict[str, Any]:
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            candidate = text[start : end + 1]
            try:
                return json.loads(candidate)
            except json.JSONDecodeError:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/ciel/hf_backends.py:116 quiet except scope=AuxLLMBackend._parse_output reason=pass")
                pass
        return {"raw": text.strip()}

    def analyse_state(
        self,
        ciel_state: Dict[str, Any],
        candidate_reply: str,
    ) -> Dict[str, Any]:
        self._lazy_init()
        prompt = self._build_prompt(ciel_state, candidate_reply)
        outputs = self._pipe(prompt, max_new_tokens=self.max_new_tokens)
        if not outputs:
            return {"raw": ""}
        generated = outputs[0].get("generated_text", "")
        if generated.startswith(prompt):
            generated = generated[len(prompt) :]
        return self._parse_output(generated)


__all__ = ["PrimaryLLMBackend", "AuxLLMBackend"]
