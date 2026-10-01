"""Petits utilitaires HTML et jeu d'icônes (trait 1,6 px, hérite de currentColor)."""

from html import escape

import config

C = config.CABINET


def e(texte):
    return escape(str(texte), quote=True)


def tel_href(numero=None):
    """Lien d'appel. `numero` : format affiché (« 04 66 … ») ou E.164 ; par défaut le cabinet.
    En maquette, les liens pointent vers /contact/ : aucun appel accidentel vers un vrai numéro."""
    if config.DEMO:
        return "/contact/"
    n = "".join(ch for ch in (numero or C["telephone_e164"]) if ch.isdigit() or ch == "+")
    if n.startswith("0"):
        n = "+33" + n[1:]
    return f"tel:{n}"


def bouton(href, texte, variante="plein", externe=False, icone=None, extra=""):
    cible = ' target="_blank" rel="noopener"' if externe else ""
    ico = ICONES[icone] if icone else ""
    return (f'<a class="btn btn--{variante}" href="{e(href)}"{cible}{extra}>{ico}'
            f'<span>{texte}</span><span class="btn__fleche" aria-hidden="true">{ICONES["fleche"]}</span></a>')


def surtitre(texte, numero=None):
    num = f'<span class="surtitre__num">{numero}</span>' if numero else ""
    return f'<p class="surtitre">{num}<span>{texte}</span></p>'


def riche(texte):
    """Mini-balisage : paragraphes séparés par une ligne vide, lignes « - » = puces."""
    blocs = []
    for bloc in texte.strip().split("\n\n"):
        lignes = [l.strip() for l in bloc.strip().split("\n") if l.strip()]
        if lignes and all(l.startswith("- ") for l in lignes):
            blocs.append("<ul class=\"liste\">" + "".join(f"<li>{e(l[2:])}</li>" for l in lignes) + "</ul>")
        else:
            blocs.append("".join(f"<p>{e(l)}</p>" for l in lignes))
    return "".join(blocs)


def _svg(corps, vb="0 0 24 24"):
    return (f'<svg class="ico" viewBox="{vb}" aria-hidden="true" focusable="false" fill="none" '
            f'stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{corps}</svg>')


ICONES = {
    "fleche": _svg('<path d="M5 12h13M13 6l6 6-6 6"/>'),
    "tel": _svg('<path d="M6.6 3.8h2.6l1.3 3.6-1.8 1.3a11 11 0 0 0 5.6 5.6l1.3-1.8 3.6 1.3v2.6a2 2 0 0 1-2.2 2A15.6 15.6 0 0 1 4.6 6a2 2 0 0 1 2-2.2Z"/>'),
    "agenda": _svg('<rect x="3.5" y="5" width="17" height="15.5" rx="3"/><path d="M3.5 10h17M8 3v4M16 3v4M8 14h3"/>'),
    "lieu": _svg('<path d="M12 21s-6.5-5.6-6.5-11a6.5 6.5 0 0 1 13 0c0 5.4-6.5 11-6.5 11Z"/><circle cx="12" cy="10" r="2.4"/>'),
    "horloge": _svg('<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>'),
    "urgence": _svg('<path d="M12 3.5 21 19.5H3Z"/><path d="M12 10v4M12 17v.3"/>'),
    "robot": _svg('<path d="M12 3v3M7 21l2-6M17 21l-2-6"/><rect x="6" y="6" width="12" height="9" rx="3"/><path d="M9.5 10.5h.01M14.5 10.5h.01"/>'),
    "camera": _svg('<path d="M3 12h11M14 9v6l6 3V6Z"/><circle cx="6" cy="12" r="0"/>'),
    "bouclier": _svg('<path d="M12 3 4.5 6v5.5c0 4.6 3.2 8 7.5 9.5 4.3-1.5 7.5-4.9 7.5-9.5V6Z"/><path d="m8.8 12 2.3 2.3 4.3-4.6"/>'),
    "equipe": _svg('<circle cx="8.5" cy="8.5" r="3"/><circle cx="16.5" cy="9.5" r="2.5"/><path d="M3 19.5c.6-3.3 3-5.5 5.5-5.5s4.9 2.2 5.5 5.5M14.5 14.2c2.6-.5 5.3 1.2 6 4.8"/>'),
    "coeur": _svg('<path d="M12 20s-7.5-4.6-7.5-10.2A4.3 4.3 0 0 1 12 7.2a4.3 4.3 0 0 1 7.5 2.6C19.5 15.4 12 20 12 20Z"/>'),
    "lecture": _svg('<circle cx="12" cy="12" r="9"/><path d="M10 8.5v7l5.5-3.5Z" fill="currentColor"/>'),
    "fichier": _svg('<path d="M6 3.5h8.5L18.5 7.5v13H6zM14 3.5V8h4.5M9 12h6M9 15.5h6"/>'),
    "check": _svg('<path d="m5 12.5 4.2 4.2L19 7"/>'),
    "maison": _svg('<path d="M4 11 12 4l8 7M6.5 9.5V20h11V9.5"/>'),
    "lune": _svg('<path d="M19 14.5A7.5 7.5 0 1 1 9.5 5a6 6 0 0 0 9.5 9.5Z"/>'),
    "pulse": _svg('<path d="M3 12h4l2-5 3.5 10 2.5-7 1.5 2H21"/>'),
    "loupe": _svg('<circle cx="11" cy="11" r="6.5"/><path d="m20 20-4.4-4.4"/>'),
    "menu": _svg('<path d="M4 7h16M4 12h16M4 17h16"/>'),
    "croix": _svg('<path d="M6 6l12 12M18 6 6 18"/>'),
    "externe": _svg('<path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/>'),
    "laser": _svg('<path d="M4 20 14 10M14 10l2-6 2 2 2 2-6 2"/><path d="M4 14l2 1M9 19l1 2M3 17h2"/>'),
    "balance": _svg('<path d="M12 4v16M6 20h12M5 8h14M5 8l-2.5 6a2.5 2.5 0 0 0 5 0Zm14 0-2.5 6a2.5 2.5 0 0 0 5 0Z"/>'),
    "diplome": _svg('<path d="M3 9 12 4.5 21 9l-9 4.5Z"/><path d="M7 11v4.5c0 1.4 2.2 2.5 5 2.5s5-1.1 5-2.5V11M21 9v5"/>'),
    "euro": _svg('<path d="M17.5 6.5A6.5 6.5 0 1 0 17.5 17.5M4 10.5h9M4 13.5h9"/>'),
    "question": _svg('<circle cx="12" cy="12" r="9"/><path d="M9.6 9.3a2.5 2.5 0 1 1 3.4 2.4c-.6.3-1 .8-1 1.5v.6M12 16.8v.2"/>'),
    "actu": _svg('<rect x="3.5" y="4.5" width="17" height="15" rx="2.5"/><path d="M7 9h10M7 12.5h10M7 16h6"/>'),
    "video": _svg('<rect x="3" y="6" width="13" height="12" rx="2.5"/><path d="m16 10 5-3v10l-5-3"/>'),
    "mail": _svg('<rect x="3.5" y="5.5" width="17" height="13" rx="2.5"/><path d="m4 7 8 6 8-6"/>'),
}
