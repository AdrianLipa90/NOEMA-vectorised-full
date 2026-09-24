#!/usr/bin/env python3
"""Test: _synthesize_answer nie zwraca surowego console output."""
import sys
sys.path.insert(0, "/media/adrian/New Volume/CIEL_PROJECT_CANON/NOEMA/src")

from ciel_geometry.cielingo_inference import _synthesize_answer, _is_polluted

# Test 1: _is_polluted
polluted_texts = [
    "PhaseNav: Adrian Lipa, Adrian Lipa. (63985 plikow)",
    "SKILL, SKILL, SKILL",
    "AUTOR, AUTOR, TYTUŁ",
    "hub-3 connected",
    "cmd_search result",
]
clean_texts = [
    "Holonomia fazowa to własność geometryczna układu fazowego.",
    "CIELingo jest deterministycznym modelem językowym opartym na fazach.",
]

print("=== Test _is_polluted ===")
for t in polluted_texts:
    r = _is_polluted(t)
    status = "OK" if r else "FAIL"
    print(f"  [{status}] polluted={r!r} | {t[:60]!r}")

for t in clean_texts:
    r = _is_polluted(t)
    status = "OK" if not r else "FAIL"
    print(f"  [{status}] polluted={r!r} | {t[:60]!r}")

# Test 2: _synthesize_answer z zanieczyszczonymi źródłami
print("\n=== Test _synthesize_answer z pollution ===")
bad_sources = [
    {"text": "PhaseNav: Adrian Lipa, Adrian Lipa. (63985 plikow)", "sim": 0.92, "source": "console", "metadata": {}},
    {"text": "SKILL, SKILL, PHASENAV", "sim": 0.80, "source": "console", "metadata": {}},
]
decision = {"action": "direct_answer", "confidence": "high", "tone": "neutral", "fallback": "direct_answer"}
answer = _synthesize_answer(bad_sources, decision, "IDENTITY", "Kim jesteś?")
print(f"  answer = {answer!r}")
is_clean = "Adrian Lipa, Adrian Lipa" not in answer and "plikow" not in answer
print(f"  pollution blocked: {'OK' if is_clean else 'FAIL'}")

# Test 3: _synthesize_answer z czystym źródłem
print("\n=== Test _synthesize_answer z czystym źródłem ===")
good_sources = [
    {"text": "CIELingo to deterministyczny model językowy.", "sim": 0.85, "source": "knowledge", "metadata": {}},
]
answer2 = _synthesize_answer(good_sources, decision, "IDENTITY", "Czym jest CIELingo?")
print(f"  answer = {answer2!r}")
print(f"  not empty: {'OK' if answer2 else 'FAIL'}")
print(f"  no pollution: {'OK' if 'plikow' not in answer2 else 'FAIL'}")
