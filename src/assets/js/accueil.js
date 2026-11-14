/* Accueil — « Un organe à la fois » : les boutons changent l'organe affiché. */
const vitrine = document.querySelector("[data-vitrine]");
if (vitrine) {
  const boutons = [...vitrine.querySelectorAll("[data-organe]")];
  const vues = [...vitrine.querySelectorAll("[data-vue]")];
  boutons.forEach((bouton) => bouton.addEventListener("click", () => {
    boutons.forEach((b) => b.setAttribute("aria-pressed", String(b === bouton)));
    vues.forEach((v) => v.classList.toggle("est-choisie", v.dataset.vue === bouton.dataset.organe));
  }));
}
