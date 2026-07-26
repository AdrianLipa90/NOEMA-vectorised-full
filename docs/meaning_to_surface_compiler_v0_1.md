# Meaning-to-Surface Compiler v0.1

## Status

Candidate implementation on a feature branch. It does not promote SOURCE, canon,
NOEMA CURRENT, or external writeback.

## Purpose

CIELingo already supports the analysis direction:

```text
surface text -> RegionalSolveResult -> MeaningEquation
```

This module adds the first bounded implementation of the missing forward direction:

```text
MeaningEquation -> SemanticPlan -> PL/EN surface text
```

The compiler treats language as a finite reconstruction program for relational
meaning. It does not claim that a word contains meaning or that structural
coverage alone proves listener-level understanding.

## Public API

```python
from cielingo_core.generation import (
    MeaningToSurfaceCompiler,
    SurfaceLexeme,
)
```

The input is the existing GLOBAL `MeaningEquation`. A language-local lexicon maps
GLOBAL slot identifiers to lemmas, grammatical forms and features.

The output is `CompiledUtterance`, containing:

- generated text and tokens;
- the language-independent `SemanticPlan`;
- a `CompilationReceipt`;
- explicit `canon_allowed=False` and `noema_writeback_allowed=False` boundaries.

## Supported v0.1 operations

- Polish and English surface realization;
- AGENT, PATIENT, THEME and the remaining existing GLOBAL semantic roles;
- assertion, question, negation and action request;
- possibility, permission, necessity and obligation modals;
- Polish role-to-case hints;
- Polish accusative-to-genitive switch for a negated PATIENT/THEME;
- Polish imperative selection;
- English simple-present agreement and question/negation do-support;
- explicit unresolved-slot placeholders;
- strict mode that refuses an unclosed realization.

## Structural receipt

For every compilation, the compiler compares requested and emitted:

- semantic slots;
- semantic roles;
- universal operators.

It reports

```text
slot_coverage
role_coverage
operator_coverage
structural_fidelity
unresolved_slots
warnings
```

The score is deliberately called **structural fidelity**, not semantic truth. A
future independent listener pass must parse the generated utterance back into a
new `MeaningEquation` and compare the reconstructed meaning with the intended
meaning.

## Example

```python
lexicon = [
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
        forms={"base": "widzieć", "present_3sg": "widzi"},
    ),
    SurfaceLexeme(
        3,
        "pl",
        "mysz",
        forms={"accusative": "mysz", "genitive": "myszy"},
    ),
]

compiler = MeaningToSurfaceCompiler(lexicon)
out = compiler.compile(meaning_equation, "pl")
print(out.text)
print(out.receipt.to_dict())
```

For a question with negation, the bounded realizer can produce:

```text
Czy kot nie widzi myszy?
```

## Boundaries

This version is not:

- a complete Polish morphology engine;
- a complete English grammar;
- an LLM or probabilistic paraphraser;
- a listener-level semantic-equivalence proof;
- a physical measurement of meaning;
- a canon or source-promotion mechanism.

Missing forms fall back to the lemma and create a warning. Missing lexical slots
remain visible as `<slot:N>` and prevent a valid receipt.

## Next implementation gates

1. Build a lexicon adapter for the existing CIELingo card and linguistic databases.
2. Add independent listener-side re-parsing and `MeaningEquation` comparison.
3. Compare relational roles, scope, temporality, modality and pragmatics separately.
4. Add a Polish morphology provider behind the stable `SurfaceLexeme.forms` ABI.
5. Replace PhaseNav linear phase averaging with circular/vector invariants before
   using phase geometry in semantic selection.
6. Add candidate generation and rank candidates by semantic reconstruction error,
   ambiguity, residue and utterance cost.

## Validation

The initial test suite covers:

- Polish assertion;
- Polish question plus negation and patient genitive;
- English question with do-support;
- Polish action request with imperative;
- visible unresolved slots;
- strict refusal on incomplete realization;
- explicit rejection of unsupported languages.
