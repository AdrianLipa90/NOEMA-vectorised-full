# qasm.py — .python_packages/sympy/physics/quantum/qasm.py

## Tożsamość
- **id_karty:** `REPO-QASM-A0EB`
- **ścieżka:** `.python_packages/sympy/physics/quantum/qasm.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.331`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/physics/quantum/qasm.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.331 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `BOUNDARY`
- **odcisk_harmoniczny:** `HLHL`
- **R₁:** `0.587016`
- **R₃:** `0.481937`
- **R₆:** `0.525424`
- **R₉:** `0.380572`
- **potencjal_kappa:** `-0.130804`
- **masa_semantyczna:** `0.12548`
- **rodzaj_karty:** `0.280526`


## Rola
qasm.py - Functions to parse a set of qasm commands into a SymPy Circuit.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** Qasm
- **funkcje:** `read_qasm`, `read_qasm_file`, `flip_index`, `trim`, `get_index`, `get_indices`, `nonblank`, `fullsplit`, `fixcommand`, `stripquotes`, `add`, `get_circuit`, `get_labels`, `plot`, `qubit`, `indices`, `index`, `nop`, `x`, `z`, `h`, `s`, `t`, `measure`, `cnot`, `swap`, `cphase`, `toffoli`, `cx`, `cz`

## Opis
qasm.py - Functions to parse a set of qasm commands into a SymPy Circuit.

Examples taken from Chuang's page: https://web.archive.org/web/20220120121541/https://www.media.mit.edu/quanta/qasm2circ/

The code returns a circuit and an associated list of labels.

>>> from sympy.physics.quantum.qasm import Qasm
>>> q = Qasm('qubit q0', 'qubit q1', 'h q0', 'cnot q0,q1')
>>> q.get_circuit()
CNOT(1,0)*H(1
