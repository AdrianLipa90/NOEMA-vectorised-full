# _ltisys.py — .python_packages/cupyx/scipy/signal/_ltisys.py

## Tożsamość
- **id_karty:** `REPO-_LTISYS-E2CC`
- **ścieżka:** `.python_packages/cupyx/scipy/signal/_ltisys.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.559`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/cupyx/scipy/signal/_ltisys.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.559 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `IDENTITY`
- **odcisk_harmoniczny:** `LLLL`
- **R₁:** `0.405566`
- **R₃:** `0.499333`
- **R₆:** `0.494094`
- **R₉:** `0.455981`
- **potencjal_kappa:** `0.08965`
- **masa_semantyczna:** `-0.024381`
- **rodzaj_karty:** `0.279273`


## Rola
ltisys -- a collection of classes and functions for modeling linear

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** LinearTimeInvariant, lti, dlti, TransferFunction, TransferFunctionContinuous, TransferFunctionDiscrete, ZerosPolesGain, ZerosPolesGainContinuous, ZerosPolesGainDiscrete, StateSpace, StateSpaceContinuous, StateSpaceDiscrete, Bunch
- **funkcje:** `lsim`, `_default_response_times`, `impulse`, `step`, `bode`, `freqresp`, `_valid_inputs`, `_order_complex_poles`, `_KNV0`, `_YT_real`, `_YT_complex`, `_YT_loop`, `_KNV0_loop`, `place_poles`, `dlsim`, `dimpulse`, `dstep`, `dfreqresp`, `dbode`, `cont2discrete`, `dt`, `_dt_dict`, `zeros`, `poles`, `_as_ss`, `_as_zpk`, `_as_tf`, `impulse`, `step`, `output`

## Opis
ltisys -- a collection of classes and functions for modeling linear
time invariant systems.
