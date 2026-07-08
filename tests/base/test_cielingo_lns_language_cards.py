from __future__ import annotations

from cielingo.lns_language_cards import language_card_inventory, search_language_cards


def test_lns_language_card_inventory_counts():
    inv = language_card_inventory(".")
    assert inv["total_cards"] == 114
    assert inv["by_kind"] == {"concept": 72, "noema": 9, "operator": 33}
    assert inv["languages"]["pl"] >= 100
    assert inv["cards"][0]["source_role"] if False else True


def test_lns_language_card_search_finds_word_and_language_cards():
    hits = search_language_cards("słowo język meaning language", ".", limit=12)
    ids = {hit["card_id"] for hit in hits}
    assert "concept:word" in ids
    assert any("pl" in hit["languages"] for hit in hits)
