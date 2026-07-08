/* ─── Simulations Page — graphics scenes and phase replay ─── */
(function() {
  'use strict';

  let currentScene = 'surface';
  let simTimer = null;

  function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

  function unwrap(payload) {
    if (!payload) return null;
    if (payload.ok === true && Object.prototype.hasOwnProperty.call(payload, 'data')) {
      return payload.data;
    }
    return payload;
  }

  registerPage('simulations', {
    title: 'Symulacje',

    render() {
      return `
        <div class="page-header">
          <h1 data-i18n="nav.simulations">Symulacje</h1>
          <p class="page-desc">Podgląd scen PhaseNav: powierzchnia, relacje, pamięć i operatory</p>
        </div>

        <div class="dash-panel">
          <div class="dash-panel-title">Sceny</div>
          <div id="sim-tabs" style="display:flex;flex-wrap:wrap;gap:8px;margin:10px 0 12px;">
            <button class="sim-btn active" data-scene="surface">Surface</button>
            <button class="sim-btn" data-scene="relations">Relacje</button>
            <button class="sim-btn" data-scene="memory">Pamięć</button>
            <button class="sim-btn" data-scene="operators">Operatory</button>
          </div>
          <div id="sim-summary" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:10px;margin-bottom:12px;"></div>
          <div id="sim-view" class="pn-graphics-view" style="min-height:420px;"></div>
        </div>

        <style>
          .sim-btn{border:1px solid rgba(68,221,255,0.2);background:rgba(255,255,255,0.02);color:var(--text);border-radius:999px;padding:6px 12px;font-size:0.78rem;cursor:pointer;font-family:var(--mono);}
          .sim-btn.active{background:rgba(68,221,255,0.12);border-color:rgba(68,221,255,0.38);color:#d7fbff;}
        </style>
      `;
    },

    init() {
      applyTranslations();
      bindTabs();
      refreshSimulations();
      simTimer = setInterval(refreshSimulations, 10000);
      return () => {
        if (simTimer) clearInterval(simTimer);
        simTimer = null;
      };
    }
  });

  function bindTabs() {
    const tabs = document.getElementById('sim-tabs');
    if (!tabs) return;
    tabs.querySelectorAll('.sim-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        currentScene = btn.dataset.scene || 'surface';
        tabs.querySelectorAll('.sim-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        refreshSimulations();
      });
    });
  }

  function refreshSimulations() {
    fetch(`/api/phasenav/graphics?scene=${encodeURIComponent(currentScene)}&q=NOEMA`)
      .then(r => r.json())
      .then(unwrap)
      .then(data => {
        renderSimulations(data || {});
      })
      .catch(() => {
        renderSimulations({});
      });
  }

  function renderSimulations(data) {
    const view = document.getElementById('sim-view');
    const summary = document.getElementById('sim-summary');
    if (!view || !summary) return;

    const scenes = data && data.scenes ? data.scenes : {};
    const scene = data && data.scene ? data.scene : (scenes[currentScene] || scenes.surface || null);
    if (scene && scene.svg) {
      view.innerHTML = scene.svg;
    } else {
      view.innerHTML = '<div style="padding:24px;color:var(--muted);">Brak sceny do wyrenderowania</div>';
    }

    const surface = data && data.surface ? data.surface : {};
    const sceneCounts = data && data.scene_counts ? data.scene_counts : {};
    summary.innerHTML = [
      ['Scene', data.scene_name || currentScene, 'aktywny widok'],
      ['Tick', surface.tick !== undefined ? surface.tick : '—', 'surface'],
      ['Koherencja', surface.coherence !== undefined ? Number(surface.coherence).toFixed(4) : '—', 'live'],
      ['Nodes', scene && scene.summary ? scene.summary.node_count : '—', 'scena'],
      ['Edges', scene && scene.summary ? scene.summary.edge_count : '—', 'scena'],
      ['Bundle', Object.keys(sceneCounts).length, 'scenes in bundle'],
    ].map(([label, value, desc]) => `
      <div class="dash-card">
        <div class="dash-card-title">${escapeHtml(label)}</div>
        <div class="dash-card-value c-phase">${escapeHtml(String(value))}</div>
        <div class="dash-card-desc">${escapeHtml(desc)}</div>
      </div>
    `).join('');
  }
})();
