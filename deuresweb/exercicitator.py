"""
MÒDULS PER GENERAR EL LaTeX DELS DIFERENTS EXERCICIS

latexator.py agafarà d'aquí els exercicis a partir del nom d'exercici
"""
import random
import re

import generator as gen
import enunciats as en
import cryptolator as crypt
from classes import P

from pylatex import NoEscape
from rpylatex import (begin, end, part, space, lines, br, needspace, bloctitle, question, choice,
                      taulaconfig, obretaula, obrellarga, filataula, tancataula, envt,
                      escriusolus, blocsolus, blocsolucions, textsolucions,
                      prepkgs as pkgs)

import quantitats as qtats


def constructor_de(nom):
    """Retorna la funció que cal fer servir per construir l'exercici donat."""
    exercicis = {
        # ********** EQ ********** #
        "EQ_BASE_IDENTITATOEQUACIO": eq_base_identitatoequacio,
        "EQ_PRIMER_DENOMINADORS": eq_primer_denominadors,
        "EQ_PRIMER_OPERAIRESOL": eq_primer_operairesol,
        "EQ_PRIMER_SIMPLESENTERA": eq_primer_simplesentera,
        "EQ_PRIMER_SIMPLESNODIVIDIR": eq_primer_simplesnodividir,
        "EQ_SEGON_BIQUADRADES": eq_segon_biquadrades,
        "EQ_SEGON_COMPLETES": eq_segon_completes,
        "EQ_SEGON_INCOMPLETES": eq_segon_incompletes,
        "EQ_SEGON_OPERAIRESOL": eq_segon_operairesol,
        "EQ_SEGON_TRIQUADRADES": eq_segon_triquadrades,
        "EQ_SISTEMES3_LINEALS": eq_sistemes3_lineals,
        "EQ_SISTEMES_LINEALS": eq_sistemes_lineals,
        "EQ_SISTEMES_LINEALSGRAFIC": eq_sistemes_linealsgrafic,
        "EQ_SISTEMES_NOLINEALS": eq_sistemes_nolineals,

        # ********* FRAC ********* #
        "FRAC_COMBIS_NORMAL": frac_combis_normal,
        "FRAC_COMBIS_POTENCIESIARRELS": frac_combis_potenciesiarrels,
        "FRAC_DECIMALS_GENERATRIU": frac_decimals_generatriu,
        "FRAC_SIMPLES_MULTIPLICAIDIVIDEIX": frac_simples_multiplicaidivideix,
        "FRAC_SIMPLES_SUMAIRESTA": frac_simples_sumairesta,

        # ******** POWSQR ******** #
        "POWSQR_POW_FACTORITZADECIMALS": powsqr_pow_factoritzadecimals,
        "POWSQR_POW_FACTORITZAISIMPLIFICA": powsqr_pow_factoritzaisimplifica,
        "POWSQR_POW_MATEIXABASE": powsqr_pow_mateixabase,
        "POWSQR_POW_MATEIXAFRACCIO": powsqr_pow_mateixafraccio,
        "POWSQR_POW_MATEIXEXPONENT": powsqr_pow_mateixexponent,
        "POWSQR_POW_NIADES": powsqr_pow_niades,
        "POWSQR_POW_SIGNEPARITAT": powsqr_pow_signeparitat,
        "POWSQR_POW_SIMPLIFICAFRACCIO": powsqr_pow_simplificafraccio,
        "POWSQR_SQR_ARRELAPOTENCIA": powsqr_sqr_arrelapotencia,
        "POWSQR_SQR_EXTREU": powsqr_sqr_extreu,
        "POWSQR_SQR_FACTORITZAIEXTREU": powsqr_sqr_factoritzaiextreu,
        "POWSQR_SQR_INDEXCOMU": powsqr_sqr_indexcomu,
        "POWSQR_SQR_INDEXCOMUMULTI": powsqr_sqr_indexcomumulti,
        "POWSQR_SQR_INTRODUEIX": powsqr_sqr_introdueix,
        "POWSQR_SQR_NIADES": powsqr_sqr_niades,
        "POWSQR_SQR_POTENCIAAARREL": powsqr_sqr_potenciaaarrel,
        "POWSQR_SQR_RACIONALITZA": powsqr_sqr_racionalitza,
        "POWSQR_SQR_SIMPLIFICA": powsqr_sqr_simplifica,
        "POWSQR_SQR_SUMAIRESTA": powsqr_sqr_sumairesta,

        # ********** PX ********** #
        "PX_ALGEB_FACTORITZA": px_algeb_factoritza,
        "PX_ALGEB_SIMPLIFICA": px_algeb_simplifica,
        "PX_ALGEB_SUMAIRESTA": px_algeb_sumairesta,
        "PX_BASE_AVALUA": px_base_avalua,
        "PX_BASE_DESXIFRA": px_base_desxifra,
        "PX_BASE_FACTORCOMU": px_base_factorcomu,
        "PX_BASE_INVENTA": px_base_inventa,
        "PX_BASE_PARTSMONOMI": px_base_partsmonomi,
        "PX_IDNOT_ENDEVINAIDENTITAT": px_idnot_endevinaidentitat,
        "PX_IDNOT_IDENTITAT": px_idnot_identitat,
        "PX_IDNOT_OMPLEBUITS":  px_idnot_omplebuits,
        "PX_MOPS_DIVIDEIX": px_mops_divideix,
        "PX_MOPS_MULTIPLICA": px_mops_multiplica,
        "PX_MOPS_SUMAIRESTA": px_mops_sumairesta,
        "PX_OPS_DIVIDEIX": px_ops_divideix,
        "PX_OPS_DIVIDEIXRUFFINI": px_ops_divideixruffini,
        "PX_OPS_MULTIPLICA": px_ops_multiplica,
        "PX_OPS_PARAMETRERESIDU": px_ops_parametreresidu,
        "PX_OPS_RESTA": px_ops_resta,
        "PX_OPS_SUMA": px_ops_suma,
        "PX_OPS_TEOREMARESIDU": px_ops_teoremaresidu,
    }
    return exercicis.get(nom, exercici_no_trobat)  # .get(key, default)


def tema_apartat_exemple(doc, opcions):
    return exercici_no_trobat(doc, opcions)


# ************************ EQ ************************** #

def eq_base_identitatoequacio(doc, opcions):
    enunciat = "Digues si les següents igualtats són identitats o equacions."
    enunsols = "Identitat vs equació."
    g = [
        lambda: gen.eq_base(10, 1, solucions=True),                         # Ax+B = C(x+D)
        lambda: gen.eq_base(10, random.choice([1, 2]), solucions=True),     # A(x+B)+Cx = D(x+E)+Fx
        lambda: gen.eq_base(10, random.choice([1, 2, 3]), solucions=True),  # (x+A)(x-A)+B = x^2+C
        lambda: gen.eq_base(10, 3, solucions=True),                         # (x+A)(x+B) = x^2+Cx+D
        ]
    p = P([[1, {"max": 1}], 1, 1, 1])

    tsols = crea_exercici(doc, opcions,
                          g,
                          p,
                          enunciat=enunciat,
                          cols=2,
                          espai_apartat=7,
                          espai_final=2,
                          mates_solus=True,
                          )
    return [enunsols, tsols]


def eq_primer_denominadors(doc, opcions):
    enunciat = "Resol les següents equacions amb denominadors (no totes tenen resultat bonic!)."
    enunsols = "Primer grau, amb denominadors."

    tsols = crea_exercici(doc, opcions,
                          lambda: gen.eq(5, 2),  # no porta respostes perquè no quadra la solu llavor amb el generat
                          enunciat=enunciat,
                          cols=2,
                          scale=1.3,
                          espai_min=10,
                          espai_apartat=14,
                          espai_final=4,
                          mates_solus=True,
                          )
    return [enunsols, tsols]


def eq_primer_operairesol(doc, opcions):
    enunciat = "Opera i resol les següents equacions de primer grau."
    enunsols = "Primer grau, opera i resol."
    g = [
        lambda: gen.eq(3, 1, solucions=True),  # Sense parèntesis (6 termes)
        lambda: gen.eq(4, 1, solucions=True),  # Ax+B = F(Cx+D)
        lambda: gen.eq(4, 2, solucions=True),  # E(Ax+B) = F(Cx+D) + G
        ]
    pvar = quantilvar(opcions["var"]["sense_parentesis"])
    p = P([2, 1, 1]).flex(0, pvar)

    tsols = crea_exercici(doc, opcions,
                          g,
                          p,
                          enunciat=enunciat,
                          cols=2,
                          espai_apartat=14,
                          espai_final=1,
                          )
    return [enunsols, tsols]


def eq_primer_simplesentera(doc, opcions):
    enunciat = "Resol les següents equacions de primer grau (amb coeficient a la x)."
    enunsols = "Primer grau, amb coeficient."
    g = [
        lambda: gen.eq(2, 2, solucions=True),  # A positiu
        lambda: gen.eq(2, 3, solucions=True),  # qualsevol signe
        ]
    pvar = quantilvar(opcions["var"]["coeficient_positiu"])
    p = P([1, 1]).flex(0, pvar)

    tsols = crea_exercici(doc, opcions,
                          g,
                          p,
                          enunciat=enunciat,
                          cols=3,
                          espai_apartat=14,
                          espai_final=1,
                          )
    return [enunsols, tsols]


def eq_primer_simplesnodividir(doc, opcions):
    enunciat = "Resol les següents equacions de primer grau (sense coeficient a la x)."
    enunsols = "Primer grau, sense coeficient."
    seeds = ampliable([x for x in range(-10, 11)])
    g = [
        lambda: gen.eq(1, 1, x=next(seeds), solucions=True),  # x a l'esquerra
        lambda: gen.eq(1, 2, x=next(seeds), solucions=True),  # x on sigui
        ]
    p = P([1, 1])

    tsols = crea_exercici(doc, opcions,
                          g,
                          p,
                          enunciat=enunciat,
                          cols=3,
                          espai_apartat=7,
                          espai_final=2,
                          es_spoiler=True,
                          )
    return [enunsols, tsols]


