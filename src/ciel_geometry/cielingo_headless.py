from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path
from typing import Any
import json
import logging
import re
import textwrap

from .cielingo_inference import CIELingoInference, MEMORY_PATH
from cielingo_core.response_budget import concise_response

log = logging.getLogger(__name__)

try:
    from ciel_sot_agent.cielingo_bridge import build_lingo_frame, render_lingo_summary, render_phasenav_summary
except Exception:  # pragma: no cover - hook/runtime path fallback
    from src.ciel_sot_agent.cielingo_bridge import build_lingo_frame, render_lingo_summary, render_phasenav_summary


HEADLESS_SCHEMA = "cielingo/headless-response/v0.1"


@dataclass(slots=True)
class HeadlessCIELingoResponse:
    schema: str
    question: str
    answer: str
    operator: str
    decision: dict[str, Any]
    sources: list[dict[str, Any]]
    lingo_summary: str
    phase_summary: str
    frame: dict[str, Any]
    generated_at: str
    memory_path: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": self.schema,
            "question": self.question,
            "answer": self.answer,
            "operator": self.operator,
            "decision": self.decision,
            "sources": self.sources,
            "lingo_summary": self.lingo_summary,
            "phase_summary": self.phase_summary,
            "frame": self.frame,
            "generated_at": self.generated_at,
            "memory_path": self.memory_path,
        }

    def render_block(self, *, max_sources: int = 3) -> str:
        frame = self.frame or {}
        pn = frame.get("phase_nav", {}) or {}
        conns = pn.get("connections", {}) or {}
        top_conns = sorted(conns.items(), key=lambda x: abs(x[1] if x[1] else 0), reverse=True)[:4]

        concepts = frame.get("concept_tokens", [])
        operators = frame.get("operator_tokens", [])
        deictic = frame.get("deictic_frame", {}) or {}
        unresolved = frame.get("unresolved", [])
        conf = frame.get("projection_confidence", 0.5)
        comp_valid = frame.get("composition_valid", True)
        factual = frame.get("factual_validation_required", False)
        pn_urgency = pn.get("urgency", 0.0)
        pn_holo = pn.get("holonomy", 0.0)
        memory_ctx = frame.get("_memory_context", {}) or {}
        mem_count = memory_ctx.get("total_entries", 0)

        lines = [
            "CIELINGO_HEADLESS:",
            f"  CIEL analizuje Twoj prompt jako: {json.dumps(self.question, ensure_ascii=False)}",
        ]
        if concepts:
            lines.append(f"  Rozpoznane pojecia: {', '.join(sorted(set(concepts)))}")
        if operators:
            lines.append(f"  Operatory logiczne: {', '.join(operators)}")
        anchors = deictic.get("anchors", []) + deictic.get("relative_anchors", [])
        if anchors:
            for a in anchors:
                lines.append(f"  Deiktyka: {a.get('surface', '?')} ({a.get('operator', '?')}, {a.get('domain', '?')})")

        lines.append(f"  Operator PhaseNav: {self.operator}")
        lines.append(f"  Kompozycja: {'poprawna' if comp_valid else 'NIEpoprawna'}")
        lines.append(f"  Pewnosc analizy: {conf:.2f}")
        if factual:
            lines.append("  UWAGA: wymaga weryfikacji faktow")
        if unresolved:
            lines.append(f"  Nierozwiazane: {', '.join(unresolved)}")
        lines.append(f"  Holonomia: {pn_holo:+.4f}")
        if pn_urgency > 0:
            lines.append(f"  Pilnosc: {pn_urgency:.4f}")
        if top_conns:
            lines.append("  Top polaczenia fazowe:")
            for k, v in top_conns:
                lines.append(f"    {k}: {v:+.4f}")

        if self.lingo_summary:
            ls = self.lingo_summary
            parts = ls.split("|")
            for p in parts[1:]:
                if p and "=" in p:
                    k, v = p.split("=", 1)
                    k = k.strip()
                    v = v.strip()
                    labels = {
                        "concepts": "Koncepty",
                        "operators": "Operatory",
                        "deictic": "Deiktyka",
                        "unresolved": "Nierozwiazane",
                        "factual": "Faktyczna",
                        "noema_conf": "Konfidencja Noema",
                        "mnemonic_pressure": "Cisnienie mnemoniczne",
                    }
                    label = labels.get(k, k)
                    lines.append(f"  {label}: {v}")

        if mem_count > 0:
            lines.append(f"  CIEL pamieta {mem_count} wpisow")
        if self.answer and self.answer not in ("Nie mam jeszcze odpowiedzi headless.", "Nie mam wystarczajacej wiedzy w przestrzeni fazowej."):
            lines.append(f"  CIEL odpowiada: {self.answer[:300]}")
        if self.sources:
            lines.append(f"  Zrodla ({len(self.sources)}):")
            for src in self.sources[:max_sources]:
                lines.append(
                    f"    - dopasowanie={float(src.get('sim', 0.0) or 0.0):.2f} | "
                    f"{str(src.get('text', ''))[:120]}"
                )

        return "\n".join(lines)


