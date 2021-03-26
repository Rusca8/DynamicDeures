import math
import random

from generator import fracsimple
import q_enunciats as en


def moneda():
    return bool(random.getrandbits(1))


def lleisgasos(tipus, cunit=True, sabemt=False, simples=True, solucions=False):
    si = False  # donaré atm, L, K

    # randomitzo tot (ajusto a posteriori en funció de quina llei)
    p1, p2 = [0.1 * random.randint(2, 35) for _ in range(2)]  # 0.1-3.5 atm
    t1, t2 = [random.randint(280, 350) for _ in range(2)]  # 7-77 atm
    v1, v2 = [0.1 * random.randint(2, 35) for _ in range(2)]  # 0.1-3.5 L

    if tipus == 1:  # llei de boyle-mariotte (T-ctt)
        """
        P1*V1 = P2*V2
        """
        t2 = t1
        v2 = p1 * v1 / p2

    elif tipus == 2:  # llei de Gay-Lussac (V-ctt)
        """P1/T1 = P2/T2"""
        v2 = v1
        p2 = p1 * t2 / t1

    elif tipus == 3:  # llei de Charles (P-ctt)
        """V1/T1 = V2/T2"""
        p2 = p1
        v2 = v1 * t2 / t1

    elif tipus == 4:  # equació de Claperyon (n-ctt)
        """
        P1*V1   P2*V2
        ----- = -----     (atm, L, K)
          T1      T2
        """
        v2 = (p1 * v1 * t2) / (t1 * p2)

    elif tipus == 5:  # gasos ideals
        pass
    return f"P1 = {p1}, V1 = {v1}, T1 = {t1}. P2 = {p2}, V2 = {v2}, T2 = {t2}"
    # return en.lleisgasos(tipus, p1, p2, v1, v2, t1, t2, cunit, sabemt, simples, si, solucions)


# dades genèriques
romans = ["", "I", "II", "III", "IV", "V", "VI", "VII"]
iprefix = ["", "Mono", "Di", "Tri", "Tetra", "Penta", "Hexa", "Hepta", "Octa", "Nona", "Deca"]
diatomics = [1, 7, 8, 9, 17, 35, 53]


def ioprefix(z, qtat, estat=0, zp=0, qtatp=0):
    """Retorna l'ió amb el prefix segons la quantitat (p.ex. [S2]^[2-] = disulfur)

    :param z: n. atòmic de l'element
    :param qtat: quantitat d'àtoms de l'element
    :param estat: estat d'oxidació de l'element

    ...i per distingir si cal "mono" quan z és anió oxigen...
    :param zp: n. atòmic del catió en el compost
    :param qtatp: quantitat d'àtoms del catió en el compost

    PD: Considero que es diu "Monòxid" quan l'estequiometria és 1:1 i existeixen alternatives.
        (p.ex. FeO = Monòxid de Ferro, però BaO = Òxid de Bari)
    """
    if z == 8:  # oxigen, que és especialet
        if qtat == 1 and estat == -2:
            if qtatp == 1 and "vp" in elements[zp]:
                if len(elements[zp]["vp"]) > 1:
                    return "Monòxid"
        elif qtat == 2 and estat == -1:
            return "Peròxid"
    # si no és cap cas especial (no porta elif, que ja hi ha returns)
    if qtat == 1:
        if estat < 0:
            if "nneg" in elements[z]:
                return f"{elements[z]['nneg']}"
            else:
                return "NO NNEG"
        else:
            return f"{elements[z]['nom']}"
    elif estat < 0:
        if "nneg" in elements[z]:
            return iprefix[qtat] + f"{elements[z]['nneg']}".lower()
        else:
            return iprefix[qtat] + "NO NNEG"
    return iprefix[qtat] + f"{elements[z]['nom']}".lower()


