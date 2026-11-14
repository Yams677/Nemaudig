/* Interactions communes à toutes les pages — aucune dépendance, aucune donnée transmise. */
const CALME = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const $ = (s, racine = document) => racine.querySelector(s);
const $$ = (s, racine = document) => [...racine.querySelectorAll(s)];

/* Menu (petits écrans) */
const burger = $("[data-burger]"), nav = $("#nav");
function menu(ouvert) {
  burger.setAttribute("aria-expanded", String(ouvert));
  nav.classList.toggle("est-ouverte", ouvert);
  document.documentElement.style.overflow = ouvert ? "hidden" : "";
  if (ouvert) nav.querySelector("a")?.focus();
}
// Fenêtre élargie pendant que le menu est ouvert : on le referme pour rendre le défilement
window.matchMedia("(max-width: 1180px)").addEventListener("change", (e) => { if (!e.matches) menu(false); });
burger?.addEventListener("click", () => menu(burger.getAttribute("aria-expanded") !== "true"));
document.addEventListener("keydown", (e) => { if (e.key === "Escape" && nav.classList.contains("est-ouverte")) { menu(false); burger.focus(); } });

/* Fenêtres : tiroir « maquette », fiches vidéo */
$$("[data-ouvre]").forEach((b) => b.addEventListener("click", () => document.getElementById(b.dataset.ouvre)?.showModal()));
$$("dialog").forEach((d) => {
  d.addEventListener("click", (e) => {
    const r = d.getBoundingClientRect();
    const dehors = e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom;
    if (e.target.closest("[data-ferme]") || (e.target === d && dehors)) d.close();
  });
});

/* Message court (démonstration) */
const toast = $("[data-toast]");
let minuterie = 0;
function annoncer(texte) {
  toast.textContent = texte;
  clearTimeout(minuterie);
  minuterie = setTimeout(() => { toast.textContent = ""; }, 4200);
}
document.addEventListener("click", (e) => {
  const lien = e.target.closest("[data-demo-tel]");
  if (!lien) return;
  e.preventDefault();
  annoncer(`Démonstration : en ligne, ce lien appellera le ${lien.dataset.demoTel}.`);
});

/* Apparition douce au défilement */
if (!CALME && !document.documentElement.classList.contains("fige") && "IntersectionObserver" in window) {
  const cibles = $$(".bloc__tete, .chiffres li, .ligne, .medecin, .etapes li, .carte, .actu, .video, .engagements li, .soutiens li, .famille, .lieu, .technique, .deux-colonnes > *");
  const vu = new IntersectionObserver((entrees) => entrees.forEach((x) => {
    if (x.isIntersecting) { x.target.classList.add("est-vu"); vu.unobserve(x.target); }
  }), { rootMargin: "0px 0px -8% 0px" });
  cibles.forEach((el) => {
    if (el.getBoundingClientRect().top < window.innerHeight) return; // déjà à l'écran : ne pas le masquer
    el.style.setProperty("--rang", String([...el.parentElement.children].indexOf(el) % 6));
    el.classList.add("apparait");
    vu.observe(el);
  });
}

/* Imprimer une fiche pratique */
$$("[data-imprimer]").forEach((b) => b.addEventListener("click", () => window.print()));

/* Recherche dans les questions fréquentes (dans le navigateur uniquement) */
const champ = $("[data-recherche]");
if (champ) {
  const questions = $$("[data-question]"), etat = $("[data-recherche-etat]"), total = questions.length;
  const normaliser = (t) => t.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "");
  const index = questions.map((q) => normaliser(q.textContent));
  champ.addEventListener("input", () => {
    const mots = normaliser(champ.value).split(/\s+/).filter((m) => m.length > 1);
    let n = 0;
    questions.forEach((q, i) => {
      const garde = mots.every((m) => index[i].includes(m));
      q.hidden = !garde;
      if (garde) n++;
    });
    etat.textContent = mots.length ? (n ? `${n} question${n > 1 ? "s" : ""} sur ${total}.` : "Aucune question ne correspond. Le secrétariat vous répondra.") : `${total} questions, issues des fiches du cabinet.`;
  });
}

/* Carte : chargée seulement à la demande */
$$("[data-carte]").forEach((bloc) => {
  $("[data-carte-charger]", bloc)?.addEventListener("click", (e) => {
    const cadre = document.createElement("iframe");
    cadre.src = bloc.dataset.carte;
    cadre.title = "Carte OpenStreetMap du cabinet Nemaudig";
    cadre.loading = "lazy";
    cadre.referrerPolicy = "no-referrer";
    e.currentTarget.replaceWith(cadre);
    cadre.tabIndex = 0;
    cadre.focus();
  });
});

/* Centres : le lieu survolé s'allume sur le schéma */
$$("[data-lieu]").forEach((lieu) => {
  const point = $(`[data-point="${lieu.dataset.lieu}"]`);
  if (!point) return;
  const allumer = (oui) => point.classList.toggle("est-actif", oui);
  lieu.addEventListener("pointerenter", () => allumer(true));
  lieu.addEventListener("pointerleave", () => allumer(false));
  lieu.addEventListener("focusin", () => allumer(true));
  lieu.addEventListener("focusout", () => allumer(false));
});
