# ops.py — .python_packages/mypyc/ir/ops.py

## Tożsamość
- **id_karty:** `REPO-OPS-DFDB`
- **ścieżka:** `.python_packages/mypyc/ir/ops.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.578`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypyc/ir/ops.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.578 |
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
Low-level opcodes for compiler intermediate representation (IR).

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** BasicBlock, Value, Register, Integer, Float, CString, Undef, Op, BaseAssign, Assign, AssignMulti, ControlOp, Goto, Branch, Return, Unreachable, RegisterOp, IncRef, DecRef, Call
- **funkcje:** `has_fixed_width_int`, `terminated`, `terminator`, `is_void`, `is_void`, `numeric_value`, `can_raise`, `sources`, `set_sources`, `stolen`, `unique_sources`, `accept`, `sources`, `set_sources`, `stolen`, `accept`, `sources`, `set_sources`, `stolen`, `accept`, `targets`, `set_target`, `targets`, `set_target`, `sources`, `set_sources`, `accept`, `targets`, `set_target`, `sources`

## Opis
Low-level opcodes for compiler intermediate representation (IR).

Opcodes operate on abstract values (Value) in a register machine. Each
value has a type (RType). A value can hold various things, such as:

- local variables or temporaries (Register)
- intermediate values of expressions (RegisterOp subclasses)
- condition flags (true/false)
- literals (integer literals, True, False, etc.)

NOTE: As
