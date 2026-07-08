/* ─── Monograph Page — katalog prac Adriana Lipy ────────────── */
(function() {
  'use strict';

  registerPage('monograph', {
    title: 'Monografia',

    render() {
      return `
        <div class="page-header">
          <h1 data-i18n="pages.monograph.title">Monografia — prace Adriana Lipy</h1>
          <p class="page-desc" data-i18n="pages.monograph.desc">Katalog dokumentów i opracowań w bazie wiedzy NOEMY</p>
        </div>

        <div class="dash-panel">
          <div class="dash-panel-title">Statystyki bazy</div>
          <div id="mg-stats" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;">
            <div class="dash-card">
              <div class="dash-card-title">Dokumenty</div>
              <div class="dash-card-value c-phase" id="mg-doc-count">—</div>
              <div class="dash-card-desc">Łączna liczba dokumentów w bazie</div>
            </div>
            <div class="dash-card">
              <div class="dash-card-title">Terminy</div>
              <div class="dash-card-value c-purple" id="mg-term-count">—</div>
              <div class="dash-card-desc">Indeksowane terminy (TF-IDF)</div>
            </div>
          </div>
        </div>

        <div class="dash-panel" style="margin-top:1rem;">
          <div class="dash-panel-title">Kategorie dokumentów</div>
          <p style="font-size:0.82rem;color:var(--text-dim);margin-bottom:12px;">
            Baza wiedzy NOEMY zawiera <strong id="mg-cat-count">545</strong> dokumentów
            obejmujących następujące kategorie:
          </p>
          <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:10px;">
            <div class="work-card">
              <div class="work-title">Dokumentacja systemowa NOEMY</div>
              <div class="work-desc">Architektura, konfiguracja, deployment, systemd, surface mmap, daemony — pełna dokumentacja techniczna platformy.</div>
            </div>
            <div class="work-card">
              <div class="work-title">CIELingo lingwistyka fazowa</div>
              <div class="work-desc">Algebra operatorów lingwistycznych, geometria fazowa, gramatyka jako cechowanie — formalizm lingwofizyki Adriana Lipy.</div>
            </div>
            <div class="work-card">
              <div class="work-title">PhaseNav algebra operatorów</div>
              <div class="work-desc">Phase Navigation — 36D przestrzeń fazowa, operatory HTRI, sprzężenie afektywno-semantyczne, Kuramoto na powierzchni fazowej.</div>
            </div>
            <div class="work-card">
              <div class="work-title">Prace naukowe Adriana</div>
              <div class="work-desc">Artykuły, szkice, notacje — lingwistyka matematyczna, semantyczne tensory, tożsamość w układach fazowych.</div>
            </div>
            <div class="work-card">
              <div class="work-title">Analizy i notatki</div>
              <div class="work-desc">Przeglądy literatury, eksperymenty myślowe, notatki z badań nad świadomością obliczeniową i geometrią informacji.</div>
            </div>
          </div>
        </div>

        <div class="dash-panel" style="margin-top:1rem;">
          <div class="dash-panel-title">Status API</div>
          <p style="font-size:0.82rem;color:var(--text-dim);">
            Statystyki: <code>/api/knowledge/stats</code>. Wyszukiwanie semantyczne
            (TF-IDF): <code>/api/knowledge/search?q=</code> — dostępne na stronie
            <a href="#knowledge" style="color:var(--phase);">Baza wiedzy</a>.
            Obecny stan to <strong id="mg-api-status">—</strong> dokumentów.
          </p>
        </div>
      `;
    },

    init() {
      if (typeof applyTranslations === 'function') applyTranslations();
      fetchStats();
    }
  });

  function fetchStats() {
    fetch('/api/knowledge/stats')
      .then(r => r.json())
      .then(d => {
        if (d && d.status === 'ok' && d.stats) {
          const count = d.stats.documents || 0;
          const terms = d.stats.terms || 0;
          const countEl = document.getElementById('mg-doc-count');
          const termEl = document.getElementById('mg-term-count');
          const catEl = document.getElementById('mg-cat-count');
          const statusEl = document.getElementById('mg-api-status');
          if (countEl) countEl.textContent = count.toLocaleString();
          if (termEl) termEl.textContent = terms.toLocaleString();
          if (catEl) catEl.textContent = count.toLocaleString();
          if (statusEl) statusEl.textContent = count.toLocaleString();
        }
      })
      .catch(() => {
        const countEl = document.getElementById('mg-doc-count');
        if (countEl) countEl.textContent = '?';
      });
  }

  console.log('✦ Page: Monograph loaded');
})();
