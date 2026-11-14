"""Schémas pédagogiques animés (SVG) — pilotés par assets/js/schemas.js.

Attributs lus par le script (progression t de 0 à 1 sur `data-duree` secondes) :
  data-trace           tracé qui se dessine entre data-de et data-a
  data-pointe="#id"    élément placé à la tête du tracé #id
  data-flux            points lumineux qui circulent le long du tracé entre data-de et data-a
  data-vu-de / -a      élément visible seulement dans cet intervalle
Schémas de principe, volontairement simplifiés : à faire relire par l'équipe.
"""
from html import escape

VUE = 'viewBox="0 0 480 360" role="img"'


def _etapes(etapes):
    return "".join(f'<li data-de="{de}" data-a="{a}">{escape(t)}</li>' for de, a, t in etapes)


def _figure(cle, titre, duree, fige, svg, etapes, note):
    return f'''<figure class="schema" data-schema="{cle}" data-duree="{duree}" data-fige="{fige}">
  <div class="schema__cadre">
    <svg {VUE} aria-labelledby="schema-{cle}-titre"><title id="schema-{cle}-titre">{escape(titre)}</title>{svg}</svg>
    <button class="schema__lecture" type="button" data-lecture data-etat="lecture"><span class="visuellement-cache">Mettre l'animation en pause</span></button>
  </div>
  <figcaption>
    <p class="repere">{escape(titre)}</p>
    <ol class="schema__etapes">{_etapes(etapes)}</ol>
    <p class="schema__note">{escape(note)}</p>
  </figcaption>
</figure>'''


def _colon():
    trajet = ("M250 338 L250 300 C250 272 300 290 318 268 C334 248 372 262 372 232 L372 118 "
              "C372 84 340 78 316 92 C276 116 204 116 164 92 C140 78 108 84 108 118 L108 262")
    svg = f'''
  <path class="sch-tube" d="{trajet}"/>
  <path class="sch-tube-int" d="{trajet}"/>
  <path class="sch-plis" d="{trajet}"/>
  <circle class="sch-polype" cx="238" cy="98" r="5"/>
  <path id="sch-colon-trajet" class="sch-trace" d="{trajet}" data-trace data-de="0.04" data-a="0.8"/>
  <g data-pointe="#sch-colon-trajet"><circle class="sch-halo" r="11"/><circle class="sch-pointe" r="4"/></g>
  <g data-vu-de="0.5" data-vu-a="1"><circle class="sch-anneau" cx="238" cy="98" r="13"/>
    <path class="sch-fil" d="M238 85 L238 52"/><text class="sch-texte sch-texte--fort" x="238" y="44" text-anchor="middle">Polype repéré</text></g>
  <text class="sch-texte" x="266" y="334">Rectum</text>
  <text class="sch-texte" x="322" y="298">Sigmoïde</text>
  <text class="sch-texte" x="394" y="180">Côlon gauche</text>
  <text class="sch-texte" x="240" y="140" text-anchor="middle">Côlon transverse</text>
  <text class="sch-texte" x="86" y="180" text-anchor="end">Côlon droit</text>
  <text class="sch-texte" x="86" y="266" text-anchor="end">Cæcum</text>'''
    return _figure("colon", "Coloscopie : la progression de l'endoscope", 14, 0.8, svg, [
        (0, 0.5, "L'endoscope souple progresse du rectum vers le côlon droit."),
        (0.5, 0.8, "Un polype est repéré sur la paroi : il pourra être retiré."),
        (0.8, 1, "Arrivé au début du côlon, l'appareil est retiré lentement en examinant la paroi."),
    ], "Schéma de principe, vu de face. L'examen est réalisé par un gastro-entérologue.")


