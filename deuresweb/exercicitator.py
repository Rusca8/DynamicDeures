"""
MÒDULS PER GENERAR EL LaTeX DELS DIFERENTS EXERCICIS

latexator.py agafarà d'aquí els exercicis a partir del nom d'exercici
"""
import random
import re

import generator as gen
import enunciats as en
import cryptolator as crypt

from pylatex import NoEscape
from rpylatex import (begin, end, part, space, lines, br, needspace, bloctitle, question, choice,
                      taulaconfig, obretaula, obrellarga, filataula, tancataula, envt,
                      escriusolus, blocsolus, blocsolucions, textsolucions)

import quantitats as qtats


def constructor_de(nom):
    """Retorna la funció que cal fer servir per construir l'exercici donat."""
    exercicis = {
        # ********** PX ********** #
        "PX_ALGEB_FACTORITZA": px_algeb_factoritza,
        "PX_ALGEB_SIMPLIFICA": px_algeb_simplifica,
        "PX_BASE_AVALUA": px_base_avalua,
        "PX_BASE_DESXIFRA": px_base_desxifra,
        "PX_BASE_FACTORCOMU": px_base_factorcomu,
        "PX_BASE_INVENTA": px_base_inventa,
        "PX_BASE_PARTSMONOMI": px_base_partsmonomi,
        "PX_IDNOT_ENDEVINAIDENTITAT": px_idnot_endevinaidentitat,
        "PX_IDNOT_IDENTITAT": px_idnot_identitat,
        "PX_OPS_DIVIDEIX": px_ops_divideix,
        "PX_OPS_DIVIDEIXRUFFINI": px_ops_divideixruffini,
        "PX_OPS_MULTIPLICA": px_ops_multiplica,
        "PX_OPS_PARAMETRERESIDU": px_ops_parametreresidu,
        "PX_OPS_RESTA": px_ops_resta,
        "PX_OPS_SUMA": px_ops_suma,
        "PX_OPS_TEOREMARESIDU": px_ops_teoremaresidu,
    }
    return exercicis.get(nom, exercici_no_trobat)  # .get(key, default)


def px_algeb_factoritza(doc, opcions):
    enunciat = "Factoritza els polinomis següents."
    enunsols = "Factoritzar polinomis."
    g = [
        lambda: gen.px(7, 1, solucions=True),  # sense K ni x factor comú
        lambda: gen.px(7, 2, solucions=True),  # sense K factor comú
        lambda: gen.px(7, 3, solucions=True),  # pot tenir de tot
        ]
    pvar = quantilvar(opcions["var"]["sense_constant"])
    p = p_flex([25, 50, 100], pvar, 1)

    tsols = crea_exercici(doc, opcions,
                          g,
                          p,
                          enunciat=enunciat,
                          cols=2,
                          espai_apartat=10,
                          espai_final=10,
                          mates_solus=True,
                          )
    return [enunsols, tsols]


def px_algeb_simplifica(doc, opcions):
    enunciat = "Factoritza els polinomis següents."
    enunsols = "Factoritzar polinomis."
    tsols = crea_exercici(doc, opcions,
                          lambda: gen.px(8, solucions=True),
                          enunciat=enunciat,
                          scale=scale_per("fraccions"),
                          espai_apartat=10,
                          mates_solus=True,
                          )
    return [enunsols, tsols]


def px_base_avalua(doc, opcions):
    enunciat = "Avalua en el punt demanat."
    enunsols = "Avaluar polinomis."
    tsols = crea_exercici(doc, opcions,
                          lambda: gen.px(6, 1, solucions=True),
                          enunciat=enunciat,
                          espai_apartat=10,
                          mates=False,
                          )
    return [enunsols, tsols]


def px_base_desxifra(doc, opcions):
    enunciat = "Extreu factor comú per desxifrar el missatge amagat."
    enunsols = "Desxifrar per factor comú."

    def g():
        sol = en.factorcomu()
        text = r"\ \ \penalty-200".join([f" ${x}$ " for x in crypt.fc_frase(sol)])
        sol = f"{sol}."
        return text, sol
    tsols = crea_exercici(doc, opcions,
                          g,
                          enunciat=enunciat,
                          espai_apartat=20,
                          mates=False,
                          es_spoiler=True,
                          )
    return [enunsols, tsols]


