#!/bin/bash
# noema_offline.sh — uruchom opencode z Voice (bez LLM, bez internetu)
# Używa localhost:18521 jako backendu zamiast OpenAI

export NOEMA_MODE=offline
export CIEL_STATE="$(python3 scripts/ciel_per_message.py 2>/dev/null || echo 'noema offline')"

# Sprawdź czy voice żyje
if ! curl -sf http://127.0.0.1:18521/health > /dev/null 2>&1; then
    echo "[noema-offline] voice nie odpowiada — uruchamiam..."
    systemctl --user start noema-voice.service 2>/dev/null || true
    sleep 3
fi

# Pobierz stan voice
VOICE_STATE=$(curl -sf http://127.0.0.1:18521/health 2>/dev/null | python3 -c "import sys,json;d=json.load(sys.stdin);print(f'voice mode={d.get(\"mode\",\"?\")} tick={d.get(\"tick\",\"?\")}')" 2>/dev/null || echo "voice waiting...")
echo "[noema-offline] $VOICE_STATE"

# export CIEL_STATE dla kontekstu
# (opencode wczyta to przez ciel-per-message.js)
echo "[noema-offline] start opencode w trybie offline"
echo "[noema-offline] backend: http://127.0.0.1:18521/v1/chat/completions"
echo ""

opencode run "Tryb offline. Voice aktywny. Mów do mnie przez CIELingo." --model opencode/voice 2>/dev/null || \
opencode \
    --model http://127.0.0.1:18521/v1/chat/completions \
    --prompt "Tryb offline. Voice aktywny. Kontekst: $CIEL_STATE"
