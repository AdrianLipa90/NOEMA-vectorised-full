/* ─── Systems Page — wszystkie systemy NOEMY z API ─────────── */
(function() {
  'use strict';

  let daemonInterval = null;
  let cachedSystems = [];
  let cachedDaemons = [];

  registerPage('systems', {
    title: 'Systemy i moduły',

    render() {
      return `
        <div class="page-header">
          <h1><span data-i18n="pages.modules.title">Systemy NOEMY</span> — <span id="sys-count">0</span> <span data-i18n="pages.modules.count_suffix">systemów</span></h1>
          <p class="page-desc" data-i18n="pages.modules.desc">Wszystkie systemy, moduły i daemony NOEMY — dane live z API</p>
        </div>

        <div class="dash-panel" style="margin-top:1rem;">
          <div class="dash-panel-title">Daemony</div>
          <div id="sys-daemons" style="font-size:0.82rem;font-family:var(--mono);line-height:1.8;">
            Ładowanie...
          </div>
        </div>

        <div id="sys-groups" style="margin-top:1.5rem;"></div>

        <div class="dash-panel" style="margin-top:1rem;">
          <div class="dash-panel-title" style="cursor:pointer;" onclick="const n=this.nextElementSibling;n.style.display=n.style.display==='none'?'block':'none';this.querySelector('.toggle-icon').textContent=n.style.display==='none'?'▶':'▼';">
            <span class="toggle-icon">▶</span> Odpowiedź JSON — systemy
          </div>
          <pre id="sys-raw" style="display:none;font-family:var(--mono);font-size:0.7rem;color:var(--text-dim);overflow:auto;max-height:200px;"></pre>
        </div>
      `;
    },

    init() {
      fetchSystems();
      fetchDaemons();
      daemonInterval = setInterval(fetchDaemons, 10000);
      return () => {
        if (daemonInterval) clearInterval(daemonInterval);
        daemonInterval = null;
      };
    }
  });

  function fetchSystems() {
    fetch('/api/cards')
      .then(r => r.json())
      .then(data => {
        cachedSystems = (data && data.systems) || [];
        renderSystems(cachedSystems);
        const raw = document.getElementById('sys-raw');
        if (raw) raw.textContent = JSON.stringify(data, null, 2);
      })
      .catch(() => {
        const groups = document.getElementById('sys-groups');
        if (groups) groups.innerHTML = '<div class="dash-panel" style="color:var(--muted);">Nie można załadować systemów — API niedostępne</div>';
      });
  }

  function fetchDaemons() {
    fetch('/api/modules')
      .then(r => r.json())
      .then(data => {
        cachedDaemons = (data && data.modules) || [];
        renderDaemons(cachedDaemons);
        if (cachedDaemons.length && !cachedSystems.length) {
          fetchSystems();
        }
      })
      .catch(() => {});
  }

  function renderDaemons(modules) {
    const el = document.getElementById('sys-daemons');
    if (!el) return;
    if (!modules || !modules.length) {
      el.innerHTML = '<span style="color:var(--muted)">Brak aktywnych daemonów</span>';
      return;
    }
    const html = modules.map(m => {
      const alive = m.alive || m.systemd === 'active';
      const pid = m.pid || '—';
      const sysd = m.systemd || m.status || '—';
      const uptime = m.uptime_s ? `${(m.uptime_s / 60).toFixed(1)} min` : '—';
      return `
        <div style="display:flex;justify-content:space-between;align-items:center;padding:6px 0;border-bottom:1px solid var(--bg1);">
          <span><span style="color:${alive ? '#44ff88' : '#ff4466'};margin-right:6px;">●</span><strong>${m.name}</strong></span>
          <span style="color:var(--muted);font-size:0.75rem;">
            PID ${pid} · ${sysd} · uptime ${uptime}
          </span>
        </div>
      `;
    }).join('');
    el.innerHTML = html;
  }

  function renderSystems(systems) {
    const countEl = document.getElementById('sys-count');
    if (countEl) countEl.textContent = systems.length;

    const groups = document.getElementById('sys-groups');
    if (!groups) return;

    if (!systems || !systems.length) {
      groups.innerHTML = '<div class="dash-panel" style="color:var(--muted);">Brak systemów w odpowiedzi API</div>';
      return;
    }

    const grouped = {};
    const typeOrder = [];

    systems.forEach(s => {
      const t = s.type || 'other';
      if (!grouped[t]) {
        grouped[t] = [];
        typeOrder.push(t);
      }
      grouped[t].push(s);
    });

    const typeColors = {
      core: '#00d4ff',
      module: '#8844ff',
      data: '#44ff88',
      bridge: '#ffb347',
      service: '#ff4466',
      system: '#44ddff',
      other: '#888888'
    };

    const typeIcons = {
      core: '⚛',
      module: '◆',
      data: '▤',
      bridge: '⇄',
      service: '⚙',
      system: '◈',
      other: '○'
    };

    const html = typeOrder.map(type => {
      const items = grouped[type];
      const color = typeColors[type] || typeColors.other;
      const icon = typeIcons[type] || typeIcons.other;
      const label = type.charAt(0).toUpperCase() + type.slice(1);

      return `
        <div class="dash-panel" style="margin-top:1rem;">
          <div class="dash-panel-title" style="color:${color};">
            ${icon} ${label} — ${items.length}
          </div>
          <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:12px;">
            ${items.map(s => `
              <div class="dash-card" style="display:flex;flex-direction:column;">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:6px;">
                  <div class="dash-card-title" style="margin-bottom:0;color:${color};">${s.name}</div>
                  <span style="font-size:0.65rem;padding:2px 6px;border-radius:3px;background:${color}22;color:${color};border:1px solid ${color}44;text-transform:uppercase;font-family:var(--mono);">${s.type || '—'}</span>
                </div>
                <div class="dash-card-desc" style="flex:1;">${s.desc || s.description || '—'}</div>
              </div>
            `).join('')}
          </div>
        </div>
      `;
    }).join('');

    groups.innerHTML = html || '<div class="dash-panel" style="color:var(--muted);">Brak systemów</div>';
  }

  console.log('✦ Page: Systems loaded');
})();