def px_base_factorcomu(doc, opcions):
    enunciat = "Extreu factor comú de les expressions següents."
    enunsols = "Extreure factor comú."
    g = [
         lambda: gen.px(0, 1, termes=2),  # una variable, 2 termes
         lambda: gen.px(0, 1, termes=3),  # una variable, 3 termes
         lambda: gen.px(0, 2, termes=2),  # més variables, 2 termes
         lambda: gen.px(0, 2, termes=3),  # més variables, 3 termes
        ]
    pvar = quantilvar(opcions["var"]["una_variable"])
    p = p_flex([25, 50, 75, 100], pvar, 1)

    tsols = crea_exercici(doc, opcions,
                          g,
                          p,
                          enunciat=enunciat,
                          cols=2,
                          espai_apartat=10,
                          espai_final=4,
                          )
    return [enunsols, tsols]


def px_base_inventa(doc, opcions):
    enunciat = "Inventa't un polinomi que compleixi cadascuna de les descripcions següents."
    enunsols = "Inventar polinomis."
    tsols = crea_exercici(doc, opcions,
                          lambda: en.px_invent(),
                          enunciat=enunciat,
                          espai_apartat=10,
                          mates=False,
                          )
    return [enunsols, tsols]


def px_base_partsmonomi(doc, opcions):
    enunciat = "Indica el coeficient, la part literal, les variables i el grau dels següents monomis."
    enunsols = "Parts de monomis."
    tsols = crea_exercici(doc, opcions,
                          lambda: gen.rand_multimon(random.choice([2, 2, 3])),
                          enunciat=enunciat,
                          cols=4,
                          espai_apartat=10,
                          espai_final=2,
                          )
    return [enunsols, tsols]


def px_idnot_endevinaidentitat(doc, opcions):
    return exercici_no_trobat(doc, opcions)


def px_idnot_identitat(doc, opcions):
    # TODO que crea_exercici rebi la funció que faré servir per generar la llista de gs (per defecte és g_list)
    # (canviar-li el nom a la g_list normal tq quadri amb la nomenclatura de "funcions generadores d'apartats")
    # ...tècnicament, fet així puc pregenerar els exercicis com ho feia amb finorg
    #  (els exercicis especialets que necessiten pregenerar, tindran la seva pròpia funció pregeneradora alternativa)
    # ...i això serveix també per control de repetits. Sembla que hem trobat la manera.
    return exercici_no_trobat(doc, opcions)


def px_ops_divideix(doc, opcions):
    enunciat = "Fes les següents divisions aplicant la regla de Ruffini."
    enunsols = "Divisions per Ruffini."
    g = [
        lambda: gen.px(5, 1, solucions=True),  # ordenat complet exacte
        lambda: gen.px(5, 2, solucions=True),  # ordenat complet
        lambda: gen.px(5, 3, solucions=True),  # ordenat
        lambda: gen.px(5, 4, solucions=True),  # desordenat
    ]
    pvar = quantilvar(opcions["var"]["ordenat"])
    p = p_flex([15, 30, 60, 100], pvar, 2)

    tsols = crea_exercici(doc, opcions,
                          g,
                          p,
                          enunciat=enunciat,
                          espai_apartat=10,
                          )
    return [enunsols, tsols]


def px_ops_divideixruffini(doc, opcions):
    enunciat = "Fes les següents divisions aplicant la regla de Ruffini."
    enunsols = "Divisions per Ruffini."
    g = [
        lambda: gen.px(4, 1, solucions=True),  # ordenat complet exacte
        lambda: gen.px(4, 2, solucions=True),  # ordenat complet
        lambda: gen.px(4, 3, solucions=True),  # ordenat
        lambda: gen.px(4, 4, solucions=True),  # desordenat
    ]
    pvar = quantilvar(opcions["var"]["ordenat"])
    p = p_flex([15, 30, 60, 100], pvar, 2)

    tsols = crea_exercici(doc, opcions,
                          g,
                          p,
                          enunciat=enunciat,
                          espai_apartat=10,
                          )
    return [enunsols, tsols]


