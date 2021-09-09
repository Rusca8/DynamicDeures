"""
MÒDULS PER GENERAR EL LaTeX DELS DIFERENTS EXERCICIS

latexator.py agafarà d'aquí els exercicis a partir del nom d'exercici
"""
import random

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
    return exercici_no_trobat if nom not in exercicis else exercicis[nom]


def px_algeb_factoritza(doc, opcions):
    return exercici_no_trobat(doc, opcions)


def px_algeb_simplifica(doc, opcions):
    return exercici_no_trobat(doc, opcions)


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

    def f():
        sol = en.factorcomu()
        text = r"\ \ \penalty-200".join([f" ${x}$ " for x in crypt.fc_frase(sol)])
        sol = f"{sol}."
        return text, sol
    tsols = crea_exercici(doc, opcions,
                          f,
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
    var = quantilvar(opcions["var"]["una_variable"])
    p = p_flex([25, 50, 75, 100], var, 1)

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
    return exercici_no_trobat(doc, opcions)


def px_ops_divideix(doc, opcions):
    return exercici_no_trobat(doc, opcions)


def px_ops_divideixruffini(doc, opcions):
    return exercici_no_trobat(doc, opcions)


def px_ops_multiplica(doc, opcions):
    return exercici_no_trobat(doc, opcions)


def px_ops_parametreresidu(doc, opcions):
    return exercici_no_trobat(doc, opcions)


def px_ops_resta(doc, opcions):
    return exercici_no_trobat(doc, opcions)


def px_ops_suma(doc, opcions):
    return exercici_no_trobat(doc, opcions)


def px_ops_teoremaresidu(doc, opcions):
    return exercici_no_trobat(doc, opcions)


# ******************************* Esquelets ********************************* #
def crea_exercici(doc, opcions, g, p="", enunciat="EM FALTA L'ENUNCIAT, NEN", cols=1,
                  espai_apartat=4, espai_final=0, mates=True, mates_solus=False, es_spoiler=False):
    """Munta un exercici LaTeX (exercici sense varietat interna) a partir de les seves dades.

    :param doc: document on posarem l'exercici
    :param opcions: opcions que ens passa el formulari de l'exercici
    :param g: funcions generadores (lambdes passades des de fora)
    :param p: quantils on vull que s'acabi cada funció generadora
    :param enunciat: l'enunciat que vols
    :param cols: quantitat de columnes que tindrà l'exercici
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
        gs = [g for _ in range(n)]

    for x in range(0, n):
        part(doc)
        generat = gs[x]()
        if type(generat) == tuple:  # 'generat' serà <str> si l'ex. no porta solució, o <tuple> si sí que en porta
            text = generat[0]
            sols.append(generat[1])
        else:  # si no ve amb solució
            text = generat

        if mates:
            text = f"${text}$"
        doc.append(NoEscape(r"%s" % text))
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


# ----------------------------------------------------------------------------------------- #
def exercici_no_trobat(doc, opcions):
    needspace(doc, 8)
    question(doc, "42")
    doc.append("No s'ha trobat cap constructor per l'exercici " + opcions["exnom"].upper())
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

    :param p: percentatges (quartils)
    :param pvar: percentatge de variant que han demanat
    :param nvar: posició (dins la llista g) de l'última funció abans del canvi de variant
    """
    pre = p[:nvar+1]
    post = p[nvar+1:]
    frontera = pre[-1]
    pre = [q*pvar//frontera for q in pre]
    post = [pvar + (q-frontera)*(100-pvar)//(post[-1]-frontera) for q in post]
    return pre + post


def g_list(n, g, p):  # TODO passar a generador?
    """Retorna una llista amb 'quina funció de g cal fer servir per cada apartat'

    :param n: quants apartats hi haurà
    :param g: llista de funcions que faré servir
    :param p: llista de quantils de les funcions
    """
    if len(p) + 1 == len(g) and p[-1] != 100:  # permeto no escriure l'últim 100
        p.append(100)
    if len(p) != len(g):  # si no quadra, malament
        return [lambda: "no em quadren els quantils" for _ in range(n)]
    elif p[-1] != 100:
        p[-1] = 100

    llista = []
    for x in range(n):
        for i in range(len(g)):
            if x+1 <= p[i]*n//100 or (x == 0 and p[0]):
                llista.append(g[i])
                break

    if len(llista) != n:  # si falten, omplo amb els més difícils
        print("Compte que no has fet bé la llista de gs")
        while len(llista) < n:
            llista.append(g[-1])

    return llista


def espai_per(tal):
    espais = {
        "res": 0,  # enganxadots
        "interlineat": 4,  # separació normal mínima entre apartats
        "una": 10,  # una línia de resposta
    }
    return 42 if tal not in espais else espais[tal]


def cm(mm):
    return f"{mm // 10}.{mm % 10}cm"