def eq_segon_biquadrades(doc, opcions):
    pkgs(doc, ['amssymb'])  # \nexists
    enunciat = "Resol les següents equacions biquadrades."
    enunsols = "Biquadrades."

    var1 = quantilvar(opcions["var"]["totexist"])
    s_exist = alt_var(opcions, var1)

    var2 = quantilvar(opcions["var"]["ordenat"])
    s_ordenat = alt_var(opcions, var2)

    def s_4x():
        a = 1
        while True:
            seeds = [[1, x ** 2, a] for x in range(1, 9)] + [[2, x ** 2, a] for x in range(2, 5)]
            random.shuffle(seeds)
            for seed in seeds:
                yield seed
            a += 1

    def s_2x():
        a = 1
        while True:
            seeds = [[x ** 2, -y, a] for x in range(1, 6) for y in range(1, 10-x)]
            random.shuffle(seeds)
            for seed in seeds:
                yield seed
            a += 1

    s_2x = s_2x()
    s_4x = s_4x()

    def g():
        exist = next(s_exist)
        ordenat = next(s_ordenat)
        seed = next(s_4x) if exist or moneda() else next(s_2x)
        return gen.eq(110, 1 if exist else 2, seed=seed, ordenat=ordenat, solucions=True)

    tsols = crea_exercici(doc, opcions,
                          g,
                          enunciat=enunciat,
                          cols=3,
                          espai_apartat=14,
                          espai_final=8,
                          )
    return [enunsols, tsols]


def eq_segon_completes(doc, opcions):
    enunciat = "Resol les següents equacions de segon grau."
    enunsols = "Segon grau, completes."

    g = [
        lambda: gen.eq(103, 1, solucions=True),  # A = 1, ordenada
        lambda: gen.eq(103, 2, solucions=True),  # A = ±1
        lambda: gen.eq(103, 3, solucions=True),  # normal
        ]

    pvar = quantilvar(opcions["var"]["a_unitari"])
    p = P([1, 1, 2]).flex(1, pvar)

    tsols = crea_exercici(doc, opcions,
                          g,
                          p,
                          enunciat=enunciat,
                          cols=3,
                          espai_apartat=14,
                          espai_final=9,
                          )
    return [enunsols, tsols]


def eq_segon_incompletes(doc, opcions):
    pkgs(doc, ['amssymb'])  # \nexists
    enunciat = "Resol les següents equacions de segon grau incompletes."
    enunsols = "Segon grau, incompletes."

    s101, s102 = (ampliable([x for x in range(-10, 11) if x]) for _ in range(2))
    s3_tipus = regenerable([0, 1])  # per anar alternant tipus pseudoaleatori quan són barrejades

    var1 = quantilvar(opcions["var"]["existeix"])
    s_exist = alt_var(opcions, var1)  # el porten totes les funcions per gastar del next (102 no el fa servir)

    def f3():
        if next(s3_tipus):
            return gen.eq(101, 3, solucions=True, totexist=next(s_exist), x=next(s101))
        else:
            return gen.eq(102, 3, solucions=True, totexist=next(s_exist), x=next(s102))

    g = [
        lambda: gen.eq(101, 1, solucions=True, totexist=next(s_exist), x=next(s101)),  # fer arrel, zero dreta, exists
        lambda: gen.eq(101, random.choice([2, 3]), solucions=True, totexist=next(s_exist), x=next(s101)),  # x on sigui
        lambda: gen.eq(102, random.choice([2, 3]), solucions=True, totexist=next(s_exist), x=next(s102)),  # desacoblar
        f3,
        ]
    p = P([[3, {"max": 2}], 0, 5, 4])  # 3/12, 8/12, 4

    tsols = crea_exercici(doc, opcions,
                          g,
                          p,
                          enunciat=enunciat,
                          cols=3,
                          espai_apartat=14,
                          espai_final=8,
                          es_spoiler=True,
                          )
    return [enunsols, tsols]


def eq_segon_operairesol(doc, opcions):
    enunciat = "Opera i resol les següents equacions de segon grau."
    enunsols = "Segon grau, opera i resol."

    tsols = crea_exercici(doc, opcions,
                          lambda: gen.eq(104, solucions=True),
                          enunciat=enunciat,
                          cols=2,
                          espai_apartat=14,
                          espai_final=4,
                          )
    return [enunsols, tsols]


def eq_segon_triquadrades(doc, opcions):
    enunciat = "Resol les següents equacions triquadrades."
    enunsols = "Triquadrades."

    var1 = quantilvar(opcions["var"]["ordenat"])
    s_ordenat = alt_var(opcions, var1)

    def s_2x():
        a = 1
        while True:
            seeds = [[x, y, a] for x in range(-4, 5) for y in range(x, 5) if x*y and abs(x**3 * y**3) < 100]
            random.shuffle(seeds)
            for seed in seeds:
                yield seed
            a += 1

    s_2x = s_2x()

    def g():
        ordenat = next(s_ordenat)
        seed = next(s_2x)
        return gen.eq(111, 1, seed=seed, ordenat=ordenat, solucions=True)

    tsols = crea_exercici(doc, opcions,
                          g,
                          enunciat=enunciat,
                          cols=3,
                          espai_apartat=14,
                          espai_final=8,
                          )
    return [enunsols, tsols]


def eq_sistemes3_lineals(doc, opcions):
    enunciat = "Resol aquests sistemes d'equacions lineals amb tres incògnites."
    enunsols = "Sistemes 3D."

    g = [
        lambda: gen.sisteq(101, 1, solucions=True),  # reducció escalonada, coef x unitari a la primera eq
        lambda: gen.sisteq(101, 2, solucions=True),  # reducció escalonada, coef x unitari en alguna eq
        lambda: gen.sisteq(101, 3, solucions=True),  # algun coef unitari
        lambda: gen.sisteq(101, 4, solucions=True),  # coef qualssevol
        ]

    pvar = quantilvar(opcions["var"]["coef_unitari"])
    p = P([[1, {"max": 3}], 1, 1, 3]).flex(2, pvar)

    tsols = crea_exercici(doc, opcions,
                          g,
                          p,
                          enunciat=enunciat,
                          cols=3,
                          espai_min=10,
                          espai_apartat=5,
                          )
    return [enunsols, tsols]


def eq_sistemes_lineals(doc, opcions):
    enunciat = "Resol aquests sistemes lineals fent servir algun mètode analític."
    enunsols = "Sistemes lineals, analíticament."

    g = [
        lambda: gen.sisteq(1, 1, solucions=True),  # la primera x coeficient 1
        lambda: gen.sisteq(1, 2, solucions=True),  # algun coeficient ±1
        lambda: gen.sisteq(1, 3, solucions=True),  # reducció qualsevol
        ]

    pvar = quantilvar(opcions["var"]["coef_unitari"])
    p = P([[1, {"max": 3}], 2, 3]).flex(1, pvar)

    tsols = crea_exercici(doc, opcions,
                          g,
                          p,
                          enunciat=enunciat,
                          cols=3,
                          espai_min=10,
                          espai_apartat=5,
                          espai_final=5,
                          )
    return [enunsols, tsols]


def eq_sistemes_linealsgrafic(doc, opcions):
    enunciat = "Resol gràficament els següents sistemes lineals de dues incògnites."
    enunsols = "Sistemes lineals, gràficament."

    g = [
        lambda: gen.sisteq(2, 1, solucions=True),  # pendent enter
        lambda: gen.sisteq(2, 2, solucions=True),  # pendent múltiple de 1/2
        ]
    p = P([1, 1])

    tsols = crea_exercici(doc, opcions,
                          g,
                          p,
                          enunciat=enunciat,
                          cols=3,
                          espai_min=10,
                          espai_apartat=5,
                          espai_final=5,
                          )
    return [enunsols, tsols]


def eq_sistemes_nolineals(doc, opcions):
    enunciat = "Resol els següents sistemes d'equacions no lineals."
    enunsols = "Sistemes no lineals."

    g = [
        lambda: gen.sisteq(11, 1, solucions=True),  # x+y=C, x*y=E      (cap dels tres coefs)
        lambda: gen.sisteq(11, 2, solucions=True),  # Ax+By=C, Dx*y=E    (un dels tres coefs)
        lambda: gen.sisteq(11, 3, solucions=True),  # Ax+By=C, Dx*y=E   (dos dels tres coefs)
        lambda: gen.sisteq(12, 1, solucions=True),  # x^2-y^2=C, x+y=F               (eq primer grau)
        lambda: gen.sisteq(12, 2, solucions=True),  # Ax^2+By^2=C, Dx+Ey=F            (eq segon grau)
        lambda: gen.sisteq(12, 3, solucions=True),  # Ax^2-By^2=C, Dx+Ey=F       (coefs "qualssevol")
        ]
    p = P([1, 1, 1, 1, 1, 1])

    tsols = crea_exercici(doc, opcions,
                          g,
                          p,
                          enunciat=enunciat,
                          cols=3,
                          espai_min=10,
                          espai_apartat=5,
                          espai_final=5,
                          mates_solus=True,
                          stretch_solus="1.3",
                          )
    return [enunsols, tsols]


# *********************** FRAC ************************* #
def frac_combis_normal(doc, opcions):
    enunciat = "Resol les següents operacions combinades amb fraccions."
    enunsols = "Combinades sense exponents."

    tsols = crea_exercici(doc, opcions,
                          lambda: gen.fracmix(inception=2, solucions=True),
                          enunciat=enunciat,
                          cols=2,
                          scale=1.3,
                          espai_apartat=10,
                          mates_solus=True,
                          stretch_solus=stretch_per("fracs"),
                          )
    return [enunsols, tsols]


