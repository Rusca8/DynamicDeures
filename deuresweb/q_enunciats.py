import random


def kelv(t, u="C"):
    """Retorna t en kelvin (donada en ºC)"""
    if u == "C" and t >= -273:
        return t + 273
    else:
        print("temperatura negativa")
        return 42.42


def cels(t, u="K"):
    """Retorna t en centígrad (donada en K)"""
    if u == "K" and t >= 0:
        return t - 273
    else:
        print("temperatura negativa")
        return 42.42


def pasc(p, u="atm"):
    """Retorna p en pascals (donada en atm... o mmHg)"""
    if u == "atm" and p >= 0:
        return p * 101325
    elif u == "mmHg" and p >= 0:
        return p * 101325/760
    else:
        print("pressió negativa")
        return -42.42


def atm(p, u="Pa"):
    """Retorna p en atmosferes (donada per en Pa... o mmHg)"""
    if u == "Pa" and p >= 0:
        return p / 101325
    elif u == "mmHg" and p >= 0:
        return p / 760
    else:
        print("pressió negativa")
        return -42.42


def mmhg(p, u="atm"):
    """Retorna p en milímetres de mercuri (donada per en atm... o Pa)"""
    if u == "atm" and p >= 0:
        return p * 760
    elif u == "Pa" and p >= 0:
        return p * 760/101325
    else:
        print("pressió negativa")
        return -42.42


def litres(v, u="m3"):
    """Retorna volum en litres (donat en m3)"""
    if u == "m3" and v >= 0:
        return v * 1000
    else:
        print("volum negatiu")
        return -43.42


def m3(v, u="l"):
    """Retorna volum en m3 (donat en litres)"""
    if u == "l" and v >= 0:
        return v / 1000
    else:
        print("volum negatiu")
        return -43.42


def t_text(t, u="K"):
    """Donada t en K, retorna en les unitats demanades i amb les unitats"""
    if u == "K":
        return f"{t} K"
    elif u == "C":
        return f"{cels(t)} ºC"
    else:
        return "EI NO TINC AQUESTES UNITATS"


def p_text(p, u="atm"):
    """Donada p en atm, retorna en les unitats demanades i amb les unitats"""
    if u == "atm":
        return f"{p} atm"
    elif u == "Pa":
        return f"{pasc(p, 'atm')} Pa"
    elif u == "mmHg":
        return f"{mmhg(p, 'atm')} mmHg"
    else:
        return "EI NO TINC AQUESTES UNITATS"


def v_text(v, u="l"):
    """Donada v en L, retorna en les unitats demanades i amb les unitats"""
    if u == "l":
        return f"{v} L"
    elif u == "m3":
        return f"{m3(v)} m3"
    else:
        return "EI NO TINC AQUESTES UNITATS"

def lleisgasos(tipus, p1=1, p2=1, v1=1, v2=1, t1=1, t2=1, cunit=True, sabemt=False, simples=True, si=False,
               solucions=False):
    """Retorna enunciat d'un problema de gasos ideals

    :param tipus: 1 t-ctt, 2 v-ctt, 3 p-ctt, 4 general n-ctt, 5 general
    :param p1: pressió inicial (atm... Pa)
    :param p2: pressió final (atm)
    :param v1: volum inicial (L)
    :param v2: volum final (L)
    :param t1: temperatura inicial (K)
    :param t2: temperatura final (K)
    :param cunit: permetre canvis d'unitats
    :param sabemt: evitar aïllar temperatures
    :param simples: pregunta directa (no pregunta variacions ni dóna múltiples)
    :param si: unitats venen en SI
    :param solucions: retornar solucions amb l'enunciat.
    :return: text de l'enunciat
    """

    text = "Gas 42"
    if si:
        p1, p2 = [atm(x) for x in [p1, p2]]
        v1, v2 = [litres(x) for x in [v1, v2]]

    if tipus in [1, 3]:
        pass
    if tipus == 4:
        pregunto = random.randint(1, 6)
        t_intro = "Tenim un gas"
        t_dades = " a"
        for i, x in enumerate(sorted([1, 2, 3])):
            if i == 0:
                pass
            elif i == 2 or (i == 1 and pregunto in [1, 2, 3]):
                t_dades += " i"
            elif i < 2 or (i < 1 and pregunto in [1, 2, 3]):
                t_dades += ","
            if x != pregunto:
                if x == 1:  # p
                    t_dades += f" una pressió de {p_text(p1, 'atm')}"
                elif x == 2:  # v
                    t_dades += f" un volum de {v_text(v1, 'l')}"
                else:  # t
                    t_dades += f" una temperatura de {t_text(t1, 'K')}"
        t_dades += "."
        t_pretext = " Si"
        for i, x in enumerate(sorted([4, 5, 6])):
            if i == 0:
                pass
            elif i == 2 or (i == 1 and pregunto in [4, 5, 6]):
                t_pretext += " i"
            elif i < 2 or (i < 1 and pregunto in [4, 5, 6]):
                t_pretext += ","
            if x != pregunto:
                if i == 2 and pregunto in [1, 2, 3]:
                    if x == 4:  # p2
                        t_pretext += " la pressió "
                if x == 4:  # p2
                    if p2 > p1:
                        t_pretext += " pugem"
                    else:
                        t_pretext += " baixem"
                    t_pretext += f" la pressió fins a {p_text(p2, 'atm')}"
                elif x == 5:  # v2
                    if v2 > v1:
                        t_pretext += " pugem"
                    else:
                        t_pretext += " baixem"
                    t_pretext += f" el volum fins a {v_text(v2, 'l')}"
                else:  # t2
                    if t2 > t1:
                        t_pretext += " pugem"
                    else:
                        t_pretext += " baixem"
                    t_pretext += f" la temperatura fins a {t_text(t2, 'K')}"
        t_pretext += "..."
        t_pregunta = ""







    return text