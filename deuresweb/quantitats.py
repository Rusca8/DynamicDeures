"""
Quantitat d'apartats que significa "no", "poques", "normal", "moltes", "mitja", "plana" i "doble",
en funció de l'exercici.
"""


def quantitats_de(nom):
    """Retorna la llista de quantitats corresponent a l'exercici escollit."""
    exercicis = {
        # ********** PX ********** #
        "PX_ALGEB_FACTORITZA": [0, 2, 3, 6, 12, 20, 46],
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
    return exercicis.get(nom, [0, 2, 3, 4, 5, 12, 24])  # .get(key, default)











