# log_trace.py — .python_packages/mypyc/transform/log_trace.py

## Tożsamość
- **id_karty:** `REPO-LOG_TRACE-B466`
- **ścieżka:** `.python_packages/mypyc/transform/log_trace.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.546`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypyc/transform/log_trace.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.546 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CAUSE`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.440841`
- **R₃:** `0.698384`
- **R₆:** `0.560357`
- **R₉:** `0.385177`
- **potencjal_kappa:** `0.165796`
- **masa_semantyczna:** `0.077602`
- **rodzaj_karty:** `0.2472`


## Rola
This optional pass adds logging of various executed operations.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** LogTraceEventTransform
- **funkcje:** `insert_event_trace_logging`, `get_load_global_name`, `visit_call`, `visit_primitive_op`, `visit_call_c`, `visit_get_attr`, `visit_set_attr`, `visit_box`, `visit_unbox`, `visit_cast`, `visit_inc_ref`, `visit_dec_ref`, `log_inc_ref`, `log`, `log_event`

## Opis
This optional pass adds logging of various executed operations.

Some subset of the executed operations are logged to the mypyc_trace.txt file.

This is useful for performance analysis. For example, it's possible
to identify how frequently various primitive functions are called,
and in which code locations they are called.
