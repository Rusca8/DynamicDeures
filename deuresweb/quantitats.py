"""
Quantitat d'apartats que significa "no", "poques", "normal", "moltes", "mitja", "plana" i "doble",
en funció de l'exercici.
"""


def quantitats_de(nom):
    """Retorna la llista de quantitats corresponent a l'exercici escollit.

        "exercici": [no, poques, normal, moltes, mitja, plana, doble]
    """
    exercicis = {
        # ********** EQ ********** #
        "EQ_BASE_IDENTITATOEQUACIO": [0, 2, 4, 8, 14, 33, 70],
        "EQ_PRIMER_DENOMINADORS": [0, 2, 4, 8, 10, 20, 42],
        "EQ_PRIMER_OPERAIRESOL": [0, 2, 4, 8, 10, 22, 44],
        "EQ_PRIMER_SIMPLESENTERA": [0, 3, 9, 12, 15, 33, 69],
        "EQ_PRIMER_SIMPLESNODIVIDIR": [0, 6, 9, 15, 21, 51, 105],
        "EQ_SEGON_COMPLETES": [0, 6, 9, 12, 15, 33, 66],
        "EQ_SEGON_INCOMPLETES": [0, 6, 9, 12, 15, 33, 66],
        "EQ_SEGON_OPERAIRESOL": [0, 2, 4, 8, 10, 22, 44],
        "EQ_SISTEMES3_LINEALS": [0, 3, 6, 9, 12, 27, 60],
        "EQ_SISTEMES_LINEALS": [0, 3, 6, 9, 12, 36, 77],
        "EQ_SISTEMES_LINEALSGRAFIC": [0, 2, 3, 6, 12, 36, 77],
        "EQ_SISTEMES_NOLINEALS": [0, 3, 6, 9, 12, 36, 77],
        # ********** PX ********** #
        "PX_ALGEB_FACTORITZA": [0, 2, 4, 6, 12, 20, 46],
        "PX_ALGEB_SIMPLIFICA": [0, 1, 2, 4, 5, 10, 51],
        "PX_BASE_AVALUA": [0, 1, 3, 5, 6, 12, 26],
        "PX_BASE_DESXIFRA": [0, 1, 2, 3, 4, 7, 14],
        "PX_BASE_FACTORCOMU": [0, 2, 4, 6, 12, 26, 54],
        "PX_BASE_INVENTA": [0, 1, 3, 5, 6, 12, 26],
        "PX_BASE_PARTSMONOMI": [0, 2, 4, 8, 24, 52, 108],
        "PX_IDNOT_ENDEVINAIDENTITAT": [0, 2, 4, 8, 20, 44, 88],
        "PX_IDNOT_IDENTITAT": [0, 2, 4, 8, 20, 44, 88],
        "PX_OPS_DIVIDEIX": [0, 2, 3, 4, 5, 12, 24],
        "PX_OPS_DIVIDEIXRUFFINI": [0, 2, 3, 4, 5, 12, 24],
        "PX_OPS_MULTIPLICA": [0, 2, 3, 4, 5, 12, 24],
        "PX_OPS_PARAMETRERESIDU": [0, 1, 3, 5, 6, 12, 26],
        "PX_OPS_RESTA": [0, 2, 3, 4, 5, 12, 24],
        "PX_OPS_SUMA": [0, 2, 3, 4, 5, 12, 24],
        "PX_OPS_TEOREMARESIDU": [0, 1, 3, 5, 6, 12, 26],
    }
    print(f"Quantitats de {nom} no disponibles") if nom not in exercicis else None
    return exercicis.get(nom, [0, 2, 3, 4, 5, 12, 24])  # .get(key, default)











