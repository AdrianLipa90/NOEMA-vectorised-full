from pathlib import Path

from src.cielingo.stage0_radical_cards import (
    load_radicals,
    load_language_entries,
    load_alignments,
    validate_all,
)

ROOT = Path(__file__).resolve().parents[1]
RADICALS = ROOT / "cards/cielingo_radicals/radical_cards_seed_v0_1.jsonl"
EN = ROOT / "cards/cielingo_languages/en/slot_entries_test_v0_1.jsonl"
JA = ROOT / "cards/cielingo_languages/ja/slot_entries_test_v0_1.jsonl"
ALIGN = ROOT / "cards/cielingo_alignments/alignment_seed_en_ja_v0_1.jsonl"


def test_seed_counts_match():
    assert len(load_radicals(RADICALS)) == 24
    assert len(load_language_entries(EN)) == 24
    assert len(load_language_entries(JA)) == 24
    assert len(load_alignments(ALIGN)) == 24


def test_every_radical_has_en_and_ja_entry():
    radicals = {r.slot_id for r in load_radicals(RADICALS)}
    en = {e.slot_id for e in load_language_entries(EN)}
    ja = {e.slot_id for e in load_language_entries(JA)}
    assert radicals == en == ja


def test_no_source_by_default():
    assert all(r.source_binding != "SOURCE" for r in load_radicals(RADICALS))
    assert all(e.source_binding != "SOURCE" for e in load_language_entries(EN))
    assert all(e.source_binding != "SOURCE" for e in load_language_entries(JA))
    assert all(a.source_binding != "SOURCE" for a in load_alignments(ALIGN))


def test_japanese_entries_need_native_review():
    ja = load_language_entries(JA)
    assert all(e.needs_native_review for e in ja)
    assert all(e.j_functionals["J_native_review_required"] == 1.0 for e in ja)


def test_local_holonomy_differs_between_en_and_ja():
    en_by_slot = {e.slot_id: e for e in load_language_entries(EN)}
    ja_by_slot = {e.slot_id: e for e in load_language_entries(JA)}
    # File slot: EN article load vs JA particle/politeness load are deliberately distinct.
    assert en_by_slot[15].j_functionals["J_article_load"] > 0
    assert ja_by_slot[15].j_functionals["J_particle_load"] > en_by_slot[15].j_functionals["J_article_load"]


def test_alignment_does_not_claim_identity():
    for alignment in load_alignments(ALIGN):
        for member in alignment.members:
            assert member["equivalence_type"] != "identity"


def test_verify_and_file_slots_exist_for_ad_hoc_sentence_equations():
    radicals = {r.label: r for r in load_radicals(RADICALS)}
    assert "CHECK_VERIFY" in radicals
    assert "FILE" in radicals

    en = {e.slot_id: e for e in load_language_entries(EN)}
    ja = {e.slot_id: e for e in load_language_entries(JA)}
    assert "check" in en[16].surface_forms
    assert "file" in en[15].surface_forms
    assert "確認する" in ja[16].surface_forms
    assert "ファイル" in ja[15].surface_forms


def test_full_seed_validation_passes():
    result = validate_all(RADICALS, EN, JA, ALIGN)
    assert result["ok"], result["issues"]