def _estomac():
    contour = ("M236 20 L236 92 C212 110 196 150 188 190 C182 222 160 236 128 240 L96 240 M96 268 L132 268 "
               "C196 268 262 250 300 200 C332 158 334 104 306 82 C290 70 272 72 264 86 L264 20")
    svg = f'''
  <path class="sch-contour" d="{contour}"/>
  <path class="sch-flux-guide" d="M250 24 L250 96 C254 130 262 150 258 180" data-flux data-n="4" data-de="0" data-a="0.38"/>
  <path class="sch-flux-guide" d="M258 180 C290 170 296 130 270 120 C240 112 220 150 232 190 C240 214 270 210 258 180" data-flux data-n="7" data-de="0.28" data-a="0.78" data-tours="2"/>
  <path class="sch-onde" d="M196 196 C214 206 238 226 246 250" data-vu-de="0.34" data-vu-a="0.46"/>
  <path class="sch-onde" d="M176 222 C192 228 208 244 212 262" data-vu-de="0.48" data-vu-a="0.6"/>
  <path class="sch-onde" d="M156 234 C166 240 172 252 172 266" data-vu-de="0.62" data-vu-a="0.74"/>
  <path class="sch-flux-guide" d="M214 232 C186 250 150 254 100 254" data-flux data-n="3" data-de="0.66" data-a="1" data-couleur="turquoise"/>
  <text class="sch-texte" x="278" y="40">Œsophage</text>
  <text class="sch-texte" x="344" y="150">Estomac</text>
  <text class="sch-texte" x="150" y="296" text-anchor="middle">Pylore</text>
  <text class="sch-texte" x="70" y="226" text-anchor="middle">Duodénum</text>'''
    return _figure("estomac", "L'estomac : brasser, puis libérer", 12, 0.55, svg, [
        (0, 0.3, "Les aliments arrivent par l'œsophage."),
        (0.3, 0.66, "L'estomac les brasse et les mélange au suc gastrique."),
        (0.66, 1, "Le contenu passe, par petites quantités, dans le duodénum."),
    ], "Schéma de principe : les contractions sont représentées par des ondes.")


def _foie():
    svg = '''
  <path class="sch-contour sch-contour--plein" d="M70 150 C70 100 130 80 220 84 C300 86 380 96 410 120 C420 132 400 150 370 160 C320 176 270 200 230 230 C190 258 120 262 90 232 C74 214 70 180 70 150 Z"/>
  <path class="sch-contour sch-contour--turquoise" d="M214 226 C228 232 232 252 222 266 C212 276 200 268 202 252 C204 240 208 232 214 226 Z"/>
  <path class="sch-flux-guide" d="M330 336 C320 286 290 240 246 186" data-flux data-n="5" data-de="0" data-a="0.5" data-couleur="bleu"/>
  <path class="sch-flux-guide" d="M228 156 C234 114 242 72 248 24" data-flux data-n="5" data-de="0.3" data-a="0.78"/>
  <path class="sch-flux-guide" d="M236 198 C230 212 222 222 216 234 C214 250 220 262 232 276 C252 300 282 314 318 322" data-flux data-n="4" data-de="0.6" data-a="1" data-couleur="turquoise"/>
  <text class="sch-texte" x="346" y="342">Sang venu de l'intestin</text>
  <text class="sch-texte" x="262" y="34">Sang épuré, vers le cœur</text>
  <text class="sch-texte" x="186" y="296" text-anchor="end">Vésicule biliaire</text>
  <text class="sch-texte" x="334" y="318">Bile</text>
  <text class="sch-texte sch-texte--fort" x="150" y="166" text-anchor="middle">Foie</text>'''
    return _figure("foie", "Le foie : épurer, transformer, fabriquer la bile", 13, 0.7, svg, [
        (0, 0.32, "Le sang venu de l'intestin arrive au foie par la veine porte."),
        (0.32, 0.6, "Le foie l'épure, transforme et stocke les nutriments."),
        (0.6, 1, "Il fabrique la bile, stockée dans la vésicule puis libérée dans l'intestin."),
    ], "Schéma de principe, vu de face.")


SCHEMAS = {"colon": _colon, "estomac": _estomac, "foie": _foie}


def schema(cle):
    return SCHEMAS[cle]() if cle in SCHEMAS else ""