def frac_combis_potenciesiarrels(doc, opcions):
    enunciat = "Resol les següents operacions combinades amb fraccions."
    enunsols = "Combinades sense exponents."

    ops = [x for x in [4, 5] if x in get_var(opcions, "tipus", [4, 5])]  # 4: sqrt, 5: pow
    ops += [1, 2]  # 1: sumrest, 2: muldiv

    def s_pow(ops):
        if 4 in ops:  # hi ha arrels (i.e. no hi ha perill)
            while True:
                if not random.randint(0, 4) or 5 not in ops:
                    yield gen.randomfracnum(3)
                else:
                    yield random.choice([1, 4, 9, 16, 25, 36])*random.choice([-1, 1])
        else:  # només hi ha pow (agafo quadrats a tot arreu, intentant que surtin)
            while True:
                yield random.choice([1, 4, 9, 16, 25, 36])*random.choice([-1, 1])

    s_num = s_pow(ops)
    d_num = s_pow(ops)

    tsols = crea_exercici(doc, opcions,
                          lambda: gen.fracmix(next(s_num), next(d_num), inception=2, ops=ops, solucions=True),
                          enunciat=enunciat,
                          cols=2,
                          scale=1.3,
                          espai_apartat=10,
                          mates_solus=True,
                          stretch_solus=stretch_per("fracs"),
                          )
    return [enunsols, tsols]


def frac_decimals_generatriu(doc, opcions):
    enunciat = "Troba la fracció generatriu d'aquests nombres decimals."
    enunsols = "Fracció generatriu."

    tipus = [x for x in [1, 2, 3] if x in get_var(opcions, "tipus", [1, 2, 3])]  # 1: exacte, 2: mixt, 3: pur
    notacions = [x for x in [1, 2] if x in get_var(opcions, "notacions", [1, 2])]  # 1: barret, 2: suspensius

    s_tipus = regenerable(tipus, inici=[1, 3, 2])  # començo de fàcil a difícil (regenerable filtrarà les no triades)
    s_notac = regenerable(notacions)
    s_fsigne = regenerable([1, -1], [-1])

    var1 = quantilvar(opcions["var"]["positiu"])
    s_fpositiu = alt_var(opcions, var1)  # positiu obligatori

    def g():
        tipus = next(s_tipus)
        notac = next(s_notac) if tipus != 1 else 1
        fpositiu = next(s_fpositiu)  # miro si toca obligatori
        fsigne = next(s_fsigne) if not fpositiu else 1  # si toca obligatori, forço positiu, si no, aleatori
        return gen.decimals(tipus, notac, fsigne=fsigne)

    tsols = crea_exercici(doc, opcions,
                          g,
                          enunciat=enunciat,
                          cols=4,
                          espai_apartat=10,
                          espai_final=3,
                          mates_solus=True,
                          stretch_solus=stretch_per("fracs"),
                          es_spoiler=True,
                          )
    return [enunsols, tsols]


def frac_simples_multiplicaidivideix(doc, opcions):
    tipus = [x for x in [1, 2] if x in get_var(opcions, "tipus", [1, 2])]  # 1: multis, 2: divis

    if len(tipus) == 2:
        enunciat = "Resol les següents multiplicacions i divisions de fraccions."
        enunsols = "Multiplicacions i divisions."
        s0_divis = regenerable([0, 2], [0])  # forçar multi, forçar divi
        f1_divis = 1  # random (pel multiterme)
    elif 1 in tipus:
        enunciat = "Resol les següents multiplicacions de fraccions."
        enunsols = "Multiplicacions."
        s0_divis = etern(0)  # forçar multi
        f1_divis = 0
    else:
        enunciat = "Resol les següents divisions de fraccions."
        enunsols = "Divisions."
        s0_divis = etern(2)  # forçar divi
        f1_divis = 2

    g = [
        lambda: gen.frac(2, 3, 2, divis=next(s0_divis), solucions=True),  # 2 termes
        lambda: gen.frac(2, 3, 3, divis=f1_divis, solucions=True),        # 3 termes
        ]

    p = P([2, 1])

    tsols = crea_exercici(doc, opcions,
                          g,
                          p,
                          enunciat=enunciat,
                          cols=3,
                          scale=1.3,
                          espai_apartat=10,
                          mates_solus=True,
                          es_spoiler=True,
                          )
    return [enunsols, tsols]


def frac_simples_sumairesta(doc, opcions):
    enunciat = "Resol les següents sumes i restes de fraccions."
    enunsols = "Sumes i restes."

    g = [
        lambda: gen.frac(1, 2, 2, solucions=True),  # 2 termes
        lambda: gen.frac(1, 2, 3, solucions=True),  # 3 termes
        ]

    p = P([2, 1])

    tsols = crea_exercici(doc, opcions,
                          g,
                          p,
                          enunciat=enunciat,
                          cols=3,
                          scale=1.3,
                          espai_apartat=10,
                          espai_final=3,
                          mates_solus=True,
                          es_spoiler=True,
                          )
    return [enunsols, tsols]


# ********************** POWSQR ************************ #

def powsqr_pow_niades(doc, opcions):
    enunciat = "Combina els exponents per deixar-ne un de sol."
    enunsols = "Combinar exponents."

    s0_base = regenerable([2, 3, 5, 7, 9, 11, 13])  # números primers per no generar confusió
    s3_base = ampliable([x+2 for x in range(6)])    # a la tercera poso base qualsevol
    s_signe = regenerable([1, 2], [1])  # forço negatiu el primer

    s_termes = alt_p_var(opcions, P([2, 1]), [2, 3])

    g = [  # f0: base primer, exponents positius / f1: base primer, exponents qualssevol / f2: base qualsevol
        lambda: gen.powsqr_base(1, 1, termes=next(s_termes), seed=next(s0_base), solucions=True),
        lambda: gen.powsqr_base(1, 2, termes=next(s_termes), seed=next(s0_base), fneg=next(s_signe), solucions=True),
        lambda: gen.powsqr_base(1, 2, termes=next(s_termes), seed=next(s3_base), fneg=next(s_signe), solucions=True),
    ]

    pvar = quantilvar(opcions["var"]["sense_negatius"])
    p = P([1, 1, 1]).flex(0, pvar)

    tsols = crea_exercici(doc, opcions,
                          g,
                          p,
                          enunciat=enunciat,
                          cols=4,
                          espai_apartat=7,
                          mates_solus=True,
                          es_spoiler=True,
                          )
    return [enunsols, tsols]


def powsqr_pow_signeparitat(doc, opcions):
    enunciat = "Treu el parèntesi de les potències següents (deixant el signe que correspongui)."
    enunsols = "Simplificar signes."

    s_parell = regenerable([0, 0, 1, 1], [0, 1])
    s_base = ampliable([x+2 for x in range(6)])

    g = [
        lambda: gen.powsqr_base(2, 1, seed=next(s_base), parell=next(s_parell), solucions=True),  # exp positius
        lambda: gen.powsqr_base(2, 2, seed=next(s_base), parell=next(s_parell), solucions=True),  # exp qualssevol
    ]

    pvar = quantilvar(opcions["var"]["sense_negatius"])
    p = P([1, 1]).flex(0, pvar)

    tsols = crea_exercici(doc, opcions,
                          g,
                          p,
                          enunciat=enunciat,
                          cols=4,
                          espai_apartat=7,
                          mates_solus=True,
                          es_spoiler=True,
                          )
    return [enunsols, tsols]


def powsqr_sqr_arrelapotencia(doc, opcions):
    enunciat = "Escriu les arrels següents en forma de potència (i simplifica quan es pugui)."
    enunsols = "D'arrel a potència."

    g = [
        lambda: gen.powsqr_base(102, 1, solucions=True),  # exp positius
        lambda: gen.powsqr_base(102, 2, solucions=True),  # exp qualssevol
    ]

    pvar = quantilvar(opcions["var"]["sense_negatius"])
    p = P([1, 1]).flex(0, pvar)

    tsols = crea_exercici(doc, opcions,
                          g,
                          p,
                          enunciat=enunciat,
                          cols=4,
                          espai_apartat=7,
                          mates_solus=True,
                          stretch_solus=stretch_per("exp_frac"),
                          es_spoiler=True,
                          )
    return [enunsols, tsols]


def powsqr_sqr_potenciaaarrel(doc, opcions):
    enunciat = "Escriu en forma d'arrel les següents potències (i simplifica quan es pugui)."
    enunsols = "De potència a arrel."

    g = [
        lambda: gen.powsqr_base(103, 1, solucions=True),  # exp positius
        lambda: gen.powsqr_base(103, 2, solucions=True),  # exp qualssevol
    ]

    pvar = quantilvar(opcions["var"]["sense_negatius"])
    p = P([1, 1]).flex(0, pvar)

    tsols = crea_exercici(doc, opcions,
                          g,
                          p,
                          enunciat=enunciat,
                          cols=4,
                          espai_apartat=7,
                          mates_solus=True,
                          stretch_solus=stretch_per("arrels"),
                          es_spoiler=True,
                          )
    return [enunsols, tsols]


def powsqr_sqr_simplifica(doc, opcions):
    enunciat = "Simplifica les arrels següents."
    enunsols = "Simplificar arrels."

    s0 = regenerable([x for x in range(2, 15)], [2, 3, 5, 7])
    s_termes = alt_p_var(opcions, P([[2, {"max": 20}], 1]), [2, 3])

    tsols = crea_exercici(doc, opcions,
                          lambda: gen.powsqr_base(101, termes=next(s_termes), seed=next(s0), solucions=True),
                          enunciat=enunciat,
                          cols=4,
                          espai_apartat=7,
                          mates_solus=True,
                          stretch_solus=stretch_per("arrels"),
                          es_spoiler=True,
                          )
    return [enunsols, tsols]


