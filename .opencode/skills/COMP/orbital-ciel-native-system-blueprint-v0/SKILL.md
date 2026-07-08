---
name: ciel-native-system-blueprint-v0
priority: 4
description: >
  >
---
# CIEL Native Orbital System — blueprint v0

## Contents

- **1.1. Co już istnieje i działa**: Z lokalnej diagnostyki: - rdzeń `systems/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega` przechodzi testy CPU: **56/56 passed**, 
- **1.2. Co jest problemem teraz**: Obecny stan jest dobry jako surowiec, ale nie jako produkt docelowy: - powierzchnia jest zbyt bliska klasycznemu cockpit
- **1.3. Decyzja strategiczna**: **Nie rozwijać HTML/webview jako finalnej powierzchni produktu.** **Budować nową natywną aplikację desktopową**, zachowu
- **2. Cel produktu**: Celem nie jest zwykły panel aplikacji. Celem jest: > **natywny relacyjny system orbitalny**, w którym użytkownik, inform
- **2.1. Definicja robocza produktu**: Produkt ma być: - samodzielną aplikacją desktopową, - niezależną od lokalnego serwera jako mechanizmu UI, - opartą na re
- **2.2. Czego produkt **nie** ma być**: Nie ma to być: - wrapper dla web app, - zwykły chat z dekoracyjnym interfejsem, - launcher modeli, - dashboard DevOps, -
- **3.1. Prymat relacji**: Hierarchia semantyczna systemu: `relacja -> tożsamość -> pamięć -> proces -> artefakt` To oznacza: - użytkownik i CIEL s
- **3.2. LLM jako atraktor tymczasowy**: LLM jest bootstrapem semantycznym i operatorem pomocniczym w fazie wczesnej. Docelowo priorytet ma mieć: 1. wiedza własn

## Key Points

- rdzeń `systems/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega` przechodzi testy CPU: **56/56 passed**,
- główne ścieżki `UnifiedSystem`, bridge pamięć-core-vocabulary i Euler closure są uruchamialne,
- warstwa LLM/GPU jest obecnie **opcjonalna**, nie wymagana dla rdzenia,
- `ciel-omega-demo` jest działającym shellem przejściowym, ale nadal opartym o logikę panelu runtime, a nie natywną geometrię systemu.
- powierzchnia jest zbyt bliska klasycznemu cockpitowi runtime,
- geometria stanu nie jest jeszcze natywnym modelem działania systemu,
- LLM nie jest jeszcze jawnie zredukowany do roli atraktora tymczasowego,
- pliki/moduły/procesy nie mają jeszcze pełnej tożsamości orbitalnej,
- UI nie jest niezależną natywną aplikacją z własnym trybem i własną fizyką interfejsu.
- **frontend natywny:** Qt / PySide6 + QML,
- **backend systemowy:** Python, wyprowadzony z `CIEL_OMEGA_COMPLETE_SYSTEM`,
- **LLM:** moduł pomocniczy, nie centrum systemu,

## Code

```
Typy bytów:
- plik,
- moduł,
- operator,
- pamięć,
- proces,
- sesja,
- artefakt,
- model,
- źródło dowodowe,
- kontrakt / postulat / aksjomat.

Docelowy moduł:
- `ciel_native/registry/`

---

## 4.3. Warstwa C — Autonomy Layer

To warstwa zarządzająca przejściem od zależności od LLM do autonomii CIEL.

### Funkcja
Odpowiada za decyzję:
- czy odpowiedź ma wynikać z własnej pamięci i wiedzy,
- czy system potrzebuje retrieval,
- czy system potrzebuje operatora zewnętrznego,
- kiedy LLM jest dopusz
```

```
Gdzie:
- `alpha_llm` ma maleć w czasie i wraz ze wzrostem pokrycia wiedzy własnej,
- `alpha_ciel` ma rosnąć wraz ze stabilizacją registry, pamięci i operatorów lokalnych.

Docelowy moduł:
- `ciel_native/autonomy/`

---

## 4.4. Warstwa D — Geometry Engine

To warstwa mapująca stan systemu na geometrię roboczą.

### Funkcja
- wyznacza pozycję bytów na dysku Poincaré,
- utrzymuje orbitę i precesję,
- pokazuje sprzężenia i napięcia,
- oblicza ruch między stanami UI,
- pozwala na przejścia ciągłe za
```

---
*Extracted from: `src/CIEL_Orbital_Foundation_Packk/CIEL_NATIVE_SYSTEM_BLUEPRINT_v0.md` (693 lines, 16975B)*