def dde(z, qtat=0):
    if (z in [1, 8, 13, 33, 38, 47, 50, 51, 79]  # TODO faltaria veure si algun dels extra sense valència tenen
            and not (qtat not in [0, 1, 6, 7])  # només si és hex, hept o res (el "mono" només el porta l'oxigen)
            and not (z == 8 and qtat == 1)):  # de monooxigen (?)
        return " d'"
    else:
        return " de "


# stats extrets
els_v = [1, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 19, 20, 24, 25, 26, 27, 28, 29, 30, 33, 34, 35, 37, 38, 42,
         47, 48, 50, 51, 52, 53, 55, 56, 78, 79, 80, 82, 83, 87, 88]
els_vp = [1, 3, 4, 5, 6, 7, 11, 12, 13, 14, 15, 16, 17, 19, 20, 24, 25, 26, 27, 28, 29, 30, 33, 34, 35, 37, 38, 42, 47,
          48, 50, 51, 52, 53, 55, 56, 78, 79, 80, 82, 83, 87, 88]
els_vn = [1, 6, 7, 8, 9, 14, 15, 16, 17, 33, 34, 35, 51, 52, 53]
els_ve = [7, 8]
els_nneg = [1, 7, 8, 9, 15, 16, 17, 33, 34, 35, 51, 52, 53]
# llista
elements = [
    # [Símbol, Nom Element, {
    #                        nneg: nom ió negatiu,
    #                        mm: massa molar,
    #                        ist: isòtops,
    #                        vp: valències positives,
    #                        vn: valència negativa,
    #                        ve: valències extra (excepcions)
    #                        ime: ió més estable
    #                        }]
    {"sym": "X", "nom": "Element",
     },
    # 1
    {"sym": "H", "nom": "Hidrogen",
     "nneg": "Hidrur",
     "vp": [1],
     "vn": [-1],
     "ime": 1,
     "oen": 11,
     },
    {"sym": "He", "nom": "Heli",
     },
    {"sym": "Li", "nom": "Liti",
     "vp": [1],
     "ime": 1,
     "oen": 100,
     },
    {"sym": "Be", "nom": r"Beri\lgem i",
     "vp": [2],
     "ime": 2,
     "oen": 94,
     },
    {"sym": "B", "nom": "Bor",
     "vp": [3],
     "ime": 3,
     "oen": 22,
     },
    {"sym": "C", "nom": "Carboni",
     "nneg": "Carbur",
     "vp": [2, 4],
     "vn": [-4],
     "oen": 17,
     },
    {"sym": "N", "nom": "Nitrogen",
     "nneg": "Nitrur",
     "vp": [1, 3, 5],
     "vn": [-3],
     "ve": [2, 4],
     "ime": -3,
     "oen": 12,
     },
    {"sym": "O", "nom": "Oxigen",
     "nneg": "Òxid",
     "vn": [-2],
     "ve": [-1],
     "ime": -2,
     "oen": 6,
     },
    {"sym": "F", "nom": "Fluor",
     "nneg": "Fluorur",
     "vn": [-1],
     "ime": -1,
     "oen": 1,
     },
    # 10
    {"sym": "Ne", "nom": "Neó",
     },
    {"sym": "Na", "nom": "Sodi",
     "vp": [1],
     "ime": 1,
     "oen": 101,
     },
    {"sym": "Mg", "nom": "Magnesi",
     "vp": [2],
     "ime": 2,
     "oen": 95,
     },
    {"sym": "Al", "nom": "Alumini",
     "vp": [3],
     "ime": 3,
     "oen": 23,
     },
    {"sym": "Si", "nom": "Silici",
     "nneg": "Silicur",
     "vp": [4],
     "vn": [-4],
     "oen": 18,
     },
    {"sym": "P", "nom": "Fòsfor",
     "nneg": "Fosfur",
     "vp": [3, 5],
     "vn": [-3],
     "ime": -3,
     "oen": 13,
     },
    {"sym": "S", "nom": "Sofre",
     "nneg": "Sulfur",
     "vp": [4, 6],
     "vn": [-2],
     "ime": -2,
     "oen": 7,
     },
    {"sym": "Cl", "nom": "Clor",
     "nneg": "Clorur",
     "vp": [1, 3, 5, 7],
     "vn": [-1],
     "ime": -1,
     "oen": 2,
     },
    {"sym": "Ar", "nom": "Argó",
     },
    {"sym": "K", "nom": "Potassi",
     "vp": [1],
     "ime": 1,
     "oen": 102,
     },
    # 20
    {"sym": "Ca", "nom": "Calci",
     "vp": [2],
     "ime": 2,
     "oen": 96,
     },
    {"sym": "Sc", "nom": "Escandi",
     "oen": 62,
     },
    {"sym": "Ti", "nom": "Titani",
     "oen": 58,
     },
    {"sym": "V", "nom": "Vanadi",
     "oen": 54,
     },
    {"sym": "Cr", "nom": "Crom",
     "vp": [2, 3, 6],
     "oen": 50,
     },
    {"sym": "Mn", "nom": "Manganès",
     "vp": [2, 3, 4, 6, 7],
     "oen": 46,
     },
    {"sym": "Fe", "nom": "Ferro",
     "vp": [2, 3],
     "oen": 42,
     },
    {"sym": "Co", "nom": "Cobalt",
     "vp": [2, 3],
     "oen": 38,
     },
    {"sym": "Ni", "nom": "Níquel",
     "vp": [2, 3],
     "oen": 34,
     },
    {"sym": "Cu", "nom": "Coure",
     "vp": [1, 2],
     "oen": 30,
     },
    # 30
    {"sym": "Zn", "nom": "Zinc",
     "vp": [2],
     "ime": 2,
     "oen": 27,
     },
    {"sym": "Ga", "nom": r"Ga\lgem i",
     "oen": 24,
     },
    {"sym": "Ge", "nom": "Germani",
     "oen": 19,
     },
    {"sym": "As", "nom": "Arsènic",
     "nneg": "Arsenur",
     "vp": [3, 5],
     "vn": [-3],
     "oen": 14,
     },
    {"sym": "Se", "nom": "Seleni",
     "nneg": "Selenur",
     "vp": [4, 6],
     "vn": [-2],
     "ime": -2,
     "oen": 8,
     },
    {"sym": "Br", "nom": "Brom",
     "nneg": "Bromur",
     "vp": [1, 3, 5, 7],
     "vn": [-1],
     "ime": -1,
     "oen": 3,
     },
    {"sym": "Kr", "nom": "Criptó",
     },
    {"sym": "Rb", "nom": "Rubidi",
     "vp": [1],
     "ime": 1,
     "oen": 103,
     },
    {"sym": "Sr", "nom": "Estronci",
     "vp": [2],
     "ime": 2,
     "oen": 97,
     },
    {"sym": "Y", "nom": "Itri",
     "oen": 63,
     },
    # 40
    {"sym": "Zr", "nom": "Zirconi",
     "oen": 59,
     },
    {"sym": "Nb", "nom": "Niobi",
     "oen": 55,
     },
    {"sym": "Mo", "nom": "Molibdè",
     "vp": [6],
     "oen": 51,
     },
    {"sym": "Tc", "nom": "Tecneci",
     "oen": 47,
     },
    {"sym": "Ru", "nom": "Ruteni",
     "oen": 43,
     },
    {"sym": "Rh", "nom": "Rodi",
     "oen": 39,
     },
    {"sym": "Pd", "nom": "Paladi",
     "oen": 35,
     },
    {"sym": "Ag", "nom": "Argent",
     "vp": [1],
     "oen": 31,
     },
    {"sym": "Cd", "nom": "Cadmi",
     "vp": [2],
     "oen": 28,
     },
    {"sym": "In", "nom": "Indi",
     "oen": 25,
     },
    # 50
    {"sym": "Sn", "nom": "Estany",
     "vp": [2, 4],
     "oen": 20,
     },
    {"sym": "Sb", "nom": "Antimoni",
     "nneg": "Antimonur",
     "vp": [3, 5],
     "vn": [-3],
     "ime": -3,
     "oen": 15,
     },
    {"sym": "Te", "nom": r"Te\lgem uri",
     "nneg": r"Te\lgem urur",
     "vp": [4, 6],
     "vn": [-2],
     "ime": -2,
     "oen": 9,
     },
    {"sym": "I", "nom": "Iode",
     "nneg": "Iodur",
     "vp": [1, 3, 5, 7],
     "vn": [-1],
     "ime": -1,
     "oen": 4,
     },
    {"sym": "Xe", "nom": "Xenó",
     },
    {"sym": "Cs", "nom": "Cesi",
     "vp": [1],
     "ime": 1,
     "oen": 114,
     },
    {"sym": "Ba", "nom": "Bari",
     "vp": [2],
     "ime": 2,
     "oen": 98,
     },
    {"sym": "La", "nom": "Lantani",
     "oen": 64,
     },
    {"sym": "Ce", "nom": "Ceri",
     "oen": 65,
     },
    {"sym": "Pr", "nom": "Praseodimi",
     "oen": 66,
     },
    # 60
    {"sym": "Ne", "nom": "Neodimi",
     "oen": 67,
     },
    {"sym": "Pm", "nom": "Prometi",
     "oen": 68,
     },
    {"sym": "Sm", "nom": "Samari",
     "oen": 69,
     },
    {"sym": "Eu", "nom": "Europi",
     "oen": 70,
     },
    {"sym": "Gd", "nom": "Gadolini",
     "oen": 71,
     },
    {"sym": "Tb", "nom": "Terbi",
     "oen": 72,
     },
    {"sym": "Di", "nom": "Disprosi",
     "oen": 73,
     },
    {"sym": "Ho", "nom": "Holmi",
     "oen": 74,
     },
    {"sym": "Er", "nom": "Erbi",
     "oen": 75,
     },
    {"sym": "Tm", "nom": "Tuli",
     "oen": 76,
     },
    # 70
    {"sym": "Yb", "nom": "Iterbi",
     "oen": 77,
     },
    {"sym": "Lu", "nom": "Luteci",
     "oen": 78,
     },
    {"sym": "Hf", "nom": "Hafni",
     "oen": 60,
     },
    {"sym": "Ta", "nom": "Tàntal",
     "oen": 56,
     },
    {"sym": "W", "nom": "Tungstè",
     "oen": 52,
     },
    {"sym": "Re", "nom": "Reni",
     "oen": 48,
     },
    {"sym": "Os", "nom": "Osmi",
     "oen": 44,
     },
    {"sym": "Ir", "nom": "Iridi",
     "oen": 40,
     },
    {"sym": "Pt", "nom": "Platí",
     "vp": [2, 4],
     "oen": 36,
     },
    {"sym": "Au", "nom": "Or",
     "vp": [1, 3],
     "oen": 32,
     },
    # 80
    {"sym": "Hg", "nom": "Mercuri",
     "vp": [1, 2],
     "oen": 29,
     },
    {"sym": "Tl", "nom": "Tali",
     "oen": 26,
     },
    {"sym": "Pb", "nom": "Plom",
     "vp": [2, 4],
     "oen": 21,
     },
    {"sym": "Bi", "nom": "Bismut",
     "vp": [3, 5],
     "oen": 16,
     },
    {"sym": "Po", "nom": "Poloni",
     "oen": 10,
     },
    {"sym": "At", "nom": "Àstat",
     "oen": 5,
     },
    {"sym": "Rn", "nom": "Radó",
     },
    {"sym": "Fr", "nom": "Franci",
     "vp": [1],
     "ime": 1,
     "oen": 115,
     },
    {"sym": "Ra", "nom": "Radi",
     "vp": [2],
     "ime": 2,
     "oen": 99,
     },
    {"sym": "Ac", "nom": "Actini",
     "oen": 79,
     },
    # 90
    {"sym": "Th", "nom": "Tori",
     "oen": 80,
     },
    {"sym": "Pa", "nom": "Protoactini",
     "oen": 81,
     },
    {"sym": "U", "nom": "Urani",
     "oen": 82,
     },
    {"sym": "Np", "nom": "Neptuni",
     "oen": 83,
     },
    {"sym": "Pu", "nom": "Plutoni",
     "oen": 84,
     },
    {"sym": "Am", "nom": "Americi",
     "oen": 85,
     },
    {"sym": "Cm", "nom": "Curi",
     "oen": 86,
     },
    {"sym": "Bk", "nom": "Berkeli",
     "oen": 87,
     },
    {"sym": "Cf", "nom": "Californi",
     "oen": 88,
     },
    {"sym": "Es", "nom": "Einsteni",
     "oen": 89,
     },
    # 100
    {"sym": "Fm", "nom": "Fermi",
     "oen": 90,
     },
    {"sym": "Md", "nom": "Mendelevi",
     "oen": 91,
     },
    {"sym": "No", "nom": "Nobeli",
     "oen": 92,
     },
    {"sym": "Lr", "nom": "Laurenci",
     "oen": 93,
     },
    {"sym": "Rf", "nom": "Rutherfordi",
     "oen": 61,
     },
    {"sym": "Db", "nom": "Dubni",
     "oen": 57,
     },
    {"sym": "Sg", "nom": "Seaborgi",
     "oen": 53,
     },
    {"sym": "Bh", "nom": "Bohri",
     "oen": 49,
     },
    {"sym": "Hs", "nom": "Hassi",
     "oen": 45,
     },
    {"sym": "Mt", "nom": "Meitneri",
     "oen": 41,
     },
    # 110
    {"sym": "Ds", "nom": "Darmstadti",
     "oen": 37,
     },
    {"sym": "Rg", "nom": "Roentgeni",
     "oen": 33,
     },
    {"sym": "Cn", "nom": "Copernici",
     },
    {"sym": "Nh", "nom": "Nihoni",
     },
    {"sym": "Fl", "nom": "Flerovi",
     },
    {"sym": "Mc", "nom": "Moscovi",
     },
    {"sym": "Lv", "nom": "Livermori",
     },
    {"sym": "Ts", "nom": "Tennes",
     },
    {"sym": "Og", "nom": "Oganessó"
     },
    {"sym": "OH", "nom": "Hidròxid",  # afegeixo l'hidròxid aquí al 119 perquè és més fàcil així
     "vn": [-1],
     "nneg": "Hidròxid",
     "oen": -1
    }
]

