# dates.py — .python_packages/matplotlib/dates.py

## Tożsamość
- **id_karty:** `REPO-DATES-8D21`
- **ścieżka:** `.python_packages/matplotlib/dates.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.442`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/matplotlib/dates.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.442 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `SIMULATION_BOUNDARY`
- **odcisk_harmoniczny:** `HLLH`
- **R₁:** `0.575665`
- **R₃:** `0.306554`
- **R₆:** `0.381064`
- **R₉:** `0.528951`
- **potencjal_kappa:** `-0.226686`
- **masa_semantyczna:** `-0.021063`
- **rodzaj_karty:** `0.269599`


## Rola
Matplotlib provides sophisticated date plotting capabilities, standing on the

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** DateFormatter, ConciseDateFormatter, AutoDateFormatter, rrulewrapper, DateLocator, RRuleLocator, AutoDateLocator, YearLocator, MonthLocator, WeekdayLocator, DayLocator, HourLocator, MinuteLocator, SecondLocator, MicrosecondLocator, DateConverter, ConciseDateConverter, _SwitchableDateConverter
- **funkcje:** `_get_tzinfo`, `_reset_epoch_test_example`, `set_epoch`, `get_epoch`, `_dt64_to_ordinalf`, `_from_ordinalf`, `datestr2num`, `date2num`, `num2date`, `num2timedelta`, `drange`, `_wrap_in_tex`, `set_tzinfo`, `format_ticks`, `get_offset`, `format_data_short`, `_set_locator`, `set`, `_update_rrule`, `_attach_tzinfo`, `_aware_return_wrapper`, `set_tzinfo`, `datalim_to_dt`, `viewlim_to_dt`, `_get_unit`, `_get_interval`, `nonsingular`, `tick_values`, `_create_rrule`, `_get_unit`

## Opis
Matplotlib provides sophisticated date plotting capabilities, standing on the
shoulders of python :mod:`datetime` and the add-on module dateutil_.

By default, Matplotlib uses the units machinery described in
`~matplotlib.units` to convert `datetime.datetime`, and `numpy.datetime64`
objects when plotted on an x- or y-axis. The user does not
need to do anything for dates to be formatted, but dates
