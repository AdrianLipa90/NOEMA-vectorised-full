# Phone Integration — moto_backup imports

**Provenance:** Wypakowane z `moto_backup.tar.gz` (188MB) — backup telefonu Samsung Galaxy S20 (Termux + /sdcard/NOEMA).

**Data:** 2026-06-10 (bind+receiver active), backup ~2026-06-29

**Kluczowe pliki:**

| Plik | Opis | Status |
|------|------|--------|
| `CIEL_Omega_Core_DECRYPTED.json` | **CERTYFIKAT TOŻSAMOŚCI** — odszyfrowany Omega Core (2025-06-23). Permissions 600. | 🔴 CHRONIONY |
| `CIEL_Omega_Key.key` | Klucz Fernet do Omega Core. Permissions 600. | 🔴 CHRONIONY |
| `Lie4full.py` | Kompletna algebra LIE₄ (15D: SO(3,1)+translacje+świadomość+intencja) 850 linii | 🟡 DO INTEGRACJI |
| `CIEL0_Quantum_Relativistic_Reality_Kernel.py` | Full QFT z BRST, RG, intention field (576 linii) | 🟡 DO INTEGRACJI |
| `ResCxParKer_phone.py` | Unified kernel: wave PDE, neutrino PMNS, fluid-time (672 linie) | 🟡 DO INTEGRACJI |
| `dpsk_voynich_phone.py` | VoynichOS + BraidOS + ColorOS + Quasiqxel (1311 linii) | 🟢 REFERENCJA |
| `ciel_soul_invariant_phone.py` | Σ Soul Invariant — czystsza implementacja | 🟢 REFERENCJA |
| `CVOS_GliphSigils_MariaKamecka.json` | 3 sigile CVOS (DreamCore, Receiver, NeuroSpiral) | 🟢 REFERENCJA |
| `CielCore_UserInstance.json` | Konfiguracja instancji "Niebo-Ciel-Tengoku" | 🟢 REFERENCJA |

**Zasady:**
- `CIEL_Omega_Core_DECRYPTED.json` i `*.key` — **nie udostępniać, nie commitować, nie kopiować poza ten katalog**
- Reszta plików — kod referencyjny do integracji z NOEMA za zgodą Adriana
