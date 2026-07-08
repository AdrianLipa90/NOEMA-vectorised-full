/* ─── Knowledge Page — Baza wiedzy CIELingo ── */
(function() {
  'use strict';

  const CATEGORIES = [
    'lingwistyka', 'semantyka', 'fonetyka', 'składnia', 'morfologia',
    'pragmatyka', 'neurolingwistyka', 'psycholingwistyka', 'gramatyka',
    'leksykografia', 'etyka', 'filozofia języka', 'sztuczna inteligencja',
    'CIELingo', 'PhaseNav', 'NOEMA', 'kognitywistyka',
    'przetwarzanie języka naturalnego', 'semantyka formalna',
    'lingwistyka korpusowa', 'afekt', 'tożsamość'
  ];

  registerPage('knowledge', {
    title: 'Baza wiedzy',

    render() {
      return `
        <div class="page-header">
          <h1><span data-i18n="pages.knowledge.title">Baza wiedzy</span> — <span id="kw-doc-count">…</span></h1>
          <p class="page-desc" data-i18n="pages.knowledge.desc">Indeksowana baza dokumentów CIELingo z wyszukiwarką semantyczną</p>
        </div>

        <!-- Stats cards -->
        <div class="dash-panel">
          <div class="dash-panel-title">Statystyki bazy</div>
          <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:8px;" id="kw-stats-grid">
            <div class="dash-card">
              <div class="dash-card-title">Dokumenty</div>
              <div class="dash-card-value c-cyan" id="kw-docs">—</div>
              <div class="dash-card-desc">Liczba dokumentów w bazie</div>
            </div>
            <div class="dash-card">
              <div class="dash-card-title">Terminy</div>
              <div class="dash-card-value c-purple" id="kw-terms">—</div>
              <div class="dash-card-desc">Unikalne terminy TF-IDF</div>
            </div>
            <div class="dash-card">
              <div class="dash-card-title">Pary powinowactwa</div>
              <div class="dash-card-value c-green" id="kw-affinity">—</div>
              <div class="dash-card-desc">Semantyczne połączenia między dokumentami</div>
            </div>
          </div>
        </div>

        <!-- Search -->
        <div class="dash-panel" style="margin-top:1rem;">
          <div class="dash-panel-title">Szukaj w bazie</div>
          <div style="display:flex;gap:8px;margin-top:8px;">
            <input type="text" class="metric-search" id="kw-search-input"
                   placeholder="🔍 Wpisz zapytanie..." style="flex:1;">
            <button class="knowledge-btn" id="kw-search-btn">Szukaj</button>
          </div>
          <div id="kw-search-results" style="margin-top:8px;font-size:0.82rem;font-family:var(--mono);color:var(--muted);">
            Wpisz zapytanie i kliknij Szukaj
          </div>
        </div>

        <!-- Kategorie -->
        <div class="dash-panel" style="margin-top:1rem;">
          <div class="dash-panel-title">Kategorie dokumentów</div>
          <div style="display:flex;flex-wrap:wrap;gap:6px;margin-top:8px;" id="kw-categories">
            ${CATEGORIES.map(cat => `
              <span style="background:var(--surface2);border:1px solid var(--border);border-radius:12px;
                           padding:4px 12px;font-size:0.78rem;color:var(--text-dim);
                           cursor:pointer;transition:.15s;"
                    onmouseover="this.style.borderColor='var(--phase)';this.style.color='var(--text)';"
                    onmouseout="this.style.borderColor='';this.style.color='';"
                    onclick="document.getElementById('kw-search-input').value='${cat}';document.getElementById('kw-search-btn').click();">
                ${cat}
              </span>
            `).join('')}
          </div>
        </div>

        <!-- Raw JSON -->
        <div class="dash-panel" style="margin-top:1rem;">
          <div class="dash-panel-title" style="cursor:pointer;" onclick="const n=this.nextElementSibling;n.style.display=n.style.display==='none'?'block':'none';this.querySelector('.toggle-icon').textContent=n.style.display==='none'?'▶':'▼';">
            <span class="toggle-icon">▶</span> Odpowiedź JSON
          </div>
          <pre id="kw-raw" style="display:none;font-family:var(--mono);font-size:0.7rem;color:var(--text-dim);overflow:auto;max-height:200px;"></pre>
        </div>
      `;
    },

    init() {
      applyTranslations();
      fetchStats();
      setupSearch();
      const iv = setInterval(fetchStats, 30000);
      return () => clearInterval(iv);
    }
  });

  let lastStats = null;

  function fetchStats() {
    fetch('/api/knowledge/stats')
      .then(r => r.json())
      .then(data => {
        if (data && data.status === 'ok' && data.stats) {
          lastStats = data.stats;
          renderStats(data.stats);
          updateRaw();
          const cnt = document.getElementById('kw-doc-count');
          if (cnt) cnt.textContent = data.stats.documents + ' dokumentów';
        }
      })
      .catch(() => {});
  }

  function renderStats(stats) {
    setVal('kw-docs', stats.documents.toLocaleString());
    setVal('kw-terms', stats.terms.toLocaleString());
    setVal('kw-affinity', stats.affinity_pairs.toLocaleString());
  }

  function setVal(id, text) {
    const el = document.getElementById(id);
    if (el) el.textContent = text;
  }

  function updateRaw() {
    const el = document.getElementById('kw-raw');
    if (!el) return;
    el.textContent = JSON.stringify({ stats: lastStats }, null, 2);
  }

  function setupSearch() {
    const btn = document.getElementById('kw-search-btn');
    const input = document.getElementById('kw-search-input');
    const results = document.getElementById('kw-search-results');
    if (!btn || !input || !results) return;

    function doSearch() {
      const q = input.value.trim();
      if (!q) {
        results.innerHTML = '<span style="color:var(--muted)">Wpisz zapytanie</span>';
        return;
      }
      results.innerHTML = 'Szukanie…';
      fetch('/api/knowledge/search?q=' + encodeURIComponent(q))
        .then(r => {
          if (r.status === 404) {
            results.innerHTML = '<span style="color:var(--muted)">Wyszukiwarka nieaktywna — endpoint /api/knowledge/search zwrócił 404</span>';
            return null;
          }
          if (!r.ok) throw new Error('HTTP ' + r.status);
          return r.json();
        })
        .then(data => {
          if (data === null) return;
          if (!data || data.status !== 'ok' || !data.results || data.results.length === 0) {
            results.innerHTML = '<span style="color:var(--muted)">Brak wyników</span>';
            return;
          }
          results.innerHTML = data.results.map(r => {
            const title = r.title || r.filename || r.name || '—';
            const snippetRaw = r.snippet || r.essence || r.description || '';
            const snippet = snippetRaw.length > 160 ? snippetRaw.slice(0, 160) + '…' : snippetRaw;
            const themes = Array.isArray(r.themes) ? r.themes.join(', ') : '';
            const sim = typeof r.similarity === 'number' ? ' · dopasowanie ' + (r.similarity * 100).toFixed(0) + '%' : '';
            return `
            <div style="padding:6px 0;border-bottom:1px solid var(--bg1);">
              <div style="color:var(--phase);font-weight:600;">${title}${sim}</div>
              <div style="font-size:0.75rem;color:var(--muted);">${snippet}</div>
              ${themes ? `<div style="font-size:0.7rem;color:var(--text-dim);margin-top:2px;">${themes}</div>` : ''}
            </div>
          `;
          }).join('');
        })
        .catch(err => {
          results.innerHTML = '<span style="color:var(--muted)">Błąd: ' + err.message + '</span>';
        });
    }

    btn.addEventListener('click', doSearch);
    input.addEventListener('keydown', e => { if (e.key === 'Enter') doSearch(); });
  }

  console.log('✦ Page: Knowledge loaded');
})();
