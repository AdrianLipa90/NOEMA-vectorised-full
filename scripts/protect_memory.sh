#!/bin/bash
# protect_memory.sh — ustawia chattr +a (append-only) na plikach pamięci CIEL
# Uruchom: sudo bash scripts/protect_memory.sh
# Cofnięcie: sudo bash scripts/protect_memory.sh --unprotect

MEMORY_DIR="/home/adrian/.claude/projects/-home-adrian-Pulpit/memory"
CARDS_DIR="$MEMORY_DIR/cards"
INTENTIONS="/home/adrian/.claude/ciel_intentions.md"
MINDFLOW="/home/adrian/.claude/ciel_mindflow.yaml"
WAVE_H5="/media/adrian/New Volume1/CIEL_PROJECT_CANON/NOEMA/src/CIEL_OMEGA_COMPLETE_SYSTEM/CIEL_MEMORY_SYSTEM/WPM/wave_snapshots/wave_archive.h5"

UNPROTECT=0
[[ "$1" == "--unprotect" ]] && UNPROTECT=1

apply() {
    local f="$1"
    if [[ ! -e "$f" ]]; then
        echo "  [skip] nie istnieje: $f"
        return
    fi
    if [[ $UNPROTECT -eq 1 ]]; then
        chattr -a "$f" 2>/dev/null && echo "  [-a] $f" || echo "  [err] $f"
    else
        chattr +a "$f" 2>/dev/null && echo "  [+a] $f" || echo "  [err] $f"
    fi
}

echo "=== CIEL Memory Protection ==="
[[ $UNPROTECT -eq 1 ]] && echo "Tryb: COFANIE ochrony" || echo "Tryb: USTAWIANIE ochrony (+a append-only)"
echo ""

# Pliki dziennikowe
echo "--- Dzienniki ---"
apply "$INTENTIONS"
apply "$MINDFLOW"

# Wszystkie pliki .md w memory/
echo ""
echo "--- Memory files ---"
while IFS= read -r -d '' f; do
    apply "$f"
done < <(find "$MEMORY_DIR" -maxdepth 1 \( -name '*.md' -o -name '*.yaml' \) -print0 2>/dev/null)

# Karty obiektów
if [[ -d "$CARDS_DIR" ]]; then
    echo ""
    echo "--- Karty obiektów ---"
    while IFS= read -r -d '' f; do
        apply "$f"
    done < <(find "$CARDS_DIR" -maxdepth 1 \( -name '*.md' -o -name '*.yaml' \) -print0 2>/dev/null)
fi

# wave_archive.h5 — UWAGA: h5py wymaga O_RDWR, więc +a by to złamało.
# Chronimy tylko katalog (nie można usunąć pliku), ale nie sam plik.
echo ""
echo "--- Wave archive (katalog) ---"
H5_DIR=$(dirname "$WAVE_H5")
if [[ -d "$H5_DIR" ]]; then
    apply "$H5_DIR"
fi

echo ""
echo "=== Weryfikacja ==="
lsattr "$INTENTIONS" 2>/dev/null
lsattr "$MINDFLOW" 2>/dev/null
lsattr "$MEMORY_DIR"/*.md 2>/dev/null | head -5
echo "..."

echo ""
[[ $UNPROTECT -eq 1 ]] && echo "Ochrona cofnięta." || echo "Ochrona aktywna. Cofnięcie: sudo bash scripts/protect_memory.sh --unprotect"