def px_ops_multiplica(doc, opcions):
    enunciat = "Fes les següents multiplicacions de polinomis."
    enunsols = "Multiplicacions de polinomis."
    g = [
        lambda: gen.px(3, 1, solucions=True),  # ordenat complet
        lambda: gen.px(3, 2, solucions=True),  # ordenat incomplet
        lambda: gen.px(3, 3, solucions=True),  # desordenat amb tots els t-indep
        lambda: gen.px(3, 4, solucions=True),  # desordenat amb mínim un t-indep
        lambda: gen.px(3, 5, solucions=True),  # desordenat pot sense t-indep
    ]
    pvar = quantilvar(opcions["var"]["ordenat"])
    p = p_flex([25, 50, 60, 70, 100], pvar, 1)

    tsols = crea_exercici(doc, opcions,
                          g,
                          p,
                          enunciat=enunciat,
                          espai_apartat=10,
                          mates_solus=True,
                          )
    return [enunsols, tsols]


def px_ops_parametreresidu(doc, opcions):
    enunciat = "Calcula en cada cas el valor del paràmetre que fa que la divisió sigui exacta."
    enunsols = "Paràmetre sabent residu."

    if opcions["var"]["parametres"]:  # filtro només lletres normals, per si algú canvia l'html amb inspect o què sé jo
        parametres = [re.sub("[^a-yzA-YZ]+", "", c) for c in opcions["var"]["parametres"] if len(c) == 1] or ["k"]
    else:
        parametres = ["k", "m", "a"]

    g = [
        lambda: gen.px(106, 1, par=random.choice(parametres), solucions=True),  # k = coef sencer
        lambda: gen.px(106, 2, par=random.choice(parametres), solucions=True),  # k = factor d'un coef
        lambda: gen.px(106, 3, par=random.choice(parametres), solucions=True),  # k = factor de més d'un coef
        lambda: gen.px(106, 4, par=random.choice(parametres), solucions=True),  # k = sumand d'un coef
        lambda: gen.px(106, 5, par=random.choice(parametres), solucions=True),  # k = sumand de més d'un coef
        lambda: gen.px(106, 6, par=random.choice(parametres), solucions=True),  # k = factors i sumands barrejats
        ]
    p = [16.67, 33.33, 50.0, 66.67, 83.33, 100.0]  # [round((x+1)*100/6, 2) for x in range(6)]  # !! round(,2), pas //

    tsols = crea_exercici(doc, opcions,
                          g,
                          p,
                          enunciat=enunciat,
                          espai_apartat=10,
                          )
    return [enunsols, tsols]


def px_ops_resta(doc, opcions):
    enunciat = "Fes les següents restes de polinomis."
    enunsols = "Restes de polinomis."
    g = [
        lambda: gen.px(2, 1, noneg=True, solucions=True),   # ordenat complet, sense doble negatiu
        lambda: gen.px(2, 1, noneg=False, solucions=True),  # ordenat complet
        lambda: gen.px(2, 2, solucions=True),               # ordenat incomplet
        lambda: gen.px(2, 3, solucions=True),               # desordenat
        ]
    pvar = quantilvar(opcions["var"]["ordenat"])
    p = p_flex([[15, {"max": 3}], 30, 60, 100], pvar, 2)

    tsols = crea_exercici(doc, opcions,
                          g,
                          p,
                          enunciat=enunciat,
                          espai_apartat=10,
                          mates_solus=True,
                          )
    return [enunsols, tsols]


def px_ops_suma(doc, opcions):
    enunciat = "Fes les següents sumes de polinomis."
    enunsols = "Sumes de polinomis."
    g = [
        lambda: gen.px(1, 1, solucions=True),  # ordenat complet
        lambda: gen.px(1, 2, solucions=True),  # ordenat incomplet
        lambda: gen.px(1, 3, solucions=True),  # desordenat
        ]
    pvar = quantilvar(opcions["var"]["ordenat"])
    p = p_flex([25, 50, 100], pvar, 1)

    tsols = crea_exercici(doc, opcions,
                          g,
                          p,
                          enunciat=enunciat,
                          espai_apartat=10,
                          mates_solus=True,
                          )
    return [enunsols, tsols]


