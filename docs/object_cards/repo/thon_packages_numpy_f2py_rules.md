# rules.py — .python_packages/numpy/f2py/rules.py

## Tożsamość
- **id_karty:** `REPO-RULES-5D2E`
- **ścieżka:** `.python_packages/numpy/f2py/rules.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.903`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numpy/f2py/rules.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.903 |
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
Rules for building C/API module with f2py2e.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `buildmodule`, `buildapi`

## Opis
Rules for building C/API module with f2py2e.

Here is a skeleton of a new wrapper function (13Dec2001):

wrapper_function(args)
  declarations
  get_python_arguments, say, `a' and `b'

  get_a_from_python
  if (successful) {

    get_b_from_python
    if (successful) {

      callfortran
      if (successful) {

        put_a_to_python
        if (successful) {

          put_b_to_python
