def nom_apartat(tema, apartat, btn=False):
    """Retorna el nom de l'apartat abreviat demanat (cal tema + apartat)

        "apartat": ["Nom complet", "Nom abreviat (pels botons)"]

    :param tema: tema de l'apartat
    :param apartat: nom de l'apartat
    :param btn: True = treure versió pel text dels botons (toggle) del formulari
    """
    apartats = {
        "px": {
            "algeb": ["Factoritzar i fraccions algebraiques", "Algebraiques"],
            "base": ["Base", "Base"],
            "idnot": ["Identitats notables", "Id. Notables"],
            "ops": ["Operacions amb polinomis", "Operar polinomis"],
        },
    }
    i = 1 if btn else 0
    default = [f"FALTA EL NOM DE L'APARTAT ({apartat})", f"BOT ({apartat})"]
    return apartats[tema].get(apartat, default)[i] if tema in apartats else default[i]


def nom_tema(tema, prep=False, pdf=False):
    """Retorna el nom de l'apartat abreviat demanat

        "tema": ["Nom Complet", "amb Preposició", ".pdf"]

    """
    temes = {
        "px": ["Polinomis", "de Polinomis", "polinomis"],
    }
    if pdf:
        i = 2
    elif prep:
        i = 1
    else:
        i = 0
    default = [f"FALTA NOM DEL TEMA ({tema})", f"del TEMA QUE FALTA ({tema})", f"emtemoquenoliheposatnomalafitxa"]
    return temes.get(tema, default)[i] if tema in temes else default[i]
