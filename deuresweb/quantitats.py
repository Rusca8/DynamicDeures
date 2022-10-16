"""
Quantitat d'apartats que significa "no", "poques", "normal", "moltes", "mitja", "plana" i "doble",
en funció de l'exercici.
"""


def quantitats_de(nom, alt="def"):
    """Retorna la llista de quantitats corresponent a l'exercici escollit.

        "exercici": [no, poques, normal, moltes, mitja, plana, doble]
    """
    default = [0, 2, 3, 4, 5, 12, 24]
    alt = alt or "def"  # per si entra un "None" o alguna cosa per l'estil

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

        # ********* FRAC ********* #
        "FRAC_COMBIS_NORMAL": [0, 2, 4, 8, 12, 24, 52],
        "FRAC_COMBIS_POTENCIESIARRELS": [0, 2, 4, 8, 12, 20, 42],  # TODO nums diferents segons què trio de powsqr
        "FRAC_DECIMALS_GENERATRIU": [0, 4, 8, 12, 24, 52, 112],
        "FRAC_SIMPLES_MULTIPLICAIDIVIDEIX": [0, 3, 6, 12, 18, 37, 74],
        "FRAC_SIMPLES_SUMAIRESTA": [0, 3, 6, 12, 18, 37, 74],

        # ******** POWSQR ******** #
        "POWSQR_POW_FACTORITZADECIMALS": [0, 2, 3, 6, 17, 35, 71],
        "POWSQR_POW_FACTORITZAISIMPLIFICA": [0, 2, 3, 6, 17, 35, 71],
        "POWSQR_POW_MATEIXABASE": {"def": [0, 3, 6, 12, 21, 51, 105],
                                   "mc2":  [0, 4, 6, 8, 14, 32, 70],
                                   }.get(alt, default),
        "POWSQR_POW_MATEIXAFRACCIO": [0, 2, 4, 6, 14, 28, 58],
        "POWSQR_POW_MATEIXEXPONENT": {"def": [0, 3, 6, 12, 21, 51, 105],
                                      "mc2":  [0, 4, 6, 8, 14, 32, 70],
                                      }.get(alt, default),
        "POWSQR_POW_NIADES": [0, 4, 8, 16, 28, 68, 140],
        "POWSQR_POW_SIGNEPARITAT": [0, 4, 8, 16, 28, 68, 140],
        "POWSQR_POW_SIMPLIFICAFRACCIO": [0, 3, 6, 9, 18, 42, 87],
        "POWSQR_SQR_ARRELAPOTENCIA": [0, 4, 8, 16, 28, 68, 140],
        "POWSQR_SQR_EXTREU": [0, 4, 8, 12, 32, 66, 132],
        "POWSQR_SQR_FACTORITZAIEXTREU": [0, 3, 6, 9, 21, 51, 105],
        "POWSQR_SQR_INDEXCOMU": {"def": [0, 3, 6, 12, 21, 51, 105],
                                 "mc2":  [0, 2, 4, 6, 14, 32, 70],
                                 }.get(alt, default),
        "POWSQR_SQR_INTRODUEIX": [0, 4, 8, 12, 32, 66, 132],
        "POWSQR_SQR_NIADES": [0, 4, 8, 12, 24, 59, 124],
        "POWSQR_SQR_POTENCIAAARREL": [0, 4, 8, 16, 28, 68, 140],
        "POWSQR_SQR_RACIONALITZA": [0, 3, 6, 12, 18, 39, 86],
        "POWSQR_SQR_SIMPLIFICA": [0, 4, 8, 16, 28, 68, 140],
        "POWSQR_SQR_SUMAIRESTA": [0, 2, 4, 8, 16, 34, 69],

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
    return exercicis.get(nom, default)  # .get(key, default)











