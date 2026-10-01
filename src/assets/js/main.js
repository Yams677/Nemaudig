/* Nemaudig — interactions. Aucune dépendance, amélioration progressive :
   le site reste entièrement lisible et navigable sans JavaScript. */
(() => {
  "use strict";
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const reduit = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* En-tête : ombre au défilement */
  const entete = $("[data-entete]");
  if (entete) {
    const maj = () => entete.classList.toggle("is-defile", window.scrollY > 8);
    maj();
    window.addEventListener("scroll", maj, { passive: true });
  }

  /* Menu mobile */
  const burger = $("[data-burger]");
  const nav = $("[data-nav]");
  if (burger && nav) {
    nav.id = "menu-mobile";
    const fermer = () => {
      burger.setAttribute("aria-expanded", "false");
      burger.setAttribute("aria-label", "Ouvrir le menu");
      nav.classList.remove("is-ouvert");
      document.body.classList.remove("menu-ouvert");
    };
    burger.addEventListener("click", () => {
      const ouvert = burger.getAttribute("aria-expanded") === "true";
      if (ouvert) return fermer();
      burger.setAttribute("aria-expanded", "true");
      burger.setAttribute("aria-label", "Fermer le menu");
      nav.classList.add("is-ouvert");
      document.body.classList.add("menu-ouvert");
      const premier = $("a", nav);
      if (premier) premier.focus();
    });
    document.addEventListener("keydown", (ev) => { if (ev.key === "Escape") fermer(); });
    nav.addEventListener("click", (ev) => { if (ev.target.closest("a")) fermer(); });
  }

  /* Apparition au défilement */
  const cibles = $$("[data-reveal], [data-etape]");
  if ("IntersectionObserver" in window && !reduit) {
    const io = new IntersectionObserver((entrees) => {
      entrees.forEach((en) => {
        if (en.isIntersecting) { en.target.classList.add("is-vu"); io.unobserve(en.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    cibles.forEach((c) => io.observe(c));
  } else {
    cibles.forEach((c) => c.classList.add("is-vu"));
  }

  /* Planche anatomique : ordre d'apparition, légende au survol, synchro avec les cartes */
  $$(".planche").forEach((svg) => $$(".org", svg).forEach((o, i) => o.style.setProperty("--i", i)));

  $$("[data-planche-zone]").forEach((zone) => {
    const svg = $(".planche", zone);
    const legende = $("[data-legende]", zone);
    if (!svg) return;
    const montrer = (org) => {
      if (!legende || !org) return;
      const titre = $("title", org);
      legende.textContent = titre ? titre.textContent : "";
      const r = org.getBoundingClientRect();
      const z = zone.getBoundingClientRect();
      legende.style.left = `${r.left - z.left + r.width / 2}px`;
      legende.style.top = `${r.top - z.top}px`;
      legende.classList.add("is-visible");
    };
    const cacher = () => legende && legende.classList.remove("is-visible");
    $$("a.org, a.rep", svg).forEach((org) => {
      org.addEventListener("mouseenter", () => { montrer(org); synchroCartes(org.dataset.organe, true); });
      org.addEventListener("mouseleave", () => { cacher(); synchroCartes(org.dataset.organe, false); });
      org.addEventListener("focus", () => montrer(org));
      org.addEventListener("blur", cacher);
    });
  });

  const GROUPES = {
    paroi: ["paroi", "aine", "ombilic"], colon: ["colon", "sigmoide"], "colon-rectum": ["colon", "sigmoide", "rectum"],
    foie: ["foie", "vesicule", "pancreas"], estomac: ["estomac", "oesophage"], anus: ["anus", "rectum"],
  };
  const FAMILLE_DE = {
    oesophage: "estomac", estomac: "estomac", foie: "foie", vesicule: "foie", pancreas: "foie",
    colon: "colon-rectum", sigmoide: "colon-rectum", rectum: "colon-rectum", intestin: "colon-rectum",
    anus: "anus", aine: "paroi", ombilic: "paroi", surrenales: "surrenales",
  };
  function synchroCartes(organe, actif) {
    const cle = FAMILLE_DE[organe];
    $$("[data-organe-survol]").forEach((c) => {
      const okey = c.dataset.organeSurvol;
      c.classList.toggle("is-survol", actif && (okey === cle || (cle === "colon-rectum" && okey === "colon")));
    });
  }
  $$("[data-organe-survol]").forEach((carte) => {
    const svg = $("#planche-explorer") || $("#planche-mega") || $(".planche");
    if (!svg) return;
    const cles = GROUPES[carte.dataset.organeSurvol] || [carte.dataset.organeSurvol];
    const allumer = (on) => {
      svg.classList.toggle("a-un-survol", on);
      $$("[data-organe]", svg).forEach((o) => o.classList.toggle("is-survol", on && cles.includes(o.dataset.organe)));
      window.dispatchEvent(new CustomEvent("anatomie:survol", { detail: { cles: [carte.dataset.organeSurvol], actif: on } }));
    };
    carte.addEventListener("mouseenter", () => allumer(true));
    carte.addEventListener("mouseleave", () => allumer(false));
    carte.addEventListener("focusin", () => allumer(true));
    carte.addEventListener("focusout", () => allumer(false));
  });

  /* Méga-menu : la planche miniature suit la colonne survolée */
  const mega = $("#mega-pathologies");
  if (mega) {
    const svg = $(".planche", mega);
    $$(".mega__col[data-organe-survol]", mega).forEach((col) => {
      const cles = GROUPES[col.dataset.organeSurvol] || [col.dataset.organeSurvol];
      col.addEventListener("mouseenter", () => {
        svg.classList.add("a-un-survol");
        $$("[data-organe]", svg).forEach((o) => o.classList.toggle("is-survol", cles.includes(o.dataset.organe)));
      });
      col.addEventListener("mouseleave", () => {
        svg.classList.remove("a-un-survol");
        $$("[data-organe]", svg).forEach((o) => o.classList.remove("is-survol"));
      });
    });
  }

  /* Compteurs du hero */
  if (!reduit && "IntersectionObserver" in window) {
    $$("[data-compteur]").forEach((el) => {
      const fin = parseInt(el.dataset.compteur, 10);
      if (!fin) return;
      const io = new IntersectionObserver(([en]) => {
        if (!en.isIntersecting) return;
        io.disconnect();
        const t0 = performance.now(), duree = 1400;
        const pas = (t) => {
          const p = Math.min(1, (t - t0) / duree);
          el.textContent = Math.round(fin * (1 - Math.pow(1 - p, 3)));
          if (p < 1) requestAnimationFrame(pas);
        };
        requestAnimationFrame(pas);
      });
      io.observe(el);
    });
  }

  /* Vidéos YouTube : rien n'est chargé depuis YouTube (hors miniature) avant le clic */
  $$("[data-video]").forEach((bloc) => {
    const bouton = $("button", bloc);
    bouton.addEventListener("click", () => {
      const iframe = document.createElement("iframe");
      iframe.src = `https://www.youtube-nocookie.com/embed/${bloc.dataset.video}?autoplay=1&rel=0`;
      iframe.title = bloc.dataset.titre;
      iframe.allow = "accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture; fullscreen";
      iframe.allowFullscreen = true;
      bloc.classList.add("is-lecture");
      $(".video__media", bloc).replaceChildren(iframe);
      iframe.focus();
    });
  });

  /* Sommaire : section en cours */
  const sommaire = $("[data-sommaire]");
  if (sommaire && "IntersectionObserver" in window) {
    const liens = $$("a", sommaire);
    const io = new IntersectionObserver((entrees) => {
      entrees.forEach((en) => {
        if (!en.isIntersecting) return;
        liens.forEach((l) => l.classList.toggle("is-actif", l.getAttribute("href") === `#${en.target.id}`));
      });
    }, { rootMargin: "-20% 0px -70% 0px" });
    liens.forEach((l) => { const s = $(l.getAttribute("href")); if (s) io.observe(s); });
  }

  /* Calculateur d'IMC (classes reprises de la page « Points importants ») */
  const imc = $("[data-imc]");
  if (imc) {
    const poids = $("#imc-poids", imc), taille = $("#imc-taille", imc);
    const sortie = $("[data-imc-valeur]", imc), classe = $("[data-imc-classe]", imc), curseur = $("[data-imc-curseur]", imc);
    const CLASSES = [[18, 25, "Poids normal"], [25, 30, "Surpoids"], [30, 35, "Obésité modérée"], [35, 40, "Obésité sévère"], [40, 99, "Obésité massive ou morbide"]];
    const calc = () => {
      const p = parseFloat(String(poids.value).replace(",", ".")), t = parseFloat(String(taille.value).replace(",", "."));
      if (!(p > 20 && p < 400 && t > 100 && t < 250)) { sortie.textContent = "—"; classe.textContent = ""; curseur.style.left = "0%"; return; }
      const v = p / Math.pow(t / 100, 2);
      sortie.textContent = v.toFixed(1).replace(".", ",");
      const c = CLASSES.find(([a, b]) => v >= a && v < b);
      classe.textContent = c ? c[2] : (v < 18 ? "En dessous des classes présentées" : "");
      const pos = Math.max(0, Math.min(100, ((v - 18) / (48 - 18)) * 100));
      curseur.style.left = `${pos}%`;
    };
    [poids, taille].forEach((i) => i.addEventListener("input", calc));
    calc();
  }

  /* Voyage 3D : progression continue d'une étape à l'autre, au défilement.
     Émet « voyage:progression » (lu par anatomie3d.js) et pilote la planche SVG de secours. */
  const voyage = $("[data-voyage]");
  if (voyage) {
    const etapes = $$("[data-etape-voyage]", voyage);
    const rail = $$("[data-rail]", voyage);
    const svg = $(".planche", voyage);
    let courante = -1, demande = false;
    const calculer = () => {
      demande = false;
      const milieu = window.innerHeight / 2;
      const centres = etapes.map((el) => { const r = el.getBoundingClientRect(); return r.top + r.height / 2; });
      let f = 0;
      if (milieu >= centres[centres.length - 1]) f = centres.length - 1;
      else if (milieu > centres[0]) {
        const i = centres.findIndex((c, k) => milieu >= c && milieu < centres[k + 1]);
        f = i + (milieu - centres[i]) / (centres[i + 1] - centres[i]);
      }
      window.dispatchEvent(new CustomEvent("voyage:progression", { detail: { f } }));
      const n = Math.round(f);
      if (n === courante) return;
      courante = n;
      etapes.forEach((el, k) => el.classList.toggle("is-active", k === n));
      rail.forEach((a) => a.classList.toggle("is-actif", Number(a.dataset.rail) === n));
      const cles = (etapes[n].dataset.organes || "").split(" ").filter(Boolean);
      if (svg) {
        svg.classList.toggle("a-un-actif", cles.length > 0);
        $$("[data-organe]", svg).forEach((o) => o.classList.toggle("is-actif", cles.includes(o.dataset.organe)));
      }
    };
    const planifier = () => { if (!demande) { demande = true; requestAnimationFrame(calculer); } };
    window.addEventListener("scroll", planifier, { passive: true });
    window.addEventListener("resize", planifier);
    calculer();
  }

  /* Reflet qui suit la souris sur les boutons */
  $$(".btn").forEach((b) => b.addEventListener("pointermove", (ev) => {
    const r = b.getBoundingClientRect();
    b.style.setProperty("--mx", `${ev.clientX - r.left}px`);
    b.style.setProperty("--my", `${ev.clientY - r.top}px`);
  }));
})();
