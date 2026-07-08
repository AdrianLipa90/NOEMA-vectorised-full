---
date: 2026-06-27
tags: [knowledge-db, ocr, tesseract, tf-idf, affect]
---

# 2026-06-27 part 3 — Knowledge DB rebuild: OCR + affect fix + affinity

## OCR przez tesseract (9 PDFów)
- Lambda (2), Interstellar to Centauri, SOD, mobius1, whole project of healing
- pbh, CielOmegaSystemReport, basis of eather, DLPS starship
- **Wszystkie 545/545 z tekstem**

## term_index rebuild
- 545 docs, **54,506 unique terms**, 562,661 term-doc pairs
- TF-IDF od zera po dodaniu OCRowanych tekstów

## semantic_affinity rebuild
- Próg 0.05 → 0.02 → **10,815 affinity pairs** (było 7,710)

## Affect lexicon fix
- 99 grief/sad → "focused" dla dokumentów naukowych
- 15 → "neutral" dla mieszanych
- Tylko 14 emocjonalnych (grief/sad) zostało — faktycznie o relacjach/crime/traumie

## Testy
- "euler identity closure penalty" → step11_euler_j_functional.pdf (sim=0.25, focused)
- "neutrino PMNS mixing" → neutrino_detector (focused)
- "crimes relations" → Crimes_in_relations (sad — poprawnie)

## Knowledge DB state
| Tabela | Stan |
|--------|------|
| doc_analysis | 545 rows, wszystkie analyzed |
| term_index | 562,661 pairs, 54,506 terms |
| semantic_affinity | 10,815 par, threshold 0.02 |
| corpus_stats | 1 row |

## Key decisions
- OCR: pdftoppm + tesseract (pol+eng), pierwsze 5 stron 300dpi
- Affect: sci_count ≥ 2 → focused, ≥ 1 → neutral
- Semantic affinity: tylko TF-IDF (nie agent backend — za wolne dla 545 doków)

## Goal
- 545 dokumentów Adriana w bazie → odpowiadanie na pytania bez czytania PDFów