# amb elements només dic "mono" si són diatòmics. Amb binaris només òxids 1:1 ambigus.
# fosfina, arsina i estibina ja no estan acceptats IUPAC


def elemstats():
    """funció que faig servir per actualitzar les llistes"""
    vp = []
    vn = []
    ve = []
    v = []
    nneg = []
    for x in range(1, 119):  # de l'1 al 118
        if "vp" in elements[x]:
            vp.append(x)
        if "vn" in elements[x]:
            vn.append(x)
        if "ve" in elements[x]:
            ve.append(x)
        if "nneg" in elements[x]:
            nneg.append(x)
        if any([v in ["vp", "vn"] for v in elements[x]]):
            v.append(x)
    print(f"els_v = {v}")
    print(f"els_vp = {vp}")
    print(f"els_vn = {vn}")
    print(f"els_ve = {ve}")
    print(f"els_nneg = {nneg}")


def estatexp(estat):
    if estat == 0:
        exp = ""
    elif estat == 1:
        exp = "+"
    elif estat == -1:
        exp = "-"
    elif estat > 0:
        exp = f"{estat}+"
    else:
        exp = f"{abs(estat)}-"
    return exp


def symio(z, estat):
    exp = estatexp(estat)
    return r"$\isotope{" + elements[z]["sym"] + "}^{" + exp + "}$"


