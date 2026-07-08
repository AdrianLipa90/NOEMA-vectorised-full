/* ─── Science Page — research and knowledge surface ───────── */
(function() {
  'use strict';

  let scienceTimer = null;

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

  registerPage('science', {
    title: 'Nauka',

    render() {
      return `
        <div class="page-header">
          <h1 data-i18n="nav.science">Nauka</h1>
          <p class="page-desc">Przegląd naukowych warstw NOEMY: wiedza, metryki, architektura i dokumenty</p>
        </div>

        <div class="dash-two-col">
          <div class="dash-panel">
            <div class="dash-panel-title">Stan wiedzy</div>
            <div id="science-kb" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;"></div>
          </div>
          <div class="dash-panel">
            <div class="dash-panel-title">Połączenie z systemem</div>
            <div id="science-system" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;"></div>
          </div>
        </div>

        <div class="dash-panel" style="margin-top:1rem;">
          <div class="dash-panel-title">Wątki badawcze</div>
          <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:10px;">
            <div class="dash-card"><div class="dash-card-title">Metatime</div><div class="dash-card-desc">Czas jako struktura semantyczna, nie tylko zegar.</div></div>
            <div class="dash-card"><div class="dash-card-title">PhaseNav</div><div class="dash-card-desc">Łączenie operatorów z semantyką i afektem.</div></div>
            <div class="dash-card"><div class="dash-card-title">Lingwistyka obliczeniowa</div><div class="dash-card-desc">CIELingo jako mechanizm opisu i pamięci.</div></div>
            <div class="dash-card"><div class="dash-card-title">Architektura systemowa</div><div class="dash-card-desc">Daemony, powierzchnia i IPC jako żywy organizm.</div></div>
          </div>
        </div>
      `;
    },

    init() {
      applyTranslations();
      refreshScience();
      scienceTimer = setInterval(refreshScience, 15000);
      return () => {
        if (scienceTimer) clearInterval(scienceTimer);
        scienceTimer = null;
      };
    }
  });

  function refreshScience() {
    Promise.all([
      fetch('/api/knowledge/stats').then(r => r.json()).then(unwrap).catch(() => null),
      fetch('/api/portal/manifest').then(r => r.json()).then(unwrap).catch(() => null),
      fetch('/api/status/summary').then(r => r.json()).then(unwrap).catch(() => null),
    ]).then(([knowledgeEnvelope, manifestEnvelope, statusEnvelope]) => {
      const knowledge = knowledgeEnvelope || {};
      const manifest = manifestEnvelope || {};
      const status = statusEnvelope || {};

      const kb = document.getElementById('science-kb');
      if (kb) {
        const docs = knowledge.documents ?? knowledge.doc_count ?? '—';
        const terms = knowledge.terms ?? '—';
        const categories = knowledge.categories ?? knowledge.category_count ?? '—';
        kb.innerHTML = [
          ['Dokumenty', docs, 'indeks bazy'],
          ['Terminy', terms, 'pojęcia TF-IDF'],
          ['Kategorie', categories, 'kategoryzacja źródeł'],
        ].map(([label, value, desc]) => `
          <div class="dash-card">
            <div class="dash-card-title">${escapeHtml(label)}</div>
            <div class="dash-card-value c-green">${escapeHtml(String(value))}</div>
            <div class="dash-card-desc">${escapeHtml(desc)}</div>
          </div>
        `).join('');
      }

      const sys = document.getElementById('science-system');
      if (sys) {
        const layers = manifest && manifest.layers ? manifest.layers.length : '—';
        const pages = manifest && manifest.pages ? manifest.pages.length : '—';
        const coherence = status.surface && status.surface.coherence !== undefined ? Number(status.surface.coherence).toFixed(4) : '—';
        sys.innerHTML = [
          ['Warstwy', layers, 'opis architektury'],
          ['Strony', pages, 'katalog SPA'],
          ['Koherencja', coherence, 'stan live'],
        ].map(([label, value, desc]) => `
          <div class="dash-card">
            <div class="dash-card-title">${escapeHtml(label)}</div>
            <div class="dash-card-value c-cyan">${escapeHtml(String(value))}</div>
            <div class="dash-card-desc">${escapeHtml(desc)}</div>
          </div>
        `).join('');
      }
    });
  }
})();
