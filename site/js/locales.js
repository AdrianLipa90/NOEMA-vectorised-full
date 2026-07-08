/* ─── LOCALE — PL/EN translations ─────────────────────────── */
const LOC = {
  pl: {
    lang: "PL",
    general: { loading: "Ładowanie..." },
    nav: {
      dashboard: "Dashboard",
      cielingo: "CIELingo Chat",
      systems: "Systemy i moduły", memory: "Pamięć (M0–M11)",
      monograph: "Monografia (300+)",
      graph: "Graf wiedzy", knowledge: "Baza wiedzy",
      science: "Nauka", engineering: "Inżynieria",
      architecture: "Architektura",
      simulations: "Symulacje", phasenav: "PhaseNav",
      dtree: "Drzewo decyzji", bloch: "Sfera Blocha",
      projects: "Projekty", preferences: "Ustawienia",
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
      modules: { title: "Systemy NOEMY", desc: "Wszystkie systemy, moduły i daemony NOEMY — dane live z API", count_suffix: "systemów" },
      bloch: { title: "Sfera Blocha 36D", desc: "36 oscylatorów NOEMY — wszystkie atrybuty: φ/ω/τ/g/flavor/gravity/holonomy/analog/CIEL" },
      architecture: { title: "Architektura portalu", desc: "Mapa stron, endpointów i przepływów danych NOEMA" },
      "cielingo-chat": { title: "CIELingo", desc: "Rozmowa z CIEL — wspomagana lingofizyką fazową i pamięcią" },
      memory: { title: "Pamięć CIEL — kanały M0–M11", desc: "Koherencja kanałów pamięci i wątki CIELingo w czasie rzeczywistym" },
      phasenav: { title: "PhaseNav — stan przestrzeni fazowej", desc: "Operator algebra PhaseNav z danymi live z powierzchni fazowej NOEMY" },
      graph: { title: "Graf wiedzy NOEMY", desc: "475 węzłów · 1458 krawędzi · wiedza NOEMY" },
      knowledge: { title: "Baza wiedzy", desc: "Indeksowana baza dokumentów CIELingo z wyszukiwarką semantyczną", search: "🔍 Szukaj w bazie...", searchBtn: "Szukaj", coverageTitle: "Sprawdź pokrycie", coveragePlaceholder: "Wklej tekst aby sprawdzić czy baza go pokrywa...", coverageBtn: "Sprawdź" },
      "decision-tree": { title: "Drzewo decyzyjne", desc: "Decyzje NOEMY — żywe dane z bazy TaskPlan" },
      status: { title: "Stan systemu NOEMA", desc: "Kondycja daemonów, powierzchni fazowej i infrastruktury" },
      settings: { title: "Ustawienia", desc: "Konfiguracja systemu i stan CIEL — dane rzeczywiste" },
      projects: { title: "Projekty NOEMY", desc: "Rzeczywiste systemy i zadania — dane live z API" },
      catalogs: { title: "Katalogi — Heatmapy Holonomii", desc: "Macierze ko-okurencji tagów w SKILLS.md, PLANS.md i FUNCTIONS.md" },
      monograph: { title: "Monografia — prace Adriana Lipy", desc: "Katalog dokumentów i opracowań w bazie wiedzy NOEMY",
        stats: "Statystyki", download: "Pobierz", download_desc: "Pełna monografia NOEMA v4 w formacie PDF" }
    },
    projects: { title: "Projekty", learnMore: "Dowiedz się więcej" },
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
      cielingo: "CIELingo Chat",
      systems: "Systems & modules", memory: "Memory (M0–M11)",
      monograph: "Monograph (300+)",
      graph: "Knowledge Graph", knowledge: "Knowledge Base",
      science: "Science", engineering: "Engineering",
      architecture: "Architecture",
      simulations: "Simulations", phasenav: "PhaseNav",
      dtree: "Decision Tree", bloch: "Bloch Sphere",
      projects: "Projects", preferences: "Settings",
      status: "System Status"
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
      modules: { title: "NOEMA Systems", desc: "All NOEMA systems, modules and daemons — live data from the API", count_suffix: "systems" },
      bloch: { title: "Bloch Sphere 36D", desc: "36 NOEMA oscillators — all attributes: φ/ω/τ/g/flavor/gravity/holonomy/analog/CIEL" },
      architecture: { title: "Portal Architecture", desc: "Map of pages, endpoints and NOEMA data flows" },
      "cielingo-chat": { title: "CIELingo", desc: "Conversation with CIEL — backed by phase lingophysics and memory" },
      memory: { title: "CIEL Memory — M0–M11 channels", desc: "Memory channel coherence and CIELingo threads in real time" },
      phasenav: { title: "PhaseNav — phase space state", desc: "PhaseNav operator algebra with live data from the NOEMA phase surface" },
      graph: { title: "NOEMA Knowledge Graph", desc: "475 nodes · 1458 edges · NOEMA knowledge" },
      knowledge: { title: "Knowledge Base", desc: "Indexed CIELingo document base with semantic search", search: "🔍 Search the database...", searchBtn: "Search", coverageTitle: "Check coverage", coveragePlaceholder: "Paste text to check if database covers it...", coverageBtn: "Check" },
      "decision-tree": { title: "Decision Tree", desc: "NOEMA decisions — live data from the TaskPlan database" },
      status: { title: "NOEMA System Status", desc: "Daemon, phase-surface and infrastructure health" },
      settings: { title: "Settings", desc: "System configuration and CIEL state — real data" },
      projects: { title: "NOEMA Projects", desc: "Real systems and tasks — live data from the API" },
      catalogs: { title: "Catalogs — Holonomy Heatmaps", desc: "Co-occurrence matrices for SKILLS.md, PLANS.md and FUNCTIONS.md" },
      monograph: { title: "Monograph — Adrian Lipa's work", desc: "Catalog of documents and papers in the NOEMA knowledge base",
        stats: "Stats", download: "Download", download_desc: "Complete NOEMA v4 monograph in PDF format" }
    },
    projects: { title: "Projects", learnMore: "Learn more" },
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
