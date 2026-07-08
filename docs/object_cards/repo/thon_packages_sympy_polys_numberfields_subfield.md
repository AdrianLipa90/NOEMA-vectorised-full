# subfield.py — .python_packages/sympy/polys/numberfields/subfield.py

## Tożsamość
- **id_karty:** `REPO-SUBFIELD-E320`
- **ścieżka:** `.python_packages/sympy/polys/numberfields/subfield.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.291`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/polys/numberfields/subfield.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.291 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_NECESSITY`
- **odcisk_harmoniczny:** `LLLL`
- **R₁:** `0.449701`
- **R₃:** `0.392905`
- **R₆:** `0.402231`
- **R₉:** `0.439135`
- **potencjal_kappa:** `-0.089486`
- **masa_semantyczna:** `-0.210953`
- **rodzaj_karty:** `0.286192`


## Rola
Functions in ``polys.numberfields.subfield`` solve the "Subfield Problem" and

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `is_isomorphism_possible`, `field_isomorphism_pslq`, `field_isomorphism_factor`, `field_isomorphism`, `_switch_domain`, `_linsolve`, `primitive_element`, `to_number_field`, `_canonicalize`

## Opis
Functions in ``polys.numberfields.subfield`` solve the "Subfield Problem" and
allied problems, for algebraic number fields.

Following Cohen (see [Cohen93]_ Section 4.5), we can define the main problem as
follows:

* **Subfield Problem:**

  Given two number fields $\mathbb{Q}(\alpha)$, $\mathbb{Q}(\beta)$
  via the minimal polynomials for their generators $\alpha$ and $\beta$, decide
  whether on