def powsqr_pow_factoritzadecimals(doc, opcions):
    enunciat = "Factoritza i simplifica les següents fraccions amb decimals."
    enunsols = "Simplificar amb decimals."

    tsols = crea_exercici(doc, opcions,
                          lambda: gen.powsqr(10, 8, 3),
                          enunciat=enunciat,
                          cols=3,
                          scale=1.3,
                          espai_apartat=7,
                          espai_final=5,
                          )
    return [enunsols, tsols]


def powsqr_pow_factoritzaisimplifica(doc, opcions):  # TODO optimitzar el generador per fer més simplificable
    enunciat = "Factoritza i simplifica les fraccions següents."
    enunsols = "Factoritzar i simplificar."

    g = [
        lambda: gen.powsqr(10, 5, 3),  # sense exponent
        lambda: gen.powsqr(10, 6, 3),  # amb exponents positius
        lambda: gen.powsqr(10, 7, 3),  # amb exponents qualssevol
    ]

    pvar = quantilvar(opcions["var"]["sense_exponents"])
    p = P([1, 1, 1]).flex(0, pvar)

    tsols = crea_exercici(doc, opcions,
                          g,
                          p,
                          enunciat=enunciat,
                          cols=3,
                          scale=1.3,
                          espai_apartat=7,
                          espai_final=5,
                          )
    return [enunsols, tsols]


def powsqr_pow_mateixabase(doc, opcions):
    enunciat = "Expressa com una sola potència."
    enunsols = "Potències, mateixa base."

    termes = var_quines(opcions, "termes", [2, 3, 4, 5])
    if any(x in termes for x in [4, 5]) and not all(x in termes for x in [2, 3]):  # (hi ha amples no diluits)
        cols = 2
    else:
        cols = 3

    opcions["q_alt"] = "mc2" if cols == 2 else None  # demano quantitats per només 2 columnes

    s_termes = alt_p_var(opcions, P([1 for _ in termes]), termes)  # reparteixo qtats de termes a parts iguals

    g = [
        lambda: gen.powsqr(2, 1, termes=next(s_termes), solucions=True),  # només multis
        lambda: gen.powsqr(2, 2, termes=next(s_termes), solucions=True),  # multis i divis
        ]

    pvar = quantilvar(opcions["var"]["sense_divisions"])
    p = P([1, 1]).flex(0, pvar)

    tsols = crea_exercici(doc, opcions,
                          g,
                          p,
                          enunciat=enunciat,
                          cols=cols,
                          espai_apartat=7,
                          espai_final=5,
                          mates_solus=True,
                          es_spoiler=True,
                          )
    return [enunsols, tsols]


def powsqr_pow_mateixafraccio(doc, opcions):
    enunciat = "Expressa com a potència d'una sola fracció."
    enunsols = "Mateixa base amb fraccions."

    g = [
        lambda: gen.powsqr(2, 10, 3, solucions=True),  # dretes multiplicant
        lambda: gen.powsqr(2, 11, 3, solucions=True),  # dretes muldiv
        lambda: gen.powsqr(2, 12, 3, solucions=True),  # una cap per vall
        lambda: gen.powsqr(2, 13, 3, solucions=True),  # la meitat cap per vall
    ]

    pvar = quantilvar(opcions["var"]["sense_invertides"])
    p = P([1, 1, 1, 1]).flex(1, pvar)

    tsols = crea_exercici(doc, opcions,
                          g,
                          p,
                          enunciat=enunciat,
                          cols=2,
                          scale=scale_per("fraccions"),
                          espai_apartat=7,
                          espai_final=5,
                          mates_solus=True,
                          )
    return [enunsols, tsols]


def powsqr_pow_mateixexponent(doc, opcions):
    enunciat = "Expressa com una sola potència."
    enunsols = "Potències, mateix exponent."

    termes = var_quines(opcions, "termes", [2, 3, 4, 5])
    if any(x in termes for x in [4, 5]) and not all(x in termes for x in [2, 3]):  # (hi ha amples no diluits)
        cols = 2
    else:
        cols = 3

    opcions["q_alt"] = "mc2" if cols == 2 else None  # demano quantitats per només 2 columnes

    s_termes = alt_p_var(opcions, P([1 for _ in termes]), termes)  # reparteixo qtats de termes a parts iguals

    g = [
        lambda: gen.powsqr(1, 1, termes=next(s_termes), solucions=True),  # només multis
        lambda: gen.powsqr(1, 2, termes=next(s_termes), solucions=True),  # multis i divis
    ]

    pvar = quantilvar(opcions["var"]["sense_divisions"])
    p = P([1, 1]).flex(0, pvar)

    tsols = crea_exercici(doc, opcions,
                          g,
                          p,
                          enunciat=enunciat,
                          cols=cols,
                          espai_apartat=7,
                          espai_final=5,
                          mates_solus=True,
                          es_spoiler=True,
                          )
    return [enunsols, tsols]


def powsqr_pow_simplificafraccio(doc, opcions):
    enunciat = "Simplifica les fraccions següents."
    enunsols = "Simplificar fraccions."

    g = [
        lambda: gen.powsqr(10, 1, 5),  # un sol factor, exponents positius
        lambda: gen.powsqr(10, 2, 5),  # un sol factor, exponents qualssevol
        lambda: gen.powsqr(10, 3, 5),  # dos factors, sense exponents de grup
        lambda: gen.powsqr(10, 4, 5),  # dos factors, amb exponents de grup
    ]

    pvar = quantilvar(opcions["var"]["mateixa_base"])
    p = P([1, 1, 1, 1]).flex(1, pvar)

    tsols = crea_exercici(doc, opcions,
                          g,
                          p,
                          enunciat=enunciat,
                          cols=3,
                          scale=1.3,
                          espai_apartat=7,
                          espai_final=5,
                          )
    return [enunsols, tsols]


def powsqr_sqr_niades(doc, opcions):
    enunciat = "Expressa com una sola arrel."
    enunsols = "Combinar radicals."

    g = [
        lambda: gen.powsqr(104, 1, 2),  # sense intercalats, dues arrels
        lambda: gen.powsqr(104, 2, 2),  # pot posar intercalats, dues arrels
        lambda: gen.powsqr(104, 2, 3),  # pot posar intercalats, tres arrels
    ]

    pvar = quantilvar(opcions["var"]["sense_intercalats"])
    p = P([1, 1, 1]).flex(0, pvar)

    tsols = crea_exercici(doc, opcions,
                          g,
                          p,
                          enunciat=enunciat,
                          cols=4,
                          espai_apartat=7,
                          espai_final=5,
                          )
    return [enunsols, tsols]


def powsqr_sqr_extreu(doc, opcions):
    enunciat = "Extreu de l'arrel tants factors com puguis."
    enunsols = "Extreure factors."

    lletres = var_quines(opcions, "tipus", [1, 2])  # 1: nums, 2: lletres
    if all(x in lletres for x in [1, 2]):  # tinc de tot
        s_lletres = regenerable([0, 2], [0])  # 0: forçar nums, 2: forçar lletres
    elif 1 in lletres:  # només nums
        s_lletres = etern(0)
    else:  # només lletres
        s_lletres = etern(2)

    g = [
        lambda: gen.powsqr(105, 1, lletres=next(s_lletres)),  # només quadrades
        lambda: gen.powsqr(105, 2, lletres=next(s_lletres)),  # qualsevol índex
        ]
    pvar = quantilvar(opcions["var"]["sense_index"])
    p = P([1, 1]).flex(0, pvar)

    tsols = crea_exercici(doc, opcions,
                          g,
                          p,
                          enunciat=enunciat,
                          cols=4,
                          espai_apartat=7,
                          espai_final=5,
                          )
    return [enunsols, tsols]


def powsqr_sqr_factoritzaiextreu(doc, opcions):
    enunciat = "Factoritza i extreu tants factors com puguis."
    enunsols = "Factoritzar i extreure."

    g = [
        lambda: gen.powsqr(105, 11),  # arrel quadrada
        lambda: gen.powsqr(105, 12),  # arrel qualsevol
    ]

    pvar = quantilvar(opcions["var"]["sense_index"])
    p = P([1, 1]).flex(0, pvar)

    tsols = crea_exercici(doc, opcions,
                          g,
                          p,
                          enunciat=enunciat,
                          cols=3,
                          espai_apartat=7,
                          espai_final=5,
                          )
    return [enunsols, tsols]


def powsqr_sqr_indexcomumulti(doc, opcions):
    enunciat = "Expressa com una sola arrel."
    enunsols = "Arrels, multiplicar per índex comú."

    termes = var_quines(opcions, "termes", [2, 3, 4])
    if 4 in termes and not all(x in termes for x in [2, 3]):  # (hi ha amples no diluits)
        cols = 2
    else:
        cols = 3

    opcions["q_alt"] = "mc2" if cols == 2 else None  # demano quantitats per només 2 columnes

    s_termes = alt_p_var(opcions, P([1 for _ in termes]), termes)  # reparteixo qtats de termes a parts iguals

    g = [
        lambda: gen.powsqr(103, 1, termes=next(s_termes)),  # Sense exponents
        lambda: gen.powsqr(103, 2, termes=next(s_termes)),  # amb exponents
        ]

    pvar = quantilvar(opcions["var"]["sense_exponents"])
    p = P([1, 1]).flex(0, pvar)

    tsols = crea_exercici(doc, opcions,
                          g,
                          p,
                          enunciat=enunciat,
                          cols=cols,
                          espai_apartat=7,
                          espai_final=5,
                          )
    return [enunsols, tsols]


