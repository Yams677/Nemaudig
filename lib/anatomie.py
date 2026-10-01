"""Planche anatomique de l'appareil digestif — SVG dessiné à la main, schématique.

Vue de face : le côté droit du patient est à GAUCHE de l'image (convention
anatomique). viewBox 0 0 400 600.

planche(actif=..., interactif=True) : chaque organe devient un lien vers sa
famille de pathologies ; `actif` met un ou plusieurs organes en lumière.
"""

from lib.html import e

# (clé, libellé, lien, liste de (type, d, extra))  — type : "f" surface pleine, "t" tube (trait épais)
ORGANES = [
    ("oesophage", "Œsophage", "/pathologies/oesophage-estomac/", [
        ("t", "M201,14 C198,46 209,78 206,108 C203,136 212,160 216,178", ' stroke-width="10"'),
    ]),
    ("surrenales", "Glandes surrénales", "/pathologies/surrenales/", [
        ("f", "M150,262 C156,250 170,250 174,262 C168,266 156,267 150,262 Z", ""),
        ("f", "M244,250 C250,238 264,238 268,250 C262,254 250,255 244,250 Z", ""),
    ]),
    ("pancreas", "Pancréas", "/pathologies/cancer-du-pancreas/", [
        ("f", "M186,292 C182,279 194,271 207,275 C232,269 262,260 290,246 C303,241 310,252 301,260 "
              "C277,276 241,290 215,298 C202,302 189,301 186,292 Z", ""),
        ("t", "M201,254 C185,256 175,267 175,283 C175,301 190,311 210,307 C223,305 233,299 239,291", ' stroke-width="9"'),
    ]),
    ("foie", "Foie", "/pathologies/foie-vesicule-pancreas/", [
        ("f", "M106,152 C138,128 222,128 266,148 C256,158 240,166 226,180 C212,196 196,212 176,222 "
              "C150,236 120,236 104,218 C90,200 92,166 106,152 Z", ""),
    ]),
    ("vesicule", "Vésicule biliaire", "/pathologies/vesicule-biliaire/", [
        ("f", "M143,212 C152,204 168,209 167,224 C166,240 152,247 145,238 C139,230 137,219 143,212 Z", ""),
    ]),
    ("estomac", "Estomac", "/pathologies/oesophage-estomac/", [
        ("f", "M214,176 C222,150 263,139 285,161 C305,181 301,232 277,254 C259,270 226,272 206,258 "
              "L199,250 C214,248 232,243 242,231 C252,217 244,195 230,188 C224,184 218,182 214,176 Z", ""),
    ]),
    ("intestin", "Intestin grêle", "/pathologies/mici/", [
        ("t", "M176,346 C200,334 246,334 262,348 C271,359 250,365 230,363 C205,361 181,363 173,375 "
              "C166,389 200,393 228,391 C252,389 271,393 267,407 C263,421 230,419 205,419 C185,419 168,425 172,437 "
              "C175,446 160,446 150,436", ' stroke-width="10"'),
    ]),
    ("colon", "Côlon", "/pathologies/colon-rectum/", [
        ("t", "M140,446 C129,424 128,362 134,322 C138,302 151,296 171,300 C200,306 221,319 246,315 "
              "C266,311 281,297 293,301 C301,307 297,341 297,381 C297,411 297,425 291,439", ' stroke-width="22"'),
    ]),
    ("sigmoide", "Côlon sigmoïde", "/pathologies/diverticules-du-sigmoide/", [
        ("t", "M291,439 C278,463 247,447 233,453 C219,459 213,471 208,483", ' stroke-width="18"'),
    ]),
    ("rectum", "Rectum", "/pathologies/colon-rectum/", [
        ("t", "M208,483 C204,500 203,514 203,528", ' stroke-width="18"'),
    ]),
    ("anus", "Canal anal", "/pathologies/proctologie/", [
        ("f", "M195,536 C195,530 211,530 211,536 C211,546 195,546 195,536 Z", ""),
    ]),
]

# Repères de paroi et de surface (pas des organes au sens strict).
REPERES = [
    ("aine", "Région de l'aine", "/pathologies/hernie-inguinale/",
     "M118,452 C138,478 162,500 186,512 M282,452 C262,478 238,500 214,512"),
    ("ombilic", "Ombilic", "/pathologies/hernie-ombilicale/", None),
]

LIBELLES = {k: l for k, l, *_ in ORGANES} | {k: l for k, l, *_ in REPERES}

SILHOUETTE = ("M178,0 C178,22 172,34 150,42 C110,54 76,62 66,100 C58,140 70,200 82,260 C90,310 88,350 96,400 "
              "C104,450 118,490 150,520 C170,540 186,556 200,562 C214,556 230,540 250,520 C282,490 296,450 304,400 "
              "C312,350 310,310 318,260 C330,200 342,140 334,100 C324,62 290,54 250,42 C228,34 222,22 222,0")

# Côtes et bassin, en filigrane.
OSSATURE = (
    "M120,118 C150,104 250,104 280,118 M112,140 C150,124 250,124 288,140 M108,164 C150,146 250,146 292,164 "
    "M108,190 C140,174 170,172 196,186 M292,190 C260,174 230,172 204,186 M112,216 C132,206 150,204 168,210 "
    "M288,216 C268,206 250,204 232,210 "
    "M118,440 C150,420 176,430 192,452 M282,440 C250,420 224,430 208,452"
)

