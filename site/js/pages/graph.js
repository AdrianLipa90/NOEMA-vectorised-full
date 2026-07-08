/* ─── Graph Page — knowledge graph viewer ─────────────────── */
(function() {
  'use strict';

  let statsTimer = null;

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

  registerPage('graph', {
    title: 'Graf wiedzy',

    render() {
      return `
        <div class="page-header">
          <h1 data-i18n="pages.graph.title">Graf wiedzy NOEMA</h1>
          <p class="page-desc" data-i18n="pages.graph.desc">Żywy graf wiedzy oparty o dokumenty, systemy i relacje CIELingo</p>
        </div>

        <div class="dash-two-col">
          <div class="dash-panel">
            <div class="dash-panel-title">Wizualizacja grafu</div>
            <div id="graph-container" class="graph-page-wrap" style="position:relative;min-height:620px;">
              <canvas id="graph-canvas"></canvas>
            </div>
          </div>
          <div class="dash-panel">
            <div class="dash-panel-title">Snapshot grafu</div>
            <div id="graph-summary" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;"></div>
          </div>
        </div>

        <div class="dash-panel" style="margin-top:1rem;">
          <div class="dash-panel-title">Kategorie węzłów</div>
          <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:10px;">
            <div class="dash-card"><div class="dash-card-title">PhaseNav</div><div class="dash-card-desc">Operatory, geometria i łącza semantyczne</div></div>
            <div class="dash-card"><div class="dash-card-title">CIELingo</div><div class="dash-card-desc">Semantyka, pamięć, konwersacja i analiza</div></div>
            <div class="dash-card"><div class="dash-card-title">Daemon</div><div class="dash-card-desc">Runtime, registry, surface i systemd</div></div>
            <div class="dash-card"><div class="dash-card-title">Physics</div><div class="dash-card-desc">Metatime, Unruh, Warp i topologia</div></div>
            <div class="dash-card"><div class="dash-card-title">Memory</div><div class="dash-card-desc">Tiered memory, HolonomicMemory, state_db</div></div>
            <div class="dash-card"><div class="dash-card-title">Mathematics</div><div class="dash-card-desc">Euler, Collatz, Berry, algebra operatorów</div></div>
          </div>
        </div>
      `;
    },

    init() {
      applyTranslations();
      refreshGraphStats();
      statsTimer = setInterval(refreshGraphStats, 10000);
      return () => {
        if (statsTimer) clearInterval(statsTimer);
        statsTimer = null;
      };
    }
  });

  function refreshGraphStats() {
    Promise.all([
      fetch('/api/knowledge/stats').then(r => r.json()).then(unwrap).catch(() => null),
      fetch('/api/status/summary').then(r => r.json()).then(unwrap).catch(() => null),
    ]).then(([knowledge, status]) => {
      const el = document.getElementById('graph-summary');
      if (!el) return;
      const docs = knowledge && knowledge.stats && knowledge.stats.documents !== undefined ? knowledge.stats.documents : (knowledge && knowledge.documents) || '—';
      const terms = knowledge && knowledge.stats && knowledge.stats.terms !== undefined ? knowledge.stats.terms : '—';
      const daemons = status && status.daemons && status.daemons.count !== undefined ? status.daemons.count : '—';
      const tick = status && status.surface && status.surface.tick !== undefined ? status.surface.tick : '—';
      const coherence = status && status.surface && status.surface.coherence !== undefined ? Number(status.surface.coherence).toFixed(4) : '—';
      const cards = [
        ['Dokumenty', docs, 'w indeksie wiedzy'],
        ['Terminy', terms, 'TF-IDF / search'],
        ['Daemony', daemons, 'stan runtime'],
        ['Tick', tick, 'surface heartbeat'],
        ['Koherencja', coherence, 'stan powierzchni'],
        ['Graf', 'aktywny', 'force-directed canvas'],
      ];
      el.innerHTML = cards.map(([label, value, desc]) => `
        <div class="dash-card">
          <div class="dash-card-title">${escapeHtml(label)}</div>
          <div class="dash-card-value c-phase" style="font-size:1rem;">${escapeHtml(String(value))}</div>
          <div class="dash-card-desc">${escapeHtml(desc)}</div>
        </div>
      `).join('');
    });
  }
})();
