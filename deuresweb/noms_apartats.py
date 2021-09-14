def nom_apartat(tema, apartat):
    apartats = {
        "px": {
            "algeb": "Factoritzar i fraccions algebraiques",
            "base": "Base",
            "idnot": "Identitats notables",
            "ops": "Operacions amb polinomis"
        },
    }
    return (apartats[tema].get(apartat, f"FALTA EL NOM DE L'APARTAT ({apartat})".upper()) if tema in apartats
            else f"FALTA EL TEMA I EL NOM DE L'APARTAT ({apartat})")