def nomio(z, estat, textio=False, nomaj=False):
    if estat > 0:
        if len(elements[z]["vp"]) > 1:
            stock = f" ({romans[estat]})"
        else:
            stock = ""
        if textio:
            nom = "Ió " + elements[z]["nom"] + stock
        else:
            if nomaj:
                nom = elements[z]["nom"].lower() + stock
            else:
                nom = elements[z]["nom"] + stock
    elif estat < 0:
        if "nneg" in elements[z]:
            if textio:
                nom = "Ió " + elements[z]["nneg"]
            else:
                nom = elements[z]["nneg"]
                if nomaj:
                    nom = nom.lower()
        else:
            if textio:
                nom = "(Anió " + elements[z]["nom"] + ")"
            else:
                nom = "(" + elements[z]["nom"] + ")"
    else:
        nom = elements[z]["nom"]
    return nom


def nomsistem(elems=[], estats=[2, -2]):
    try:  # asseguro que és una llista d'elements també quan només és un element
        len(elems[0])
    except:
        elems = [elems]
    if len(elems) == 1:  # monoelemental
        if elems[0][1] == 1 and not elems[0][0] in diatomics:  # qtat == 1 i no diatòmic
            nom = elements[elems[0][0]]["nom"]
        else:
            nom = iprefix[elems[0][1]] + f"{elements[elems[0][0]]['nom']}".lower()

    elif len(elems) == 2:  # compost binari
        # els "mono" ens els estalviem excepte amb els òxids 1:1 ambigus
        nomp = ioprefix(elems[0][0], elems[0][1], estats[0])
        nomn = ioprefix(elems[1][0], elems[1][1], estats[1], elems[0][0], elems[0][1])
        print(nomn, elems)
        nom = nomn + dde(elems[0][0], elems[0][1]) + nomp.lower()
    else:
        return "No faig tan grans encara"
    return nom


