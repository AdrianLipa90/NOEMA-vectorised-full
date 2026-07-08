# test_fp.py — .python_packages/mpmath/tests/test_fp.py

## Tożsamość
- **id_karty:** `REPO-TEST_FP-A78A`
- **ścieżka:** `.python_packages/mpmath/tests/test_fp.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.724`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mpmath/tests/test_fp.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.724 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_PERMISSION`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.453718`
- **R₃:** `0.541785`
- **R₆:** `0.466054`
- **R₉:** `0.529069`
- **potencjal_kappa:** `0.025212`
- **masa_semantyczna:** `0.161862`
- **rodzaj_karty:** `0.285369`


## Rola
Easy-to-use test-generating code:

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `ae`, `test_conj`, `test_fp_number_parts`, `test_fp_cospi_sinpi`, `test_fp_expj`, `test_fp_bernoulli`, `test_fp_gamma`, `test_fp_psi`, `test_fp_zeta`, `test_fp_hyp2f1`, `test_fp_erf`, `test_fp_lambertw`, `test_fp_stress_ei_e1`

## Opis
Easy-to-use test-generating code:

cases = '''
exp 2.25
log 2.25
'''

from mpmath import *
mp.dps = 20
for test in cases.splitlines():
    if not test:
        continue
    words = test.split()
    fname = words[0]
    args = words[1:]
    argstr = ", ".join(args)
    testline = "%s(%s)" % (fname, argstr)
    ans = str(eval(testline))
    print "    assert ae(fp.%s, %s)" % (testline, ans)
