/* ─── Architecture Page — mapa portalu, API i przepływów danych ── */
(function() {
  'use strict';

  let refreshInterval = null;
  let lastManifest = null;
  let lastSummary = null;
  let lastContracts = null;

  function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

  registerPage('architecture', {
    title: 'Architektura portalu',

    render() {
      return `
        <div class="page-header">
          <h1 data-i18n="pages.architecture.title">Architektura portalu</h1>
          <p class="page-desc" data-i18n="pages.architecture.desc">Mapa stron, endpointów i przepływów danych NOEMA</p>
        </div>

        <div class="dash-panel" style="background:linear-gradient(135deg,rgba(0,212,255,0.08),rgba(136,68,255,0.08));border-color:rgba(255,255,255,0.08);">
          <div class="dash-panel-title">Portal snapshot</div>
          <div id="arch-summary" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:10px;font-size:0.82rem;">
            Ładowanie...
          </div>
        </div>

        <div class="dash-panel" style="margin-top:1rem;">
          <div class="dash-panel-title">Warstwy architektury</div>
          <div id="arch-layers" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:10px;">
            Ładowanie...
          </div>
        </div>

        <div class="dash-two-col" style="margin-top:1rem;">
          <div class="dash-panel">
            <div class="dash-panel-title">Strony portalu</div>
            <div id="arch-pages" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:10px;">
              Ładowanie...
            </div>
          </div>
          <div class="dash-panel">
            <div class="dash-panel-title">Data flow</div>
            <div id="arch-pipelines" style="font-family:var(--mono);font-size:0.8rem;line-height:1.7;">
              Ładowanie...
            </div>
          </div>
        </div>

        <div class="dash-panel" style="margin-top:1rem;">
          <div class="dash-panel-title">Kontrakty API</div>
          <div id="arch-contracts" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:10px;">
            Ładowanie...
          </div>
        </div>

        <div class="dash-panel" style="margin-top:1rem;">
          <div class="dash-panel-title">Kontrakty huba</div>
          <div id="arch-hub-contracts" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:10px;">
            Ładowanie...
          </div>
        </div>

        <div class="dash-panel" style="margin-top:1rem;">
          <div class="dash-panel-title" style="cursor:pointer;" onclick="const n=this.nextElementSibling;n.style.display=n.style.display==='none'?'block':'none';this.querySelector('.toggle-icon').textContent=n.style.display==='none'?'▶':'▼';">
            <span class="toggle-icon">▶</span> Odpowiedź JSON
          </div>
          <pre id="arch-raw" style="display:none;font-family:var(--mono);font-size:0.7rem;color:var(--text-dim);overflow:auto;max-height:260px;"></pre>
        </div>
      `;
    },

    init() {
      applyTranslations();
      refresh();
      refreshInterval = setInterval(refresh, 12000);
      return () => {
        if (refreshInterval) clearInterval(refreshInterval);
        refreshInterval = null;
      };
    }
  });

  function refresh() {
    Promise.all([
      fetch('/api/portal/manifest').then(r => r.json()).catch(() => null),
      fetch('/api/status/summary').then(r => r.json()).catch(() => null),
      fetch('/api/hub/contracts').then(r => r.json()).catch(() => null),
    ]).then(([manifestEnvelope, summaryEnvelope, contractsEnvelope]) => {
      const manifest = unwrap(manifestEnvelope);
      const summary = unwrap(summaryEnvelope);
      const contracts = unwrap(contractsEnvelope);
      lastManifest = manifestEnvelope;
      lastSummary = summaryEnvelope;
      lastContracts = contractsEnvelope;
      renderSummary(manifest, summary);
      renderLayers(manifest);
      renderPages(manifest);
      renderEndpoints(manifest);
      renderPipelines(manifest);
      renderContracts(manifest, summary);
      renderHubContracts(contracts);
      updateRaw();
    });
  }

  function unwrap(payload) {
    if (!payload) return null;
    if (payload.ok === true && Object.prototype.hasOwnProperty.call(payload, 'data')) {
      return payload.data;
    }
    return payload;
  }

  function renderSummary(manifest, summary) {
    const el = document.getElementById('arch-summary');
    if (!el) return;
    const portal = manifest && (manifest.hub || manifest.portal) ? (manifest.hub || manifest.portal) : {};
    const live = summary && summary.portal ? summary.portal : {};
    const daemons = summary && summary.daemons ? summary.daemons : {};
    const surface = summary && summary.surface ? summary.surface : {};
    const blocks = [
      { label: 'Hub', value: portal.name || 'CIEL Server Hub', desc: `port ${portal.port || '—'}` },
      { label: 'Uptime', value: live.uptime_s !== undefined ? `${live.uptime_s}s` : '—', desc: 'czas pracy portalu' },
      { label: 'Strony', value: manifest && manifest.summary && manifest.summary.page_count !== undefined ? manifest.summary.page_count : (manifest && manifest.pages ? manifest.pages.length : '—'), desc: 'pełny katalog SPA' },
      { label: 'Daemony', value: daemons.count !== undefined ? daemons.count : '—', desc: 'w rejestrze' },
      { label: 'Tick', value: surface.tick !== undefined ? surface.tick : '—', desc: 'ostatni surface tick' },
      { label: 'Koherencja', value: surface.coherence !== undefined ? Number(surface.coherence).toFixed(4) : '—', desc: 'stan powierzchni' },
      { label: 'Wersja', value: manifest && manifest.version ? manifest.version : '—', desc: 'kontrakt manifestu' },
    ];
    el.innerHTML = blocks.map(b => `
      <div class="dash-card" style="padding:0.8rem;">
        <div class="dash-card-title">${b.label}</div>
        <div class="dash-card-value c-cyan" style="font-size:1.1rem;">${escapeHtml(String(b.value))}</div>
        <div class="dash-card-desc">${escapeHtml(b.desc)}</div>
      </div>
    `).join('');
  }

  function renderPages(manifest) {
    const el = document.getElementById('arch-pages');
    if (!el) return;
    const pages = manifest && manifest.pages ? manifest.pages : [];
    if (!pages.length) {
      el.innerHTML = '<div class="dash-card" style="color:var(--muted);">Brak manifestu stron</div>';
      return;
    }
    el.innerHTML = pages.map(page => `
      <div class="dash-card" style="display:flex;flex-direction:column;gap:6px;">
        <div style="display:flex;justify-content:space-between;align-items:center;">
          <div class="dash-card-title" style="margin:0;">${escapeHtml(page.title || page.route || '—')}</div>
          <span style="font-size:0.65rem;padding:2px 6px;border-radius:3px;background:rgba(0,212,255,0.12);color:#44ddff;border:1px solid rgba(68,221,255,0.25);font-family:var(--mono);">
            #${escapeHtml(page.route || '—')}
          </span>
        </div>
        <div class="dash-card-desc">${escapeHtml(page.purpose || '—')}</div>
        <div style="font-size:0.72rem;color:var(--text-dim);font-family:var(--mono);line-height:1.5;">
          ${(page.sources || []).map(s => `<div>↳ ${escapeHtml(s)}</div>`).join('')}
        </div>
        <div style="font-size:0.72rem;color:var(--text-dim);">${escapeHtml(page.notes || '')}</div>
      </div>
    `).join('');
  }

  function renderLayers(manifest) {
    const el = document.getElementById('arch-layers');
    if (!el) return;
    const layers = manifest && manifest.layers ? manifest.layers : [];
    if (!layers.length) {
      el.innerHTML = '<div class="dash-card" style="color:var(--muted);">Brak warstw w manifeście</div>';
      return;
    }
    el.innerHTML = layers.map(layer => `
      <div class="dash-card" style="display:flex;flex-direction:column;gap:6px;">
        <div class="dash-card-title" style="margin:0;">${escapeHtml(layer.name || '—')}</div>
        <div class="dash-card-desc">${escapeHtml(layer.role || '—')}</div>
        <div style="font-size:0.72rem;color:var(--text-dim);font-family:var(--mono);line-height:1.5;">
          ${(layer.sources || []).map(s => `<div>• ${escapeHtml(s)}</div>`).join('')}
        </div>
      </div>
    `).join('');
  }

  function renderEndpoints(manifest) {
    const el = document.getElementById('arch-contracts');
    if (!el) return;
    const endpoints = manifest && manifest.endpoints ? manifest.endpoints : [];
    if (!endpoints.length) {
      el.innerHTML = '<div class="dash-card" style="color:var(--muted);">Brak endpointów w manifeście</div>';
      return;
    }
    el.innerHTML = endpoints.map(ep => `
      <div class="dash-card" style="padding:0.8rem;">
        <div class="dash-card-title">${escapeHtml(ep.path || '—')}</div>
        <div class="dash-card-desc">${escapeHtml(ep.purpose || '—')}</div>
      </div>
    `).join('');
  }

  function renderPipelines(manifest) {
    const el = document.getElementById('arch-pipelines');
    if (!el) return;
    const pipes = manifest && manifest.pipelines ? manifest.pipelines : [];
    if (!pipes.length) {
      el.innerHTML = '<span style="color:var(--muted)">Brak zdefiniowanych przepływów</span>';
      return;
    }
    el.innerHTML = pipes.map(p => `
      <div style="padding:8px 10px;border:1px solid var(--border);border-radius:8px;margin-bottom:8px;background:rgba(255,255,255,0.02);">
        <div style="display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;">
          <strong style="color:#44ddff;">${escapeHtml(p.label || 'pipeline')}</strong>
          <span style="color:var(--text-dim);">${escapeHtml(p.from || '—')} → ${escapeHtml(p.to || '—')}</span>
        </div>
      </div>
    `).join('');
  }

  function renderContracts(manifest, summary) {
    const el = document.getElementById('arch-contracts');
    if (!el) return;
    const portal = manifest && (manifest.hub || manifest.portal) ? (manifest.hub || manifest.portal) : {};
    const summaryPortal = summary && summary.portal ? summary.portal : {};
    const contracts = [
      { name: 'Hub root', value: portal.root || '—', note: 'statyczny katalog site/' },
      { name: 'Live summary', value: summaryPortal.surface_alive ? 'alive' : 'offline', note: 'summary z /api/status/summary' },
      { name: 'Metrics API', value: '/api/metrics', note: 'katalog metryk dla dashboardu' },
      { name: 'Architecture API', value: '/api/portal/manifest', note: 'źródło mapy portalu' },
    ];
    el.innerHTML += contracts.map(c => `
      <div class="dash-card" style="padding:0.8rem;">
        <div class="dash-card-title">${escapeHtml(c.name)}</div>
        <div class="dash-card-value c-purple" style="font-size:0.95rem;">${escapeHtml(c.value)}</div>
        <div class="dash-card-desc">${escapeHtml(c.note)}</div>
      </div>
    `).join('');
  }

  function renderHubContracts(contracts) {
    const el = document.getElementById('arch-hub-contracts');
    if (!el) return;
    const endpoints = contracts && contracts.endpoints ? contracts.endpoints : [];
    if (!endpoints.length) {
      el.innerHTML = '<div class="dash-card" style="color:var(--muted);">Brak kontraktów huba</div>';
      return;
    }
    el.innerHTML = endpoints.map(ep => `
      <div class="dash-card" style="padding:0.8rem;">
        <div class="dash-card-title">${escapeHtml(ep.path || '—')}</div>
        <div class="dash-card-desc">${escapeHtml(ep.summary || ep.description || ep.name || '—')}</div>
      </div>
    `).join('');
  }

  function updateRaw() {
    const el = document.getElementById('arch-raw');
    if (!el) return;
    el.textContent = JSON.stringify({ manifest: lastManifest, summary: lastSummary, contracts: lastContracts }, null, 2);
  }
})();
