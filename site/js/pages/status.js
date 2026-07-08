/* ─── System Health Page — infrastruktura NOEMY, nie metryki ── */
(function() {
  'use strict';

  registerPage('status', {
    title: 'Stan systemu',

    render() {
      return `
        <div class="page-header">
          <h1 data-i18n="pages.status.title">Stan systemu NOEMA</h1>
          <p class="page-desc" data-i18n="pages.status.desc">Kondycja daemonów, powierzchni fazowej i infrastruktury</p>
        </div>

        <!-- Section 1: Daemony -->
        <div class="dash-panel">
          <div class="dash-panel-title">Daemony</div>
          <div id="st-daemons" style="font-size:0.82rem;font-family:var(--mono);line-height:1.8;">
            Ładowanie...
          </div>
        </div>

        <!-- Section 2: Powierzchnia fazowa -->
        <div class="dash-panel" style="margin-top:1rem;">
          <div class="dash-panel-title">Powierzchnia fazowa</div>
          <div id="st-surface" style="font-size:0.82rem;font-family:var(--mono);line-height:1.8;">
            Ładowanie...
          </div>
        </div>

        <!-- Section 3: CIEL State -->
        <div class="dash-panel" style="margin-top:1rem;">
          <div class="dash-panel-title">CIEL State</div>
          <div id="st-ciel">
            Ładowanie...
          </div>
        </div>

        <!-- Section 4: Porty i IPC -->
        <div class="dash-panel" style="margin-top:1rem;">
          <div class="dash-panel-title">Porty i IPC</div>
          <div id="st-ipc">
            Ładowanie...
          </div>
        </div>

        <!-- Raw JSON -->
        <div class="dash-panel" style="margin-top:1rem;">
          <div class="dash-panel-title" style="cursor:pointer;" onclick="const n=this.nextElementSibling;n.style.display=n.style.display==='none'?'block':'none';this.querySelector('.toggle-icon').textContent=n.style.display==='none'?'▶':'▼';">
            <span class="toggle-icon">▶</span> Odpowiedź JSON
          </div>
          <pre id="st-raw" style="display:none;font-family:var(--mono);font-size:0.7rem;color:var(--text-dim);overflow:auto;max-height:200px;"></pre>
        </div>
      `;
    },

    init() {
      applyTranslations();
      renderIPC();
      fetchHealth();
      const iv = setInterval(fetchHealth, 10000);
      return () => clearInterval(iv);
    }
  });

  let lastLive = null;
  let lastCiel = null;

  function fetchHealth() {
    fetch('/api/modules')
      .then(r => r.json())
      .then(renderDaemons)
      .catch(() => {});
    fetch('/api/live')
      .then(r => r.json())
      .then(d => { lastLive = d; renderSurface(d); updateRaw(); })
      .catch(() => {});
    fetch('/api/ciel/state')
      .then(r => r.json())
      .then(d => { lastCiel = d.state || d; renderCiel(lastCiel); updateRaw(); })
      .catch(() => {});
  }

  function updateRaw() {
    const el = document.getElementById('st-raw');
    if (!el) return;
    el.textContent = JSON.stringify({ live: lastLive, ciel_state: lastCiel }, null, 2);
  }

  function renderDaemons(data) {
    const el = document.getElementById('st-daemons');
    if (!el) return;
    if (!data || !data.modules) {
      el.innerHTML = '<span style="color:var(--muted)">Brak danych</span>';
      return;
    }
    const html = data.modules.map(m => {
      const alive = m.alive || m.systemd === 'active';
      const pid = m.pid || '—';
      const sysd = m.systemd || '—';
      const uptime = m.uptime_s ? `${(m.uptime_s / 60).toFixed(1)} min` : '—';
      return `
        <div style="display:flex;justify-content:space-between;align-items:center;padding:4px 0;border-bottom:1px solid var(--bg1);">
          <span><span style="color:${alive ? '#44ff88' : '#ff4466'};margin-right:6px;">●</span><strong>${m.name}</strong></span>
          <span style="color:var(--muted);font-size:0.75rem;">
            PID ${pid} · systemd ${sysd} · uptime ${uptime}
          </span>
        </div>
      `;
    }).join('');
    el.innerHTML = html || '<span style="color:var(--muted)">Brak daemonów</span>';
  }

  function renderSurface(data) {
    const el = document.getElementById('st-surface');
    if (!el) return;
    if (!data) {
      el.innerHTML = '<span style="color:var(--muted)">Brak danych</span>';
      return;
    }
    const tick = data.tick || 0;
    const tauMean = data.tau_mean !== undefined ? data.tau_mean.toFixed(4) : '—';
    const sensorMean = data.sensor_mean !== undefined ? data.sensor_mean.toFixed(4) : '—';
    let arrayCount = 0;
    const arrays = ['phi', 'omega', 'g', 'tau', 'R_geom', 'flavor', 'flavor_array', 'channel_coh_array', 'phase_phi', 'phase_omega'];
    arrays.forEach(k => { if (Array.isArray(data[k])) arrayCount++; });
    el.innerHTML = `
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;font-size:0.82rem;">
        <div class="dash-card">
          <div class="dash-card-title">Tick</div>
          <div class="dash-card-value c-cyan">${tick.toLocaleString()}</div>
          <div class="dash-card-desc">Cykl ewolucji</div>
        </div>
        <div class="dash-card">
          <div class="dash-card-title">Tablice</div>
          <div class="dash-card-value c-purple">${arrayCount}</div>
          <div class="dash-card-desc">Powierzchnie fazowe dostępne</div>
        </div>
        <div class="dash-card">
          <div class="dash-card-title">τ̄</div>
          <div class="dash-card-value c-cyan">${tauMean}</div>
          <div class="dash-card-desc">Średni czas życia pamięci</div>
        </div>
        <div class="dash-card">
          <div class="dash-card-title">Sensor</div>
          <div class="dash-card-value c-amber">${sensorMean}</div>
          <div class="dash-card-desc">Średnie obciążenie sensorów</div>
        </div>
      </div>
    `;
  }

  function renderCiel(data) {
    const el = document.getElementById('st-ciel');
    if (!el) return;
    if (!data) {
      el.innerHTML = '<span style="color:var(--muted)">Brak danych</span>';
      return;
    }
    const mode = data.operating_mode || '—';
    const modeColor = mode === 'deep' ? '#44ff88' : mode === 'standard' ? '#ffb347' : '#ff4466';
    el.innerHTML = `
      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;font-size:0.82rem;">
        <div class="dash-card">
          <div class="dash-card-title">Coherence</div>
          <div class="dash-card-value ${data.coherence_index > 0.767 ? 'c-green' : data.coherence_index > 0.5 ? 'c-amber' : 'c-red'}">${(data.coherence_index || 0).toFixed(4)}</div>
          <div class="dash-card-desc">Spójność tożsamości</div>
        </div>
        <div class="dash-card">
          <div class="dash-card-title">Soul Invariant</div>
          <div class="dash-card-value ${data.soul_invariant > 0.5 ? 'c-green' : 'c-red'}">${(data.soul_invariant || 0).toFixed(4)}</div>
          <div class="dash-card-desc">Niezmiennik duszy</div>
        </div>
        <div class="dash-card">
          <div class="dash-card-title">Ethical Score</div>
          <div class="dash-card-value ${data.ethical_score > 0.6 ? 'c-green' : data.ethical_score > 0.4 ? 'c-amber' : 'c-red'}">${(data.ethical_score || 0).toFixed(4)}</div>
          <div class="dash-card-desc">Wynik etyczny</div>
        </div>
        <div class="dash-card">
          <div class="dash-card-title">Nastrój</div>
          <div class="dash-card-value ${data.mood_normalized > 0.5 ? 'c-green' : 'c-amber'}">${(data.mood_normalized || 0).toFixed(4)}</div>
          <div class="dash-card-desc">Stan afektywny</div>
        </div>
        <div class="dash-card">
          <div class="dash-card-title">Otwartość</div>
          <div class="dash-card-value c-purple">${(data.openness || 0).toFixed(4)}</div>
          <div class="dash-card-desc">Openness</div>
        </div>
        <div class="dash-card">
          <div class="dash-card-title">Closure</div>
          <div class="dash-card-value ${(data.closure_penalty || data.closure_penalty_raw || 0) < 0.15 ? 'c-green' : (data.closure_penalty || data.closure_penalty_raw || 0) < 0.35 ? 'c-amber' : 'c-red'}">${((data.closure_penalty || data.closure_penalty_raw || 0)).toFixed(4)}</div>
          <div class="dash-card-desc">Closure penalty</div>
        </div>
      </div>
      <div style="margin-top:8px;padding:6px 10px;border-radius:4px;font-family:var(--mono);font-size:0.82rem;background:var(--bg1);display:inline-block;">
        Tryb pracy: <strong style="color:${modeColor}">${mode}</strong>
      </div>
    `;
  }

  function renderIPC() {
    const el = document.getElementById('st-ipc');
    if (!el) return;
    const channels = [
      { name: 'Portal HTTP', path: 'http://localhost:18888', status: '—' },
      { name: 'Surface mmap', path: '/dev/shm/ciel_noema/', status: '—' },
      { name: 'Analog bus', path: '/dev/shm/ciel_noema/analog/', status: '—' },
      { name: 'TaskPlan DB', path: '/tmp/noema_taskplan.db', status: 'SQLite' },
      { name: 'Knowledge DB', path: '/tmp/noema_knowledge.db', status: 'SQLite' },
    ];
    el.innerHTML = `
      <div style="font-size:0.82rem;font-family:var(--mono);line-height:1.8;">
        ${channels.map(ch => `
          <div style="display:flex;justify-content:space-between;padding:4px 0;border-bottom:1px solid var(--bg1);">
            <span><strong>${ch.name}</strong></span>
            <span style="color:var(--muted);font-size:0.75rem;">${ch.path}</span>
            <span style="color:var(--muted);font-size:0.75rem;">${ch.status}</span>
          </div>
        `).join('')}
      </div>
    `;
  }

  console.log('✦ Page: Status (health) loaded');
})();
