"""Meaning-to-surface compiler for CIELingo.

The compiler performs the missing forward transformation::

    MeaningEquation -> SemanticPlan -> language-local surface form

It is intentionally bounded. Version 0.1 is a deterministic symbolic
realizer for Polish and English, not a statistical language model and not a
claim of complete morphology. Missing inflectional forms remain visible in
receipts instead of being silently invented.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Iterable, Mapping

from cielingo_core.global_layer.contracts import MeaningEquation


class CompilationError(ValueError):
    """Raised when an input meaning equation cannot be compiled safely."""


class GrammaticalCase(str, Enum):
    NOMINATIVE = "nominative"
    GENITIVE = "genitive"
    DATIVE = "dative"
    ACCUSATIVE = "accusative"
    INSTRUMENTAL = "instrumental"
    LOCATIVE = "locative"


@dataclass(frozen=True)
class SurfaceLexeme:
    """Language-local lexical realization of one GLOBAL semantic slot.

    ``forms`` is deliberately open: callers may supply case forms for nouns
    and tense/person forms for verbs without changing the compiler ABI.
    """

    slot_id: int
    language_id: str
    lemma: str
    pos: str = "noun"
    forms: Mapping[str, str] = field(default_factory=dict)
    features: Mapping[str, str] = field(default_factory=dict)

    def form(self, *keys: str) -> tuple[str, str | None]:
        for key in keys:
            value = self.forms.get(key)
            if value:
                return str(value), key
        return self.lemma, None


@dataclass(frozen=True)
class SemanticArgument:
    role: str
    slot_id: int


@dataclass(frozen=True)
class SemanticPlan:
    equation_id: str
    language_id: str
    predicate_slot: int | None
    arguments: tuple[SemanticArgument, ...]
    operators: tuple[str, ...]
    is_question: bool
    is_negated: bool
    is_action_request: bool
    modal: str | None


@dataclass(frozen=True)
class CompilationReceipt:
    """Auditable structural round-trip receipt.

    This checks whether the emitted surface plan preserves requested slots,
    roles and operators. It does *not* claim listener-level semantic
    equivalence; that later gate requires re-parsing by an independent
    listener model.
    """

    required_slots: tuple[int, ...]
    emitted_slots: tuple[int, ...]
    required_roles: tuple[str, ...]
    emitted_roles: tuple[str, ...]
    required_operators: tuple[str, ...]
    emitted_operators: tuple[str, ...]
    unresolved_slots: tuple[int, ...]
    slot_coverage: float
    role_coverage: float
    operator_coverage: float
    structural_fidelity: float
    warnings: tuple[str, ...] = ()

    @property
    def valid(self) -> bool:
        return not self.unresolved_slots and self.structural_fidelity == 1.0

    def to_dict(self) -> dict[str, Any]:
        out = asdict(self)
        out["valid"] = self.valid
        return out


@dataclass(frozen=True)
class CompiledUtterance:
    text: str
    tokens: tuple[str, ...]
    language_id: str
    semantic_plan: SemanticPlan
    receipt: CompilationReceipt
    canon_allowed: bool = False
    noema_writeback_allowed: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "text": self.text,
            "tokens": list(self.tokens),
            "language_id": self.language_id,
            "semantic_plan": asdict(self.semantic_plan),
            "receipt": self.receipt.to_dict(),
            "canon_allowed": self.canon_allowed,
            "noema_writeback_allowed": self.noema_writeback_allowed,
        }


@dataclass
class _RealizationState:
    emitted_slots: set[int] = field(default_factory=set)
    emitted_roles: set[str] = field(default_factory=set)
    emitted_operators: set[str] = field(default_factory=set)
    unresolved_slots: set[int] = field(default_factory=set)
    warnings: list[str] = field(default_factory=list)


ROLE_ORDER: tuple[str, ...] = (
    "AGENT",
    "PATIENT",
    "THEME",
    "RECIPIENT",
    "INSTRUMENT",
    "SOURCE",
    "GOAL",
    "LOCATION",
    "TIME",
    "CAUSE",
    "PURPOSE",
    "CONDITION",
    "MANNER",
    "EVIDENCE",
    "CLAIM",
    "MEMORY_TRACE",
    "CONSENT_TARGET",
    "BOUNDARY",
)

_MODAL_NAMES = {
    "MODAL_POSSIBILITY": "possibility",
    "MODAL_PERMISSION": "permission",
    "MODAL_NECESSITY": "necessity",
    "MODAL_OBLIGATION": "obligation",
}


def _enum_name(value: Any) -> str:
    raw = getattr(value, "value", value)
    return str(raw)


def _flatten_slot_value(value: int | list[int] | str) -> list[int]:
    if isinstance(value, int):
        return [value]
    if isinstance(value, list):
        return [item for item in value if isinstance(item, int)]
    return []


def _ordered_arguments(equation: MeaningEquation) -> tuple[SemanticArgument, ...]:
    collected: list[SemanticArgument] = []
    for role, value in equation.roles.items():
        role_name = _enum_name(role)
        for slot_id in _flatten_slot_value(value):
            collected.append(SemanticArgument(role=role_name, slot_id=slot_id))
    rank = {name: i for i, name in enumerate(ROLE_ORDER)}
    return tuple(sorted(collected, key=lambda arg: (rank.get(arg.role, 999), arg.slot_id)))


def _operator_names(equation: MeaningEquation) -> tuple[str, ...]:
    names: list[str] = []
    for operator in equation.operators:
        name = _enum_name(operator.operator_type)
        if name not in names:
            names.append(name)
    return tuple(names)


def _build_plan(equation: MeaningEquation, language_id: str) -> SemanticPlan:
    operators = _operator_names(equation)
    modal = next((_MODAL_NAMES[name] for name in operators if name in _MODAL_NAMES), None)
    return SemanticPlan(
        equation_id=equation.equation_id,
        language_id=language_id,
        predicate_slot=equation.predicate_slot,
        arguments=_ordered_arguments(equation),
        operators=operators,
        is_question="QUESTION" in operators,
        is_negated="NEGATION" in operators,
        is_action_request="ACTION_REQUEST" in operators,
        modal=modal,
    )


class MeaningToSurfaceCompiler:
    """Deterministic compiler from GLOBAL meaning to PL/EN surface text."""

    def __init__(self, lexemes: Iterable[SurfaceLexeme], *, strict: bool = False):
        self.strict = strict
        self._lexicon: dict[tuple[str, int], SurfaceLexeme] = {}
        for lexeme in lexemes:
            key = (lexeme.language_id.lower(), lexeme.slot_id)
            if key in self._lexicon:
                raise CompilationError(f"duplicate lexeme for language/slot {key}")
            self._lexicon[key] = lexeme

    def compile(self, equation: MeaningEquation, language_id: str) -> CompiledUtterance:
        issues = equation.validate()
        if issues:
            raise CompilationError("; ".join(issues))
        language = language_id.lower()
        if language not in {"pl", "en"}:
            raise CompilationError(f"unsupported language_id: {language_id}")

        plan = _build_plan(equation, language)
        state = _RealizationState()
        if language == "pl":
            words = self._realize_polish(plan, state)
        else:
            words = self._realize_english(plan, state)

        text = self._finish(words, question=plan.is_question)
        receipt = self._receipt(plan, state)
        if self.strict and not receipt.valid:
            unresolved = ", ".join(map(str, receipt.unresolved_slots)) or "none"
            raise CompilationError(
                f"surface realization did not close; unresolved slots: {unresolved}; "
                f"fidelity={receipt.structural_fidelity:.3f}"
            )
        return CompiledUtterance(
            text=text,
            tokens=tuple(text.rstrip(".?!").split()),
            language_id=language,
            semantic_plan=plan,
            receipt=receipt,
            canon_allowed=False,
            noema_writeback_allowed=False,
        )

    def _lexeme(self, language: str, slot_id: int, state: _RealizationState) -> SurfaceLexeme:
        lexeme = self._lexicon.get((language, slot_id))
        if lexeme is not None:
            state.emitted_slots.add(slot_id)
            return lexeme
        state.unresolved_slots.add(slot_id)
        state.warnings.append(f"missing_lexeme:{language}:{slot_id}")
        return SurfaceLexeme(slot_id=slot_id, language_id=language, lemma=f"<slot:{slot_id}>")

    @staticmethod
    def _subject_features(subject: SurfaceLexeme | None) -> tuple[str, str]:
        if subject is None:
            return "3", "singular"
        return subject.features.get("person", "3"), subject.features.get("number", "singular")

    @staticmethod
    def _finish(words: list[str], *, question: bool) -> str:
        compact = " ".join(word.strip() for word in words if word and word.strip())
        compact = compact.replace(" ,", ",").replace(" .", ".")
        if not compact:
            compact = "<empty-meaning>"
        compact = compact[0].upper() + compact[1:]
        if compact[-1] not in ".?!":
            compact += "?" if question else "."
        return compact

    @staticmethod
    def _coverage(required: set[Any], emitted: set[Any]) -> float:
        if not required:
            return 1.0
        return len(required & emitted) / len(required)

    def _receipt(self, plan: SemanticPlan, state: _RealizationState) -> CompilationReceipt:
        required_slots = {arg.slot_id for arg in plan.arguments}
        if plan.predicate_slot is not None:
            required_slots.add(plan.predicate_slot)
        required_roles = {arg.role for arg in plan.arguments}
        required_operators = set(plan.operators)

        slot_coverage = self._coverage(required_slots, state.emitted_slots)
        role_coverage = self._coverage(required_roles, state.emitted_roles)
        operator_coverage = self._coverage(required_operators, state.emitted_operators)
        fidelity = round((slot_coverage + role_coverage + operator_coverage) / 3.0, 6)
        return CompilationReceipt(
            required_slots=tuple(sorted(required_slots)),
            emitted_slots=tuple(sorted(state.emitted_slots)),
            required_roles=tuple(sorted(required_roles)),
            emitted_roles=tuple(sorted(state.emitted_roles)),
            required_operators=tuple(sorted(required_operators)),
            emitted_operators=tuple(sorted(state.emitted_operators)),
            unresolved_slots=tuple(sorted(state.unresolved_slots)),
            slot_coverage=round(slot_coverage, 6),
            role_coverage=round(role_coverage, 6),
            operator_coverage=round(operator_coverage, 6),
            structural_fidelity=fidelity,
            warnings=tuple(state.warnings),
        )

    def _predicate(self, plan: SemanticPlan, state: _RealizationState) -> SurfaceLexeme:
        if plan.predicate_slot is None:
            state.warnings.append("missing_predicate_slot")
            return SurfaceLexeme(
                slot_id=-1,
                language_id=plan.language_id,
                lemma="<predicate>",
                pos="verb",
            )
        return self._lexeme(plan.language_id, plan.predicate_slot, state)

    @staticmethod
    def _arguments_by_role(plan: SemanticPlan) -> dict[str, list[int]]:
        out: dict[str, list[int]] = {}
        for arg in plan.arguments:
            out.setdefault(arg.role, []).append(arg.slot_id)
        return out

    def _realize_polish(self, plan: SemanticPlan, state: _RealizationState) -> list[str]:
        args = self._arguments_by_role(plan)
        subject_id = args.get("AGENT", [None])[0]
        subject = self._lexeme("pl", subject_id, state) if subject_id is not None else None
        predicate = self._predicate(plan, state)
        person, number = self._subject_features(subject)

        words: list[str] = []
        if plan.is_question:
            words.append("czy")
            state.emitted_operators.add("QUESTION")
        if not plan.is_action_request and subject is not None:
            form, used = subject.form(GrammaticalCase.NOMINATIVE.value)
            words.append(form)
            state.emitted_roles.add("AGENT")
            if used is None and subject.pos == "noun":
                state.warnings.append(f"missing_form:pl:{subject.slot_id}:nominative")
        elif plan.is_action_request:
            state.emitted_operators.add("ACTION_REQUEST")
            if subject is not None:
                state.emitted_roles.add("AGENT")

        modal_word = self._polish_modal(plan.modal)
        if plan.modal:
            state.emitted_operators.add(self._modal_operator_name(plan.modal))
        if plan.is_negated:
            words.append("nie")
            state.emitted_operators.add("NEGATION")

        if modal_word:
            words.append(modal_word)
            verb, used = predicate.form("infinitive", "base")
        elif plan.is_action_request:
            verb, used = predicate.form("imperative_2sg", "imperative", "base")
        else:
            key = f"present_{person}{'pl' if number == 'plural' else 'sg'}"
            verb, used = predicate.form(key, "present_3sg", "present", "base")
        words.append(verb)
        if used is None:
            state.warnings.append(f"missing_form:pl:{predicate.slot_id}:verb")

        for role in ROLE_ORDER:
            if role == "AGENT":
                continue
            for slot_id in args.get(role, []):
                lexeme = self._lexeme("pl", slot_id, state)
                prefix, case = self._polish_role_surface(role, negated=plan.is_negated)
                form, used = lexeme.form(case.value) if case else lexeme.form("default")
                if prefix:
                    words.append(prefix)
                words.append(form)
                state.emitted_roles.add(role)
                if case and used is None and lexeme.pos == "noun":
                    state.warnings.append(f"missing_form:pl:{slot_id}:{case.value}")

        if "ASSERTION" in plan.operators:
            state.emitted_operators.add("ASSERTION")
        return words

    def _realize_english(self, plan: SemanticPlan, state: _RealizationState) -> list[str]:
        args = self._arguments_by_role(plan)
        subject_id = args.get("AGENT", [None])[0]
        subject = self._lexeme("en", subject_id, state) if subject_id is not None else None
        predicate = self._predicate(plan, state)
        person, number = self._subject_features(subject)
        third_singular = person == "3" and number != "plural"

        base, base_used = predicate.form("base", "infinitive")
        finite, finite_used = predicate.form(
            "present_3sg" if third_singular else "present_non3sg",
            "present",
            "base",
        )
        if base_used is None:
            state.warnings.append(f"missing_form:en:{predicate.slot_id}:base")

        words: list[str] = []
        modal_word = self._english_modal(plan.modal)
        if plan.modal:
            state.emitted_operators.add(self._modal_operator_name(plan.modal))

        subject_surface = subject.lemma if subject else None
        if plan.is_action_request:
            words.append(base)
            state.emitted_operators.add("ACTION_REQUEST")
            if subject is not None:
                state.emitted_roles.add("AGENT")
        elif plan.is_question:
            state.emitted_operators.add("QUESTION")
            if modal_word:
                words.append(modal_word)
            else:
                words.append("does" if third_singular else "do")
            if subject_surface:
                words.append(subject_surface)
                state.emitted_roles.add("AGENT")
            if plan.is_negated:
                words.append("not")
                state.emitted_operators.add("NEGATION")
            words.append(base)
        else:
            if subject_surface:
                words.append(subject_surface)
                state.emitted_roles.add("AGENT")
            if modal_word:
                words.append(modal_word)
                if plan.is_negated:
                    words.append("not")
                    state.emitted_operators.add("NEGATION")
                words.append(base)
            elif plan.is_negated:
                words.extend(["does" if third_singular else "do", "not", base])
                state.emitted_operators.add("NEGATION")
            else:
                words.append(finite)
                if finite_used is None:
                    state.warnings.append(f"missing_form:en:{predicate.slot_id}:finite")

        for role in ROLE_ORDER:
            if role == "AGENT":
                continue
            for slot_id in args.get(role, []):
                lexeme = self._lexeme("en", slot_id, state)
                prefix = self._english_role_prefix(role)
                if prefix:
                    words.append(prefix)
                words.append(lexeme.lemma)
                state.emitted_roles.add(role)

        if "ASSERTION" in plan.operators:
            state.emitted_operators.add("ASSERTION")
        return words

    @staticmethod
    def _modal_operator_name(modal: str) -> str:
        return {
            "possibility": "MODAL_POSSIBILITY",
            "permission": "MODAL_PERMISSION",
            "necessity": "MODAL_NECESSITY",
            "obligation": "MODAL_OBLIGATION",
        }[modal]

    @staticmethod
    def _polish_modal(modal: str | None) -> str | None:
        return {
            None: None,
            "possibility": "może",
            "permission": "może",
            "necessity": "musi",
            "obligation": "musi",
        }[modal]

    @staticmethod
    def _english_modal(modal: str | None) -> str | None:
        return {
            None: None,
            "possibility": "may",
            "permission": "may",
            "necessity": "must",
            "obligation": "must",
        }[modal]

    @staticmethod
    def _polish_role_surface(
        role: str,
        *,
        negated: bool,
    ) -> tuple[str | None, GrammaticalCase | None]:
        table: dict[str, tuple[str | None, GrammaticalCase | None]] = {
            "PATIENT": (
                None,
                GrammaticalCase.GENITIVE if negated else GrammaticalCase.ACCUSATIVE,
            ),
            "THEME": (
                None,
                GrammaticalCase.GENITIVE if negated else GrammaticalCase.ACCUSATIVE,
            ),
            "RECIPIENT": (None, GrammaticalCase.DATIVE),
            "INSTRUMENT": (None, GrammaticalCase.INSTRUMENTAL),
            "SOURCE": ("z", GrammaticalCase.GENITIVE),
            "GOAL": ("do", GrammaticalCase.GENITIVE),
            "LOCATION": ("w", GrammaticalCase.LOCATIVE),
            "TIME": (None, GrammaticalCase.ACCUSATIVE),
            "CAUSE": ("z powodu", GrammaticalCase.GENITIVE),
            "PURPOSE": ("dla", GrammaticalCase.GENITIVE),
            "CONDITION": ("jeśli", GrammaticalCase.NOMINATIVE),
            "MANNER": (None, None),
            "EVIDENCE": ("według", GrammaticalCase.GENITIVE),
            "CLAIM": (None, None),
            "MEMORY_TRACE": ("w pamięci", GrammaticalCase.GENITIVE),
            "CONSENT_TARGET": ("za zgodą", GrammaticalCase.GENITIVE),
            "BOUNDARY": ("do granicy", GrammaticalCase.GENITIVE),
        }
        return table.get(role, (None, None))

    @staticmethod
    def _english_role_prefix(role: str) -> str | None:
        return {
            "PATIENT": None,
            "THEME": None,
            "RECIPIENT": "to",
            "INSTRUMENT": "with",
            "SOURCE": "from",
            "GOAL": "to",
            "LOCATION": "in",
            "TIME": "at",
            "CAUSE": "because of",
            "PURPOSE": "for",
            "CONDITION": "if",
            "MANNER": None,
            "EVIDENCE": "according to",
            "CLAIM": None,
            "MEMORY_TRACE": "in memory of",
            "CONSENT_TARGET": "with consent from",
            "BOUNDARY": "up to",
        }.get(role)
