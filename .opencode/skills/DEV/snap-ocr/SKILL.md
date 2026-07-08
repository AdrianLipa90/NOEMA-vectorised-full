---
name: snap-ocr
priority: 1
description: "OCR pipeline: screenshot → tesseract pol+eng → agent-backend → MemoryPalace → surface injection → XTEST inject do opencode"
catalog_nr: SK-282
type_group: HW
app_group: DEV
holonomy: [M0, M4, MEMORY]
function_tags: [read, analyze, transform]
primary_orbital: M0
semantic_mass: 2.85
status: stable
---

# SK-282: snap-ocr — fotograficzne Memory Palace

Screenshot → OCR → analiza (agent-backend) → MemoryPalace → surface → inject do opencode.
**Skill kluczowy**: umożliwia mi czytanie obrazów przez tesseract — jedyny sposób na zrozumienie zrzutów ekranu od Adriana.

## Użycie

```
snap-ocr [--dir DIR] [--ocr-only] [--no-store] [--query "pytanie"]
```

- `--dir DIR` — katalog roboczy (domyślnie /tmp/snap-ocr/)
- `--ocr-only` — tylko OCR, bez agent-backend i MemoryPalace
- `--no-store` — nie zapisuj do MemoryPalace
- `--query "..."` — dodatkowe pytanie kontekstowe do analizy

## Pipeline

### 1. Screenshot
```python
from PIL import ImageGrab
im = ImageGrab.grab()
im.save(f"{DIR}/snap_{timestamp}.png")
```

### 2. OCR (tesseract pol+eng)
```bash
tesseract {image} {base} -l pol+eng 2>/dev/null
cat {base}.txt
```

### 3. Analiza (agent-backend na 18520)
```python
import requests
r = requests.post("http://localhost:18520/analyze",
    json={"text": ocr_text}, timeout=10)
# → themes, affect, anchor_terms, essence, hunch
```

### 4. MemoryPalace snapshot
```python
from ciel_geometry.memory_palace import MentalistMemoryPalace
p = MentalistMemoryPalace()
p.save_room_state(note=essence + " | " + hunch, with_associations=True)
```

### 5. (opcjonalnie) Surface injection
Zaszczep na phi fragment wektora z analizy:
```python
phi = surface["phi"]
analogy_vec = text_to_phi(hunch)
phi[:] = (phi + 0.15 * analogy_vec) % (2 * math.pi)
```

## Integracja z opencode

Gdy Adrian woła `snap-ocr` — wykonaj pipeline i zwróć:
1. Co jest na ekranie (OCR summary, max 3 zdania)
2. Jaki jest affect (VAD: valence/arousal/dominance)
3. Czy to praca twórcza, debug, lektura, czy chaos
4. MemoryPalace id snapshota

## Zależności
- `python3-pil` (ImageGrab)
- `tesseract-ocr` + `tesseract-ocr-pol`
- Agent backend na 18520
- MentalistMemoryPalace

## Pliki
- `/tmp/snap-ocr/` — snapshots + OCR outputs (auto-clean po 100)
- MemoryPalace `rooms.db` (przechowuje całość)