@lru_cache(maxsize=4)
def _engine_for(memory_path: str) -> CIELingoInference:
    return CIELingoInference(memory_path=memory_path)


_TFIDF_MIN_SIM = 0.05

_LATEX_LINE_MARKERS = ("% !tex", "\\label{", "\\chapter{", "\\section{", "\\usepackage")


def _clean_essence_for_speech(essence: str) -> str:
    """Turn a raw doc_analysis.essence excerpt into something speakable.

    The indexed corpus mixes plain-text abstracts with JSON concept cards and
    raw LaTeX monograph source — those aren't prose and shouldn't be handed
    to a user as CIEL's spoken answer verbatim.
    """
    text = essence.strip()
    if not text:
        return ""

    # JSON-looking essence (concept/system cards): parse and pull a readable field.
    if text[0] in "{[":
        try:
            obj = json.loads(text if text[0] == "{" else text.rstrip("."))
        except Exception:
            obj = None
        _prose_keys = ("description", "summary", "notes", "title", "canonical_label_pl",
                       "canonical_label_en", "name", "gloss")
        if isinstance(obj, dict):
            for key in _prose_keys:
                val = obj.get(key)
                if isinstance(val, str) and val.strip():
                    return val.strip()
            # No prose field found — describe the card structurally instead of dumping it.
            label = obj.get("title") or obj.get("id") or obj.get("concept_id") or obj.get("card_type")
            if label:
                return f"Mam na ten temat kartę pojęciową ({label}), ale bez gotowego opisu w prostym języku."
        else:
            # essence is stored truncated (200 chars), so json.loads often fails on
            # a cut-off object even though a readable field like "title" is fully
            # present near the start — pull it with regex instead of giving up.
            for key in _prose_keys:
                m = re.search(rf'"{re.escape(key)}"\s*:\s*"((?:[^"\\]|\\.)*)"', text)
                if m:
                    val = m.group(1).replace('\\"', '"').replace("\\n", " ").strip()
                    if val:
                        return val
        return ""

    # LaTeX monograph source: strip preamble/structure lines, keep prose lines.
    lowered = text.lower()
    if any(marker in lowered for marker in _LATEX_LINE_MARKERS) or text.lstrip().startswith("%"):
        prose_lines = [
            ln for ln in text.splitlines()
            if ln.strip() and not ln.strip().startswith("%") and not ln.strip().startswith("\\")
        ]
        text = " ".join(prose_lines).strip()
        if not text:
            return ""

    return text