def molec(elems=[], charge=0):
    """construeix molècula amb llista d'elements [z, qtat] i la càrrega total"""
    try:  # comprovo que dins la llista hi ha llistes (que és una llista d'elements i no un sol element)
        len(elems[0])
    except:  # si només era un, el converteixo en llista
        elems = [elems]
    charge = estatexp(charge)
    text = []
    for el in elems:
        if el[1] == 1:
            qtat = ""
        else:
            qtat = f"{el[1]}"
        sym = elements[el[0]]["sym"]
        if el[0] == 119 and el[1] > 1:  # hidròxid parentesiat
            sym = f"({sym})"
        text.append(r"\isotope{" + sym + "}_{" + qtat + "}")
    return "$" + "".join(text) + "^{" + charge + "}$"


def nommolec(elems=[], valens=[], nomencs=[1, 2, 3]):
    """Anomena el compost a partir de llista d'elements i estats.

    :param elems: llista d'elements de la molècula [[elem, qtat], [elem, qtat]]
    :param valens: llista de valències dels elements anteriors
    :param nomencs: llista de nomenclatures a extreure (1 stock, 2 sistem, 3 comú)
    """
    try:  # comprovo que dins la llista hi ha llistes (que és una llista d'elements i no un sol element)
        len(elems[0])
    except:  # si només era un, el converteixo en llista
        elems = [elems]
    if len(elems) != 2:
        return "De moment fa binaris"
    # muntatge stock
    stock = "-"
    if 1 in nomencs:
        stock = nomio(elems[1][0], valens[1]) + dde(elems[0][0]) + nomio(elems[0][0], valens[0], nomaj=True)
    # muntatge sistem
    sistem = "-"
    if 2 in nomencs:
        sistem = nomsistem(elems, valens)
    # llista comuns
    comu = "-"
    if 3 in nomencs:
        if elems == [[1, 2], [8, 1]]:
            comu = "Aigua"
        elif elems == [[7, 1], [1, 3]]:
            comu = "Amoníac"
        elif elems == [[6, 1], [1, 4]]:
            comu = "Metà"
        elif elems == [[11, 1], [17, 1]]:
            comu = "Sal Comuna"
    noms = []
    for n in nomencs:
        if n == 1:
            noms.append(stock)
        elif n == 2:
            noms.append(sistem)
        elif n == 3:
            noms.append(comu)
        else:
            noms.append("?")
    print(noms)
    return noms


