/* Accueil — animations. Rien ne démarre si l'utilisateur a demandé des animations
   réduites (ou en mode figé, `?fige=1`) : le contenu est alors simplement affiché. */
const calme = window.matchMedia("(prefers-reduced-motion: reduce)").matches || document.documentElement.classList.contains("fige");

/* Arches : léger déplacement selon la position du pointeur */
const arches = document.querySelector(".arches");
if (arches && !calme && window.matchMedia("(hover: hover)").matches) {
  const zone = arches.closest(".ouverture");
  zone.addEventListener("pointermove", (e) => {
    const r = zone.getBoundingClientRect();
    arches.style.setProperty("--px", ((e.clientX - r.left) / r.width - 0.5).toFixed(3));
    arches.style.setProperty("--py", ((e.clientY - r.top) / r.height - 0.5).toFixed(3));
  });
  zone.addEventListener("pointerleave", () => { arches.style.setProperty("--px", 0); arches.style.setProperty("--py", 0); });
}

/* Chiffres : le nombre compte jusqu'à sa valeur quand il arrive à l'écran */
const chiffres = document.querySelector(".chiffres");
if (chiffres) {
  const compter = () => {
    chiffres.classList.add("est-vu");
    if (calme) return;
    chiffres.querySelectorAll("[data-compte]").forEach((el, rang) => {
      const fin = Number(el.dataset.compte), debut = performance.now() + rang * 120, duree = 1400;
      const pas = (t) => {
        const k = Math.min(1, Math.max(0, (t - debut) / duree));
        el.textContent = String(Math.round(fin * (1 - Math.pow(1 - k, 3))));
        if (k < 1) requestAnimationFrame(pas);
      };
      el.textContent = "0";
      requestAnimationFrame(pas);
    });
  };
  new IntersectionObserver(([x], obs) => { if (x.isIntersecting) { compter(); obs.disconnect(); } }, { threshold: 0.4 }).observe(chiffres);
}

/* Bandeau défilant : bouton de pause */
const defilant = document.querySelector("[data-defilant]");
if (defilant) {
  const bouton = defilant.querySelector("[data-pause]");
  bouton.addEventListener("click", () => {
    const pause = defilant.classList.toggle("est-en-pause");
    bouton.setAttribute("aria-pressed", String(pause));
  });
}

/* Un organe à la fois : choix au clic, et passage automatique tant que personne n'y touche */
const vitrine = document.querySelector("[data-vitrine]");
if (vitrine) {
  const boutons = [...vitrine.querySelectorAll("[data-organe]")];
  const vues = [...vitrine.querySelectorAll("[data-vue]")];
  const pause = vitrine.querySelector("[data-pause]");
  const DUREE = 6000;
  let index = 0, minuterie = 0, visible = false, survol = false, arret = calme;
  vitrine.style.setProperty("--duree", `${DUREE}ms`);

  function montrer(i) {
    index = (i + boutons.length) % boutons.length;
    boutons.forEach((b, k) => b.setAttribute("aria-pressed", String(k === index)));
    vues.forEach((v) => v.classList.toggle("est-choisie", v.dataset.vue === boutons[index].dataset.organe));
  }
  /* (Re)lance le compte à rebours ; la jauge du bouton actif repart de zéro. */
  function programmer() {
    clearTimeout(minuterie);
    const lecture = !arret && visible && !survol;
    vitrine.classList.remove("est-en-lecture");
    if (!lecture) return;
    void vitrine.offsetWidth;
    vitrine.classList.add("est-en-lecture");
    minuterie = setTimeout(() => { montrer(index + 1); programmer(); }, DUREE);
  }
  function arreter(oui) {
    arret = oui;
    pause.setAttribute("aria-pressed", String(oui));
    pause.textContent = oui ? "Reprendre le changement automatique" : "Arrêter le changement automatique";
    programmer();
  }
  boutons.forEach((b, i) => b.addEventListener("click", () => { montrer(i); arreter(true); }));
  pause.addEventListener("click", () => arreter(!arret));
  const toucher = (oui) => () => { survol = oui; programmer(); };
  vitrine.addEventListener("pointerenter", toucher(true));
  vitrine.addEventListener("pointerleave", toucher(false));
  vitrine.addEventListener("focusin", toucher(true));
  vitrine.addEventListener("focusout", toucher(false));
  new IntersectionObserver(([x]) => { visible = x.isIntersecting; programmer(); }, { threshold: 0.35 }).observe(vitrine);
  if (calme) pause.hidden = true;
}

/* Parcours : la ligne avance à mesure que la section traverse l'écran */
const etapes = document.querySelector("[data-avance]");
if (etapes) {
  const items = [...etapes.children];
  const mesurer = () => {
    const r = etapes.getBoundingClientRect();
    const avance = calme ? 1 : Math.min(1, Math.max(0, (window.innerHeight * 0.8 - r.top) / (r.height + window.innerHeight * 0.3)));
    etapes.style.setProperty("--avance", avance.toFixed(3));
    items.forEach((li, i) => li.classList.toggle("est-atteinte", avance >= i / items.length + 0.02));
  };
  window.addEventListener("scroll", mesurer, { passive: true });
  window.addEventListener("resize", mesurer);
  mesurer();
}