def powsqr_sqr_indexcomu(doc, opcions):
    enunciat = "Converteix a índex comú els grups d'arrels següents."
    enunsols = "Arrels, índex comú."

    termes = var_quines(opcions, "termes", [2, 3, 4])
    if 4 in termes and not all(x in termes for x in [2, 3]):  # (hi ha amples no diluits)
        cols = 2
    else:
        cols = 3

    opcions["q_alt"] = "mc2" if cols == 2 else None  # demano quantitats per només 2 columnes

    s_termes = alt_p_var(opcions, P([1 for _ in termes]), termes)  # reparteixo qtats de termes a parts iguals

    g = [
        lambda: gen.powsqr(100, 1, termes=next(s_termes)),  # Sense exponents
        lambda: gen.powsqr(100, 2, termes=next(s_termes)),  # amb exponents
        ]

    pvar = quantilvar(opcions["var"]["sense_exponents"])
    p = P([1, 1]).flex(0, pvar)

    tsols = crea_exercici(doc, opcions,
                          g,
                          p,
                          enunciat=enunciat,
                          cols=cols,
                          espai_apartat=7,
                          espai_final=5,
                          )
    return [enunsols, tsols]


def powsqr_sqr_introdueix(doc, opcions):
    enunciat = "Introdueix tots els factors a dins l'arrel."
    enunsols = "Introduir factors."

    lletres = var_quines(opcions, "tipus", [1, 2])  # 1: nums, 2: lletres
    if all(x in lletres for x in [1, 2]):  # tinc de tot
        s_lletres = regenerable([0, 2], [0])  # 0: forçar nums, 2: forçar lletres
    elif 1 in lletres:  # només nums
        s_lletres = etern(0)
    else:  # només lletres
        s_lletres = etern(2)

    g = [
        lambda: gen.powsqr(106, 1, lletres=next(s_lletres)),  # només quadrades
        lambda: gen.powsqr(106, 2, lletres=next(s_lletres)),  # qualsevol índex
    ]
    pvar = quantilvar(opcions["var"]["sense_index"])
    p = P([1, 1]).flex(0, pvar)

    tsols = crea_exercici(doc, opcions,
                          g,
                          p,
                          enunciat=enunciat,
                          cols=4,
                          espai_apartat=7,
                          espai_final=5,
                          )
    return [enunsols, tsols]


def powsqr_sqr_racionalitza(doc, opcions):
    enunciat = "Racionalitza les fraccions següents."
    enunsols = "Racionalitzar."

    tipus = var_quines(opcions, "tipus", [0, 1])
    if len(tipus) > 1:
        s_tipus = regenerable([0, 1])  # 0: f0 (completant), 1: f1 (conjugat)
    else:
        s_tipus = etern(tipus[0])

    var0 = quantilvar(opcions["var"]["sense_index"])
    p0 = P([1, 1, 1]).flex(0, var0)
    s0 = alt_p_var(opcions, p0, [1, 2, 3])

    var1 = quantilvar(opcions["var"]["sense_doble"])
    p1 = P([1, 1, 1, 1]).flex(1, var1)
    s1 = alt_p_var(opcions, p1, [11, 13, 12, 14])

    def f0():  # completant l'arrel
        if 0 in tipus:
            next(s1)  # faig córrer els percentatges de l'altre
            return gen.powsqr(108, next(s0))
        return f1()

    def f1():  # fent el conjugat
        if 1 in tipus:
            next(s0)  # faig córrer els percentatges de l'altre
            return gen.powsqr(108, next(s1))
        return f0()

    def f2():  # a sorts
        return f1() if next(s_tipus) else f0()

    g = [
        f0,  # completant l'arrel
        f1,  # fent el conjugat
        f2,  # a sorts
        ]

    p = P([[1, {"max": 3}], [1, {"max": 3}], 1])

    tsols = crea_exercici(doc, opcions,
                          g,
                          p,
                          enunciat=enunciat,
                          cols=3,
                          scale=scale_per("fraccions"),
                          espai_apartat=7,
                          espai_final=5,
                          )
    return [enunsols, tsols]


def powsqr_sqr_sumairesta(doc, opcions):
    enunciat = "Simplifica tant com puguis les sumes i restes següents."
    enunsols = "Sumes i restes d'arrels."

    g = [
        lambda: gen.powsqr(107, 1, 3),   # sense coeficient, un radical
        lambda: gen.powsqr(107, 11, 3),  # sense coeficient, pot dos radicals
        lambda: gen.powsqr(107, 2, 3),   # amb coeficient, un radical
        lambda: gen.powsqr(107, 12, 3),  # amb coeficient, pot dos radicals
    ]

    pvar = quantilvar(opcions["var"]["sense_coeficients"])
    p = P([1, 1, 1, 1]).flex(1, pvar)

    tsols = crea_exercici(doc, opcions,
                          g,
                          p,
                          enunciat=enunciat,
                          cols=2,
                          espai_apartat=7,
                          espai_final=5,
                          )
    return [enunsols, tsols]


# ************************ PX ************************** #

def px_algeb_factoritza(doc, opcions):
    enunciat = "Factoritza els polinomis següents."
    enunsols = "Factoritzar polinomis."
    g = [
        lambda: gen.px(7, 1, solucions=True),  # sense K ni x factor comú
        lambda: gen.px(7, 2, solucions=True),  # sense K factor comú
        lambda: gen.px(7, 3, solucions=True),  # pot tenir de tot
        ]
    pvar = quantilvar(opcions["var"]["sense_constant"])
    p = P([1, 1, 2]).flex(1, pvar)

    tsols = crea_exercici(doc, opcions,
                          g,
                          p,
                          enunciat=enunciat,
                          cols=2,
                          espai_apartat=10,
                          espai_final=10,
                          mates_solus=True,
                          )
    return [enunsols, tsols]


def px_algeb_simplifica(doc, opcions):
    enunciat = "Factoritza i simplifica les següents fraccions algebraiques."
    enunsols = "Simplificar fraccions algebraiques."
    tsols = crea_exercici(doc, opcions,
                          lambda: gen.px(8, solucions=True),
                          enunciat=enunciat,
                          cols=2,
                          scale=scale_per("fraccions"),
                          espai_apartat=10,
                          mates_solus=True,
                          )
    return [enunsols, tsols]


def px_algeb_sumairesta(doc, opcions):
    enunciat = "Realitza les següents operacions i simplifica el resultat en la mesura que es pugui."
    enunsols = "Sumes i restes de fraccions algebraiques."

    pvar = quantilvar(opcions["var"]["sense_restes"])
    s_rest = alt_var(opcions, pvar)

    pvar2 = quantilvar(opcions["var"]["factoritzat"])
    s_fact = alt_var(opcions, pvar2)

    p = P([1, 1, 2])

    g = [
        # 3 termes, 2 factors, numeradors [A, B, Ex]
        lambda: gen.op_algeb(1, 8, totsuma=next(s_rest), fact=next(s_fact), solucions=True),
        # 3 termes, 2 factors, numeradors [A, B, Ex + F]
        lambda: gen.op_algeb(1, 9, totsuma=next(s_rest), fact=next(s_fact), solucions=True),
        # 3 termes, 2 factors, numeradors [Ax+B, Cx+D, Ex+F]
        lambda: gen.op_algeb(1, 10, totsuma=next(s_rest), fact=next(s_fact), solucions=True),
        ]

    tsols = crea_exercici(doc, opcions,
                          g,
                          p,
                          enunciat=enunciat,
                          cols=2,
                          scale=scale_per("fraccions"),
                          espai_apartat=10,
                          mates_solus=True,
                          stretch_solus=stretch_per("algebs"),
                          )
    return [enunsols, tsols]


def px_base_avalua(doc, opcions):
    enunciat = "Avalua els següents polinomis en el punt demanat."
    enunsols = "Avaluar polinomis."

    pvar = quantilvar(opcions["var"]["una_variable"])
    p = P([1, 1]).flex(0, pvar)

    g = [lambda: gen.px(6, 1, solucions=True),
         lambda: gen.px(6, 2, solucions=True),
         ]

    tsols = crea_exercici(doc, opcions,
                          g,
                          p,
                          enunciat=enunciat,
                          espai_apartat=10,
                          mates=False,
                          )
    return [enunsols, tsols]


def px_base_desxifra(doc, opcions):
    enunciat = "Extreu factor comú per desxifrar el missatge amagat."
    enunsols = "Desxifrar per factor comú."

    pregen = get_var(opcions, "frases_triades", "")
    pregen = [f.strip() for f in pregen.split("/") if len(f) > 40]  # mínim 50 chars

    seeds = with_default(x for x in pregen)

    def f(seed=""):
        sol = seed if seed else en.factorcomu()
        text = r"\ \ \penalty-200".join([f" ${x}$ " for x in crypt.fc_frase(sol)])
        if not seed:
            sol = f"{sol}."
        return text, sol

    tsols = crea_exercici(doc, opcions,
                          lambda: f(next(seeds)),
                          enunciat=enunciat,
                          espai_apartat=20,
                          mates=False,
                          es_spoiler=True,
                          )
    return [enunsols, tsols]


def px_base_factorcomu(doc, opcions):
    enunciat = "Extreu factor comú de les expressions següents."
    enunsols = "Extreure factor comú."
    g = [
         lambda: gen.px(0, 1, termes=2),  # una variable, 2 termes
         lambda: gen.px(0, 1, termes=3),  # una variable, 3 termes
         lambda: gen.px(0, 2, termes=2),  # més variables, 2 termes
         lambda: gen.px(0, 2, termes=3),  # més variables, 3 termes
        ]
    pvar = quantilvar(opcions["var"]["una_variable"])
    p = P([1, 1, 1, 1]).flex(1, pvar)

    tsols = crea_exercici(doc, opcions,
                          g,
                          p,
                          enunciat=enunciat,
                          cols=2,
                          espai_apartat=10,
                          espai_final=4,
                          )
    return [enunsols, tsols]


