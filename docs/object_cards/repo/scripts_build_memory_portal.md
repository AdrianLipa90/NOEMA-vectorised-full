# build_memory_portal.py — scripts/build_memory_portal.py

## Tożsamość
- **id_karty:** `REPO-BUILD_MEMORY_PORTAL-600C`
- **ścieżka:** `scripts/build_memory_portal.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `3.321`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/build_memory_portal.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 3.321 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `UNRUH_DRIVE`
- **odcisk_harmoniczny:** `HLLH`
- **R₁:** `0.695214`
- **R₃:** `0.356299`
- **R₆:** `0.471302`
- **R₉:** `0.535169`
- **potencjal_kappa:** `0.138014`
- **masa_semantyczna:** `0.204514`
- **rodzaj_karty:** `0.244249`


## Rola
CIEL Memory Portal Generator

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_init_tags_table`, `_get_sessions`, `_auto_tag_session`, `auto_tag_all_sessions`, `_build_tag_index`, `_load_memory_entries`, `_load_live`, `_tag_class`, `_render_tags`, `_src_cls`, `_src_label`, `_session_preview`, `_rel_path`, `_topbar`, `_html_wrap`, `build_index`, `build_archive`, `build_memory`, `generate`, `nav`

## Opis
CIEL Memory Portal Generator

Buduje statyczny portal HTML w ~//media/adrian/New Volume1/CIEL_memories/portal/

Strony:
  index.html   — hub: ostatnie sesje + metryki + szybkie linki
  archive.html — przegląd wszystkich sesji z filtrowaniem po tagu/źródle
  memory.html  — mapa tagów (consciousness geometry)

Dane:
  data/sessions.json   — eksport SQLite: sesje z tagami
  data/tag_index.json  — {ta
