/* Explorateur : un organe à la fois. Les fiches et les images sont déjà dans la page ;
   le script n'en montre qu'une et tient l'adresse à jour (#foie, #colon…). */
const racine = document.querySelector("[data-explorateur]");
const donnees = JSON.parse(document.getElementById("donnees").textContent);
const fiches = racine.querySelector(".organes");
const onglets = [...racine.querySelectorAll("[data-choix]")];
const images = [...racine.querySelectorAll("[data-image]")];
const scene = racine.querySelector(".explorateur__scene");
const calme = window.matchMedia("(prefers-reduced-motion: reduce)").matches || document.documentElement.classList.contains("fige");

function choisir(organe, { defiler = false, foyer = false, adresse = true } = {}) {
  if (!donnees.noms[organe]) organe = donnees.ordre[0];
  fiches.querySelectorAll(".organe").forEach((el) => el.classList.toggle("est-choisi", el.dataset.organe === organe));
  images.forEach((el) => el.classList.toggle("est-choisie", el.dataset.image === organe));
  onglets.forEach((a) => (a.dataset.choix === organe ? a.setAttribute("aria-current", "true") : a.removeAttribute("aria-current")));
  scene.style.setProperty("--teinte", `var(--${donnees.teintes[organe]})`);
  if (adresse) history.replaceState(null, "", `#${organe}`);
  const fiche = document.getElementById(organe);
  if (defiler) fiche.scrollIntoView({ behavior: calme ? "auto" : "smooth", block: "start" });
  if (foyer) fiche.querySelector("h2").focus({ preventScroll: true });
}

fiches.classList.add("est-pilote");
onglets.forEach((a) => a.addEventListener("click", (e) => {
  e.preventDefault();
  choisir(a.dataset.choix, { defiler: window.innerWidth < 900, foyer: true });
}));
window.addEventListener("hashchange", () => {
  const ancre = location.hash.slice(1);
  if (donnees.noms[ancre]) choisir(ancre); // « #contenu » et autres ancres ne changent pas la fiche
});
// Sans ancre dans l'adresse, on montre le premier organe sans modifier l'adresse
choisir(location.hash.slice(1), { adresse: !!donnees.noms[location.hash.slice(1)] });