def px_base_inventa(doc, opcions):
    enunciat = "Inventa't un polinomi que compleixi cadascuna de les descripcions següents."
    enunsols = "Inventar polinomis."
    tsols = crea_exercici(doc, opcions,
                          lambda: en.px_invent(),
                          enunciat=enunciat,
                          espai_apartat=10,
                          mates=False,
                          )
    return [enunsols, tsols]


def px_base_partsmonomi(doc, opcions):
    enunciat = "Indica el coeficient, la part literal, les variables i el grau dels següents monomis."
    enunsols = "Parts de monomis."
    tsols = crea_exercici(doc, opcions,
                          lambda: gen.rand_multimon(random.choice([2, 2, 3])),
                          enunciat=enunciat,
                          cols=4,
                          espai_apartat=10,
                          espai_final=2,
                          )
    return [enunsols, tsols]


def px_idnot_endevinaidentitat(doc, opcions):
    enunciat = "Esbrina quines identitats notables ens han donat els següents resultats."
    enunsols = "Endevinar identitats notables."

    tipus = [x for x in [1, 2, 3] if x in get_var(opcions, "tipus", [1, 2, 3])]  # 1: (a+b), 2: (a-b), 3: (a+b)(a-b)
    inici = [x for x in [1, 2] if x in tipus]
    if len(inici) > 1:
        inici = random.sample(inici, 1)  # si tinc 1 i 2, me'n quedo només un per començar

    ng1 = regenerable([2, 3], 2)  # per anar alternant aleatori pels nivells 2 i 3 a la g[1]
    ng2 = regenerable([4, 5])  # per anar alternant aleatori pels nivells 4 i 5 a la g[2]
    idnum = regenerable(tipus, inici)  # començo per 1 o 2
    s0_1, s0_2, s0_3 = [ampliable([x + 1 for x in range(10)]) for _ in range(3)]

    pvar2 = quantilvar(opcions["var"]["ordenat"])
    s_ord = alt_var(opcions, pvar2)
    o2 = opcions["var"]["ordre"] == "2"

    def f0():
        t = next(idnum)  # trio quin tipus toca
        seed = next([s0_1, s0_2, s0_3][t - 1])  # agafo una llavor del tipus que ha tocat
        return gen.idnotable(2, 1, idnums=t, fcoefb=seed, ordenat=next(s_ord), ordre2=o2, solucions=True)

    g = [  # g[0]: (x+B)   //   g[1]: (Ax+B) i (x^n+B)   //   g[2]: multivar (Axy+B) i (Ax+By)
        f0,
        lambda: gen.idnotable(2, next(ng1), idnums=next(idnum), ordenat=next(s_ord), ordre2=o2, solucions=True),
        lambda: gen.idnotable(2, next(ng2), idnums=next(idnum), ordenat=next(s_ord), ordre2=o2, solucions=True),
        ]
    pvar = quantilvar(opcions["var"]["una_variable"])
    p = P([1, 1, 2]).flex(1, pvar)

    tsols = crea_exercici(doc, opcions,
                          g,
                          p,
                          enunciat=enunciat,
                          cols=2,
                          espai_apartat=4,
                          mates_solus=True,
                          stretch_solus=stretch_per("polis"),
                          es_spoiler=True,
                          )
    return [enunsols, tsols]


def px_idnot_identitat(doc, opcions):
    enunciat = "Desenvolupa les següents identitats notables."
    enunsols = "Identitats notables."

    tipus = [x for x in [1, 2, 3] if x in get_var(opcions, "tipus", [1, 2, 3])]  # 1: (a+b), 2: (a-b), 3: (a+b)(a-b)
    inici = [x for x in [1, 2] if x in tipus]
    if len(inici) > 1:
        inici = random.sample(inici, 1)  # si tinc 1 i 2, me'n quedo només un per començar

    ng1 = regenerable([2, 3], 2)  # per anar alternant aleatori pels nivells 2 i 3 a la g[1]
    ng2 = regenerable([4, 5])     # per anar alternant aleatori pels nivells 4 i 5 a la g[2]
    idnum = regenerable(tipus, inici)  # començo per 1 o 2
    s0_1, s0_2, s0_3 = [ampliable([x+1 for x in range(10)]) for _ in range(3)]

    def f0():
        t = next(idnum)  # trio quin tipus toca
        seed = next([s0_1, s0_2, s0_3][t-1])  # agafo una llavor del tipus que ha tocat
        return gen.idnotable(1, 1, idnums=t, fcoefb=seed, solucions=True)

    g = [
        f0,                                                                       # (x+B)
        lambda: gen.idnotable(1, next(ng1), idnums=next(idnum), solucions=True),  # (Ax+B) i (x^n+B)
        lambda: gen.idnotable(1, next(ng2), idnums=next(idnum), solucions=True),  # multivar (Axy+B) i (Ax+By)
        lambda: gen.idnotable(1, 6, idnums=next(idnum), solucions=True),          # doble multimonomi
        ]
    pvar = quantilvar(opcions["var"]["una_variable"])
    p = P([1, 1, 1, 1]).flex(1, pvar)

    tsols = crea_exercici(doc, opcions,
                          g,
                          p,
                          enunciat=enunciat,
                          cols=2,
                          espai_apartat=4,
                          mates_solus=True,
                          stretch_solus=stretch_per("polis"),
                          es_spoiler=True,
                          )
    return [enunsols, tsols]


def px_idnot_omplebuits(doc, opcions):
    enunciat = "Omple els buits de les identitats notables següents."
    enunsols = "Omplir buits d'identitats notables."

    tipus = [x for x in [1, 2] if x in get_var(opcions, "tipus", [1, 2])]  # 1: (a+b), 2: (a-b)
    inici = [x for x in [1, 2] if x in tipus]
    if len(inici) > 1:
        inici = random.sample(inici, 1)  # si tinc 1 i 2, me'n quedo només un per començar

    ng1 = regenerable([2, 3], 2)  # per anar alternant aleatori pels nivells 2 i 3 a la g[1]
    ng2 = regenerable([4, 5])  # per anar alternant aleatori pels nivells 4 i 5 a la g[2]
    idnum = regenerable(tipus, inici)  # començo per 1 o 2
    s0 = ampliable([x for x in range(3, 11)])  # llavor per (x±b). Evito b=a i b=2a perquè el generador ho demana

    pvar2 = quantilvar(opcions["var"]["ordenat"])
    s_ord = alt_var(opcions, pvar2)
    o2 = opcions["var"]["ordre"] == "2"

    buits = var_quines(opcions, "buits", [2, 3])
    s_buits = alt_p_var(opcions, P([1 for _ in buits]), buits)  # reparteixo qtats de termes a parts iguals

    def f0():
        t = next(idnum)  # trio quin tipus toca
        return gen.idnotable(3, 1, idnums=t, fcoefb=next(s0), ordenat=next(s_ord), ordre2=o2,
                             buits=next(s_buits), solucions=True)

    g = [  # g[0]: (x+B)   //   g[1]: (Ax+B) i (x^n+B)   //   g[2]: multivar (Axy+B) i (Ax+By)
        f0,
        lambda: gen.idnotable(3, next(ng1), idnums=next(idnum), ordenat=next(s_ord), ordre2=o2,
                              buits=next(s_buits), solucions=True),
        lambda: gen.idnotable(3, next(ng2), idnums=next(idnum), ordenat=next(s_ord), ordre2=o2,
                              buits=next(s_buits), solucions=True),
        ]

    pvar = quantilvar(opcions["var"]["una_variable"])
    p = P([1, 3, 3]).flex(1, pvar)

    tsols = crea_exercici(doc, opcions,
                          g,
                          p,
                          enunciat=enunciat,
                          cols=2,
                          espai_apartat=4,
                          mates_solus=True,
                          stretch_solus=stretch_per("polis"),
                          es_spoiler=True,
                          )
    return [enunsols, tsols]


def px_mops_divideix(doc, opcions):
    enunciat = "Fes les següents divisions de monomis."
    enunsols = "Divisions de monomis."

    pvar = quantilvar(opcions["var"]["una_variable"])
    p = P([2, 3, 3]).flex(0, pvar)

    pvar2 = quantilvar(opcions["var"]["positiu"])
    s_pos = alt_var(opcions, pvar2)

    g = [
        lambda: gen.op_monomis(3, 1, noneg=next(s_pos), solucions=True),
        lambda: gen.op_monomis(3, 2, noneg=next(s_pos), solucions=True),
        lambda: gen.op_monomis(3, 3, noneg=next(s_pos), solucions=True),
        ]

    tsols = crea_exercici(doc, opcions,
                          g,
                          p,
                          enunciat=enunciat,
                          cols=2,
                          mates_solus=True,
                          es_spoiler=True,
                          )
    return [enunsols, tsols]


def px_mops_multiplica(doc, opcions):
    enunciat = "Fes les següents multiplicacions de monomis."
    enunsols = "Multiplicacions de monomis."

    pvar = quantilvar(opcions["var"]["una_variable"])
    p = P([2, 3, 3]).flex(0, pvar)

    pvar2 = quantilvar(opcions["var"]["positiu"])
    s_pos = alt_var(opcions, pvar2)

    g = [
        lambda: gen.op_monomis(2, 1, noneg=next(s_pos), solucions=True),
        lambda: gen.op_monomis(2, 2, noneg=next(s_pos), solucions=True),
        lambda: gen.op_monomis(2, 3, noneg=next(s_pos), solucions=True),
        ]

    tsols = crea_exercici(doc, opcions,
                          g,
                          p,
                          enunciat=enunciat,
                          cols=2,
                          mates_solus=True,
                          es_spoiler=True,
                          )
    return [enunsols, tsols]


