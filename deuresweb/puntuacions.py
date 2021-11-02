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
        # ********** EQ ********** #
        "EQ_BASE_IDENTITATOEQUACIO": 1,
        "EQ_PRIMER_DENOMINADORS": 3,
        "EQ_PRIMER_OPERAIRESOL": 2,
        "EQ_PRIMER_SIMPLESENTERA": 1,
        "EQ_PRIMER_SIMPLESNODIVIDIR": 1,
        "EQ_SEGON_COMPLETES": 3,
        "EQ_SEGON_INCOMPLETES": 2,
        "EQ_SEGON_OPERAIRESOL": 3,
        "EQ_SISTEMES3_LINEALS": 5,
        "EQ_SISTEMES_LINEALS": 4,
        "EQ_SISTEMES_LINEALSGRAFIC": 4,
        "EQ_SISTEMES_NOLINEALS": 5,

        # ********* FRAC ********* #
        "FRAC_COMBIS_NORMAL": 3,
        "FRAC_COMBIS_POTENCIESIARRELS": 4,
        "FRAC_DECIMALS_GENERATRIU": 1,
        "FRAC_SIMPLES_MULTIPLICAIDIVIDEIX": 1,
        "FRAC_SIMPLES_SUMAIRESTA": 1,

        # ******** POWSQR ******** #
        "POWSQR_POW_FACTORITZADECIMALS": 4,
        "POWSQR_POW_FACTORITZAISIMPLIFICA": 3,
        "POWSQR_POW_MATEIXABASE": 1,
        "POWSQR_POW_MATEIXAFRACCIO": 2,
        "POWSQR_POW_MATEIXEXPONENT": 1,
        "POWSQR_POW_SIMPLIFICAFRACCIO": 2,
        "POWSQR_SQR_COMBINA": 2,
        "POWSQR_SQR_EXTREU": 2,
        "POWSQR_SQR_FACTORITZAIEXTREU": 3,
        "POWSQR_SQR_INDEXCOMU": 2,
        "POWSQR_SQR_INTRODUEIX": 1,
        "POWSQR_SQR_RACIONALITZA": 4,
        "POWSQR_SQR_SUMAIRESTA": 3,

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
