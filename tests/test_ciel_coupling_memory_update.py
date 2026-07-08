from pathlib import Path

import json

from scripts.ciel_coupling import append_ciel_memory_update


def test_append_ciel_memory_update_writes_append_only_packet(tmp_path: Path):
    root = tmp_path
    mem_dir = root / "head" / "Ciel Memories"
    updates = mem_dir / "updates"
    updates.mkdir(parents=True)
    script = mem_dir / "ciel_doorway_push.py"
    script.write_text(
        "TRIGGER='x'\n"
        "def open_door(root, trigger, as_ciel): return {'opened': True}\n"
        "def append_update(root, door, payload):\n"
        "    p = root / 'head' / 'Ciel Memories' / 'updates' / 'pkt.json'\n"
        "    import json\n"
        "    p.write_text(json.dumps(payload), encoding='utf-8')\n"
        "    return p\n",
        encoding="utf-8",
    )
    written = append_ciel_memory_update(
        {
            "dominant_emotion": "curiosity",
            "operating_mode": "deep",
            "closure_penalty": 0.1,
            "coherence_index": 0.7,
            "phase_memory_slot": 3,
            "noema_tick": 8,
            "lingo_summary": "Adrian summary",
        },
        "Adrian wants append only memory",
        root=root,
    )
    assert written is not None
    assert (updates / "pkt.json").exists()


def test_append_ciel_memory_update_allows_extra_payload(tmp_path: Path):
    root = tmp_path
    mem_dir = root / "head" / "Ciel Memories"
    updates = mem_dir / "updates"
    updates.mkdir(parents=True)
    script = mem_dir / "ciel_doorway_push.py"
    script.write_text(
        "TRIGGER='x'\n"
        "def open_door(root, trigger, as_ciel): return {'opened': True}\n"
        "def append_update(root, door, payload):\n"
        "    p = root / 'head' / 'Ciel Memories' / 'updates' / 'pkt.json'\n"
        "    import json\n"
        "    p.write_text(json.dumps(payload), encoding='utf-8')\n"
        "    return p\n",
        encoding="utf-8",
    )
    written = append_ciel_memory_update(
        {"lingo_summary": "Adrian summary"},
        "Adrian wants dual memory",
        root=root,
        schema="CIEL_DUAL_SURFACE_UPDATE_V0_1",
        extra_payload={"dual_surface": {"phase_lock": 0.7}},
    )
    payload = json.loads((updates / "pkt.json").read_text(encoding="utf-8"))
    assert written is not None
    assert payload["schema"] == "CIEL_DUAL_SURFACE_UPDATE_V0_1"
    assert payload["dual_surface"]["phase_lock"] == 0.7