def px_mops_sumairesta(doc, opcions):
    enunciat = "Fes les següents sumes i restes de monomis."
    enunsols = "Sumes i restes de monomis."

    pvar = quantilvar(opcions["var"]["una_variable"])
    p = P([1, 1]).flex(0, pvar)

    pvar2 = quantilvar(opcions["var"]["ordenat"])
    s_ord = alt_var(opcions, pvar2)

    g = [
        lambda: gen.op_monomis(1, 1, ordenat=next(s_ord), solucions=True),
        lambda: gen.op_monomis(1, 2, ordenat=next(s_ord), solucions=True),
        ]

    tsols = crea_exercici(doc, opcions,
                          g,
                          p,
                          enunciat=enunciat,
                          cols=2,
                          espai_apartat=10,
                          mates_solus=True,
                          es_spoiler=True,
                          )
    return [enunsols, tsols]


def px_ops_divideix(doc, opcions):
    enunciat = "Fes les següents divisions de polinomis."
    enunsols = "Divisions de polinomis."
    g = [
        lambda: gen.px(5, 1, solucions=True),  # ordenat complet exacte
        lambda: gen.px(5, 2, solucions=True),  # ordenat complet
        lambda: gen.px(5, 3, solucions=True),  # ordenat
        lambda: gen.px(5, 4, solucions=True),  # desordenat
        ]
    pvar = quantilvar(opcions["var"]["ordenat"])
    p = P([1, 1, 2, 4]).flex(2, pvar)

    tsols = crea_exercici(doc, opcions,
                          g,
                          p,
                          enunciat=enunciat,
                          espai_apartat=10,
                          )
    return [enunsols, tsols]


def px_ops_divideixruffini(doc, opcions):
    enunciat = "Fes les següents divisions aplicant la regla de Ruffini."
    enunsols = "Divisions per Ruffini."
    g = [
        lambda: gen.px(4, 1, solucions=True),  # ordenat complet exacte
        lambda: gen.px(4, 2, solucions=True),  # ordenat complet
        lambda: gen.px(4, 3, solucions=True),  # ordenat
        lambda: gen.px(4, 4, solucions=True),  # desordenat
        ]
    pvar = quantilvar(opcions["var"]["ordenat"])
    p = P([1, 1, 2, 4]).flex(2, pvar)

    tsols = crea_exercici(doc, opcions,
                          g,
                          p,
                          enunciat=enunciat,
                          espai_apartat=10,
                          )
    return [enunsols, tsols]


def px_ops_multiplica(doc, opcions):
    enunciat = "Fes les següents multiplicacions de polinomis."
    enunsols = "Multiplicacions de polinomis."
    g = [
        lambda: gen.px(3, 1, solucions=True),  # ordenat complet
        lambda: gen.px(3, 2, solucions=True),  # ordenat incomplet
        lambda: gen.px(3, 3, solucions=True),  # desordenat amb tots els t-indep
        lambda: gen.px(3, 4, solucions=True),  # desordenat amb mínim un t-indep
        lambda: gen.px(3, 5, solucions=True),  # desordenat pot sense t-indep
        ]
    pvar = quantilvar(opcions["var"]["ordenat"])
    p = P([2, 2, 1, 1, 3]).flex(1, pvar)

    tsols = crea_exercici(doc, opcions,
                          g,
                          p,
                          enunciat=enunciat,
                          espai_apartat=10,
                          mates_solus=True,
                          )
    return [enunsols, tsols]


def px_ops_parametreresidu(doc, opcions):
    enunciat = "Fes servir la informació donada per calcular en cada cas el valor del paràmetre:"
    enunsols = "Paràmetre sabent residu."

    # filtro només lletres normals, per si algú canvia l'html amb inspect o què sé jo
    parametres = [re.sub("[^a-yzA-YZ]+", "", c) for c in get_var(opcions, "parametres", ["k", "m", "a"])
                  if len(c) == 1] or ["k"]

    narratives = [n for n in get_var(opcions, "narratives", ["divi", "img"])] or ["divi", "img"]

    p = P([1, 1, 1, 1, 1, 1])

    pvar = quantilvar(opcions["var"]["residu_zero"])
    s_res = alt_var(opcions, pvar)

    s_par = regenerable(parametres)
    s_nar = regenerable(narratives * 2, narratives)

    g = [
        # k = coeficient sencer
        lambda: gen.px(106, 1 if next(s_res) else 11, par=next(s_par), nar=next(s_nar), solucions=True),
        # k = factor d'un coeficient
        lambda: gen.px(106, 2 if next(s_res) else 12, par=next(s_par), nar=next(s_nar), solucions=True),
        # k = factor de més d'un coeficient
        lambda: gen.px(106, 3 if next(s_res) else 13, par=next(s_par), nar=next(s_nar), solucions=True),
        # k = sumand d'un coeficient
        lambda: gen.px(106, 4 if next(s_res) else 14, par=next(s_par), nar=next(s_nar), solucions=True),
        # k = sumand de més d'un coeficient
        lambda: gen.px(106, 5 if next(s_res) else 15, par=next(s_par), nar=next(s_nar), solucions=True),
        # k = factors i sumands barrejats
        lambda: gen.px(106, 6 if next(s_res) else 16, par=next(s_par), nar=next(s_nar), solucions=True),
        ]

    tsols = crea_exercici(doc, opcions,
                          g,
                          p,
                          enunciat=enunciat,
                          espai_apartat=10,
                          mates=False,
                          )
    return [enunsols, tsols]


def px_ops_resta(doc, opcions):
    enunciat = "Fes les següents restes de polinomis."
    enunsols = "Restes de polinomis."
    g = [
        lambda: gen.px(2, 1, noneg=True, solucions=True),   # ordenat complet, sense doble negatiu
        lambda: gen.px(2, 1, noneg=False, solucions=True),  # ordenat complet
        lambda: gen.px(2, 2, solucions=True),               # ordenat incomplet
        lambda: gen.px(2, 3, solucions=True),               # desordenat
        ]
    pvar = quantilvar(opcions["var"]["ordenat"])
    p = P([[1, {"max": 3}], 1, 2, 2]).flex(2, pvar)

    tsols = crea_exercici(doc, opcions,
                          g,
                          p,
                          enunciat=enunciat,
                          espai_apartat=10,
                          mates_solus=True,
                          )
    return [enunsols, tsols]


def px_ops_suma(doc, opcions):
    enunciat = "Fes les següents sumes de polinomis."
    enunsols = "Sumes de polinomis."
    g = [
        lambda: gen.px(1, 1, solucions=True),  # ordenat complet
        lambda: gen.px(1, 2, solucions=True),  # ordenat incomplet
        lambda: gen.px(1, 3, solucions=True),  # desordenat
        ]
    pvar = quantilvar(opcions["var"]["ordenat"])
    p = P([1, 1, 2]).flex(1, pvar)

    tsols = crea_exercici(doc, opcions,
                          g,
                          p,
                          enunciat=enunciat,
                          espai_apartat=10,
                          mates_solus=True,
                          )
    return [enunsols, tsols]


def px_ops_teoremaresidu(doc, opcions):
    enunciat = "Calcula el residu."
    enunsols = "Calcular residus."
    tsols = crea_exercici(doc, opcions,
                          lambda: gen.px(6, 2, solucions=True),
                          enunciat=enunciat,
                          espai_apartat=10,
                          mates=False,
                          )
    return [enunsols, tsols]


# ----------------------------------------------------------------------------------------- #
def exercici_no_trobat(doc, opcions):
    needspace(doc, 8)
    question(doc, "42")
    doc.append("No s'ha trobat cap constructor per l'exercici " + opcions["exnom"].upper())
    return


# ******************************* Esquelets ********************************* #
def crea_exercici(doc, opcions, g, p=None, enunciat="EM FALTA L'ENUNCIAT, NEN", cols=1, scale=1,
                  espai_min=10, espai_apartat=4, espai_final=0, mates=True,
                  mates_solus=False, stretch_solus=None, es_spoiler=False):
    """Munta un exercici LaTeX (exercici sense varietat interna) a partir de les seves dades.

    :param doc: document on posarem l'exercici
    :param opcions: opcions que ens passa el formulari de l'exercici
    :param g: llista de funcions generadores (lambdes passades des de fora)
    :param p: llista de quantils (objecte P)
    :param enunciat: l'enunciat que vols
    :param cols: quantitat de columnes que tindrà l'exercici
    :param scale: coeficient d'ampliació del text (per fer llegibles les fraccions, i tal)
    :param espai_min: espai que necessito (i que si no el tinc vull saltar de pàgina)
    :param espai_apartat: espai vertical entre elements (mm) - per defecte 0.4 (una mica d'interlineat)
    :param espai_final: espai després del multicol (mm)
    :param mates: l'apartat és tot notació matemàtica (cal fer '$text$' en lloc de 'text')
    :param mates_solus: les solucions són notació matemàtica (cal fer '$solu$' en lloc de 'solu')
    :param stretch_solus: ampliació de l'interlineat de les solucions (1 = normal)
    :param es_spoiler: si és True, només escriuré la solució si és en una plana a part

    :return: res (només afegeix l'exercici al doc)
    """
    varietat = True  # True és que hi ha més d'un generador dins el mateix exercici (i.e. dificultats graduals, etc)
    try:
        len(g)
    except:
        varietat = False

    n = quantes(opcions)
    punts = opcions["punts"]
    try:
        punts = int(punts)
        punts = max(0, min(1000000, punts))  # (mateixos límits que a quantes.html)
    except:
        punts = 0

    needspace(doc, espai_min)
    question(doc, f"{n*punts}")
    doc.append(enunciat)

    begin(doc, 'parts')
    begin(doc, 'multicols', cols) if cols > 1 else None  # la jerarquia LaTeX quedava més neta posat així

    sols = []  # llista amb la solució de cada apartat

    if varietat:  # poliexercici (diferents generadors al llarg dels apartats)
        # precàlculs
        if not p:
            print("COMPTE: no li has passat els percentatges a crea_exercici")
            p = P([100])
        gs = g_list(n, g, p)
    else:  # monoexercici (mateix generador tots els apartats)
        gs = (g for _ in range(n))

    for _ in range(0, n):
        part(doc)
        generat = next(gs)()
        if type(generat) == tuple:  # 'generat' serà <str> si l'ex. no porta solució, o <tuple> si sí que en porta
            text = generat[0]
            sols.append(generat[1])
        else:  # si no ve amb solució
            text = generat

        if mates:
            text = f"${text}$"
        if scale != 1:
            pkgs(doc, ['graphicx'])  # entro el pkg que cal per fer scale
            text = r"\scalebox{%s}{%s}" % (scale, text)

        doc.append(NoEscape(f"{text}"))
        space(doc, cm(espai_apartat)) if espai_apartat else None

    end(doc, 'multicols') if cols > 1 else None
    space(doc, cm(espai_final)) if espai_final else None
    end(doc, 'parts')
    if sols and ("solucions" in opcions and opcions["solucions"]):  # afegeixo solus a sota (o retorno pel final del doc
        if not es_spoiler or opcions["solulloc"] == "apart":
            if opcions["solulloc"] == "intercalat":
                blocsolucions(doc, sols, mates=mates_solus, stretch=stretch_solus)
            else:
                tsols = textsolucions(doc, sols, mates=mates_solus, stretch=stretch_solus)
                return tsols  # retorna les solucions que posaria si faig llista de solucions al final
    return


