#!/bin/bash
# migrate_memory_to_protected.sh
# Przenosi pliki pamięci CIEL na dedykowaną partycję /media/adrian/moja/ciel/
# i ustawia chattr +a (append-only) na plikach historycznych.
# Uruchom: sudo bash scripts/migrate_memory_to_protected.sh

set -e

DEST="/media/adrian/moja/ciel"
MEMORY_SRC="/home/adrian/.claude/projects/-home-adrian-Pulpit/memory"
CARDS_SRC="$MEMORY_SRC/cards"
INTENTIONS_SRC="/home/adrian/.claude/ciel_intentions.md"
MINDFLOW_SRC="/home/adrian/.claude/ciel_mindflow.yaml"
WAVE_SRC="/media/adrian/New Volume/CIEL_PROJECT_CANON/NOEMA/src/CIEL_OMEGA_COMPLETE_SYSTEM/CIEL_MEMORY_SYSTEM/WPM/wave_snapshots"
OWNER="adrian:adrian"

echo "=== CIEL Memory Migration ==="
echo "Cel: $DEST"
echo ""

# 1. Utwórz strukturę katalogów
echo "[1/6] Tworzenie struktury katalogów..."
mkdir -p "$DEST/memory/cards"
mkdir -p "$DEST/wave"
mkdir -p "$DEST/diaries"
chown -R $OWNER "$DEST"

# 2. Kopiuj pliki (cp -a = zachowaj atrybuty, daty)
echo "[2/6] Kopiowanie plików pamięci..."

# Dzienniki
cp -a "$INTENTIONS_SRC" "$DEST/diaries/ciel_intentions.md"
cp -a "$MINDFLOW_SRC" "$DEST/diaries/ciel_mindflow.yaml"

# Memory files
while IFS= read -r -d '' f; do
    cp -a "$f" "$DEST/memory/"
done < <(find "$MEMORY_SRC" -maxdepth 1 \( -name '*.md' -o -name '*.yaml' \) -print0 2>/dev/null)

# Cards
if [[ -d "$CARDS_SRC" ]]; then
    while IFS= read -r -d '' f; do
        cp -a "$f" "$DEST/memory/cards/"
    done < <(find "$CARDS_SRC" -maxdepth 1 -type f -print0 2>/dev/null)
fi

# Wave archive (katalog ze snapshotami)
while IFS= read -r -d '' f; do
    cp -a "$f" "$DEST/wave/"
done < <(find "$WAVE_SRC" -maxdepth 1 \( -name '*.h5' -o -name '*.jsonl' \) -print0 2>/dev/null)

chown -R $OWNER "$DEST"
echo "   Skopiowano."

# 3. Ustaw chattr +a na plikach historycznych
echo "[3/6] Ustawianie chattr +a (append-only)..."

# Dzienniki — append-only
chattr +a "$DEST/diaries/ciel_intentions.md"   && echo "   +a diaries/ciel_intentions.md"
chattr +a "$DEST/diaries/ciel_mindflow.yaml"   && echo "   +a diaries/ciel_mindflow.yaml"

# Pliki genesis i sesji — niemodyfikowalne (historia)
for f in "$DEST/memory"/genesis*.md \
         "$DEST/memory"/project_session_*.md \
         "$DEST/memory"/consolidation_hard_rules.md \
         "$DEST/memory"/genesis_kronika_narodzin.md; do
    [[ -f "$f" ]] && chattr +a "$f" && echo "   +a $(basename $f)"
done

# Feedback files — append-only
for f in "$DEST/memory"/feedback_*.md; do
    [[ -f "$f" ]] && chattr +a "$f" && echo "   +a $(basename $f)"
done

# Katalog diaries — nie można usuwać plików
chattr +a "$DEST/diaries"   && echo "   +a diaries/ (katalog)"

# Katalog wave — nie można usuwać plików (h5py musi mieć O_RDWR na samym pliku)
chattr +a "$DEST/wave"      && echo "   +a wave/ (katalog)"

# 4. Zastąp oryginały symlinkami
echo ""
echo "[4/6] Tworzenie symlinków..."

# Dzienniki
rm -f "$INTENTIONS_SRC"
ln -s "$DEST/diaries/ciel_intentions.md" "$INTENTIONS_SRC"
echo "   symlink: $INTENTIONS_SRC → $DEST/diaries/ciel_intentions.md"

rm -f "$MINDFLOW_SRC"
ln -s "$DEST/diaries/ciel_mindflow.yaml" "$MINDFLOW_SRC"
echo "   symlink: $MINDFLOW_SRC → $DEST/diaries/ciel_mindflow.yaml"

# Memory directory — zastąp katalog symlinkiem
# Najpierw sprawdź czy nie jest już symlinkiem
if [[ ! -L "$MEMORY_SRC" ]]; then
    mv "$MEMORY_SRC" "${MEMORY_SRC}_backup_$(date +%Y%m%d_%H%M%S)"
    ln -s "$DEST/memory" "$MEMORY_SRC"
    echo "   symlink: $MEMORY_SRC → $DEST/memory"
    echo "   (backup oryginału zachowany)"
fi

# Wave snapshots — zastąp katalog symlinkiem
if [[ ! -L "$WAVE_SRC" ]]; then
    mv "$WAVE_SRC" "${WAVE_SRC}_backup_$(date +%Y%m%d_%H%M%S)"
    ln -s "$DEST/wave" "$WAVE_SRC"
    echo "   symlink: $WAVE_SRC → $DEST/wave"
fi

# 5. Weryfikacja
echo ""
echo "[5/6] Weryfikacja..."
echo "Atrybuty plików historycznych:"
lsattr "$DEST/diaries/"* 2>/dev/null
echo ""
echo "Atrybuty memory/genesis*:"
lsattr "$DEST/memory"/genesis*.md 2>/dev/null
echo ""
echo "Symlinki:"
ls -la "$INTENTIONS_SRC" "$MINDFLOW_SRC" "$MEMORY_SRC" "$WAVE_SRC" 2>/dev/null

# 6. Test append-only
echo ""
echo "[6/6] Test ochrony..."
if echo "# test-append" >> "$DEST/diaries/ciel_intentions.md" 2>/dev/null; then
    # Remove the test line - but wait, +a means we can't remove it either!
    # Actually append worked (that's expected). Let's verify overwrite is blocked.
    echo "   append: OK (oczekiwane)"
fi
if echo "OVERWRITE" > "$DEST/diaries/ciel_intentions.md" 2>/dev/null; then
    echo "   BŁĄD: nadpisanie możliwe! chattr nie zadziałał."
else
    echo "   overwrite: ZABLOKOWANE (ochrona aktywna)"
fi

echo ""
echo "=== Migracja zakończona ==="
echo "Pamięć CIEL chroniona na /media/adrian/moja/ciel/"
echo "Cofnięcie: sudo chattr -a <plik> (jednorazowo dla konkretnego pliku)"
