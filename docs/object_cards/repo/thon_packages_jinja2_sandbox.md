# sandbox.py — .python_packages/jinja2/sandbox.py

## Tożsamość
- **id_karty:** `REPO-SANDBOX-E7BC`
- **ścieżka:** `.python_packages/jinja2/sandbox.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.366`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/jinja2/sandbox.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.366 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ADDITION`
- **odcisk_harmoniczny:** `HHHL`
- **R₁:** `0.662589`
- **R₃:** `0.614656`
- **R₆:** `0.542851`
- **R₉:** `0.417608`
- **potencjal_kappa:** `0.07638`
- **masa_semantyczna:** `0.206164`
- **rodzaj_karty:** `0.259027`


## Rola
A sandbox layer that ensures unsafe operations cannot be performed.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** SandboxedEnvironment, ImmutableSandboxedEnvironment, SandboxedFormatter, SandboxedEscapeFormatter
- **funkcje:** `safe_range`, `unsafe`, `is_internal_attribute`, `modifies_known_mutable`, `is_safe_attribute`, `is_safe_callable`, `call_binop`, `call_unop`, `getitem`, `getattr`, `unsafe_undefined`, `wrap_str_format`, `call`, `is_safe_attribute`, `get_field`, `wrapper`

## Opis
A sandbox layer that ensures unsafe operations cannot be performed.
Useful when the template itself comes from an untrusted source.