def px_ops_teoremaresidu(doc, opcions):
    enunciat = "Calcula el residu."
    enunsols = "Calcular residus."
    tsols = crea_exercici(doc, opcions,
                          lambda: gen.px(6, 2, solucions=True),
                          enunciat=enunciat,
                          espai_apartat=10,
                          mates=False,
                          )
    return [enunsols, tsols]


# ----------------------------------------------------------------------------------------- #
def tema_apartat_exemple(doc, opcions):
    return exercici_no_trobat(doc, opcions)


def exercici_no_trobat(doc, opcions):
    needspace(doc, 8)
    question(doc, "42")
    doc.append("No s'ha trobat cap constructor per l'exercici " + opcions["exnom"].upper())
    return


# ******************************* Esquelets ********************************* #
def crea_exercici(doc, opcions, g, p="", enunciat="EM FALTA L'ENUNCIAT, NEN", cols=1, scale=1,
                  espai_apartat=4, espai_final=0, mates=True, mates_solus=False, es_spoiler=False):
    """Munta un exercici LaTeX (exercici sense varietat interna) a partir de les seves dades.

    :param doc: document on posarem l'exercici
    :param opcions: opcions que ens passa el formulari de l'exercici
    :param g: llista de funcions generadores (lambdes passades des de fora)
    :param p: llista de quantils on vull que s'acabi cada funció generadora (amb opcions o el que sigui, per g_list)
    :param enunciat: l'enunciat que vols
    :param cols: quantitat de columnes que tindrà l'exercici
    :param scale: coeficient d'ampliació del text (per fer llegibles les fraccions, i tal)
    :param espai_apartat: espai vertical entre elements (mm) - per defecte 0.4 (una mica d'interlineat)
    :param espai_final: espai després del multicol (mm)
    :param mates: l'apartat és tot notació matemàtica (cal fer '$text$' en lloc de 'text')
    :param mates_solus: les solucions són notació matemàtica (cal fer '$solu$' en lloc de 'solu')
    :param es_spoiler: si és True, només escriuré la solució si és en una plana a part

    :return: res (només afegeix l'exercici al doc)
    """
    varietat = True  # True és que hi ha més d'un generador dins el mateix exercici (i.e. dificultats graduals, etc)
    try:
        len(g)
    except:
        varietat = False

    n = quantes(opcions)
    punts = opcions["punts"]
    try:
        punts = int(punts)
        punts = max(0, min(1000000, punts))  # (mateixos límits que a quantes.html)
    except:
        punts = 0

    needspace(doc, 8)
    question(doc, f"{n*punts}")
    doc.append(enunciat)

    begin(doc, 'parts')
    begin(doc, 'multicols', cols) if cols > 1 else None  # la jerarquia LaTeX quedava més neta posat així

    sols = []  # llista amb la solució de cada apartat

    if varietat:  # poliexercici (diferents generadors al llarg dels apartats)
        # precàlculs
        gs = g_list(n, g, p)
    else:  # monoexercici (mateix generador tots els apartats)
        gs = (g for _ in range(n))

    for _ in range(0, n):
        part(doc)
        generat = next(gs)()
        if type(generat) == tuple:  # 'generat' serà <str> si l'ex. no porta solució, o <tuple> si sí que en porta
            text = generat[0]
            sols.append(generat[1])
        else:  # si no ve amb solució
            text = generat

        if mates:
            text = f"${text}$"
        if scale != 1:
            text = r"\scalebox{%s}{%s}" % (scale, text)

        doc.append(NoEscape(f"{text}"))
        space(doc, cm(espai_apartat)) if espai_apartat else None

    end(doc, 'multicols') if cols > 1 else None
    space(doc, cm(espai_final)) if espai_final else None
    end(doc, 'parts')
    if sols:
        if not es_spoiler or opcions["solulloc"] == "apart":
            if opcions["solulloc"] == "intercalat":
                blocsolucions(doc, sols, mates=mates_solus)
            else:
                tsols = textsolucions(sols, mates=mates_solus)
                return tsols  # retorna les solucions que posaria si faig llista de solucions al final
    return


