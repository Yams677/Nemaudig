/* Schémas pédagogiques animés (voir lib/schemas.py pour les attributs).
   Lecture seulement lorsque le schéma est à l'écran ; bouton pause ; animations
   réduites : image fixe représentative, lecture possible à la demande. */
const CALME = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const SVG = "http://www.w3.org/2000/svg";
const borne = (x) => Math.min(1, Math.max(0, x));
const part = (el, t) => borne((t - Number(el.dataset.de || 0)) / (Number(el.dataset.a || 1) - Number(el.dataset.de || 0)));

function preparer(figure) {
  const svg = figure.querySelector("svg");
  const duree = Number(figure.dataset.duree) * 1000;
  const etapes = [...figure.querySelectorAll(".schema__etapes li")];
  const bouton = figure.querySelector("[data-lecture]");

  const traces = [...svg.querySelectorAll("[data-trace]")].map((el) => {
    const longueur = el.getTotalLength();
    el.style.strokeDasharray = `${longueur} ${longueur}`;
    return { el, longueur };
  });
  const pointes = [...svg.querySelectorAll("[data-pointe]")].map((el) => ({ el, trace: traces.find((t) => t.el === svg.querySelector(el.dataset.pointe)) }));
  const flux = [...svg.querySelectorAll("[data-flux]")].map((el) => {
    const n = Number(el.dataset.n || 4);
    const points = Array.from({ length: n }, () => {
      const c = document.createElementNS(SVG, "circle");
      c.setAttribute("r", "3.2");
      c.setAttribute("class", `sch-point${el.dataset.couleur ? ` sch-point--${el.dataset.couleur}` : ""}`);
      el.after(c);
      return c;
    });
    return { el, points, longueur: el.getTotalLength(), tours: Number(el.dataset.tours || 1) };
  });
  const visibles = [...svg.querySelectorAll("[data-vu-de]")];

  function dessiner(t) {
    for (const { el, longueur } of traces) el.style.strokeDashoffset = String(longueur * (1 - part(el, t)));
    for (const { el, trace } of pointes) {
      const p = trace.el.getPointAtLength(trace.longueur * part(trace.el, t));
      el.setAttribute("transform", `translate(${p.x.toFixed(1)} ${p.y.toFixed(1)})`);
    }
    for (const f of flux) {
      const avance = part(f.el, t);
      const enCours = avance > 0 && avance < 1;
      f.points.forEach((c, i) => {
        const u = (avance * (f.tours + 0.6) + i / f.points.length * 0.6) % 1;
        const p = f.el.getPointAtLength(f.longueur * u);
        c.setAttribute("cx", p.x.toFixed(1)); c.setAttribute("cy", p.y.toFixed(1));
        c.style.opacity = enCours ? String(Math.min(1, u * 8, (1 - u) * 8) * Math.min(1, avance * 10, (1 - avance) * 10)) : "0";
      });
    }
    for (const el of visibles) el.classList.toggle("est-vu", t >= Number(el.dataset.vuDe) && t <= Number(el.dataset.vuA));
    for (const li of etapes) li.classList.toggle("est-actif", t >= Number(li.dataset.de) && t < Number(li.dataset.a) + (li.dataset.a === "1" ? 0.01 : 0));
  }

  let t = CALME ? Number(figure.dataset.fige) : 0, lecture = !CALME, aLecran = false, dernier = 0, boucle = 0;
  function image(maintenant) {
    boucle = 0;
    if (!lecture || !aLecran) return;
    if (dernier) t = (t + (maintenant - dernier) / duree) % 1;
    dernier = maintenant;
    dessiner(t);
    boucle = requestAnimationFrame(image);
  }
  const relancer = () => { dernier = 0; if (!boucle) boucle = requestAnimationFrame(image); };
  function etatBouton() {
    bouton.dataset.etat = lecture ? "lecture" : "pause";
    bouton.querySelector("span").textContent = lecture ? "Mettre l'animation en pause" : "Lire l'animation";
  }
  bouton.addEventListener("click", () => { lecture = !lecture; etatBouton(); if (lecture) relancer(); });
  new IntersectionObserver(([entree]) => { aLecran = entree.isIntersecting; if (aLecran) { dessiner(t); relancer(); } }, { threshold: 0.2 }).observe(figure);
  etatBouton();
  dessiner(t);
}

document.querySelectorAll("[data-schema]").forEach(preparer);
