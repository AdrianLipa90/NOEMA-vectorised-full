/* ─── SPA Router — hash-based, zero-dependency ───────────── */
(function() {
  'use strict';

  // ─── Page registry ──────────────────────────────────────────
  const pages = {};
  let currentRoute = null;
  let currentCleanup = null;
  let currentSubroute = ''; // exposed for sub-page routing

  // ─── Register a page ────────────────────────────────────────
  window.registerPage = function(route, config) {
    pages[route] = {
      render: config.render || (() => ''),
      init: config.init || (() => {}),
      destroy: config.destroy || (() => {}),
      title: config.title || route,
      // Sub-route support: if configured, hash `route/xyz` will match this page
      // and pass `xyz` as subroute. The page's render/init receive subroute.
      subrouteInit: config.subrouteInit || null,
      subrouteRender: config.subrouteRender || null,
    };
  };

  // ─── Navigate to a route ────────────────────────────────────
  window.navigate = function(hash) {
    const raw = hash.replace(/^#/, '') || 'dashboard';

    // Try exact match, then prefix match for sub-routes
    let page = pages[raw];
    let subroute = '';
    let route = raw;
    if (!page) {
      const parts = raw.split('/');
      while (parts.length > 1) {
        parts.pop();
        const prefix = parts.join('/');
        if (pages[prefix]) {
          page = pages[prefix];
          subroute = raw.slice(prefix.length + 1);
          route = prefix;
          break;
        }
      }
    }

    if (route === currentRoute && subroute === currentSubroute) return;

    // Destroy current page
    if (currentCleanup) {
      try { currentCleanup(); } catch (e) { console.warn('Page destroy error:', e); }
      currentCleanup = null;
    }
    if (pages[currentRoute] && pages[currentRoute].destroy) {
      try { pages[currentRoute].destroy(); } catch (e) { console.warn('Page destroy error:', e); }
    }

    currentRoute = route;
    currentSubroute = subroute;

    // Update URL
    const targetHash = subroute ? route + '/' + subroute : route;
    if (window.location.hash !== '#' + targetHash) {
      window.location.hash = '#' + targetHash;
    }

    // Update sidebar
    document.querySelectorAll('.nav-item').forEach(el => {
      el.classList.toggle('active', el.dataset.route === route);
    });

    // Update topbar title
    const tt = document.getElementById('topbar-title');
    if (tt) {
      tt.textContent = page ? page.title : 'NOEMA';
    }

    // Render page
    const container = document.getElementById('page-container');
    if (!container) return;

    if (!page) {
      container.innerHTML = `<div class="page-loading"><h2>404</h2><span>Page not found: ${route}</span></div>`;
      return;
    }

    // Use subrouteRender if available and we have a subroute
    let html;
    if (subroute && page.subrouteRender) {
      html = page.subrouteRender(subroute);
    } else {
      html = page.render();
    }
    container.innerHTML = `<div class="page-enter">${html}</div>`;
    
    // Init page (pass subroute if available)
    try {
      if (subroute && page.subrouteInit) {
        currentCleanup = page.subrouteInit(subroute);
      } else {
        currentCleanup = page.init();
      }
    } catch (e) {
      console.warn('Page init error:', e);
    }
  };

  // ─── Expose for pages to check current subroute ─────────────
  window.getSubroute = function() { return currentSubroute; };

  // ─── Hash change handler ────────────────────────────────────
  window.addEventListener('hashchange', function() {
    navigate(window.location.hash);
  });

  // ─── Sidebar click handler ──────────────────────────────────
  document.addEventListener('click', function(e) {
    const navItem = e.target.closest('.nav-item');
    if (navItem && navItem.dataset.route) {
      // Close sidebar on mobile
      document.getElementById('sidebar').classList.remove('open');
      document.getElementById('sidebar-overlay').classList.remove('open');
      navigate(navItem.dataset.route);
      e.preventDefault();
    }
  });

  // ─── Mobile sidebar toggle ──────────────────────────────────
  document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.getElementById('topbar-hamburger');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebar-overlay');
    const closeBtn = document.getElementById('sidebar-close');

    if (hamburger) {
      hamburger.addEventListener('click', function() {
        sidebar.classList.toggle('open');
        overlay.classList.toggle('open');
      });
    }
    if (overlay) {
      overlay.addEventListener('click', function() {
        sidebar.classList.remove('open');
        overlay.classList.remove('open');
      });
    }
    if (closeBtn) {
      closeBtn.addEventListener('click', function() {
        sidebar.classList.remove('open');
        overlay.classList.remove('open');
      });
    }
  });

  console.log('✦ SPA Router ready');
})();