# **************************** Complementàries ****************************** #
def quantes(opcions):
    if opcions["quantes"] != "tria":
        i = ["no", "poques", "normal", "moltes", "mitja", "plana", "doble"].index(opcions["quantes"])
        return qtats.quantitats_de(opcions["exnom"])[i]
    else:
        q = opcions["qtriada"]
        try:
            q = int(q)
            q = max(1, min(qtats.quantitats_de(opcions["exnom"])[-1], q))
        except:
            print("Has fet alguna cosa rara amb la quantitat triada...")
            q = 1
        return q


def quantilvar(var):
    """retorna el quantil on acaba la variable (per les opcions dels exercicis)"""
    try:
        v = ["no", "poques", "meitat", "moltes", "totes"].index(var)
    except:
        v = 2
    return v*100//4


def p_flex(p, pvar, nvar):
    """estira els quartils (de la llista de percentatges) per ajustar-los al % de variant que han demanat

    :param p: percentatges (quartils) ...pot incloure opcions [25, [50, {"max": 3}], 75, 100]
    :param pvar: percentatge de variant que han demanat
    :param nvar: posició (dins la llista g) de l'última funció abans del canvi de variant
    """
    # separo les opcions dels percentatges
    opcions = []
    for i, pi in enumerate(p):
        try:  # assumeixo que té opcions
            opcions.append(pi[1])
            p[i] = pi[0]
        except:  # no en tenia (entro un dict buit per poder tractar a tothom igual)
            opcions.append({})

    if p[-1] != 100:  # si ve sense l'últim (perquè se sobreentén) l'afegeixo.
        p.append(100)
    pre = p[:nvar+1]
    post = p[nvar+1:]
    frontera = pre[-1]
    pre = [round(q*pvar/frontera, 2) for q in pre]  # sense round(, 2) pots acabar amb parts tipus [1, 3, 3, 4, 5, 6, 6]
    post = [pvar + round((q-frontera)*(100-pvar)/(post[-1]-frontera), 2) for q in post]

    p = pre + post
    return [[pi, opcions[i]] for i, pi in enumerate(p)]  # recombino amb els dicts


def g_list(n, g, p):
    """Retorna un generador amb 'quina funció de g cal fer servir per cada apartat'

    :param n: quants apartats hi haurà
    :param g: llista de funcions que faré servir
    :param p: llista de quantils de les funcions (pot incloure opcions tipus: [25, [50, {max: 3}], 75, 100])
    """
    # preprocessing
    maxs = []
    for i, pi in enumerate(p):
        try:  # agafo les opcions  ...si és num (sense opcions) no podrà fer pi[1] i saltarà a baix
            maxs.append(pi[1].get("max", 100000))  # el get és per si hi ha opcions però no "max" dins les opcions
            p[i] = pi[0]  # deixo el num sol
        except:
            maxs.append(100000)  # random altíssim (és prou alt segur, pq l'abecedari capa a uns 600 apartats màxim)

    if len(p) + 1 == len(g) and p[-1] != 100:  # permeto no escriure l'últim 100
        p.append(100)
    if len(p) != len(g):  # si no quadra, malament
        for _ in range(n):
            yield lambda: "no em quadren els quantils"
    elif p[-1] != 100:
        p[-1] = 100

    # muntatge
    count = [0, 0]  # [apartat, quants]
    for x in range(n):  # per cada apartat de l'exercici
        for i in range(len(g)):  # comprova quina g li toca fer servir
            if (x+1)*1000 <= (p[i]*n)*10+1 or (x == 0 and p[0]):  # *1000 / *10+1 arregla problemes d'arrodoniment
                if i != count[0]:  # comença una nova g (reset comptador)
                    count = [i, 0]
                if count[1] < maxs[i]:  # encara puc fer servir aquesta g
                    yield g[i]
                    count[1] += 1
                    break
                else:  # ja tinc el màxim (baixo la p actual per forçar la g següent)
                    p[i] = 0

        else:  # si no break (si no li toca res, li toca l'últim)
            yield g[-1]


def espai_per(tal):
    espais = {
        "res": 0,  # enganxadots
        "interlineat": 4,  # separació normal mínima entre apartats
        "una": 10,  # una línia de resposta
    }
    return 42 if tal not in espais else espais[tal]


def cm(mm):
    return f"{mm // 10}.{mm % 10}cm"


def scale_per(tal):
    scales = {
        "fraccions": 1.3,
    }
    return scales.get(tal, 1)  # (torna "1" si no el troba)
