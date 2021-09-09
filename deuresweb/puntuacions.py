"""
Puntuació per apartat de cada tipus d'exercici.

La coherència crec que la faré intra-fitxa, perquè si fem exàmens en plan macedònia
valdrà la pena que cada tema de l'examen tingui un pes semblant als altres
(i.e. si en un examen hi ha un tema fàcil i un difícil, igualment volem que saber
un dels dos temes sigui més o menys la meitat de la nota).
"""


def punts_de(nom):
    """Retorna la puntuació per defecte (punts/apartat) de l'exercici escollit"""
    exercicis = {
        # ********** PX ********** #
        "PX_ALGEB_FACTORITZA": 4,
        "PX_ALGEB_SIMPLIFICA": 5,
        "PX_BASE_AVALUA": 1,
        "PX_BASE_DESXIFRA": 5,
        "PX_BASE_FACTORCOMU": 2,
        "PX_BASE_INVENTA": 1,
        "PX_BASE_PARTSMONOMI": 1,
        "PX_IDNOT_ENDEVINAIDENTITAT": 3,
        "PX_IDNOT_IDENTITAT": 2,
        "PX_OPS_DIVIDEIX": 4,
        "PX_OPS_DIVIDEIXRUFFINI": 3,
        "PX_OPS_MULTIPLICA": 3,
        "PX_OPS_PARAMETRERESIDU": 3,
        "PX_OPS_RESTA": 2,
        "PX_OPS_SUMA": 2,
        "PX_OPS_TEOREMARESIDU": 2,
    }
    return 42 if nom not in exercicis else exercicis[nom]
