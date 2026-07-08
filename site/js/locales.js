/* ─── LOCALE — PL/EN translations ─────────────────────────── */
const LOC = {
  pl: {
    lang: "PL",
    general: { loading: "Ładowanie..." },
    nav: {
      dashboard: "Dashboard",
      live: "Live",
      metrics: "Metryki",
      systems: "Systemy i moduły", memory: "Pamięć (M0–M11)",
      monograph: "Monografia (300+)",
      graph: "Graf wiedzy", knowledge: "Baza wiedzy",
      science: "Nauka", engineering: "Inżynieria",
      architecture: "Architektura",
      simulations: "Symulacje", phasenav: "PhaseNav",
      dtree: "Drzewo decyzji", bloch: "Sfera Blocha",
      projects: "Projekty", preferences: "Preferencje",
      status: "Stan systemu"
    },
    hero: {
      badge: "v4.0 · 2026",
      title: "NOEMA",
      subtitle: "Phase-Based Computation Substrate",
      desc: "24 oscylatory Kuramoto · Silnik semantyczny CIELingo · Algebra operatorów PhaseNav<br>Pamięć warstwowa · 14 współbieżnych daemonów · Rezonans dual-surface",
      daemons: "daemonów", coherence: "koherencja", agent: "AGENT", docs: "dokumentów"
    },
    pages: {
      dashboard: { title: "Dashboard", desc: "Stan systemu NOEMA w czasie rzeczywistym",
        coh_desc: "Ogólna spójność systemu", gamma_desc: "Spowolnienie czasu Kuramoto",
        mass_desc: "Skumulowane znaczenie", euler_desc: "Reziduum tożsamości Eulera",
        mood_desc: "Stan afektywny systemu", flavor: "Flavor Vector", channels: "Kanały",
        phase_wheel: "Koło fazowe",
        card_tick_title: "Tick", card_tick_desc: "Cykl ewolucji powierzchni",
        card_coherence_title: "Kuramoto R", card_coherence_desc: "Globalna synchronizacja (flavor[0])",
        card_agent_title: "AGENT (M1)", card_agent_desc: "Koherencja kanału Working",
        card_gamma_title: "γ (dylatacja)", card_gamma_desc: "Spowolnienie czasu Kuramoto",
        card_mass_title: "Masa semantyczna", card_mass_desc: "Skumulowane znaczenie",
        card_euler_title: "Euler R", card_euler_desc: "Domknięcie fazy Berry'ego",
        card_mood_title: "Nastrój", card_mood_desc: "Stan afektywny systemu",
        card_omega_desc: "Średnia częstotliwość", card_tau_desc: "Średni czas życia",
        card_sensor_title: "Sensor", card_sensor_desc: "Średnia sensor_raw",
        card_unruh_title: "Unruh", card_unruh_desc: "Moc Unruha",
        card_density_desc: "Gęstość semantyczna",
        channel_coherence: "Koherencja kanałów (M0–M11)", daemons: "Daemony",
        all_metrics: "Wszystkie metryki", search_metric: "🔍 Szukaj metryki...",
        raw_json: "Odpowiedź JSON", loading: "Ładowanie...", no_signal: "brak sygnału",
        source_label: "źródło" },
      modules: { title: "Moduły systemowe", desc: "Daemony NOEMY — status i sterowanie" },
      bloch: { title: "Sfera Blocha 36D", desc: "36 oscylatorów NOEMY — wszystkie atrybuty: φ/ω/τ/g/flavor/gravity/holonomy/analog/CIEL" },
      phasenav: { title: "PhaseNav Explorer", desc: "35 operatorów w 24-wymiarowej przestrzeni fazowej" },
      graph: { title: "Graf wiedzy NOEMY", desc: "475 węzłów · 1458 krawędzi · wiedza NOEMY" },
      knowledge: { title: "Baza wiedzy", desc: "545 dokumentów — wyszukiwanie TF-IDF", search: "🔍 Szukaj w 545 dokumentach...", searchBtn: "Szukaj", coverageTitle: "Sprawdź pokrycie", coveragePlaceholder: "Wklej tekst aby sprawdzić czy baza go pokrywa...", coverageBtn: "Sprawdź" },
      "decision-tree": { title: "Drzewo decyzyjne", desc: "Wszystkie branching pointy — warunki, decyzje, konsekwencje" },
      status: { title: "Status systemu", desc: "Live podsumowanie systemu NOEMA z bazy danych" },
      settings: { title: "Ustawienia", desc: "Konfiguracja systemu NOEMA" },
      projects: { title: "Projekty", desc: "Przegląd projektów i skryptów NOEMY" },
      catalogs: { title: "Katalogi — Heatmapy Holonomii", desc: "Macierze ko-okurencji tagów w SKILLS.md, PLANS.md i FUNCTIONS.md" },
      monograph: { title: "Monografia NOEMA v4", desc: "Pełna dokumentacja techniczna",
        stats: "Statystyki", download: "Pobierz", download_desc: "Pełna monografia NOEMA v4 w formacie PDF" }
    },
    projects: { title: "Projekty", learnMore: "Dowiedz się więcej" },
    live: {
      title: "Live NOEMA",
      desc: "Stan powierzchni fazowej w czasie rzeczywistym",
      daemons: "Daemony", metrics: "Metryki",
      flavor: "Flavor vector",
      card_tick_desc: "Cykl ewolucji",
      card_agent_desc: "Koherencja M1_Working",
      card_gamma_desc: "Spowolnienie τ",
      card_mass_title: "Masa", card_mass_desc: "Semantyczna masa",
      card_mood_desc: "Stan afektywny",
      card_euler_desc: "Domknięcie fazy Berry'ego",
      card_omega_desc: "Średnia częstotliwość",
      card_tau_desc: "Średni czas życia",
      card_sensor_desc: "Średnia sensor_raw",
      card_unruh_desc: "Moc Unruha",
      card_density_desc: "Gęstość semantyczna",
      channel_coherence: "Koherencja kanałów (M0–M11)",
      raw_json: "Surowy JSON", loading: "Ładowanie...", no_signal: "brak sygnału"
    },
    phasenav: {
      title: "PhaseNav Explorer",
      desc: "35 operatorów · 24D przestrzeń fazowa · Berry connection",
      coherence: "koherencja"
    },
    graph: {
      title: "Knowledge Graph",
      desc: "475 węzłów · 1458 krawędzi · wiedza NOEMY",
      categories: {
        PhaseNav: "PhaseNav", CIELingo: "CIELingo", Daemon: "Daemon",
        Physics: "Fizyka", Memory: "Pamięć", System: "System",
        Linguistics: "Językoznawstwo", Mathematics: "Matematyka"
      }
    },
    monograph: {
      title: "Monografia",
      desc: "Pełna dokumentacja techniczna NOEMA v4",
      chapters: "rozdziałów", pages: "stron", figures: "figur", size: "MB PDF",
      download: "📄 Pobierz PDF", browse: "Przeglądaj projekty"
    },
    catalogs: {
      title: "Katalogi — Heatmapy Holonomii",
      desc: "Macierze ko-okurencji tagów w 3 katalogach systemowych. Każda komórka to liczba dokumentów łączących daną parę tagów.",
      tab: { skills: "🧠 Skille (8)", plans: "📗 Plany (5)", functions: "📙 Funkcje (2)" },
      loading: "Ładowanie heatmapów...",
      noData: "Brak danych.",
      loadError: "Nie udało się załadować heatmapów",
      backModules: "← Moduły",
      countPositions: "pozycji",
      countHeatmaps: "heatmapów",
      semanticMass: "Masa semantyczna"
    },
    metrics: {
      coherence: "Koherencja", agent: "AGENT", m2: "M2",
      gamma: "Gamma", mass: "Masa", mood: "Nastrój",
      euler: "Euler R", snapshot: "Snapshot",
      omega_mean: "ω̄", omega_3: "AGENT ω[3]", tau_mean: "τ̄",
      phi_coh: "Koherencja fazowa", closure_penalty: "Kara domknięcia",
      density: "Gęstość semant.", unruh: "Moc Unruh",
      openness: "Otwartość", m2_coherence: "MEMORY",
      agent_coherence: "AGENT", Z_geom_mean: "Impedancja geom.",
      omega_std: "Rozrzut ω"
    },
    footer: {
      author: "Adrian Lipa &copy; 2026",
      tagline: "Zbudowane dla mnie. Przeze mnie."
    }
  },

  en: {
    lang: "EN",
    general: { loading: "Loading..." },
    nav: {
      dashboard: "Dashboard",
      live: "Live",
      metrics: "Metrics",
      modules: "Modules", bloch: "Bloch Sphere",
      projects: "Projects", phasenav: "PhaseNav",
      graph: "Knowledge Graph", settings: "Settings",
      monograph: "Monograph", catalogs: "Catalogs",
      dtree: "Decision Tree", status: "Status"
    },
    hero: {
      badge: "v4.0 · 2026",
      title: "NOEMA",
      subtitle: "Phase-Based Computation Substrate",
      desc: "24 Kuramoto oscillators · CIELingo semantic engine · PhaseNav operator algebra<br>Tiered memory · 14 concurrent daemons · Dual-surface resonance",
      daemons: "daemons", coherence: "coherence", agent: "AGENT", docs: "documents"
    },
    pages: {
      dashboard: { title: "Dashboard", desc: "NOEMA system state in real time",
        coh_desc: "Overall system coherence", gamma_desc: "Kuramoto time dilation",
        mass_desc: "Accumulated meaning", euler_desc: "Euler identity residual",
        mood_desc: "System affective state", flavor: "Flavor Vector", channels: "Channels",
        phase_wheel: "Phase Wheel",
        card_tick_title: "Tick", card_tick_desc: "Surface evolution cycle",
        card_coherence_title: "Kuramoto R", card_coherence_desc: "Global synchronization (flavor[0])",
        card_agent_title: "AGENT (M1)", card_agent_desc: "Working channel coherence",
        card_gamma_title: "γ (dilation)", card_gamma_desc: "Kuramoto time dilation",
        card_mass_title: "Semantic mass", card_mass_desc: "Accumulated meaning",
        card_euler_title: "Euler R", card_euler_desc: "Berry phase closure",
        card_mood_title: "Mood", card_mood_desc: "System affective state",
        card_omega_desc: "Mean frequency", card_tau_desc: "Mean lifetime",
        card_sensor_title: "Sensor", card_sensor_desc: "Mean sensor_raw",
        card_unruh_title: "Unruh", card_unruh_desc: "Unruh power",
        card_density_desc: "Semantic density",
        channel_coherence: "Channel coherence (M0–M11)", daemons: "Daemons",
        all_metrics: "All metrics", search_metric: "🔍 Search metric...",
        raw_json: "Raw JSON response", loading: "Loading...", no_signal: "no signal",
        source_label: "source" },
      modules: { title: "System Modules", desc: "NOEMA daemons — status and control" },
      bloch: { title: "Bloch Sphere 36D", desc: "36 NOEMA oscillators — all attributes: φ/ω/τ/g/flavor/gravity/holonomy/analog/CIEL" },
      phasenav: { title: "PhaseNav Explorer", desc: "35 operators in 24-dimensional phase space" },
      graph: { title: "NOEMA Knowledge Graph", desc: "475 nodes · 1458 edges · NOEMA knowledge" },
      knowledge: { title: "Knowledge Base", desc: "545 documents — TF-IDF search", search: "🔍 Search in 545 documents...", searchBtn: "Search", coverageTitle: "Check coverage", coveragePlaceholder: "Paste text to check if database covers it...", coverageBtn: "Check" },
      "decision-tree": { title: "Decision Tree", desc: "All branching points — conditions, decisions, consequences" },
      status: { title: "System Status", desc: "Live NOEMA system summary from database" },
      settings: { title: "Settings", desc: "NOEMA system configuration" },
      projects: { title: "Projects", desc: "NOEMA projects and scripts overview" },
      catalogs: { title: "Catalogs — Holonomy Heatmaps", desc: "Co-occurrence matrices for SKILLS.md, PLANS.md and FUNCTIONS.md" },
      monograph: { title: "NOEMA v4 Monograph", desc: "Full technical documentation",
        stats: "Stats", download: "Download", download_desc: "Complete NOEMA v4 monograph in PDF format" }
    },
    projects: { title: "Projects", learnMore: "Learn more" },
    live: {
      title: "NOEMA Live",
      desc: "Phase surface state in real time",
      daemons: "Daemons", metrics: "Metrics",
      flavor: "Flavor vector",
      card_tick_desc: "Evolution cycle",
      card_agent_desc: "M1_Working coherence",
      card_gamma_desc: "τ slowdown",
      card_mass_title: "Mass", card_mass_desc: "Semantic mass",
      card_mood_desc: "Affective state",
      card_euler_desc: "Berry phase closure",
      card_omega_desc: "Mean frequency",
      card_tau_desc: "Mean lifetime",
      card_sensor_desc: "Mean sensor_raw",
      card_unruh_desc: "Unruh power",
      card_density_desc: "Semantic density",
      channel_coherence: "Channel coherence (M0–M11)",
      raw_json: "Raw JSON", loading: "Loading...", no_signal: "no signal"
    },
    phasenav: {
      title: "PhaseNav Explorer",
      desc: "35 operators · 24D phase space · Berry connection",
      coherence: "coherence"
    },
    graph: {
      title: "Knowledge Graph",
      desc: "475 nodes · 1458 edges · NOEMA knowledge",
      categories: {
        PhaseNav: "PhaseNav", CIELingo: "CIELingo", Daemon: "Daemon",
        Physics: "Physics", Memory: "Memory", System: "System",
        Linguistics: "Linguistics", Mathematics: "Mathematics"
      }
    },
    monograph: {
      title: "Monograph",
      desc: "Complete NOEMA v4 technical documentation",
      chapters: "chapters", pages: "pages", figures: "figures", size: "MB PDF",
      download: "📄 Download PDF", browse: "Browse projects"
    },
    catalogs: {
      title: "Catalogs — Holonomy Heatmaps",
      desc: "Co-occurrence matrices across 3 system catalogs. Each cell counts documents sharing a tag pair.",
      tab: { skills: "🧠 Skills (8)", plans: "📗 Plans (5)", functions: "📙 Functions (2)" },
      loading: "Loading heatmaps...",
      noData: "No data.",
      loadError: "Failed to load heatmaps",
      backModules: "← Modules",
      countPositions: "items",
      countHeatmaps: "heatmaps",
      semanticMass: "Semantic Mass"
    },
    metrics: {
      coherence: "Coherence", agent: "AGENT", m2: "M2",
      gamma: "Gamma", mass: "Mass", mood: "Mood",
      euler: "Euler R", snapshot: "Snapshot",
      omega_mean: "ω̄", omega_3: "AGENT ω[3]", tau_mean: "τ̄",
      phi_coh: "Phase Coherence", closure_penalty: "Closure Penalty",
      density: "Semantic Dens.", unruh: "Unruh Power",
      openness: "Openness", m2_coherence: "MEMORY",
      agent_coherence: "AGENT", Z_geom_mean: "Geom. Impedance",
      omega_std: "ω Spread"
    },
    footer: {
      author: "Adrian Lipa &copy; 2026",
      tagline: "Built for me. By me."
    }
  }
};

