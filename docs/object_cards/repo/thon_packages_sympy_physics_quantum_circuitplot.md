# circuitplot.py — .python_packages/sympy/physics/quantum/circuitplot.py

## Tożsamość
- **id_karty:** `REPO-CIRCUITPLOT-5249`
- **ścieżka:** `.python_packages/sympy/physics/quantum/circuitplot.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.018`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/physics/quantum/circuitplot.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.018 |
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
Matplotlib based plotting of quantum circuits.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** CircuitPlot, Mz, Mx, CreateOneQubitGate
- **funkcje:** `circuit_plot`, `render_label`, `labeller`, `CreateCGate`, `update`, `_create_grid`, `_create_figure`, `_plot_wires`, `_plot_measured_wires`, `_gates`, `_plot_gates`, `_measurements`, `_finish`, `one_qubit_box`, `two_qubit_box`, `control_line`, `control_point`, `not_point`, `swap_point`, `ControlledGate`

## Opis
Matplotlib based plotting of quantum circuits.

Todo:

* Optimize printing of large circuits.
* Get this to work with single gates.
* Do a better job checking the form of circuits to make sure it is a Mul of
  Gates.
* Get multi-target gates plotting.
* Get initial and final states to plot.
* Get measurements to plot. Might need to rethink measurement as a gate
  issue.
* Get scale and figsize to
