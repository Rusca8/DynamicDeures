import math
import random

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
    #return en.lleisgasos(tipus, p1, p2, v1, v2, t1, t2, cunit, sabemt, simples, si, solucions)


for _ in range(6):
    print(lleisgasos(4))