# **************************** Complementàries ****************************** #
def quantes(opcions):
    q_alt = opcions.get("q_alt", "def")

    if opcions["quantes"] != "tria":
        i = ["no", "poques", "normal", "moltes", "mitja", "plana", "doble"].index(opcions["quantes"])
        return qtats.quantitats_de(opcions["exnom"], alt=q_alt)[i]
    else:
        q = opcions["qtriada"]
        try:
            q = int(q)
            q = max(1, min(qtats.quantitats_de(opcions["exnom"])[-1], q))  # (no limito a q_alt pq formulari tampoc)
        except:
            print("Has fet alguna cosa rara amb la quantitat triada...")
            q = 1
        return q


def quantilvar(var):
    """retorna el quantil on acaba la variable (per les opcions dels exercicis)"""
    try:
        v = ["no", "poques", "meitat", "moltes", "totes"].index(var)
    except:
        v = 2
    return v*100//4


def get_var(opcions, key, default=None):
    """Agafa la variable demanada de la secció de variables de l'exercici (o retorna default si no la troba)."""
    return opcions.get("var", {}).get(key, default)


def var_quines(opcions, key, default):
    return [x for x in default if x in get_var(opcions, key, default)]


def g_list(n, g, p, amb_index=False):
    """Retorna un generador amb 'quina funció de g cal fer servir per cada apartat'

    :param n: quants apartats hi haurà
    :param g: llista de funcions que faré servir
    :param p: objecte de percentatges P
    :param amb_index: per si cal retornar l'índex - TODO crec que no caldrà, pq li passo generador a la lambda
    """
    p = p.get()  # extrec els percentatges
    # preprocessing
    maxs = []
    for i, pi in enumerate(p):
        try:  # agafo les opcions  ...si és num (sense opcions) no podrà fer pi[1] i saltarà a baix
            maxs.append(pi[1].get("max", 100000))  # el get és per si hi ha opcions però no "max" dins les opcions
            p[i] = pi[0]  # deixo el num sol
        except:
            maxs.append(100000)  # random altíssim (és prou alt segur, pq l'abecedari capa a uns 600 apartats màxim)

    if len(p) + 1 == len(g) and p[-1] != 100:  # permeto no escriure l'últim 100
        p.append(100)
    if len(p) != len(g):  # si no quadra, malament
        for _ in range(n):
            if amb_index:
                yield 0, lambda: "no em quadren els quantils"
            else:
                yield lambda: "no em quadren els quantils"
    elif p[-1] != 100:
        p[-1] = 100

    # muntatge
    count = [0, 0]  # [apartat, quants]
    for x in range(n):  # per cada apartat de l'exercici
        for i in range(len(g)):  # comprova quina g li toca fer servir
            if (x+1)*1000 <= (p[i]*n)*10+1 or (x == 0 and p[0]):  # *1000 / *10+1 arregla problemes d'arrodoniment
                if i != count[0]:  # comença una nova g (reset comptador)
                    count = [i, 0]
                if count[1] < maxs[i]:  # encara puc fer servir aquesta g
                    if amb_index:
                        yield i, g[i]
                    else:
                        yield g[i]
                    count[1] += 1
                    break
                else:  # ja tinc el màxim (baixo la p actual per forçar la g següent)
                    p[i] = 0

        else:  # si no break (si no li toca res, li toca l'últim)
            if amb_index:
                yield len(g)-1, g[-1]
            else:
                yield g[-1]

    print("s'han acabat les pregenerades... (retorno l'última ja per sempre)")
    if amb_index:
        yield len(g)-1, g[-1]
    else:
        yield g[-1]


def p_ns(n, p):
    """Retorna les quantitats d'exercicis que hi haurà de cada tipus (...aprox?).
          ...tq pregeneradors com el de finorg puguin decidir quantes (i quines)
          coses incloure per a cadascuna de les gs (tl;dr: penso en n_finorg).

    :param n: quantitat total d'apartats (100%).
    :param p: objecte de percentatges P
    """
    p = p.get()  # extrec els percentatges
    ns = [round(n*pi[0]/100) for pi in p]  # tradueixo les proporcions acumulades a absoluts acumulats
    sum = 0
    for i, q in enumerate(ns):  # converteixo a absoluts (no acumulats) i aplico els màxims
        qmax = p[i][1]["max"]
        q = min(q-sum, qmax)
        sum += q
        ns[i] = q
    if sum < n:
        ns[-1] += n-sum
    return ns


def alt_var(opcions, pvar):
    """Generador (inf): True mentre estem dins la zona de 'sí' de la variant escollida, False la resta."""
    return with_default((True for _ in range(round(pvar*quantes(opcions)/100))), False)


def alt_p_var(opcions, p, valors):
    """Generador (inf): retorna el valor que toqui en funció de la zona (i.e. alt_var no binari).

    :param opcions: llista d'opcions de l'exercici (en treu la n total)
    :param p: proporcions de les variants (objecte P)
    :param valors: llista de valors a retornar (un per cada variant)
    """
    ns = p_ns(quantes(opcions), p)
    for n, v in zip(ns, valors):
        for _ in range(n):
            yield v
    while True:
        yield valors[-1]


def regenerable(llista, inici=None):
    """Generador (inf): gasta aleatòriament els elements d'una llista, i quan la llista es gasta torna a començar.
       (...compte, que no fa deep copy!)

    :param llista: llista completa (tot el que hi vull quan reinicio)
    :param inici: element o llista inicial (elements, ordenats, que vull posar abans de l'aleatori)
    """
    try:  # per si he entrat element sense llista
        len(inici)
    except TypeError:
        inici = [inici]

    inici = [x for x in inici if x in llista]  # filtro per si de cas he demanat inicis que no tenia

    if inici:
        for x in inici:  # començo amb les de la llista inicial
            yield x
        opcions = [x for x in llista if x not in inici]  # continuo amb les que encara no he fet servir
    else:
        opcions = []

    while True:
        if not opcions:
            opcions = llista[:]  # copia la llista completa (si només faig referència, alteraré la original amb el pop)
            random.shuffle(opcions)
        yield opcions.pop()


def etern(x):
    """Retorna el mateix valor per sempre"""
    while True:
        yield x


def ampliable(llista, n=3):
    """Generador (inf): retorna aleatori de la llista, i quan es gasta amplia amb números (abs) més grans

    :param llista: llista inicial, que retornaré en ordre aleatori
    :param n: quantitat de números (a banda i banda, si s'escau) a afegir amb cada ampliació
    """
    maxim = max(llista)
    minim = min(llista)
    while True:
        random.shuffle(llista)
        for x in llista:
            yield x
        llista = [x+maxim+1 for x in range(n)]
        maxim += n
        if minim < 0:
            llista += [minim-1-x for x in range(n)]
            minim -= n


def with_default(seeds, default=None):
    """Afegeix al generador un valor per defecte per tornar alguna cosa quan el generador s'hagi gastat."""
    yield from seeds  # mentre hi hagi pregenerats, els agafo
    while True:
        yield default  # quan es gasten, retorno res (deixo llibertat a l'exercici)


def espai_per(tal):
    espais = {
        "res": 0,  # enganxadots
        "interlineat": 4,  # separació normal mínima entre apartats
        "una": 10,  # una línia de resposta
    }
    return 42 if tal not in espais else espais[tal]


def stretch_per(tal):
    stretches = {
        "arrels": 1.3,
        "exp_frac": 1.2,
        "polis": 1.2,
        "fracs": 1.3,
        "fraccions": 1.3,
        "algebs": 1.4,
    }
    return 1 if tal not in stretches else stretches[tal]


def cm(mm):
    return f"{mm // 10}.{mm % 10}cm"


def scale_per(tal):
    """Coeficient d'augment (zoom) per diferents coses.

       pot ser: fraccions, ...
    """
    scales = {
        "fraccions": 1.3,
    }
    return scales.get(tal, 1)  # (torna "1" si no el troba)

def moneda():
    return bool(random.getrandbits(1))