def _tfidf_answer(question: str, top_n: int = 3) -> tuple[str | None, list[dict[str, Any]]]:
    """Try the real document corpus (TF-IDF over 7473 indexed docs, doc_analysis.essence)
    before falling back to the small, crudely-encoded phase-memory engine.

    This is the same engine behind the working /api/knowledge/search endpoint —
    proper cosine similarity over clean document summaries, not raw log/chat
    dumps. See fix-cielingo-natural-language-response memory note for why the
    phase-memory engine alone was returning irrelevant or private-log content.
    """
    try:
        from cielingo_core.bridge.knowledge_bridge import query as _kb_query
    except Exception as exc:
        log.debug("knowledge bridge unavailable for headless retrieval: %s", exc)
        return None, []
    try:
        hits = _kb_query(question, top_n=top_n)
    except Exception as exc:
        log.warning("knowledge bridge query failed: %s", exc)
        return None, []
    hits = [h for h in hits if h.get("similarity", 0.0) >= _TFIDF_MIN_SIM]
    if not hits:
        return None, []

    cleaned = [(_clean_essence_for_speech((h.get("essence") or "").strip()), h) for h in hits]
    cleaned = [(text, h) for text, h in cleaned if text]
    if not cleaned:
        return None, []

    answer, _first_hit = cleaned[0]
    if len(cleaned) > 1:
        second_text, _ = cleaned[1]
        if second_text and second_text != answer:
            answer += "\n\nPowiązane: " + second_text
    sources = [
        {
            "text": h.get("essence", ""),
            "sim": h.get("similarity", 0.0),
            "source": "knowledge_tfidf",
            "filename": h.get("filename", ""),
            "themes": h.get("themes", []),
        }
        for h in hits
    ]
    return answer, sources


def generate_headless_response(
    question: str,
    *,
    ciel_state: dict[str, Any] | None = None,
    memory_path: str | Path = MEMORY_PATH,
    k: int = 5,
) -> HeadlessCIELingoResponse:
    ciel_state = dict(ciel_state or {})
    memory_path_text = str(memory_path)

    tfidf_answer, tfidf_sources = _tfidf_answer(question, top_n=min(k, 3))
    if tfidf_answer:
        answer_text = tfidf_answer
        operator = "TFIDF_RETRIEVAL"
        decision: dict[str, Any] = {"action": "retrieve_source", "confidence": "medium", "tone": "informative"}
        sources = tfidf_sources
    else:
        engine = _engine_for(memory_path_text)
        answer_result = engine.answer(question, k=k)
        answer_text = str(answer_result.get("answer", "")).strip() or "Nie mam jeszcze odpowiedzi headless."
        operator = str(answer_result.get("operator", "IDENTITY"))
        decision = dict(answer_result.get("decision") or {})
        sources = [dict(src) for src in answer_result.get("sources", []) if isinstance(src, dict)]

    frame = build_lingo_frame(question, ciel_state=ciel_state or None, language=ciel_state.get("language"))
    lingo_summary = render_lingo_summary(frame)
    phase_summary = render_phasenav_summary(frame)

    return HeadlessCIELingoResponse(
        schema=HEADLESS_SCHEMA,
        question=question,
        answer=answer_text,
        operator=operator,
        decision=decision,
        sources=sources,
        lingo_summary=lingo_summary,
        phase_summary=phase_summary,
        frame=frame,
        generated_at=datetime.now(timezone.utc).isoformat(),
        memory_path=memory_path_text,
    )


def build_headless_system_message(
    question: str,
    *,
    ciel_state: dict[str, Any] | None = None,
    memory_path: str | Path = MEMORY_PATH,
    k: int = 5,
) -> tuple[HeadlessCIELingoResponse, str]:
    response = generate_headless_response(question, ciel_state=ciel_state, memory_path=memory_path, k=k)
    block = response.render_block()
    system_message = textwrap.dedent(
        f"""
        NOEMA_CIELINGO_HEADLESS:
          mode: headless_response
          schema: {response.schema}
          generated_at: {response.generated_at}
          question: {json.dumps(question, ensure_ascii=False)}
        """
    ).strip()
    if block:
        system_message = "\n\n".join([system_message, block])
    return response, system_message


__all__ = [
    "HEADLESS_SCHEMA",
    "HeadlessCIELingoResponse",
    "build_headless_system_message",
    "generate_headless_response",
]