# Organe → zones à éclairer (certaines pathologies concernent plusieurs organes).
GROUPES = {
    "paroi": ["paroi", "aine", "ombilic"],
    "colon": ["colon", "sigmoide"],
    "colon-rectum": ["colon", "sigmoide", "rectum"],
    "foie": ["foie", "vesicule"],
}


def _organe(cle, libelle, lien, formes, interactif, actifs):
    classes = "org" + (" is-actif" if cle in actifs else "")
    dessin = "".join(
        f'<path class="org__{"t" if t == "t" else "f"}" d="{d}"{extra}/>' for t, d, extra in formes)
    if interactif:
        return (f'<a class="{classes}" data-organe="{cle}" href="{lien}" aria-label="{e(libelle)} — voir les pathologies">'
                f'<title>{e(libelle)}</title>{dessin}</a>')
    return f'<g class="{classes}" data-organe="{cle}">{dessin}</g>'


def planche(actif=None, interactif=False, ident="planche", classe="", titre="Schéma de l'appareil digestif"):
    actifs = set()
    for a in ([actif] if isinstance(actif, str) else (actif or [])):
        actifs.update(GROUPES.get(a, [a]))
    organes = "".join(_organe(k, l, lien, f, interactif, actifs) for k, l, lien, f in ORGANES)

    aine = REPERES[0]
    cl_aine = "rep rep--aine" + (" is-actif" if "aine" in actifs else "")
    cl_omb = "rep rep--ombilic" + (" is-actif" if "ombilic" in actifs else "")
    cl_paroi = "paroi" + (" is-actif" if "paroi" in actifs else "")
    cl_peau = "silhouette" + (" is-actif" if "peau" in actifs else "")
    if interactif:
        aine_svg = (f'<a class="{cl_aine}" data-organe="aine" href="{aine[2]}" aria-label="Région de l\'aine — hernie inguinale">'
                    f'<title>Région de l\'aine</title><path d="{aine[3]}"/></a>')
        omb_svg = (f'<a class="{cl_omb}" data-organe="ombilic" href="/pathologies/hernie-ombilicale/" aria-label="Ombilic — hernie ombilicale">'
                   f'<title>Ombilic</title><circle cx="203" cy="352" r="6"/></a>')
    else:
        aine_svg = f'<g class="{cl_aine}" data-organe="aine"><path d="{aine[3]}"/></g>'
        omb_svg = f'<g class="{cl_omb}" data-organe="ombilic"><circle cx="203" cy="352" r="6"/></g>'

    extras = ""
    if "thorax" in actifs:
        extras += ('<g class="rep is-actif" data-organe="thorax"><rect x="128" y="86" width="20" height="16" rx="5"/>'
                   '<path d="M146,92 C164,86 176,74 184,52" fill="none"/></g>')
    if "sacrum" in actifs:
        extras += '<g class="rep is-actif" data-organe="sacrum"><circle cx="200" cy="552" r="7"/></g>'

    return f'''<svg class="planche {classe}" id="{ident}" viewBox="0 0 400 600" role="img" aria-labelledby="{ident}-t" xmlns="http://www.w3.org/2000/svg">
<title id="{ident}-t">{e(titre)}</title>
<defs>
  <linearGradient id="{ident}-scan" x1="0" x2="0" y1="0" y2="1">
    <stop offset="0" stop-color="var(--scan)" stop-opacity="0"/>
    <stop offset=".5" stop-color="var(--scan)" stop-opacity=".55"/>
    <stop offset="1" stop-color="var(--scan)" stop-opacity="0"/>
  </linearGradient>
  <clipPath id="{ident}-clip"><path d="{SILHOUETTE} Z"/></clipPath>
</defs>
<path class="{cl_peau}" d="{SILHOUETTE}"/>
<path class="{cl_paroi}" d="M112,300 C118,380 140,460 200,500 C260,460 282,380 288,300"/>
<path class="ossature" d="{OSSATURE}"/>
<path class="diaphragme" d="M100,176 C140,120 260,120 300,176"/>
<g class="organes">{organes}</g>
{aine_svg}{omb_svg}{extras}
<g clip-path="url(#{ident}-clip)" aria-hidden="true"><rect class="scan" x="0" y="-80" width="400" height="80" fill="url(#{ident}-scan)"/></g>
</svg>'''


def donnees_3d():
    """Mêmes tracés que la planche SVG, exportés pour la version 3D (assets/js/anatomie3d.js)."""
    import json
    organes = [{"cle": k, "libelle": l, "lien": lien, "formes": [{"type": t, "d": d} for t, d, _ in f]}
               for k, l, lien, f in ORGANES]
    organes.append({"cle": "aine", "libelle": "Région de l'aine", "lien": REPERES[0][2],
                    "formes": [{"type": "r", "d": REPERES[0][3]}]})
    organes.append({"cle": "ombilic", "libelle": "Ombilic", "lien": "/pathologies/hernie-ombilicale/",
                    "formes": [{"type": "o", "d": "M203,352"}]})
    return json.dumps({"organes": organes, "silhouette": SILHOUETTE}, ensure_ascii=False)
