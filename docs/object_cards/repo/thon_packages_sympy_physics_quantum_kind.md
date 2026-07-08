# kind.py — .python_packages/sympy/physics/quantum/kind.py

## Tożsamość
- **id_karty:** `REPO-KIND-2AB5`
- **ścieżka:** `.python_packages/sympy/physics/quantum/kind.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.922`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/physics/quantum/kind.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.922 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `FOLD`
- **odcisk_harmoniczny:** `LHHH`
- **R₁:** `0.351212`
- **R₃:** `0.661831`
- **R₆:** `0.649218`
- **R₉:** `0.522246`
- **potencjal_kappa:** `-0.135067`
- **masa_semantyczna:** `-0.137397`
- **rodzaj_karty:** `0.29302`


## Rola
Kinds for Operators, Bras, and Kets.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** _KetKind, _BraKind, _OperatorKind
- **funkcje:** `_mul_number_ket_kind`, `_mul_number_bra_kind`, `_mul_operator_kind`

## Opis
Kinds for Operators, Bras, and Kets.

This module defines kinds for operators, bras, and kets. These are useful
in various places in ``sympy.physics.quantum`` as you often want to know
what the kind is of a compound expression. For example, if you multiply
an operator, bra, or ket by a number, you get back another operator, bra,
or ket - even though if you did an ``isinstance`` check you would fin