def finorg(tipus, nivell=1, descn=[6, 14]):
    """Treu exercicis de formulació inorgànica

    :param tipus: 1 ions/diat, 10 molèc
    :param nivell: dificultat interna del tipus
    :param descn: descartats negatius (evito "carbur i silicur")
    """
    fila = []
    if tipus == 1:  # ions, diatòmics i ozó
        if not random.randint(0, 20):  # ozó (i/o si se m'acudeix algun altre així friqui)
            fila = [molec([8, 3]), "-", "Trioxigen", "Ozó"]
            fila[random.choice([0, 2, 3])] = ""
        elif not random.randint(0, 3):  # diatòmic
            z = random.choice(diatomics)
            fila = [molec([z, 2]), "-", iprefix[2] + f"{elements[z]['nom']}".lower(), elements[z]['nom']]
            # buidat
            fila[random.choice([0, 2, 3])] = ""
        else:  # ió normal
            stock = ""
            if moneda():  # positiu
                z = random.choice(els_vp)
                estat = random.choice(elements[z]["vp"])
            else:  # negatiu (ur)
                z = random.choice(els_nneg)
                estat = random.choice(elements[z]["vn"])
            fila = [symio(z, estat), nomio(z, estat, True), "-", "-"]
            # buidat
            fila[random.choice([0, 1])] = ""
    elif tipus == 10:  # molècules
        # TODO random molèc comuns (com ozó al cas anterior)
        # tria
        if nivell == 1:  # binaris hidrogen (hidrur, però canviarà si agafa halògens, crec)
            zn = 1
        elif nivell == 2:  # òxids
            zn = 8
        elif nivell == 4:  # hidròxids
            zn = 119
        else:
            zn = random.choice([z for z in els_vn if z not in descn])

        if nivell == 1 and not random.randint(0, 4):
            zp = random.choice([z for z in els_vn if z != zn and z in els_vp])  # elementurs d'hidrogen
        elif nivell == 4:  # hidròxids (evito els que tenen negativa)
            zp = random.choice([z for z in els_vp if z != zn and z not in els_vn])
        else:
            zp = random.choice([z for z in els_vp if z != zn])
        # ordre segons iupac
        if all([all([x in l for x in ["vn", "vp", "oen"]]) for l in [elements[zn], elements[zp]]]):  # els dos tenen tot
            if elements[zn]["oen"] > elements[zp]["oen"]:
                zn, zp = zp, zn
        # estats d'oxidació
        vp = random.choice(elements[zp]["vp"])
        vn = random.choice(elements[zn]["vn"])
        # càlcul quantitats
        qtatp = abs(vn)
        qtatn = vp
        qtatp, qtatn = fracsimple(qtatp, qtatn)
        # muntatge (molec | stock | sistem | comú)
        m = [[zp, qtatp], [zn, qtatn]]
        noms = nommolec(m, [vp, vn])
        fila = [molec(m)] + noms
        # buidat
        if fila[3] == "-":
            deixo = random.randint(0, 2)
        else:
            deixo = random.randint(0, 3)
        fila = [c if i == deixo or c == "-" else " " for i, c in enumerate(fila)]  # esborro tots menys el que deixo
    return fila


for _ in range(6):
    print(lleisgasos(4))
