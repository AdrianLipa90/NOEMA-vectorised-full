# rrule.py — .python_packages/dateutil/rrule.py

## Tożsamość
- **id_karty:** `REPO-RRULE-DB33`
- **ścieżka:** `.python_packages/dateutil/rrule.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.910`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/dateutil/rrule.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.910 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `AFFECT`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.542195`
- **R₃:** `0.629813`
- **R₆:** `0.534142`
- **R₉:** `0.565106`
- **potencjal_kappa:** `0.141102`
- **masa_semantyczna:** `0.203631`
- **rodzaj_karty:** `0.326785`


## Rola
The rrule module offers a small, complete, and very fast, implementation of

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** weekday, rrulebase, rrule, _iterinfo, rruleset, _rrulestr, _genitem
- **funkcje:** `_invalidates_cache`, `inner_func`, `_invalidate_cache`, `_iter_cached`, `count`, `before`, `after`, `xafter`, `between`, `replace`, `_iter`, `rebuild`, `ydayset`, `mdayset`, `wdayset`, `ddayset`, `htimeset`, `mtimeset`, `stimeset`, `rrule`, `rdate`, `exrule`, `exdate`, `_iter`, `_handle_int`, `_handle_int_list`, `_handle_FREQ`, `_handle_UNTIL`, `_handle_WKST`, `_handle_BYWEEKDAY`

## Opis
The rrule module offers a small, complete, and very fast, implementation of
the recurrence rules documented in the
`iCalendar RFC <https://tools.ietf.org/html/rfc5545>`_,
including support for caching of results.
