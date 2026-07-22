"""
Czyści skażone wpisy z PhaseMemory (PDF binary, captcha pages).

Uruchom:
    python3 scripts/cielingo_phasememory_clean_corrupt.py

Tworzy backup przed modyfikacją. Nie modyfikuje .npz (dane są w .json;
.npz jest rebuildem przy następnym cold-start CIELingoInference).
"""
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

MEMORY_JSON = Path("/media/adrian/New Volume/CIEL_memories/state/cielingo_phase_memory.json")

CORRUPT_PATTERNS = [
    "%PDF-",
    "JavaScript is disabled",
    "In order to continue, we need to verify that you're not a robot",
    "Enable JavaScript and then reload the page",
]


def is_corrupt(text: str) -> bool:
    for pattern in CORRUPT_PATTERNS:
        if pattern in text[:500]:
            return True
    return False


def main():
    print(f"[{datetime.now(timezone.utc).isoformat()}] Wczytywanie {MEMORY_JSON} ...")
    data = json.loads(MEMORY_JSON.read_text(encoding="utf-8"))

    texts = data.get("texts", [])
    print(f"  Znaleziono {len(texts)} tekstów.")

    corrupt_indices = [i for i, t in enumerate(texts) if is_corrupt(t)]
    print(f"  Skażone indeksy: {corrupt_indices}")

    if not corrupt_indices:
        print("  Nic do czyszczenia.")
        return

    # Backup
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup = MEMORY_JSON.with_suffix(f".json.pre_clean_{ts}")
    shutil.copy2(MEMORY_JSON, backup)
    print(f"  Backup: {backup}")

    # Usuń skażone wpisy
    clean_texts = [t for i, t in enumerate(texts) if i not in corrupt_indices]
    data["texts"] = clean_texts
    print(f"  Po czyszczeniu: {len(clean_texts)} tekstów.")

    # Sprawdź czy są inne tablice równoległe do texts
    # (phases/vectors — jeśli są, muszą też być wyczyszczone)
    for key in data:
        if key == "texts":
            continue
        val = data[key]
        if isinstance(val, list) and len(val) == len(texts):
            print(f"  UWAGA: klucz '{key}' ma tę samą długość co texts ({len(texts)}) "
                  f"— czyszczę odpowiadające indeksy.")
            data[key] = [v for i, v in enumerate(val) if i not in corrupt_indices]

    MEMORY_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  Zapisano. Usunieto {len(corrupt_indices)} skażonych wpisów.")
    print("  Zrestartuj noema-web-research.service i noema-headless.service.")


if __name__ == "__main__":
    main()
