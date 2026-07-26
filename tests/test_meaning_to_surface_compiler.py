import pytest

from cielingo_core.generation import CompilationError, MeaningToSurfaceCompiler, SurfaceLexeme
from cielingo_core.global_layer.contracts import (
    MeaningEquation,
    UniversalOperator,
    UniversalOperatorType,
    UniversalRole,
)


def lexicon():
    return [
        SurfaceLexeme(
            1,
            "pl",
            "kot",
            forms={"nominative": "kot"},
            features={"person": "3", "number": "singular"},
        ),
        SurfaceLexeme(
            2,
            "pl",
            "widzieć",
            pos="verb",
            forms={"base": "widzieć", "infinitive": "widzieć", "present_3sg": "widzi"},
        ),
        SurfaceLexeme(
            3,
            "pl",
            "mysz",
            forms={"accusative": "mysz", "genitive": "myszy"},
        ),
        SurfaceLexeme(
            4,
            "pl",
            "przynieść",
            pos="verb",
            forms={"base": "przynieść", "imperative_2sg": "przynieś"},
        ),
        SurfaceLexeme(
            5,
            "pl",
            "woda",
            forms={"accusative": "wodę", "genitive": "wody"},
        ),
        SurfaceLexeme(
            1,
            "en",
            "the cat",
            features={"person": "3", "number": "singular"},
        ),
        SurfaceLexeme(
            2,
            "en",
            "see",
            pos="verb",
            forms={"base": "see", "present_3sg": "sees"},
        ),
        SurfaceLexeme(3, "en", "the mouse"),
    ]


def equation(*operators):
    return MeaningEquation(
        equation_id="eq-cat-see-mouse",
        predicate_slot=2,
        roles={UniversalRole.AGENT: 1, UniversalRole.PATIENT: 3},
        operators=[UniversalOperator(op) for op in operators],
    )


def test_polish_assertion_closes_structurally():
    out = MeaningToSurfaceCompiler(lexicon()).compile(
        equation(UniversalOperatorType.ASSERTION), "pl"
    )
    assert out.text == "Kot widzi mysz."
    assert out.receipt.valid
    assert out.receipt.structural_fidelity == 1.0


def test_polish_question_and_negation_select_genitive_patient():
    out = MeaningToSurfaceCompiler(lexicon()).compile(
        equation(UniversalOperatorType.QUESTION, UniversalOperatorType.NEGATION), "pl"
    )
    assert out.text == "Czy kot nie widzi myszy?"
    assert set(out.receipt.emitted_operators) == {"NEGATION", "QUESTION"}
    assert out.receipt.valid


def test_english_question_uses_do_support():
    out = MeaningToSurfaceCompiler(lexicon()).compile(
        equation(UniversalOperatorType.QUESTION), "en"
    )
    assert out.text == "Does the cat see the mouse?"
    assert out.receipt.valid


def test_polish_action_request_uses_imperative():
    eq = MeaningEquation(
        equation_id="eq-bring-water",
        predicate_slot=4,
        roles={UniversalRole.PATIENT: 5},
        operators=[UniversalOperator(UniversalOperatorType.ACTION_REQUEST)],
    )
    out = MeaningToSurfaceCompiler(lexicon()).compile(eq, "pl")
    assert out.text == "Przynieś wodę."
    assert out.receipt.valid


def test_unresolved_slot_is_visible_and_fails_receipt():
    eq = MeaningEquation(
        equation_id="eq-missing",
        predicate_slot=2,
        roles={UniversalRole.AGENT: 1, UniversalRole.PATIENT: 99},
    )
    out = MeaningToSurfaceCompiler(lexicon()).compile(eq, "en")
    assert "<slot:99>" in out.text
    assert out.receipt.unresolved_slots == (99,)
    assert not out.receipt.valid


def test_strict_mode_rejects_unclosed_realization():
    eq = MeaningEquation(
        equation_id="eq-missing",
        predicate_slot=2,
        roles={UniversalRole.PATIENT: 99},
    )
    with pytest.raises(CompilationError):
        MeaningToSurfaceCompiler(lexicon(), strict=True).compile(eq, "pl")


def test_unsupported_language_is_explicit():
    with pytest.raises(CompilationError, match="unsupported language_id"):
        MeaningToSurfaceCompiler(lexicon()).compile(equation(), "ja")
