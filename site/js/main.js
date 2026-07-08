/* ─── NOEMA Portal — Entry Point ──────────────────────────── */
(function() {
  'use strict';

  const nativeFetch = window.fetch.bind(window);

  function unwrapEnvelope(payload) {
    if (!payload) return payload;
    if (payload.ok === true && Object.prototype.hasOwnProperty.call(payload, 'data')) {
      return payload.data;
    }
    return payload;
  }

  window.fetch = function(...args) {
    return nativeFetch(...args).then((response) => {
      if (!response || typeof response.json !== 'function') {
        return response;
      }
      const originalJson = response.json.bind(response);
      response.json = async () => unwrapEnvelope(await originalJson());
      return response;
    });
  };

  // ─── Init on DOM ready ─────────────────────────────────────
  function init() {
    console.log('✦ NOEMA Portal v4 SPA');
    console.log('▸ 19 pages · 8 channel colors · BL/EN');

    // Navigate to initial route
    const hash = window.location.hash || '#dashboard';
    window.navigate(hash);

    // Expose applyTranslations globally for page re-initialization
    window.applyTranslationsGlobal = applyTranslations;

    // ─── Live tick update (every 5s from SSE or poll) ────────
    function updateTick() {
      fetch('/api/live')
        .then(r => r.json())
        .then(data => {
          const st = document.getElementById('sidebar-tick');
          if (st && data.tick) st.textContent = `tick: ${data.tick.toLocaleString()}`;
        })
        .catch(() => {});
    }
    setInterval(updateTick, 5000);
    updateTick();

    console.log('✦ Portal ready');
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
