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
els_ist = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
           30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57,
           58, 59, 60, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 90]
els_v = [1, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 19, 20, 24, 25, 26, 27, 28, 29, 30, 33, 34, 35, 37, 38, 42,
         47, 48, 50, 51, 52, 53, 55, 56, 78, 79, 80, 82, 83, 87, 88]
els_vp = [1, 3, 4, 5, 6, 7, 11, 12, 13, 14, 15, 16, 17, 19, 20, 24, 25, 26, 27, 28, 29, 30, 33, 34, 35, 37, 38, 42, 47,
          48, 50, 51, 52, 53, 55, 56, 78, 79, 80, 82, 83, 87, 88]
els_vn = [1, 6, 7, 8, 9, 14, 15, 16, 17, 33, 34, 35, 51, 52, 53]
els_ve = [7, 8]
els_nneg = [1, 6, 7, 8, 9, 14, 15, 16, 17, 33, 34, 35, 51, 52, 53]
# llista
elements = [
    # [Símbol, Nom Element, {
    #                        nneg: nom ió negatiu,
    #                        mm: massa molar,
    #                        ist: isòtops estables,
    #                        vp: valències positives,
    #                        vn: valència negativa,
    #                        ve: valències extra (excepcions),
    #                        ime: ió més estable, (font: periodictable.com)
    #                        oen: ordre electro-negativitat (IUPAC) :: El més petit va a la dreta en binaris.
    #                        }]
    {"sym": "X", "nom": "Element",
     },
    # 1
    {"sym": "H", "nom": "Hidrogen",
     "nneg": "Hidrur",
     "ist": [1, 2],
     "vp": [1],
     "vn": [-1],
     "ime": 1,
     "oen": 11,
     },
    {"sym": "He", "nom": "Heli",
     "ist": [3, 4],
     },
    {"sym": "Li", "nom": "Liti",
     "ist": [6, 7],
     "vp": [1],
     "ime": 1,
     "oen": 100,
     },
    {"sym": "Be", "nom": r"Beri\lgem i",
     "ist": [9],
     "vp": [2],
     "ime": 2,
     "oen": 94,
     },
    {"sym": "B", "nom": "Bor",
     "ist": [10, 11],
     "vp": [3],
     "ime": 3,
     "oen": 22,
     },
    {"sym": "C", "nom": "Carboni",
     "nneg": "Carbur",
     "ist": [12, 13],
     "vp": [2, 4],
     "vn": [-4],
     "oen": 17,
     },
    {"sym": "N", "nom": "Nitrogen",
     "nneg": "Nitrur",
     "ist": [14, 15],
     "vp": [1, 3, 5],
     "vn": [-3],
     "ve": [2, 4],
     "ime": -3,
     "oen": 12,
     },
    {"sym": "O", "nom": "Oxigen",
     "nneg": "Òxid",
     "ist": [16, 17, 18],
     "vn": [-2],
     "ve": [-1],
     "ime": -2,
     "oen": 6,
     },
    {"sym": "F", "nom": "Fluor",
     "nneg": "Fluorur",
     "ist": [19],
     "vn": [-1],
     "ime": -1,
     "oen": 1,
     },
    # 10
    {"sym": "Ne", "nom": "Neó",
     "ist": [20, 21, 22],
     },
    {"sym": "Na", "nom": "Sodi",
     "ist": [23],
     "vp": [1],
     "ime": 1,
     "oen": 101,
     },
    {"sym": "Mg", "nom": "Magnesi",
     "ist": [24, 25, 26],
     "vp": [2],
     "ime": 2,
     "oen": 95,
     },
    {"sym": "Al", "nom": "Alumini",
     "ist": [27],
     "vp": [3],
     "ime": 3,
     "oen": 23,
     },
    {"sym": "Si", "nom": "Silici",
     "nneg": "Silicur",
     "ist": [28, 29, 30],
     "vp": [4],
     "vn": [-4],
     "oen": 18,
     },
    {"sym": "P", "nom": "Fòsfor",
     "nneg": "Fosfur",
     "ist": [31],
     "vp": [3, 5],
     "vn": [-3],
     "ime": -3,
     "oen": 13,
     },
    {"sym": "S", "nom": "Sofre",
     "nneg": "Sulfur",
     "ist": [32, 33, 34, 36],
     "vp": [4, 6],
     "vn": [-2],
     "ime": -2,
     "oen": 7,
     },
    {"sym": "Cl", "nom": "Clor",
     "nneg": "Clorur",
     "ist": [35, 37],
     "vp": [1, 3, 5, 7],
     "vn": [-1],
     "ime": -1,
     "oen": 2,
     },
    {"sym": "Ar", "nom": "Argó",
     "ist": [36, 38, 40],
     },
    {"sym": "K", "nom": "Potassi",
     "ist": [39, 41],
     "vp": [1],
     "ime": 1,
     "oen": 102,
     },
    # 20
    {"sym": "Ca", "nom": "Calci",
     "ist": [40, 42, 43, 44, 46],
     "vp": [2],
     "ime": 2,
     "oen": 96,
     },
    {"sym": "Sc", "nom": "Escandi",
     "ist": [45],
     "oen": 62,
     },
    {"sym": "Ti", "nom": "Titani",
     "ist": [46, 47, 48, 49, 50],
     "oen": 58,
     },
    {"sym": "V", "nom": "Vanadi",
     "ist": [51],
     "oen": 54,
     },
    {"sym": "Cr", "nom": "Crom",
     "ist": [50, 52, 53, 54],
     "vp": [2, 3, 6],
     "oen": 50,
     },
    {"sym": "Mn", "nom": "Manganès",
     "ist": [55],
     "vp": [2, 3, 4, 6, 7],
     "oen": 46,
     },
    {"sym": "Fe", "nom": "Ferro",
     "ist": [54, 56, 57, 58],
     "vp": [2, 3],
     "oen": 42,
     },
    {"sym": "Co", "nom": "Cobalt",
     "ist": [59],
     "vp": [2, 3],
     "oen": 38,
     },
    {"sym": "Ni", "nom": "Níquel",
     "ist": [58, 60, 61, 62, 64],
     "vp": [2, 3],
     "oen": 34,
     },
    {"sym": "Cu", "nom": "Coure",
     "ist": [63, 65],
     "vp": [1, 2],
     "oen": 30,
     },
    # 30
    {"sym": "Zn", "nom": "Zinc",
     "ist": [64, 66, 67, 68, 70],
     "vp": [2],
     "ime": 2,
     "oen": 27,
     },
    {"sym": "Ga", "nom": r"Ga\lgem i",
     "ist": [69, 71],
     "oen": 24,
     },
    {"sym": "Ge", "nom": "Germani",
     "ist": [70, 72, 73, 74],
     "oen": 19,
     },
    {"sym": "As", "nom": "Arsènic",
     "nneg": "Arsenur",
     "ist": [75],
     "vp": [3, 5],
     "vn": [-3],
     "oen": 14,
     },
    {"sym": "Se", "nom": "Seleni",
     "nneg": "Selenur",
     "ist": [74, 76, 77, 78, 80],
     "vp": [4, 6],
     "vn": [-2],
     "ime": -2,
     "oen": 8,
     },
    {"sym": "Br", "nom": "Brom",
     "nneg": "Bromur",
     "ist": [79, 81],
     "vp": [1, 3, 5, 7],
     "vn": [-1],
     "ime": -1,
     "oen": 3,
     },
    {"sym": "Kr", "nom": "Criptó",
     "ist": [78, 80, 82, 83, 84, 86],
     },
    {"sym": "Rb", "nom": "Rubidi",
     "ist": [85],
     "vp": [1],
     "ime": 1,
     "oen": 103,
     },
    {"sym": "Sr", "nom": "Estronci",
     "ist": [84, 86, 87, 88],
     "vp": [2],
     "ime": 2,
     "oen": 97,
     },
    {"sym": "Y", "nom": "Itri",
     "ist": [89],
     "oen": 63,
     },
    # 40
    {"sym": "Zr", "nom": "Zirconi",
     "ist": [90, 91, 92, 94],
     "oen": 59,
     },
    {"sym": "Nb", "nom": "Niobi",
     "ist": [93],
     "oen": 55,
     },
    {"sym": "Mo", "nom": "Molibdè",
     "ist": [92, 94, 95, 96, 97, 98],
     "vp": [6],
     "oen": 51,
     },
    {"sym": "Tc", "nom": "Tecneci",
     "oen": 47,
     },
    {"sym": "Ru", "nom": "Ruteni",
     "ist": [96, 98, 99, 100, 101, 102, 104],
     "oen": 43,
     },
    {"sym": "Rh", "nom": "Rodi",
     "ist": [103],
     "oen": 39,
     },
    {"sym": "Pd", "nom": "Paladi",
     "ist": [102, 104, 105, 106, 108, 110],
     "oen": 35,
     },
    {"sym": "Ag", "nom": "Argent",
     "ist": [107, 109],
     "vp": [1],
     "oen": 31,
     },
    {"sym": "Cd", "nom": "Cadmi",
     "ist": [106, 108, 110, 111, 112, 114],
     "vp": [2],
     "oen": 28,
     },
    {"sym": "In", "nom": "Indi",
     "ist": [113],
     "oen": 25,
     },
    # 50
    {"sym": "Sn", "nom": "Estany",
     "ist": [112, 114, 115, 116, 117, 118, 119, 120, 122, 124],
     "vp": [2, 4],
     "oen": 20,
     },
    {"sym": "Sb", "nom": "Antimoni",
     "nneg": "Antimonur",
     "ist": [121, 123],
     "vp": [3, 5],
     "vn": [-3],
     "ime": -3,
     "oen": 15,
     },
    {"sym": "Te", "nom": r"Te\lgem uri",
     "nneg": r"Te\lgem urur",
     "ist": [120, 122, 124, 125, 126],
     "vp": [4, 6],
     "vn": [-2],
     "ime": -2,
     "oen": 9,
     },
    {"sym": "I", "nom": "Iode",
     "nneg": "Iodur",
     "ist": [127],
     "vp": [1, 3, 5, 7],
     "vn": [-1],
     "ime": -1,
     "oen": 4,
     },
    {"sym": "Xe", "nom": "Xenó",
     "ist": [124, 126, 128, 129, 130, 131, 132, 134, 136],
     },
    {"sym": "Cs", "nom": "Cesi",
     "ist": [133],
     "vp": [1],
     "ime": 1,
     "oen": 114,
     },
    {"sym": "Ba", "nom": "Bari",
     "ist": [130, 132, 134, 135, 136, 137, 138],
     "vp": [2],
     "ime": 2,
     "oen": 98,
     },
    {"sym": "La", "nom": "Lantani",
     "ist": [139],
     "oen": 64,
     },
    {"sym": "Ce", "nom": "Ceri",
     "ist": [136, 138, 140, 142],
     "oen": 65,
     },
    {"sym": "Pr", "nom": "Praseodimi",
     "ist": [141],
     "oen": 66,
     },
    # 60
    {"sym": "Ne", "nom": "Neodimi",
     "ist": [142, 143, 145, 146, 148],
     "oen": 67,
     },
    {"sym": "Pm", "nom": "Prometi",
     "oen": 68,
     },
    {"sym": "Sm", "nom": "Samari",
     "ist": [144, 149, 150, 152, 154],
     "oen": 69,
     },
    {"sym": "Eu", "nom": "Europi",
     "ist": [151, 153],
     "oen": 70,
     },
    {"sym": "Gd", "nom": "Gadolini",
     "ist": [154, 155, 156, 157, 158, 160],
     "oen": 71,
     },
    {"sym": "Tb", "nom": "Terbi",
     "ist": [159],
     "oen": 72,
     },
    {"sym": "Dy", "nom": "Disprosi",
     "ist": [156, 158, 160, 161, 162, 163, 164],
     "oen": 73,
     },
    {"sym": "Ho", "nom": "Holmi",
     "ist": [165],
     "oen": 74,
     },
    {"sym": "Er", "nom": "Erbi",
     "ist": [162, 164, 166, 167, 168, 170],
     "oen": 75,
     },
    {"sym": "Tm", "nom": "Tuli",
     "ist": [169],
     "oen": 76,
     },
    # 70
    {"sym": "Yb", "nom": "Iterbi",
     "ist": [168, 170, 171, 172, 173, 174, 176],
     "oen": 77,
     },
    {"sym": "Lu", "nom": "Luteci",
     "ist": [175],
     "oen": 78,
     },
    {"sym": "Hf", "nom": "Hafni",
     "ist": [176, 177, 178, 179, 180],
     "oen": 60,
     },
    {"sym": "Ta", "nom": "Tàntal",
     "ist": [181],
     "oen": 56,
     },
    {"sym": "W", "nom": "Tungstè",
     "ist": [180, 182, 183, 184, 186],
     "oen": 52,
     },
    {"sym": "Re", "nom": "Reni",
     "ist": [185],
     "oen": 48,
     },
    {"sym": "Os", "nom": "Osmi",
     "ist": [184, 187, 188, 189, 190, 192],
     "oen": 44,
     },
    {"sym": "Ir", "nom": "Iridi",
     "ist": [191, 193],
     "oen": 40,
     },
    {"sym": "Pt", "nom": "Platí",
     "ist": [192, 194, 195, 196, 198],
     "vp": [2, 4],
     "oen": 36,
     },
    {"sym": "Au", "nom": "Or",
     "ist": [197],
     "vp": [1, 3],
     "oen": 32,
     },
    # 80
    {"sym": "Hg", "nom": "Mercuri",
     "ist": [196, 198, 199, 200, 201, 202, 204],
     "vp": [1, 2],
     "oen": 29,
     },
    {"sym": "Tl", "nom": "Tali",
     "ist": [203, 205],
     "oen": 26,
     },
    {"sym": "Pb", "nom": "Plom",
     "ist": [204, 206, 207, 208],
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
     "ist": [232],
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
    ist = []
    vp = []
    vn = []
    ve = []
    v = []
    nneg = []
    for x in range(1, 119):  # de l'1 al 118
        if "ist" in elements[x]:
            ist.append(x)
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
    print(f"els_ist = {ist}")
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


def nommolec(elems=[], valens=[], nomencs=[1, 2, 3], estil="general"):
    """Anomena el compost a partir de llista d'elements i estats.

    :param elems: llista d'elements de la molècula [[elem, qtat], [elem, qtat]]
    :param valens: llista de valències dels elements anteriors
    :param nomencs: llista de nomenclatures a extreure (1 stock, 2 sistem, 3 comú)
    :param estil: per distingir la manera com ho fan en diferents instituts (noms comuns i caselles tapades)
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
    comu = ""
    if 3 in nomencs:
        comu = nomcomu(elems, estil="general")
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


def nomcomu(elems=[], estil="general"):
    try:  # comprovo que dins la llista hi ha llistes (que és una llista d'elements i no un sol element)
        len(elems[0])
    except:  # si només era un, el converteixo en llista
        elems = [elems]
    comu = "-"
    alt = ""
    if len(elems) == 2:  # binaris
        if elems[1][0] == 1:  # hidrurs
            if elems == [[5, 1], [1, 3]]:  # BH3
                comu = "Borà"
            elif elems == [[6, 1], [1, 4]]:  # CH4
                comu = "Metà"
            elif elems == [[7, 1], [1, 3]]:  # NH3
                comu = "Amoníac (Azà)"
            elif elems == [[13, 1], [1, 3]]:  # AlH3
                comu = "Alumà"
            elif elems == [[14, 1], [1, 4]]:  # SiH4
                comu = "Silà"
            elif elems == [[15, 1], [1, 3]]:  # PH3
                comu = "Fosfà"
                alt = "Fosfina"
            elif elems == [[31, 1], [1, 3]]:  # GaH3
                comu = "Ga\lgem à"
            elif elems == [[32, 1], [1, 4]]:  # GeH4
                comu = "Germà"
            elif elems == [[33, 1], [1, 3]]:  # AsH3
                comu = "Arsà"
                alt = "Arsina"
            elif elems == [[49, 1], [1, 3]]:  # InH3
                comu = "Indigà"
            elif elems == [[50, 1], [1, 4]]:  # SnH4
                comu = "Estannà"
            elif elems == [[51, 1], [1, 3]]:  # SbH3
                comu = "Estibà"
                alt = "Estibina"
            elif elems == [[81, 1], [1, 3]]:  # BiH3
                comu = "Ta\lgem à"
            elif elems == [[82, 1], [1, 4]]:  # PbH4
                comu = "Plumbà"
            elif elems == [[83, 1], [1, 3]]:  # BiH3
                comu = "Bismutà"
            # suprimeixo els que no fan
            if estil == "salle":
                if elems[0][0] not in [5, 6, 7, 14, 15, 33, 51]:
                    comu = "-"
                elif alt:  # poso el nom antic (alt), que és el que hi fan
                    comu = alt + f" ({comu})"
            elif estil == "general":
                if elems[0][0] not in [5, 6, 7, 14, 15, 33, 51]:
                    comu = "-"
        elif elems[0][0] == 1:  # urs d'hidrogen
            hidracid = ""
            # hidràcids
            if elems == [[1, 1], [9, 1]]:  # HF
                hidracid = "Fluorhídric"
            elif elems == [[1, 1], [17, 1]]:  # HCl
                hidracid = "Clorhídric"
            elif elems == [[1, 1], [35, 1]]:  # HBr
                hidracid = "Bromhídric"
            elif elems == [[1, 1], [53, 1]]:  # HI
                hidracid = "Iodhídric"
            elif elems == [[1, 2], [16, 1]]:  # H2S
                hidracid = "Sulfhídric"
            elif elems == [[1, 2], [34, 1]]:  # H2Se
                hidracid = "Selenhídric"
            elif elems == [[1, 2], [52, 1]]:  # H2Te
                hidracid = "Te\lgem urhídric"
            # altres comuns d'hidrogen
            elif elems == [[1, 2], [8, 1]]:  # H2O
                comu = "Aigua"
            elif elems == [[1, 2], [8, 2]]:  # H2O2
                comu = "Aigua oxigenada"
            elif elems == [[1, 2], [8, 1]]:  # H2O
                comu = "Aigua"
            if hidracid:
                comu = "Àcid " + hidracid.lower()
        else:  # altres
            if elems == [[11, 1], [17, 1]]:  # NaCl
                comu = "Sal comuna"
    return comu


def fisotops(tipus, nivell=1, prez=0):
    """Treu files de la taula d'isòtops (zapne)

    :param tipus: tipus d'exercici (1 = taula zapne)
    :param nivell: 1 sense càrrega, 2 amb càrrega
    :param prez: element (z) escollit a priori
    """
    fila = []
    if tipus == 1:
        # tria
        if not prez:
            z = random.choice(els_ist)
        else:
            z = prez
        a = random.choice(elements[z]["ist"])
        if nivell == 1:  # sense ions
            estat = 0
        elif nivell == 2:  # amb ions
            if z in els_vn and (len(elements[z]["ist"]) > 1 or moneda()):
                estat = random.choice(elements[z]["vn"])
            elif z in els_vp:
                estat = random.choice(elements[z]["vp"])
            else:
                estat = 0
        else:  # TODO amb configuració electrònica?
            return ["no", "tinc", "tants", "nivells"]
        # càlcul
        p = z
        n = a-z
        e = p-estat
        if estat:
            q = estatexp(estat)
        else:
            q = ""
        # muntatge
        symdata = (a, z, elements[z]["sym"], q)
        sym = r"$\isotope[%s][%s]{%s}^{%s}$" % symdata
        nom = elements[z]["nom"]
        fila = [nom, sym, f"{z}", f"{a}", f"{p}", f"{n}", f"{e}", f"{estat}"]
        # buidatge
        if not random.randint(0, 4):  # només símbol
            fila = [x if i == 1 else "" for i, x in enumerate(fila)]
        else:
            # trec el símbol
            fila[1] = ""
            # deixo només una de les tres instàncies de z
            for x in random.sample([0, 2, 4], 2):
                fila[x] = ""
            # deixo màssic o neutrons
            fila[random.choice([3, 5])] = ""
            # deixo càrrega o electrons
            fila[random.choice([-1, -2])] = ""
    return fila


def finorg(tipus, nivell=1, descn=[6, 14], estil="general"):
    """Treu exercicis de formulació inorgànica

    :param tipus: 1 ions/diat, 10 molèc
    :param nivell: dificultat interna del tipus
    :param descn: descartats negatius (evito "carbur i silicur")
    """
    fila = []
    if tipus == 1:  # ions, diatòmics i ozó
        if not random.randint(0, 20):  # ozó (i/o si se m'acudeix algun altre així friqui)
            fila = [molec([8, 3]), "-", "Trioxigen", "Ozó"]
        elif not random.randint(0, 3):  # diatòmic
            z = random.choice(diatomics)
            fila = [molec([z, 2]), "-", iprefix[2] + f"{elements[z]['nom']}".lower(), elements[z]['nom']]
            if z != 8 and not estil == "salle":  # iupac només accepta òxid i ozó (i fòsfor blanc). La resta sistemàtica
                fila[3] = "-"
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
        deixo = random.choice([i for i, c in enumerate(fila) if c != "-"])  # trio conservar una de les plenes
        fila = [c if i == deixo or c == "-" else " " for i, c in enumerate(fila)]  # esborro tots menys el que deixo
    elif tipus == 10:  # molècules
        # TODO random molèc comuns (com ozó al cas anterior)
        # tria
        if nivell == 1:  # binaris hidrogen (hidrur, però canviarà si agafa halògens o calcògens)
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
        noms = nommolec(m, [vp, vn], estil=estil)
        if estil == "salle":  # correccions per fer-ho com ho fan a la salle de girona (3ESO, 2021)
            if zn == 1 and noms[2] != "-":  # hidrurs amb nom propi (borà, etc)
                noms[0] = "-"  # esborro, perquè ells no ho pregunten
                noms[1] = "-"
        fila = [molec(m)] + noms
        # buidat
        deixo = random.choice([i for i, c in enumerate(fila) if c != "-"])  # trio conservar una de les plenes
        fila = [c if i == deixo or c == "-" else " " for i, c in enumerate(fila)]  # esborro tots menys el que deixo
    return fila


elemstats()
