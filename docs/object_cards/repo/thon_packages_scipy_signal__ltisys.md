# _ltisys.py — .python_packages/scipy/signal/_ltisys.py

## Tożsamość
- **id_karty:** `REPO-_LTISYS-E2C8`
- **ścieżka:** `.python_packages/scipy/signal/_ltisys.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.600`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/signal/_ltisys.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.600 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ACTION_REQUEST`
- **odcisk_harmoniczny:** `LLHL`
- **R₁:** `0.419252`
- **R₃:** `0.442825`
- **R₆:** `0.60198`
- **R₉:** `0.41548`
- **potencjal_kappa:** `-0.118614`
- **masa_semantyczna:** `0.191681`
- **rodzaj_karty:** `0.278922`


## Rola
ltisys -- a collection of classes and functions for modeling linear

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** LinearTimeInvariant, lti, dlti, TransferFunction, TransferFunctionContinuous, TransferFunctionDiscrete, ZerosPolesGain, ZerosPolesGainContinuous, ZerosPolesGainDiscrete, StateSpace, StateSpaceContinuous, StateSpaceDiscrete, Bunch
- **funkcje:** `lsim`, `_default_response_times`, `impulse`, `step`, `bode`, `freqresp`, `_valid_inputs`, `_order_complex_poles`, `_KNV0`, `_YT_real`, `_YT_complex`, `_YT_loop`, `_KNV0_loop`, `place_poles`, `dlsim`, `dimpulse`, `dstep`, `dfreqresp`, `dbode`, `dt`, `_dt_dict`, `zeros`, `poles`, `_as_ss`, `_as_zpk`, `_as_tf`, `impulse`, `step`, `output`, `bode`

## Opis
ltisys -- a collection of classes and functions for modeling linear
time invariant systems.
