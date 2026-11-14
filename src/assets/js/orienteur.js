/* Rendez-vous : trois questions pour arriver au bon numéro.
   Tout se passe dans le navigateur ; aucune réponse n'est transmise ni conservée.
   On ne demande aucun symptôme : seulement un domaine, un chirurgien, un lieu. */
const donnees = JSON.parse(document.getElementById("donnees").textContent);
const racine = document.querySelector("[data-orienteur]");
const etapes = [...racine.querySelectorAll("[data-etape]")];
const pas = [...racine.querySelectorAll("[data-pas]")];
const base = document.documentElement.dataset.base || "";
const choix = { domaine: null, chirurgien: null, lieu: null };
const parCle = (liste, cle) => liste.find((x) => x.cle === cle);

function creer(balise, classe, texte) {
  const el = document.createElement(balise);
  if (classe) el.className = classe;
  if (texte !== undefined) el.textContent = texte;
  return el;
}

let auChargement = false;
function aller(numero, foyer = !auChargement) {
  etapes.forEach((el) => { el.hidden = Number(el.dataset.etape) !== numero; });
  pas.forEach((el) => {
    const n = Number(el.dataset.pas);
    el.classList.toggle("est-fait", n < numero);
    if (n === Math.min(numero, 3)) el.setAttribute("aria-current", "step"); else el.removeAttribute("aria-current");
  });
  if (foyer) etapes.find((el) => !el.hidden).querySelector("h2").focus();
}

function boutonChirurgien(c) {
  const b = creer("button", "choix");
  b.type = "button";
  const img = new Image(48, 60);
  img.src = c.photo; img.alt = "";
  const texte = creer("span");
  texte.append(creer("span", "", c.nom), creer("small", "", c.accroche));
  b.append(img, texte);
  b.addEventListener("click", () => { choix.chirurgien = c.cle; etapeLieu(); });
  return b;
}

function etapeChirurgien() {
  const domaine = parCle(donnees.domaines, choix.domaine);
  const proposes = domaine ? donnees.chirurgiens.filter((c) => domaine.chirurgiens.includes(c.cle)) : donnees.chirurgiens;
  const liste = racine.querySelector("[data-chirurgiens]");
  liste.replaceChildren();
  racine.querySelector("[data-orientation]").textContent = domaine
    ? `Pour « ${domaine.nom} », ${proposes.length > 1 ? "ces chirurgiens sont proposés" : "ce chirurgien est proposé"} d'après les spécialités affichées.`
    : "Choisissez votre chirurgien, ou laissez le secrétariat vous orienter.";
  proposes.forEach((c) => { const li = creer("li"); li.append(boutonChirurgien(c)); liste.append(li); });
  const li = creer("li"), neutre = creer("button", "choix choix--neutre", "Sans préférence : le secrétariat m'oriente");
  neutre.type = "button";
  neutre.addEventListener("click", () => { choix.chirurgien = null; etapeLieu(); });
  li.append(neutre); liste.append(li);
  aller(2);
}

function etapeLieu() {
  const c = parCle(donnees.chirurgiens, choix.chirurgien);
  if (!c || !c.uzes) { choix.lieu = "nimes"; resultat(); return; } // un seul lieu possible : on n'impose pas la question
  const liste = racine.querySelector("[data-lieux]");
  liste.replaceChildren();
  [["nimes", "Au cabinet, à Nîmes"], ["uzes", `À Uzès — ${donnees.creneauUzes.toLowerCase()}`]].forEach(([cle, nom]) => {
    const li = creer("li"), b = creer("button", "choix", nom);
    b.type = "button";
    b.addEventListener("click", () => { choix.lieu = cle; resultat(); });
    li.append(b); liste.append(li);
  });
  aller(3);
}

function lienTel(numero) {
  const a = creer("a", "resultat__numero", numero);
  // En démonstration, site.js affiche un message au lieu d'appeler
  if (donnees.demo) { a.href = "#"; a.dataset.demoTel = numero; } else a.href = `tel:+33${numero.replace(/\s/g, "").slice(1)}`;
  return a;
}

function resultat() {
  const c = parCle(donnees.chirurgiens, choix.chirurgien);
  const zone = racine.querySelector("[data-resultat]");
  const bloc = creer("div", "resultat");
  const qui = creer("div", "resultat__qui");
  if (c) {
    const img = new Image(72, 90); img.src = c.photo; img.alt = "";
    const texte = creer("p");
    texte.append(creer("strong", "", c.nom), document.createElement("br"), creer("span", "note", c.accroche));
    qui.append(img, texte);
  } else {
    qui.style.gridTemplateColumns = "1fr";
    qui.append(creer("p", "", "Le secrétariat vous oriente vers le chirurgien le plus à même de vous prendre en charge."));
  }
  const numeros = creer("p");
  (choix.lieu === "uzes" ? donnees.telUzes : [donnees.tel]).forEach((n) => numeros.append(lienTel(n)));
  const horaires = creer("p", "note", choix.lieu === "uzes" ? `Centre hospitalier d'Uzès · ${donnees.horairesUzes}` : `Cabinet de Nîmes · ${donnees.horaires}`);
  const suite = creer("p");
  const enLigne = creer("a", "lien-fleche", "Ou en ligne, sur Maiia");
  enLigne.href = donnees.maiia; enLigne.target = "_blank"; enLigne.rel = "noopener";
  const documents = creer("a", "lien-fleche", "Les documents à apporter");
  documents.href = `${base}/preparer/`;
  suite.append(enLigne, document.createTextNode("   "), documents);
  bloc.append(qui, numeros, horaires, suite);
  zone.replaceChildren(bloc);
  aller(4);
}

racine.querySelectorAll("[data-domaine]").forEach((b) => b.addEventListener("click", () => { choix.domaine = b.dataset.domaine || null; etapeChirurgien(); }));
racine.querySelectorAll("[data-retour]").forEach((b) => b.addEventListener("click", () => (b.dataset.retour === "2" ? etapeChirurgien() : aller(Number(b.dataset.retour)))));

// Arrivée depuis la fiche d'un chirurgien : on passe directement au lieu
const preselection = new URLSearchParams(location.search).get("c");
if (parCle(donnees.chirurgiens, preselection)) { auChargement = true; choix.chirurgien = preselection; etapeLieu(); auChargement = false; }