// ─── Global state ──────────────────────────────────────────
let LANG = localStorage.getItem('noema_lang') || 'pl';

// ─── t() — translate key ──────────────────────────────────
function t(key, fallback) {
  const parts = key.split('.');
  let obj = LOC[LANG];
  for (const p of parts) {
    if (obj && obj[p] !== undefined) obj = obj[p];
    else return fallback || key;
  }
  return (typeof obj === 'string') ? obj : (fallback || key);
}

// ─── setLang() — switch language ──────────────────────────
function setLang(lang) {
  if (!LOC[lang]) return;
  LANG = lang;
  localStorage.setItem('noema_lang', lang);
  document.documentElement.lang = lang;
  applyTranslations();
  window.dispatchEvent(new CustomEvent('langchange'));
}

// ─── applyTranslations() ──────────────────────────────────
function applyTranslations() {
  // data-i18n — replace text content
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.dataset.i18n;
    const val = t(key);
    if (val !== key) el.textContent = val;
  });

  // data-i18n-html — replace inner HTML
  document.querySelectorAll('[data-i18n-html]').forEach(el => {
    const key = el.dataset.i18nHtml;
    const val = t(key);
    if (val !== key) el.innerHTML = val;
  });

  // Update lang switcher buttons
  document.querySelectorAll('.lang-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.lang === LANG);
  });
}

// ─── Init language switcher ───────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.lang-btn').forEach(btn => {
    btn.addEventListener('click', () => setLang(btn.dataset.lang));
  });
  document.documentElement.lang = LANG;
  applyTranslations();
});

console.log(`✦ Locales loaded: ${Object.keys(LOC.pl.nav).length} nav items, bilingual PL/EN`);
