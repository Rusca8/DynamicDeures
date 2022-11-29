import math
import random
from copy import deepcopy

import enunciats as en
import cryptolator as crypt
from classes import Px, npx, Mx, Fr, Mul


def moneda():
    return bool(random.getrandbits(1))


def comb(tipus, nivell=1, nums=1):
    text = "42"
    if tipus == 1:  # A+B
        if nivell == 1:  # (innecessari) A positiva, resultat positiu
            a = random.randint(1, 9 * nums)
            b = random.randint(-a, 10 * nums)
            if b >= 0:
                b = f'+{b}'
            text = f'{a}{b}='
        elif nivell == 2:  # A positiva
            a = random.randint(1, 10 * nums)
            b = random.randint(-10 * nums, 8 * nums)
            if b >= 0:
                b = f'+{b}'
            text = f'{a}{b}='
        elif nivell == 3:  # nums qualssevol
            a = random.randint(-10 * nums, 10 * nums)
            b = random.randint(-10 * nums, 10 * nums)
            if b >= 0:
                b = f'+{b}'
            text = f'{a}{b}='
    if tipus == 2:  # A±(±B)
        if nivell == 1 or nivell == 2:  # A positiva, sense -(-B) || amb -(-B)
            a = random.randint(1, 10 * nums)
            b = random.randint(-10 * nums, 10 * nums)
            if b > 0:
                text = f'(+{b})'
                if moneda():
                    text = f'{a}+' + text + "="
                else:
                    text = f'{a}-' + text + "="
            else:
                if nivell == 1 or moneda():
                    text = f'{a}+({b})='
                else:
                    text = f'{a}-({b})='
        elif nivell == 3:  # A qualsevol
            a = random.randint(-10 * nums, 10 * nums)
            b = random.randint(-10 * nums, 10 * nums)
            if b > 0:
                text = f'(+{b})'
                if moneda():
                    text = f'{a}+' + text + "="
                else:
                    text = f'{a}-' + text + "="
            else:
                if nivell == 1 or moneda():
                    text = f'{a}+({b})='
                else:
                    text = f'{a}-({b})='

    elif tipus == 3:  # A*B
        if nivell == 1 or nivell == 4:  # taules de multiplicar || divisions senzilles
            if nivell == 1:  # mult
                taula = random.randint(1, 10 + 2 * (nums - 1))  # nums inclou 11 i 12...
                text = taules(taula)
            else:  # div
                b = random.randint(1, 10 + 2 * (nums - 1))
                a = random.randint(1, 10)
                text = fr'{a * b}\div {a}'
        elif (nivell == 2 or nivell == 3) or (
                nivell == 5 or nivell == 6):  # (taules amb un signe || amb dos signes) || divisions
            a = random.randint(-10 - 2 * (nums - 1), 10 + 2 * (nums - 1))
            b = random.randint(1, 10)
            symbol = r'\times '
            if nivell == 5 or nivell == 6:  # adapto per div
                if a == 0:  # evito dividir per zero
                    a = random.randint(1, 10 + 2 * (nums - 1))
                aux = a
                a = a * b
                b = abs(aux)
                symbol = r'\div '
            if (nivell == 3 or nivell == 6 or a >= 0) and moneda():
                b = f'(-{b})'
            else:
                if moneda():
                    b = f'{b}'
                else:
                    b = f'(+{b})'
            if moneda():
                text = fr'{a}{symbol}{b}='
            else:
                if a > 0:
                    text = fr'(+{a}){symbol}{b}='
                elif a == 0:
                    text = fr'{a}{symbol}{b}'
                else:
                    text = fr'({a}){symbol}{b}='
    return text


def mixcomb(num, inception=1, op=0, previ=0, doblesigne=True, out=0, ops=[1, 2, 3], hide=[]):
    ops = ops[:]  # operacions seleccionades al formulari
    quadrats = [1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144]
    text = "42+6·7"
    maxn = 10
    if out == 0:
        out = inception

    if inception < 1:
        inception = 0
        if (4 in ops and not (4 in hide)) and (num in list(range(1, 12)) and moneda()):
            text = "\\sqrt{" + f"{pow(num, 2)}" + "}"
        elif (5 in ops and not (5 in hide)) and (num in quadrats):
            text = f"{isqrt(num)}"
            if num == 1:
                if random.choice([1, 1, 0]):
                    text = "1"
                else:
                    text = "(-1)^2"
            else:
                if moneda():
                    text = "{" + text
                else:
                    text = "{(-" + text + ")"
                text = text + "}^2"
        else:
            text = f"{num}"
    else:
        if op == 0:  # aleatori
            opcions = [1, 2, 3]
            muldivscore = len(divisors(num))
            if muldivscore == 1:  # num primers més sovint suma
                opcions += [1, 1]
                if 3 in opcions:
                    opcions.remove(2)
                    opcions.append(3)
            elif muldivscore > 3 or num == 0:  # num amb molts divisors més sovint mul div
                opcions += [2, 2, 3, 3]

            if (5 in ops and not (5 in hide)) and (num in quadrats):
                op = 5
            elif (4 in ops and not (4 in hide)) and (num in list(range(1, 12)) and random.choice([0, 0, 1])):
                op = 4  # sqrt
            else:
                op = random.choice(opcions)  # sum mul div

        if op == 1:  # suma
            a = random.randint(1, maxn * inception)
            if random.choice([0, 0, 1]):
                a = -a
            if a == num:
                if a == 1 or moneda():
                    a += 1
                else:
                    a -= 1

            b = num - a  # n = a + b

            t1 = f"{mixcomb(a, inception - 1, 0, 1, doblesigne, out, ops)}"
            t2 = f"{mixcomb(b, inception - 1, 0, 1, doblesigne, out, ops)}"
            if t2[0] == "-":
                if doblesigne and random.randint(1, 5) == 1:  # A+(-B) / A-B
                    text = f"{t1}+({t2})"
                else:
                    text = f"{t1}{t2}"
            else:
                if doblesigne and random.randint(1, 5) == 1 and t2 != 0:  # A-(-B) / A+B
                    text = f"{t1}-(-{t2})"
                else:
                    text = f"{t1}+{t2}"
            if previ in [2, 3]:
                text = f"({text})"

        elif op == 2:  # multi
            if inception == 1 and num in [-1, 1]:  # evito 1*1
                text = f"{num}"
            else:
                if num == 0:
                    a = random.randint(1, maxn * inception)
                else:
                    a = random.choice(divisors(num))
                if random.choice([0, 0, 1]):
                    a = -a
                if moneda():
                    b = a
                    a = num // b
                else:
                    b = num // a
                t1 = f"{mixcomb(a, inception - 1, 0, 2, doblesigne, out, ops)}"
                t2 = f"{mixcomb(b, inception - 1, 0, 2, doblesigne, out, ops)}"
                if t2[0] == "-":  # ±A*(-B)
                    text = f"{t1}\\cdot ({t2})"
                else:  # ±A*B
                    text = f"{t1}\\cdot {t2}"

            if previ == 3:
                text = f"({text})"

        elif op == 3:  # divi
            if abs(num) > 11 and num % 10 != 0:  # evito divisions exagerades
                if num > 13:
                    b = 2
                else:
                    b = random.choice([2, 3])
            else:
                b = random.randint(3, maxn // 2)
            if random.choice([0, 0, 1]):
                b = -b
            a = num * b

            t1 = f"{mixcomb(a, inception - 1, 0, 3, doblesigne, out, ops)}"
            t2 = f"{mixcomb(b, inception - 1, 0, 3, doblesigne, out, ops)}"
            if t2[0] == "-":  # ±A:(-B)
                text = f"{t1}:({t2})"
            else:  # ±A:B
                text = f"{t1}:{t2}"
            if previ == 3:
                text = f"({text})"

        elif op == 4:  # sqrt (no gasta nivell)
            text = "\\sqrt{" + f"{mixcomb(pow(num, 2), inception, 0, 4, doblesigne, out, ops, hide=[4, 5])}" + "}"

        elif op == 5:  # pow (no gasta nivell)
            n = isqrt(num)
            if moneda():
                n = -n
            text = "{(" + f"{mixcomb(n, inception, 0, 5, doblesigne, out, ops, hide=[5, 4])}" + ")}^2"

    if inception == out:
        return squarebracketer(text)
    else:
        return text


def decimals(tipus, notac=1, fsigne=0):
    """Retorna un número decimal del tipus escollit

    :param tipus: 1 exacte, 2 mixt, 3 pur, 4 aleatori
    :param notac: notació (1 barra, 2 suspensiu)
    :param fsigne: forçar signe (exemple de num amb mateix signe que es vol obtenir; 0 = no forçat)
    """
    text = "42.42424242..."

    if (not fsigne and moneda()) or fsigne > 0:
        s = ""
    else:
        s = "-"

    if tipus in [1, 2, 3]:  # exacte, mixt, pur
        # part entera
        e = random.randint(0, random.choice([9, 12]))

        # decimals no periòdics
        if tipus == 3:  # pur (no en té)
            n = ""
        elif tipus == 1:  # exacte (evito 2.0)
            n = random.randint(1, random.choice([9, random.choice([99, 999])]))
            if not n % 10:
                n += 1
        else:  # mixt (fins a un o dos decimals, 50%/50%)
            n = random.randint(0, random.choice([9, 99]))

        # part periòdica
        if tipus == 1:  # exacte (no en té)
            p = ""
        else:  # fins a un, dos o tres decimals (50%/25%/25%, però evito molts si n és llarg)
            pmax = 99 if n and n > 9 else random.choice([99, 999])
            p = random.randint(1, random.choice([9, pmax]))

        # control
        if p:  # p té control complet de la divisibilitat per 9, perquè (enp-en)%9 = p%9
            if p > 10:  # forço divisible per 3 o 9
                m9 = p % 9
                if m9 > 4:
                    m9 = m9-9
                if abs(m9) < 3:  # per 9
                    p += -m9
                else:  # per 3
                    m3 = p % 3
                    if m3 == 2:
                        m3 = -1
                    p += - p % 3
            elif n:  # forço divisible per 3
                p += -p % 3
        else:
            if n % 5 and n % 2 and not (n < 10 and not e):
                if n % 10 == 9:
                    n -= 1
                else:
                    n += 1

        # muntatge
        if notac == 1:
            if p:
                text = f"{e}.{n}" "\\overline{" f"{p}" "}"
            else:
                text = f"{e}.{n}"
        elif notac == 2:
            if p:
                if len(f"{p}") < 3:
                    text = f"{e}.{n}{p}{p}{p}..."
                else:
                    text = f"{e}.{n}{p}{p}..."
        text = s + text

        # solus
        num = int(f"{e}{n}{p}") - int(f"{e}{n}") or int(f"{e}{n}")
        den = int("".join(["9" for _ in f"{p}"] or "1") + "".join("0" for _ in f"{n}"))
        num, den = fracsimple(num, den)
        solu = s + r"\frac{%s}{%s}" % (num, den)

        return text, solu

    elif tipus == 4:  # barrejats
        return decimals(random.randint(1, 4), notac=notac)

    return "0.67\\overline{42}"  # just in case


def ncient(tipus, nivell=1, direc=0, signes=0, termes=3):
    """retorna exercicis de notació científica

    :param tipus: 1 num a not, 2 not a num
    :param nivell: dificultat de l'exercici (10, n*10, r*10)
    :param direc: signe exp (0 qualsevol, 1 múltiples, 2 submúltiples)
    :param signes: signe num (0 qualsevol, 1 positiu, 2 negatiu)
    :param termes: quan tipus 3, quantitat de nums a operar
    """
    text = "4.2\\cdot 10^{42}"
    if tipus == 1:  # de num a notació
        # num base
        if nivell in [1, 2]:
            if nivell == 1:  # 10^x
                num = 1
                signe = ""
            elif nivell == 2:  # z·10^x
                num = random.randint(2, 9)
                if not signes:
                    signe = random.choice(["", "", "-"])
                elif signes == 1:
                    signe = ""
                else:
                    signe = "-"

            if direc == 1 or (moneda() and not direc == 2):  # múltiple
                text = signe + f"{(num * pow(10, random.randint(2, 9))):,}".replace(",", ".")
            else:  # submúltiple
                while not num % 10:
                    num = num // 10
                text = signe + "0," + "".join(["0" for _ in range(random.randint(0, 8))]) + f"{num}"

        elif nivell == 3:  # r·10^x sense intercalats
            num = random.randint(11, random.choice([99, 999]))
            if not signes:
                signe = random.choice(["", "", "-"])
            elif signes == 1:
                signe = ""
            else:
                signe = "-"
            if direc == 1 or (moneda() and not direc == 2):  # múltiple
                text = f"{(num * pow(10, random.randint(0, 9 - len(f'{num}')))):,}".replace(",", ".")
            else:  # submúltiple
                while not num % 10:
                    num = num // 10
                text = signe + "0," + "".join(["0" for _ in range(random.randint(0, 8 - len(f'{num}')))]) + f"{num}"
        else:  # amb la coma pel mig del número (però mai darrera el primer decimal)
            num = random.randint(100, 99999)
            if not num % 10:  # evito 0 al final
                num += random.randint(1, 9)
            num = f"{num}"
            coma = random.randint(2, len(num) - 1)
            signe = random.choice(["", "", "-"])
            text = signe + num[:coma] + "," + num[coma:]

    elif tipus == 2:  # de notació a num
        if nivell == 1:  # 10s
            exp = random.randint(1, 9) * random.choice([-1, 1])
            if not random.randint(0, 20):
                exp = 0
            text = "10^{" f"{exp}" "}"
        elif nivell in [2, 3]:
            if not signes:
                signe = random.choice(["", "", "-"])
            elif signes == 1:
                signe = ""
            else:
                signe = "-"
            exp = random.randint(1, 9) * random.choice([-1, 1])
            if not random.randint(0, 20):
                exp = 0
            if nivell == 2:
                num = f"{random.randint(2, 9)}"
            else:
                num = random.randint(11, random.choice([99, random.choice([999, 9999])]))
                while not num % 10:
                    num = num // 10
                num = f"{num}"
                num = f"{num[0]}" "," f"{num[1:]}"
            text = signe + num + "\\cdot 10^{" f"{exp}" "}"

    elif tipus == 3:  # multis i divis
        if nivell == 1:  # línia
            talls = ["(" f"{ncient(2, 3)}"]
            for _ in range(termes - 1):
                talls.append(")" + random.choice(["\\cdot", "\\cdot", "\\div"]) + "(")
                talls.append(f"{ncient(2, 3)}")
            text = "".join(talls) + ")"
        elif nivell == 2:  # fracció
            ...

    return text


def frac(tipus, nivell=1, termes=2, dmax=6, divis=0, solucions=False):
    """
    Exercicis de fraccions

    :param tipus: 1 sum/rest, 2 mul/div
    :param nivell: 1 positiu, 2 pos/neg, 3 pot doble neg
    :param termes: quantes fraccions
    :param dmax: màx denominador (sum/rest), màx número (mul/div)
    :param divis: 0 no, 1 random, 2 sempre
    :param solucions: retornar solució
    """
    text = "42/42"
    n_sol = 0
    d_sol = 0

    if tipus == 1:  # sumes i restes (a/b + c/d)
        text = "6/42+7/42"
        if nivell in [1, 2, 3]:  # només sumes de nums positius / també restes (o numerador negatiu) / doble negatiu
            text = ""
            for x in range(termes):
                a = random.randint(1, 10)
                b = random.randint(2, dmax)
                if x != 0:
                    if nivell == 1 or moneda():
                        if nivell == 3 and moneda():  # doble neg
                            s = "-"
                            a = -a
                        else:
                            s = "+"
                    else:
                        if moneda():
                            s = "-"
                        else:
                            s = "+"
                            a = -a
                    text += s
                    n_sol, d_sol = frac_op(1 if s == "+" else 2, n_sol, d_sol, a, b)
                else:  # primera frac
                    n_sol = a
                    d_sol = b
                text += "\\frac{" + f"{a}" + "}{" + f"{b}" + "}"

    elif tipus == 2:  # multis i divis
        if nivell in [1, 2, 3]:
            text = ""
            for x in range(termes):
                a = random.randint(1, dmax)
                b = random.randint(2, dmax)
                if x != 0:
                    if divis == 0 or (divis == 1 and moneda()):
                        text += "\\cdot "
                        op = 3  # multi (per les solus)
                    else:
                        text += "\\div "
                        op = 4  # divi (per les solus)
                    if nivell == 1 or moneda():
                        if nivell == 3 and moneda():  # doble neg
                            a = -a
                            b = -b
                    else:
                        if moneda():
                            a = -a
                        else:
                            b = -b
                    n_sol, d_sol = frac_op(op, n_sol, d_sol, a, b)
                else:  # primera frac
                    n_sol = a
                    d_sol = b

                text += "\\frac{" + f"{a}" + "}{" + f"{b}" + "}"
    if solucions:
        return text, fraconum(n_sol, d_sol)
    return text


def frac_op(op, n1, d1, n2, d2):
    """fa la operació demanada amb les fraccions

    :param op: 1 suma, 2 resta, 3 multi, 4 divi
    :param n1: numerador primera fracció
    :param d1: denominador primera fracció
    :param n2: numerador segona fracció
    :param d2: denominador segona fracció
    """
    if op == 1:  # suma
        return fracsimple(n1*d2+n2*d1, d1*d2)
    elif op == 2:
        return fracsimple(n1*d2-n2*d1, d1*d2)
    elif op == 3:
        return fracsimple(n1*n2, d1*d2)
    else:
        return fracsimple(n1*d2, d1*n2)


def fracmix(num="?", den="?", inception=1, op=0, doblesigne=True, ops=[1, 2],
            calpowsqr=False, solucions=False):
    """
    Genera un exercici de fraccions combinades (i.e. activa rfracmix deixant constància del nivell més alt)
    """
    return rfracmix(num, den, inception, op=op, doblesigne=doblesigne, out=True, ops=ops,
                    calpowsqr=calpowsqr, solucions=solucions)


def rfracmix(num="?", den="?", inception=1, op=0, previ=0, doblesigne=True, out=False, ops=[1, 2], fet=set(),
            segona=False, calpowsqr=False, solucions=False):
    """
    Genera recursivament un exercici de fraccions combinades

    :param num: numerador del resultat
    :param den: denominador del resultat
    :param inception: nivell d'abstracció (aprox. quantes operacions abans d'arribar a una fracció)
    :param op: operació del nivell actual (en cas que vingui predefinida)
    :param previ: de quina operació vinc (per controlar cicles incòmodes i parèntesis)
    :param doblesigne: (sense ús actualment)
    :param out: nivell d'abstracció més alt (per gestionar la sortida)  # TODO bool=false excepte la primera crida
    :param ops: 1 sumrest, 2 muldiv (3 div), 4 sqrt, 5 pow
    :param fet: acumula les opcions escollides (per veure si hi ha mínim algun sqrt o pow)
    :param segona: marca les fraccions de la suma que no són la primera (per posar signe també si és +)
    :param calpowsqr: True és que cal que hi hagi pow o sqr sí o sí
    :param solucions: retornar solucions de l'exercici
    :return:
    """
    num = num if num != "?" else randomfracnum(3)  # si no venien pretriats els trio
    den = den if den != "?" else randomfracnum(3)

    ops = ops[:]  # operacions seleccionades al formulari
    quadrats = [1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144]
    text = "4/2+42/6*3/42"

    if out:  # nivell més extern de la recursió (primera vegada)
        fet = set()

    if inception < 1:  # tanca ja
        if den == 1:
            text = f"{num}"
            if previ in [2, 3] and num < 0 and segona:
                text = "(" + text + ")"
        else:
            if 5 in ops and all([n in quadrats for n in [num, den]]) and num*den > 0:
                # (no val la pena adaptar això per coses tipus -1/4, que sembla que no surten sovint)
                text = "(\\frac{" + f"{isqrt(abs(num))}" + "}{" + f"{isqrt(abs(den))}" + "})^2"
                fet.add(5)
            else:
                if 5 in ops:  # si permeto quadrats, faig quadrats dels nums individuals
                    if num > 1 and num in quadrats:
                        num = f"{isqrt(abs(num))}^2"
                        fet.add(5)
                    elif num < 1 and -num in quadrats:
                        num = f"-{isqrt(abs(num))}^2"
                        fet.add(5)
                    elif den > 1 and den in quadrats:
                        den = f"{isqrt(abs(den))}^2"
                        fet.add(5)
                    elif den < 1 and -den in quadrats:
                        den = f"-{isqrt(abs(den))}^2"
                        fet.add(5)
                text = "\\frac{" + f"{num}" + "}{" + f"{den}" + "}"

    else:  # no tanca
        if op == 0:  # trio operació (no n'hi havia de triada)
            if 5 in ops and previ != 4 and (all([abs(n) in quadrats for n in [num, den]])
                                            and not num == den == 1
                                            and (num*den > 0 or (out and not 4 in ops))):  # si és la de fora puc +/-
                op = 5  # faig quadrat de tot
            elif 4 in ops and previ not in [4, 5] and all([0 < n < 8 for n in [num, den]]):  # positius 1-7
                op = 4  # arrel (quan no deixa nums molt xungos)
            elif previ == 1 and 2 in ops:
                op = 2
            if not op:
                op = random.randint(1, 2)

        fet.add(op)

        if op == 1:  # sum/rest  (a/b + c/d (+e/f)) -> N = ad+cb (+e), D = bd
            # denominador
            b = random.choice(divisors(den))
            d = den // b
            # numerador
            c = 0
            exactes = []
            inexactes = []
            for x in range(-2, 3):  # -2 -> 2
                a = (num // d) + x
                if (num - a * d) % b == 0:  # si surt exacte (dues fraccions fan prou)
                    c = (num - a * d) // b
                    if a:
                        exactes.append([a, c])  # guardo les opcions
                else:
                    if a:
                        inexactes.append(a)
            if exactes:
                for x in exactes:  # faig una mica de neteja d'uns i números primers lletjos
                    if len(exactes) < 2:
                        break
                    if abs(x[0]) in [1, 13, 17, 19] or abs(x[1] in [1, 13, 17, 19]):
                        exactes.remove(x)
                a, c = random.choice(exactes)  # i en trio una
            elif inexactes:  # si no hi ha exactes trio alguna de les a (si no trio res queda l'última)
                a = random.choice(inexactes)
            if not c:
                c = (num - a * d) // b + random.choice([-1, 1])
            if not c:
                c = random.choice([-1, 1])
            # si l'aproximat amb dues fraccions no surt exacte...
            diff = num - (a * d + c * b)
            if diff:
                f = b * d
                e = diff
                e, f = fracsimple(e, f)
            a, b = fracsimple(a, b)
            c, d = fracsimple(c, d)

            # si algun denominador surt 1, robo un tall
            girats = False
            if b == 1 or d == 1:
                if b != 1:  # per no repetir codi en simètric, giro els nums i els retorno al final
                    a, c = c, a
                    b, d = d, b
                    girats = True
                """
                Tinc [a/1] + [c/d]
                Faig [a/1 - 1/q] + [c/d + 1/q]
                Que és [(aq-1)/q] + [(cq+d)/dq]
                    -> (aq-1)/q funciona sempre
                    -> (cq+d)/dq hauria de funcionar sempre que [d%q o cq%d] 
                """
                for q in random.choice([[2, 3], [3, 2]]) + [5, 7, 1]:  # si no funciona res, deixo 1 (no ho toco)
                    if d % q or c*q % d:
                        break
                k = random.choice([-1, 1])  # signe del tros robat aleatori (de vegades suma de vegades resta)
                if c*q+k*d == 0:  # compte a no deixar un zero a la nova c
                    k = -k
                a = a*q - k
                b = q
                c = c*q + k*d
                d = d*q
                # resimplifico
                a, b = fracsimple(a, b)
                c, d = fracsimple(c, d)

            if girats:
                a, c = c, a
                b, d = d, b

            # muntatge
            text = f"{rfracmix(a, b, inception - 1, previ=op, ops=ops, fet=fet)}"
            if c * d < 0:  # frac negativa
                text += f"-{rfracmix(-c, d, inception - 1, previ=op, ops=ops, fet=fet)}"
            else:  # frac positiva
                text += f"+{rfracmix(c, d, inception - 1, previ=op, ops=ops, fet=fet)}"

            if diff:
                if e * f < 0:
                    text += f"-{rfracmix(-e, f, 0, previ=op, ops=ops, fet=fet)}"
                else:
                    text += f"+{rfracmix(e, f, 0, previ=op, ops=ops, fet=fet)}"
            if previ in [2, 3]:
                text = "(" + text + ")"

        elif op == 2:  # mul/div (a/b * c/d) o (a/b : d/c)
            if num == 1 or den == 1:
                k = random.choice([2, 3, 4, 5])  # si la frac té un 1 multiplico per tenir més divisors
                num *= k
                den *= k

            # numerador
            a = random.choice(divisors(num))
            c = num // a
            # denominador
            b = random.choice(divisors(den))
            d = den // b

            # global
            k = random.choice([2, 3, 4])  # trio un número i el multiplico a dalt i a baix
            if moneda():
                k += 1
            if (moneda() or abs(a) == 1) and not abs(c) == 1:  # si hi ha 1 trio l'1, si no aleatori
                a *= k
            else:
                c *= k
            if (moneda() or abs(b) == 1) and not abs(d) == 1:  # si hi ha 1 trio l'1, si no aleatori
                b *= k
            else:
                d *= k

            # evito fraccions = 1
            if a == b or c == d:
                k = random.randint(2, 3)
                if a * k == b or d * k == c or (moneda() and not (b * k == a or c * k == d)):
                    b *= k
                    c *= k
                else:
                    a *= k
                    d *= k

            if inception == 1:  # si serà l'última vegada (a la següent entren números)
                for k in [2, 3, 4, 5, 7]:
                    if a % b != 0 or random.randint(1, 30) == 1:  # (ja) no tinc enter a l'esquerra (excepte alguns)
                        break
                    else:
                        if c * k % d != 0:  # no causaré enter a la dreta
                            b *= k
                            c *= k
                for k in [2, 3, 4, 5, 7]:
                    if c % d != 0 or random.randint(1, 30) == 1:  # (ja) no tinc enter a la dreta (excepte alguns)
                        break
                    else:
                        if a * k % b != 0:
                            a *= k
                            d *= k

                # evito fraccions iguals sota arrel
                if fracsimple(a, b) == fracsimple(c, d) and (previ == 4 or moneda()):
                    k = []
                    dsimp = fracsimple(c, d)[1]
                    for x in [2, 3, 5, 7]:
                        if dsimp % x:
                            k.append(x)
                    if k:
                        k = random.choice(k)
                        if moneda():
                            a *= k
                            d *= k
                        else:
                            b *= k
                            c *= k

            a, b = fracsimple(a, b)
            c, d = fracsimple(c, d)

            text = f"{rfracmix(a, b, inception - 1, previ=op, ops=ops, fet=fet)}"
            if (moneda() or c in [0, 1]) and not d == 0:  # no volem dividir per zero (ni fer un enter a la divisió)
                text += f"\\cdot {rfracmix(c, d, inception - 1, previ=op, ops=ops, fet=fet, segona=True)}"
            else:
                text += f": {rfracmix(d, c, inception - 1, previ=3, ops=ops, fet=fet, segona=True)}"

            if previ == 3:
                text = "(" + text + ")"

        elif op == 4:  # sqrt (no gasta nivell)
            text = "\\sqrt{" f"{rfracmix(pow(num, 2), pow(den, 2), inception, previ=4, ops=ops, fet=fet)}" "}"

        elif op == 5:  # pow (no gasta nivell)
            s = ""
            if num*den < 0:
                if not out:
                    print("Escolti que amb un signe de cada no en sé.")
                else:
                    s = "-"
            text = f"{s}({rfracmix(isqrt(abs(num)), isqrt(abs(den)), inception, previ=5, ops=ops, fet=fet)})^2"

    if out:
        if any([x in ops for x in [4, 5]]) and not any([x in fet for x in [4, 5]]):  # si volia powsqr i no hi ha powsqr
            print("recalculant fracmix per assegurar powsqr...")
            if 5 in ops:  # si hi ha quadrats forço quadrat a fora, que per defecte és menys comú que les arrless
                num, den = [random.choice(quadrats) for _ in range(2)]
                return fracmix(num, den, inception, op=5, doblesigne=doblesigne, ops=ops,
                               calpowsqr=calpowsqr, solucions=solucions)
            else:  # si només tinc arrles forço arrel
                num, den = [random.randint(1, 7) for _ in range(2)]
                return fracmix(num, den, inception, op=4, doblesigne=doblesigne, ops=ops,
                               calpowsqr=calpowsqr, solucions=solucions)
        text = squarebracketer(text)
        solu = fraconum(num, den, True)
        if solucions:
            return text, solu
        return text
    else:
        return text


def randomfracnum(n):
    """S'inventa un número per una fracció
    :param n: quantitat de factors
    """
    num = random.choice([2, 3, 5, 7])
    if not random.randint(0, 3):  # forço de tant en tant potències per ajudar a exercicis tipus [coses]^2
        num *= num
    else:
        for x in range(n):
            if x <= n // 2:
                num *= random.choice([1, 2])
            else:
                if moneda():
                    num *= random.choice([1, 2, 3])
                else:
                    num *= random.choice([2, 3, 5])
    return num


def fracsimple(n, d):
    """Retorna [n, d] = fracció (n/d) simplificada."""
    if n == 0:
        return [0, 1]
    elif d == 0:
        return [n, d]

    divis = divisors(d, True)
    for x in reversed(divis):  # important el reversed pq així queden els detalls pel final
        if n % x == 0 and d % x == 0:
            n = n // x
            d = d // x
    if d < 0:
        d = -d
        n = -n
    return [n, d]


def fraconum(n, d, simplifica=False):
    """Si només tinc numerador, retorna el número; si no, retorna el LaTeX de la fracció"""
    if simplifica:
        n, d = fracsimple(n, d)
    if d == 1 or d == -1:
        return f"{d*n}"  # tinc en compte el signe del denominador
    else:
        return "\\frac{" f"{n}" "}{" f"{d}" "}"


def taules(taula, div=False):
    a = random.randint(1, 10)
    if div:
        return fr'{a * taula}\div {a}='
    else:
        if moneda():
            return fr'{taula}\times {a}='
        else:
            return fr'{a}\times {taula}='


def divisors(num, tots=False):
    """Retorna els divisors d'un nombre donat (per defecte només la meitat)"""
    num = abs(num)  # per fer els divisors no m'importa el signe
    div = [1]
    for x in range(2, isqrt(num) + 1):
        if num % x == 0:
            div.append(x)
    if len(div) > 1 and not tots:
        div.remove(1)
    if tots:
        extra = []
        for x in reversed(div):
            extra.append(num // x)
        if div[-1] == extra[0]:  # evito repetits en casos com el 4
            div += extra[1:]
        else:
            div += extra
    return div


def isqrt(n):  # newton (from stackoverflow)
    """Part entera de l'arrel quadrada de n"""
    if n < 0:
        print(f"segur que vols fer l'arrel de {n}?")
        n = -n
    x = n
    y = (x + 1) // 2
    while y < x:
        x = y
        y = (x + n // x) // 2
    return x


def mcd(a, b):
    """Retorna el mcd dels dos números donats (Euler recursiu)"""
    if b == 0:
        return a
    return mcd(b, a % b)


def mcm(a, b):
    """retorna el mcm dels dos números donats (agafant el mcd)"""
    return a // mcd(a, b) * b


def squarebracketer(text):
    """Posa claudàtor al parèntesi més exterior si aquest en té més a dins."""
    bracketable = []
    inception = 0
    matrioska = False
    for x in range(len(text)):
        if text[x] == "(":
            if inception == 0:
                bracketable.append([x, -1])
            else:
                matrioska = True
            inception += 1
        elif text[x] == ")":
            inception -= 1
            if inception == 0:
                if matrioska:
                    bracketable[-1][1] = x
                else:
                    del bracketable[-1]
                matrioska = False
    for x in reversed(bracketable):
        text = text[:x[1]] + "\\rbrack " + text[x[1] + 1:]
        text = text[:x[0]] + "\\lbrack " + text[x[0] + 1:]

    return text


def apilades(tipus, nivell=1, digits=[2, 1], decimals=[0, 0]):
    text = r"\begin{array}{c}\phantom{\times99}42\\ \underline{\times\phantom{99}42}\\ \end{array}"
    if tipus == 1:  # sumes
        if nivell == 1:  # sense decimals
            text = "42+42"
            a = random.randint(max(2, pow(10, digits[0] - 1)), pow(10, digits[0]) - 1)
            b = random.randint(max(2, pow(10, digits[1] - 1)), pow(10, digits[1]) - 1)
            digitsc = math.ceil(math.log(a + b, 10))
            na = ""
            nb = ""
            for n in range(digitsc - digits[0]):
                na += "9"
            for n in range(digitsc - digits[1]):
                nb += "9"
            text = (r"\begin{array}{c}\phantom{+" + na + "}" + f"{a}" + r"\\ \underline{+\phantom{" + nb + "}"
                                                                                                           f"{b}" + r"}\\ \end{array}")
        else:  # amb decimals
            text = "4.2+4.2"
            xa = digits[0] + decimals[0]
            prea = random.randint(max(2, pow(10, xa - 1)), pow(10, xa) - 1)
            a = prea / pow(10, decimals[0])

            xb = digits[1] + decimals[1]
            preb = random.randint(max(2, pow(10, xb - 1)), pow(10, xb) - 1)
            b = preb / pow(10, decimals[1])

            res = a + b
            rdigits = math.ceil(math.log(math.floor(res), 10))
            partdecimal = round(res - math.floor(res), 7)  # cal truncar els glitches de binari (fa 2.3560000000023)
            rdecimals = 0
            while partdecimal - math.floor(partdecimal) != 0:
                partdecimal = round(partdecimal * 10, 7)
                rdecimals += 1
            digitsc = max(digits[0], digits[1], rdigits)
            decimalsc = max(decimals[0], decimals[1], rdecimals)

            nae = ""
            nad = ""
            nbe = ""
            nbd = ""
            for n in range(digitsc - digits[0]):
                nae += "9"
            for n in range(decimalsc - decimals[0]):
                nad += "9"
            for n in range(digitsc - digits[1]):
                nbe += "9"
            for n in range(decimalsc - decimals[1]):
                nbd += "9"
            text = (r"\begin{array}{c}\phantom{+" + nae + "}" + f"{a}" + r"\phantom{" + nad
                    + r"}\\ \underline{+\phantom{" + nbe + "}" + f"{b}" + r"\phantom{" + nbd + r"}}\\ \end{array}")

    elif tipus == 2:  # restes
        if nivell in [1, 2]:  # sense resultat negatiu || amb resultat negatiu
            text = "42-42"
            a = random.randint(max(2, pow(10, digits[0] - 1)), pow(10, digits[0]) - 1)
            b = random.randint(max(2, pow(10, digits[1] - 1)), pow(10, digits[1]) - 1)
            digitsc = math.ceil(math.log(max(a, b), 10))
            if nivell == 1:
                if b > a:  # poso el gros a dalt
                    aux = b
                    b = a
                    a = aux
                    aux = digits[0]
                    digits[0] = digits[1]
                    digits[1] = aux
            na = ""
            nb = ""
            for n in range(digitsc - digits[0]):
                na += "9"
            for n in range(digitsc - digits[1]):
                nb += "9"
            text = (r"\begin{array}{c}\phantom{-" + na + "}" + f"{a}" + r"\\ \underline{-\phantom{" + nb + "}"
                                                                                                           f"{b}" + r"}\\ \end{array} ")
        else:  # decimals
            text = "4.2-4.2"
            xa = digits[0] + decimals[0]
            prea = random.randint(max(2, pow(10, xa - 1)), pow(10, xa) - 1)
            a = prea / pow(10, decimals[0])

            xb = digits[1] + decimals[1]
            preb = random.randint(max(2, pow(10, xb - 1)), pow(10, xb) - 1)
            b = preb / pow(10, decimals[1])

            res = a - b
            if int(res) == 0:
                rdigits = 0
            else:
                rdigits = math.ceil(math.log(abs(int(res)), 10))
            partdecimal = round(res - math.floor(res), 7)  # cal truncar els glitches de binari (fa 2.3560000000023)
            rdecimals = 0
            while partdecimal - math.floor(partdecimal) != 0:
                partdecimal = round(partdecimal * 10, 7)
                rdecimals += 1
            digitsc = max(digits[0], digits[1], rdigits)
            decimalsc = max(decimals[0], decimals[1], rdecimals)

            nae = ""
            nad = ""
            nbe = ""
            nbd = ""
            for n in range(digitsc - digits[0]):
                nae += "9"
            for n in range(decimalsc - decimals[0]):
                nad += "9"
            for n in range(digitsc - digits[1]):
                nbe += "9"
            for n in range(decimalsc - decimals[1]):
                nbd += "9"
            text = (r"\begin{array}{c}\phantom{-" + nae + "}" + f"{a}" + r"\phantom{" + nad + r"}\\ \underline{"
                                                                                              r"-\phantom{" + nbe + "}" + f"{b}" + r"\phantom{" + nbd + r"}}\\ \end{array} ")
    elif tipus == 3:  # multis a x b = c
        if nivell == 1:  # sense decimals
            text = "42x42"
            a = random.randint(max(2, pow(10, digits[0] - 1)), pow(10, digits[0]) - 1)
            b = random.randint(max(2, pow(10, digits[1] - 1)), pow(10, digits[1]) - 1)
            digitsc = math.ceil(math.log(a * b, 10))
            na = ""
            nb = ""
            for n in range(digitsc - digits[0]):
                na += "9"
            for n in range(digitsc - digits[1]):
                nb += "9"
        else:  # amb decimals
            text = "4.2 x 4.2"

            xa = digits[0] + decimals[0]
            prea = random.randint(max(2, pow(10, xa - 1)), pow(10, xa) - 1)
            a = prea / pow(10, decimals[0])

            xb = digits[1] + decimals[1]
            preb = random.randint(max(2, pow(10, xb - 1)), pow(10, xb) - 1)
            b = preb / pow(10, decimals[1])

            digitsc = math.ceil(math.log(prea * preb, 10))
            if decimals[0]:
                na = ""
            if decimals[1]:
                nb = ""
            for n in range(digitsc - xa):
                na += "9"
            for n in range(digitsc - xb):
                nb += "9"
            # TODO ajustar per quan algun dels números no té decimals

        text = (r"\begin{array}{c}\phantom{\times" + na + "}" + f"{a}" + r"\\ \underline{\times\phantom{" + nb + "}"
                                                                                                                 f"{b}" + r"}\\ \end{array}")
    else:  # divis
        text = "42/42"
    return text


def powsqr_base(tipus, nivell=1, termes=2, seed=None, parell=2, fneg=0, solucions=False):
    """Retorna exercicis de base de potències i arrels

    :param tipus: tipus d'exercici
    :param nivell: dificultat (subtipus d'exercici)
    :param termes: quants termes (o quina quantitat d'exponents niats o el que sigui)
    :param seed: número forçat des de fora (per evitar repeticions)
    :param parell: (l'exponent) 0 imparell, 1 parell, 2 rand
    :param fneg: (forçar exp negatiu) 0 no forçar, 1 negatiu, 2 positiu
    :param solucions: retornar també la solució
    """
    text = "base^{42}"
    solu = "solu^{42}"
    primers = [2, 3, 5, 7, 11, 13, 17]

    # BASE POTÈNCIES (BPOW)
    if tipus == 1:  # combinar exponents (sense exp negatius // amb exp negatius)
        termes = max(termes, 2)  # per si de cas...
        base = seed if seed else random.choice(primers)
        exp_sol = 1
        if nivell > 1 and (fneg == 1 or (not fneg and moneda())):  # toca algun negatiu
            signes_exps = [x % 2 for x in range(termes)]  # +,-,+,-,+,-,+,-,+...
            if not random.randint(0, 2):  # de tant en tant faig extra negatiu (per practicar menys per menys)
                signes_exps[0] = 1
            random.shuffle(signes_exps)
        else:
            signes_exps = [0 for _ in range(termes)]
        print(fneg, signes_exps)
        for i, e in enumerate(range(termes)):
            exp = random.randint(2, 5)
            if signes_exps[i]:
                exp = -exp
            if not i:
                text = f"{base}^" + "{" + f"{exp}" + "}"  # el primer sense parèntesi
            else:
                text = f"({text})^" + "{" + f"{exp}" + "}"
            exp_sol *= exp
        text = squarebracketer(text)
        solu = f"{base}^" + "{" + f"{exp_sol}" + "}"

    elif tipus == 2:  # signe segons paritat: (-3)^4 = 3^4 (exponent positiu // exponent qualsevol)
        exp = random.randint(2, random.choice([10, 10, 100]))
        exp = (exp // 2) * 2  # el faig parell
        if not parell or (parell == 2 and moneda()):  # si toca el faig imparell
            exp += 1
        base = seed if seed else random.randint(1, random.randint(10, 20))

        if nivell == 1:  # exponent positiu
            s_exp = ""
        else:  # exponent qualsevol
            s_exp = random.choice(["-", ""])
        text = f"(-{base})^" + "{" + f"{s_exp}{exp}" + "}"
        s = "-" if exp % 2 else ""
        solu = s + f"{base}^" + "{" + f"{s_exp}{exp}" + "}"

    # BASE ARRELS (BSQR)
    elif tipus == 101:  # simplificar arrels
        base = seed if seed else random.choice(primers)
        index, exp = random.sample([1, 2, 3, 4, 5, 6, 7], 2)
        if exp > index:
            index, exp = exp, index
        for k in random.sample([2, 2, 3, 3, 4, 5, 10], termes-1):
            index, exp = index * k, exp * k
        text = tex_sqrt(base, index, exp)
        index, exp = fracsimple(index, exp)
        solu = tex_sqrt(base, index, exp)

    elif tipus == 102:  # convertir arrel en potència (sense exp negatius / amb negatius)
        base = random.choice(primers)
        index = seed if seed else random.randint(2, 20)
        exp = random.randint(1, max(15, index-1))
        if index == exp:
            index += 1
        if nivell == 2 and moneda():
            exp = -exp
        text = tex_sqrt(base, index, exp)
        exp, index = fracsimple(exp, index)  # simplifico la fracció per la solu
        solu = f"{base}^" + "{" + tex_frac(exp, index) + "}"

    elif tipus == 103:  # convertir potència en arrel
        base = random.choice(primers)
        index = seed if seed else random.randint(2, 20)
        exp = random.randint(1, max(15, index - 1))
        if index == exp:
            index += 1
        if nivell == 2 and moneda():
            exp = -exp
        text = f"{base}^" + "{" + tex_frac(exp, index) + "}"
        exp, index = fracsimple(exp, index)  # simplifico la fracció per la solu
        solu = tex_sqrt(base, index, exp)

    if solucions:
        return text, solu
    return text


def tex_sqrt(base, index=2, exp=1):
    """munta una arrel en latex (pot tenir un exponent a l'interior, però no posa parèntesi a la base)"""
    if index < 1:
        return "ERR: índex inesperat, amics"
    if index == 2:
        index = ""
    else:
        index = f"[{index}]"
    if exp == 0:
        return "1"
    elif exp == 1:
        exp = ""
    else:
        exp = "^{" + f"{exp}" + "}"
    if index == 1:
        return f"{base}{exp}"
    return rf"\sqrt{index}" + "{" + f"{base}{exp}" + "}"


def tex_frac(n, d):
    """munta una fracció en latex donat num i den (retorna num si den==1)"""
    if d == 1:
        return f"{n}"
    return r"\frac{" + f"{n}" + "}{" + f"{d}" + "}"


def powsqr(tipus, nivell=1, termes=2, lletres=0, fracnums=[], solucions=False):
    """Retorna exercicis de potències i arrels

    :param tipus:
    :param nivell:
    :param termes: quantitat de termes
    :param lletres: 0 = nums / 1 = nums i llet / 2 = llet
    :param fracnums: números per la fracció que fa de base a tipus 3
    :param solucions: retornar la solució de l'exercici
    :return: text en LaTeX
    """
    text = "42^6"
    solu = "42^7"

    if tipus == 1:  # potències, mateix exponent
        if nivell == 1:  # multiplicant
            text = ""
            solu = 1  # la base (l'exp serà constant, l'afegeixo després)
            exp = random.randint(2, 9)
            if random.randint(1, 4) == 4:
                exp = -exp
            if random.randint(1, 20) == 1:
                exp = random.randint(300, 1458)  # mutació exp enorme
            for x in range(termes):
                if x > 0:
                    text += r"\cdot "
                if random.randint(1, 15) == 1:  # mutació 1^27482
                    text += "1^{" + f"{random.randint(1, random.choice([9, 14958]))}" + "}"
                elif random.randint(1, 15) == 1:
                    text += f"{random.randint(2, random.choice([9, 9637]))}" + "^0"
                else:
                    base = random.randint(2, 6)
                    if not random.randint(0, 3):
                        solu *= -base
                        base = f"(-{base})"
                    else:
                        solu *= base
                    text += f"{base}" + "^{" + f"{exp}" + "}"
            # muntatge solució
            signe_solu = "-" if solu < 0 and exp % 2 else ""
            if exp == 0:
                solu = 1
                exp = ""
            elif abs(solu) == 1 or exp == 1:
                exp = ""
            solu = f"{signe_solu}{abs(solu)}^" + "{" + f"{exp}" + "}"

        elif nivell == 2:  # multiplicant i dividint
            text = ""
            solu = 1  # la base (l'exp serà constant, l'afegeixo després)
            exp = random.randint(2, 9)
            if random.randint(1, 4) == 4:
                exp = -exp
            if random.randint(1, 20) == 1:
                exp = random.randint(300, 1458)  # mutació exp enorme
            bloc = ""
            multigastada = False  # asseguro 1 div mínim
            a = 1  # per deixar content l'IDE, que li fa por accedir abans de declarar juajaj
            for x in range(termes):
                if x % 3 == 0:  # enceto el bloc de tres números (deixo pendent el primer número per triar-lo divisible)
                    a = random.randint(2, 5)  # número que haurà de ser divisible
                    if x != 0:
                        text += "\\cdot "
                    solu *= a
                else:
                    b = random.randint(2, 9)  # altres números del bloc
                    if moneda() and not multigastada:  # sortejo multi o divi (només entro si puc multi)
                        if random.randint(1, 10) == 1:  # mutació 1^27482
                            bloc += "\\cdot 1^{" + f"{random.randint(1, random.choice([9, 14958]))}" + "}"
                        elif random.randint(1, 10) == 1:
                            bloc += f"\\cdot {random.randint(2, random.choice([9, 9637]))}" + "^0"
                        else:
                            if random.randint(1, 4) == 1:
                                solu *= -b
                                b = f"(-{b})"
                            else:
                                solu *= b
                            bloc += f"\\cdot {b}^" + "{" + f"{exp}" + "}"
                        multigastada = True
                    else:  # divisió
                        a *= b
                        if random.randint(1, 4) == 1:
                            solu *= -1
                            b = f"(-{b})"
                        bloc += f"\\div {b}^" + "{" + f"{exp}" + "}"
                if x % 3 == 2 or x == (termes - 1):  # tanco el bloc
                    text += f"{a}^" + "{" + f"{exp}" + "}" + bloc
                    bloc = ""
                    multigastada = False
            # muntatge solució
            signe_solu = "-" if solu < 0 and exp % 2 else ""
            if exp == 0:
                solu = 1
                exp = ""
            elif abs(solu) == 1 or exp == 1:
                exp = ""
            solu = f"{signe_solu}{abs(solu)}^" + "{" + f"{exp}" + "}"

    elif tipus == 2:  # potències, mateixa base
        if nivell == 1 or nivell == 2:  # multiplicant // mul i div
            text = ""
            base = random.randint(2, 14)
            solu_base = base
            solu = 0  # exp (la base és ctt)
            solu_op = 1  # signe de l'exponent fruit de l'operació (1 multi, -1 divi)

            if random.randint(1, 4) == 1:
                solu_base = -base
                base = f"(-{base})"
            if random.randint(1, 20) == 1:
                base = random.randint(32, 265)  # mutació base enorme
                solu_base = base

            for x in range(termes):
                if x > 0:
                    if nivell == 1 or moneda():
                        text += r"\cdot "
                        solu_op = 1
                    else:
                        text += r"\div "
                        solu_op = -1
                if random.randint(1, 15) == 1:  # mutació 1^27482
                    text += "1^{" + f"{random.randint(1, random.choice([9, 14958]))}" + "}"
                elif random.randint(1, 15) == 1:
                    text += f"{random.randint(2, random.choice([9, 9637]))}" + "^0"
                else:
                    exp = random.randint(1, 10)
                    if random.randint(1, 4) == 1:
                        exp = -exp
                    solu += solu_op*exp
                    if exp == 1:
                        text += f"{base}"
                    else:
                        text += f"{base}" + "^{" + f"{exp}" + "}"
            # muntatge solució
            signe_solu = "-" if solu_base < 0 and solu % 2 else ""
            if solu == 0:
                solu_base = 1
                solu = ""
            elif abs(solu_base) == 1 or solu == 1:
                solu = ""
            solu = f"{signe_solu}{abs(solu_base)}^" + "{" + f"{solu}" + "}"

        elif nivell == 3:  # TODO organitzar aquest i els nivells inferiors
            text = ""
            if not fracnums:
                b1, b2 = random.sample([1, 2, 3, 4, 5, 6, 7], 2)
                b1, b2 = fracsimple(b1, b2)
            else:
                b1, b2 = fracnums

            for x in range(termes):
                if x > 0:
                    if nivell == 1 or moneda():
                        text += r"\cdot "
                    else:
                        text += r"\div "
                exp = random.randint(1, 10)
                if not random.randint(0, 3):
                    exp = -exp
                if not random.randint(0, 20) and not fracnums:
                    alt1 = random.choice([2, 3])
                    if b1 != alt1:
                        alt2 = b1
                    elif b2 != alt1:
                        alt2 = b2
                    else:
                        alt2 = random.choice([5, 7])
                    base = "\\frac{" f"{alt1}" "}{" f"{alt2}" "}"
                elif random.randint(0, 4):
                    base = "\\frac{" f"{b1}" "}{" f"{b2}" "}"
                else:
                    base = "\\frac{" f"{b2}" "}{" f"{b1}" "}"
                if exp == 1:
                    text += f"{base}"
                else:
                    text += f"\\left({base}\\right)" + "^{" + f"{exp}" + "}"

        elif nivell == 4:
            b1, b2 = random.sample([1, 2, 3, 5, 7], 2)
            b1, b2 = fracsimple(b1, b2)
            text = "\\left[" + powsqr(2, 3, fracnums=[b1, b2]) + "\\right]^{" + f"{random.randint(2, 5)}" + "}"
            exp = random.randint(2, 5)
            if moneda():
                exp = -exp
            text = "\\left[" + text + "\\right]^{" + f"{exp}" + "}"
            for _ in range(termes - 1):
                exp = random.randint(2, 5)
                if moneda():
                    exp = -exp
                bloc = "\\left[" + powsqr(2, 3, fracnums=[b1, b2]) + "\\right]^{" + f"{exp}" + "}"
                exp = random.randint(2, 5)
                if moneda():
                    exp = -exp
                bloc = "\\left[" + bloc + "\\right]^{" + f"{exp}" + "}"
                text += random.choice(["\\cdot", "\\div"]) + bloc

        elif nivell in [10, 11, 12, 13]:  # fracccions (dretes multiplicant // dretes // una girada // meitat girades)
            # precàlculs
            if nivell in [10, 11]:
                girada = [0 for _ in range(termes)]  # tot del dret
            elif nivell == 12:
                girada = [not x for x in range(termes)]  # una girada
                random.shuffle(girada)
            else:
                girada = [x % 2 for x in range(termes)]  # la meitat de cada
                random.shuffle(girada)

            if nivell in [10, 11]:
                num = random.randint(1, 7)  # permeto 1 a dalt si no pot estar a baix
            else:
                num = random.randint(2, 7)
            den = random.choice([x for x in range(2, 8) if num % x])

            # pre-solus
            sol_exp = 0

            # muntatge
            text = []
            for x in range(termes):
                if nivell == 10 or not x:  # (nivell 10 no fa divis, però primera frac no pot dividir tampoc)
                    divi = 0
                else:
                    divi = 0 if moneda() else 1  # 0: multi, 1: divi
                e = random.randint(2, 9) * random.choice([-1, 1])
                n, d = (den, num) if girada[x] else (num, den)
                if x:  # a partir de la segona porten operació al davant
                    op = [r"\cdot", r"\div"][divi]
                else:
                    op = ""
                text.append(f"{op}" + r"\left(\frac{" + f"{n}" + "}{" + f"{d}" + r"}\right) ^{" + f"{e}" + "}")

                if (divi and not girada[x]) or (girada[x] and not divi):
                    sol_exp += -e
                else:
                    sol_exp += e

            text = "".join(text)
            if sol_exp < 0 and nivell not in [10, 11]:  # si eren invertibles em quedo la positiva
                num, den = den, num
                sol_exp *= -1
            solu = r"\left(\frac{" + f"{num}" + "}{" + f"{den}" + r"}\right) ^{" + f"{sol_exp}" + "}"

    elif tipus == 3:  # potències, MCM
        if nivell == 1:  # multiplicant (exp amb signe)
            text = ""
            for x in range(termes):
                b = random.randint(2, 7)
                e = random.randint(2, 7)
                if random.randint(1, 4) == 1:
                    e = -e
                if x > 0:
                    text += "\\cdot"
                text += f"{b}^" + "{" + f"{e}" + "}"

    elif tipus == 10:  # potències, simplificar fraccions
        fracn = ""
        tn = (termes * 2) // 3  # màxim 2/3 en un sol costat
        fracd = ""
        td = tn
        primers = [2, 3, 5, 7]
        if nivell == 1 or nivell == 2:  # només un primer, exponents positius / exponents qualssevol
            random.shuffle(primers)
            base = primers[0]
            for x in range(termes):
                exp = random.randint(random.choice([-7, -5, -3]), random.choice([3, 5, 7]))
                if exp == 0 and random.randint(1, 3) != 1:
                    exp = random.choice([2, -2])
                elif exp < 0 and nivell == 1:
                    exp = abs(exp)
                terme = f"{base}"
                if exp != 1:
                    terme += "^{" + f"{exp}" + "}"

                if (moneda() and tn > 0) or td < 1:  # num
                    tn -= 1
                    if fracn == "":
                        fracn += terme
                    else:
                        fracn += "\\cdot" + terme
                else:  # den
                    td -= 1
                    if fracd == "":
                        fracd += terme
                    else:
                        fracd += "\\cdot" + terme
            text = "\\frac{" + fracn + "}{" + fracd + "}"

        elif nivell in [3, 4]:  # només primers, sense exponents de grup / amb exponents de grup
            pn = False
            pd = False
            random.shuffle(primers)
            if moneda() or termes < 6:
                bases = primers[:2]  # agafa els dos primers
            else:
                bases = primers[:3]  # agafa els tres primers
            gastat = []
            for x in range(termes):
                if x == termes - 1 and len(gastat) == 1:  # si és l'últim i només he posat una base, forço un altre
                    bases.remove(gastat[0])
                base = random.choice(bases)
                if base not in gastat:
                    gastat.append(base)
                exp = random.randint(random.choice([-7, -5, -3]), random.choice([3, 5, 7]))
                if exp == 0 and random.randint(1, 3) != 1:
                    exp = random.choice([2, -2])
                terme = f"{base}"
                if exp != 1:
                    terme += "^{" + f"{exp}" + "}"

                if (moneda() and tn > 0) or td < 1:  # num
                    tn -= 1
                    if fracn == "":
                        fracn += terme
                    else:
                        if moneda():
                            fracn += "\\cdot" + terme
                        else:
                            fracn = terme + "\\cdot" + fracn
                    if nivell == 4 and random.randint(1, termes) == 1 and not pn:
                        exp = random.randint(-5, 5)
                        if exp == 0:
                            exp = random.choice([-2, 2])
                        fracn = "(" + fracn + ")^{" + f"{exp}" + "}"
                        pn = True
                else:  # den
                    td -= 1
                    if fracd == "":
                        fracd += terme
                    else:
                        if moneda():
                            fracd += "\\cdot" + terme
                        else:
                            fracd = terme + "\\cdot" + fracd
                    if nivell == 4 and random.randint(1, termes) == 1 and not pd:
                        exp = random.randint(2, 5)
                        if moneda():
                            exp = -exp
                        fracd = "(" + fracd + ")^{" + f"{exp}" + "}"
                        pd = True
            text = "\\frac{" + fracn + "}{" + fracd + "}"

        elif nivell in [5, 6, 7]:  # números compostos sense exponent / amb exponent positiu / amb exponent qualsevol
            tnum = []
            tden = []
            for x in range(termes):
                if (moneda() and tn > 0) or td < 1:  # num
                    if nivell == 6:  # TODO veure què és això
                        tnum.append(random.choice(primers))  # primers és a l'entrada del tipus [2, 3, 5, 7]
                    else:
                        tnum.append(random.choice([2, 3, 5, 7, 11, 13]))
                    tn -= 1
                else:  # den
                    if nivell == 6:
                        tden.append(random.choice(primers))
                    else:
                        tden.append(random.choice([2, 3, 5, 7, 11, 13]))
                    td -= 1
            for x in range(termes):
                minpos = 0
                for y in range(len(tnum)):
                    if tnum[y] < tnum[minpos]:
                        minpos = y
                tnum[minpos] *= random.choice(primers)
                minpos = 0
                for y in range(len(tden)):
                    if tden[y] < tden[minpos]:
                        minpos = y
                tden[minpos] *= random.choice(primers)
            for x in tnum:
                if fracn == "":
                    fracn = f"{x}"
                else:
                    fracn += f"\\cdot {x}"
                if nivell in [6, 7]:
                    exp = random.randint(2, 4)
                    if moneda() and nivell == 7:
                        exp = -exp
                    fracn += "^{" + f"{exp}" + "}"
            for x in tden:
                if fracd == "":
                    fracd = f"{x}"
                else:
                    fracd += f"\\cdot {x}"
                if nivell in [6, 7]:
                    exp = random.randint(2, 4)
                    if moneda() and nivell == 7:
                        exp = -exp
                    fracd += "^{" + f"{exp}" + "}"

            text = "\\frac{" + fracn + "}{" + fracd + "}"

        elif nivell in [8]:  # decimals (x10^-n)
            tnum = []
            tden = []
            for x in range(termes):
                if (moneda() and tn > 0) or td < 1:  # num
                    tnum.append(random.choice(primers))
                    tn -= 1
                else:  # den
                    tden.append(random.choice(primers))
                    td -= 1
            for x in range(termes // 2 + 1):
                minpos = 0
                for y in range(len(tnum)):
                    if tnum[y] < tnum[minpos]:
                        minpos = y
                tnum[minpos] *= random.choice([2, 3])
                minpos = 0
                for y in range(len(tden)):
                    if tden[y] < tden[minpos]:
                        minpos = y
                tden[minpos] *= random.choice(primers)
            for x in tnum:
                zeros = random.randint(1, 2)
                for y in range(zeros):
                    x = f"0{x}"
                x = f"0.{x}"
                while x[-1] == "0":
                    x = x[:-1]
                if fracn == "":
                    fracn = f"{x}"
                else:
                    fracn += f"\\cdot {x}"
            for x in tden:
                zeros = random.randint(1, 2)
                for y in range(zeros):
                    x = f"0{x}"
                x = f"0.{x}"
                while x[-1] == "0":
                    x = x[:-1]
                if fracd == "":
                    fracd = f"{x}"
                else:
                    fracd += f"\\cdot {x}"

            text = "\\frac{" + fracn + "}{" + fracd + "}"
    elif tipus == 101:  # arrels, mateix exponent
        ...
    elif tipus == 102:  # arrels, mateixa base (té sentit?)
        ...
    elif tipus in [100, 103]:  # arrels, índex comú
        if nivell == 1:  # multiplicant, sense exponent
            text = ""
            for x in range(termes):
                b = random.randint(2, 7)
                ind = random.randint(2, 6)
                if ind == 2:
                    ind = ""
                if x > 0:
                    if tipus == 100:
                        text += ", "
                    else:
                        text += "\\cdot "
                text += "\\sqrt[" + f"{ind}" + "]{" + f"{b}" + "}"
        if nivell == 2:  # multiplicant, amb exponent
            text = ""
            for x in range(termes):
                b = random.randint(2, 7)
                ind = random.randint(2, 6)
                opcions = [2, 3, 4, 5, 6, 7]
                opcions.remove(ind)
                if ind == 2:
                    ind = ""
                e = random.choice(opcions)
                if x > 0:
                    if tipus == 100:
                        text += ",\\ "
                    else:
                        text += "\\cdot "
                text += "\\sqrt[" + f"{ind}" + "]{" + f"{b}^" + "{" + f"{e}" + "}" + "}"
    elif tipus == 104:  # arrels, combinar radicals
        text = f"{random.randint(2, 9)}"
        if nivell in [1, 2]:  # sense intercalar / pot intercalar
            for x in range(termes):
                tprev = "\\sqrt"
                ind = random.randint(2, 5)
                if ind > 2:
                    tprev += f"[{ind}]"
                tprev += "{"
                text = tprev + text + "}"
                if nivell > 1 and x < termes - 1 and moneda():
                    text = f"{random.randint(2, 4)}" + text
    elif tipus == 105:  # arrels, extreure factors
        if nivell == 1:  # només quadrades, factoritzat
            numeros = [2, 3, 5, 7]
            lets = ["a", "b", "c", "d", "x", "y", "z"]
            if random.randint(1, 10) == 1:
                lets[2] = "ç"
            primers = []
            if lletres < 2:
                primers += numeros
            if lletres > 0:
                if moneda():
                    primers += lets[:4]
                else:
                    primers += lets[4:]
            factors = random.sample(primers, random.randint(1, 3))
            if not any(x in numeros for x in factors[1:]):  # no hi ha més números després del primer
                punts = False
            else:
                punts = True
            for x in range(len(factors)):
                if len(factors) == 1:
                    exp = random.randint(2, 8)
                else:
                    exp = random.randint(1, 5)
                if exp == 1:
                    factors[x] = f"{factors[x]}"
                else:
                    factors[x] = f"{factors[x]}^" + "{" + f"{exp}" + "}"
            for x in range(len(factors)):
                if x == 0:
                    text = f"{factors[x]}"
                else:
                    if not punts or (factors[x][0] in lets and factors[x - 1][0] in lets):
                        pass
                    else:
                        text += "\\cdot "
                    text += f"{factors[x]}"
            text = "\\sqrt{" + text + "}"

        elif nivell == 2:  # qualsevol índex, factoritzat
            index = random.randint(2, 5)
            numeros = [2, 3, 5, 7]
            lets = ["a", "b", "c", "d", "x", "y", "z"]
            if random.randint(1, 10) == 1:
                lets[2] = "ç"
            primers = []
            if lletres < 2:
                primers += numeros
            if lletres > 0:
                if moneda():
                    primers += lets[:4]
                else:
                    primers += lets[4:]
            factors = random.sample(primers, random.randint(1, 3))
            if not any(x in numeros for x in factors[1:]):  # no hi ha més números després del primer
                punts = False
            else:
                punts = True
            for x in range(len(factors)):
                if len(factors) == 1:
                    exp = random.randint(index, 3 + index)
                else:
                    exp = random.randint(1, 3 + index)
                if exp == 1:
                    factors[x] = f"{factors[x]}"
                else:
                    factors[x] = f"{factors[x]}^" + "{" + f"{exp}" + "}"
            for x in range(len(factors)):
                if x == 0:
                    text = f"{factors[x]}"
                else:
                    if not punts or (factors[x][0] in lets and factors[x - 1][0] in lets):
                        pass
                    else:
                        text += "\\cdot "
                    text += f"{factors[x]}"
            if index == 2:
                text = "\\sqrt{" + text + "}"
            else:
                text = "\\sqrt[" + f"{index}" + "]{" + text + "}"

        elif nivell == 11:  # només quadrades, per factoritzar
            seed = random.choice([2, 2, 3, 3, 5, 5, 7])
            factors = 1
            if moneda():
                seed = pow(seed, 2)
                factors += 1
            for x in range(random.randint(3, 5) - factors):
                seed *= random.choice([2, 3])
            text = "\\sqrt{" + f"{seed}" + "}"

        elif nivell == 12:  # índex qualsevol, per factoritzar
            index = random.randint(2, 4)
            if index == 2:
                return powsqr(105, 11)
            else:
                seed = random.choice([2, 3])
                if moneda():
                    seed *= seed
                seed *= pow(random.choice([2, 3]), index)
                if seed < 100 and random.choice([0, 1, 1]):
                    seed *= 10
                text = "\\sqrt[" + f"{index}" + "]{" + f"{seed}" + "}"

    elif tipus == 106:  # arrels, entrar factors
        if nivell == 1:  # només quadrades
            numeros = [2, 3, 5, 7]
            lets = ["a", "b", "c", "d", "x", "y", "z"]
            factors = []
            if random.randint(1, 10) == 1:
                lets[2] = "ç"
            if lletres < 2:
                factors += numeros
            if lletres > 0:
                factors += random.choice([lets[:4], lets[4:]])
            factors = random.sample(factors, random.choice([1, 3]))
            seed = random.choice(factors)
            if len(factors) > 1 and moneda():
                factors.remove(seed)
            seed = f"{seed}"
            exp = random.choice([1, 1, 3, 3, 5])
            if exp > 1:
                seed += "^{" + f"{exp}" + "}"
            text = "\\sqrt{" + seed + "}"

            if not any(x in numeros for x in factors[:-1]):  # no hi ha més números després del primer (dibuixa E<-D)
                punts = False
            else:
                punts = True
            for x in range(len(factors)):
                exp = random.randint(1, 3)
                if exp > 1:
                    exp = "^{" + f"{exp}" + "}"
                else:
                    exp = ""
                if x > 0:
                    if not punts or (factors[x] in lets and factors[x - 1] in lets):
                        pass
                    else:
                        text = "\\cdot " + text
                text = f"{factors[x]}" + exp + text
        elif nivell == 2:  # qualsevol índex
            index = random.randint(2, 5)
            numeros = [2, 3, 5, 7]
            lets = ["a", "b", "c", "d", "x", "y", "z"]
            factors = []
            if random.randint(1, 10) == 1:
                lets[2] = "ç"
            if lletres < 2:
                factors += numeros
            if lletres > 0:
                factors += random.choice([lets[:4], lets[4:]])
            factors = random.sample(factors, random.choice([1, 3]))
            seed = random.choice(factors)
            if len(factors) > 1 and moneda():
                factors.remove(seed)
            seed = f"{seed}"
            exps = [1, 2, 3, 4, 5, 6, 7, 8]
            for x in range(len(exps)):
                if exps[x] % index == 0:
                    exps[x] = exps[x] - 1  # rebaixo els múltiples de l'arrel (així no es poden treure fora)
            exp = random.choice(exps)
            if exp > 1:
                seed += "^{" + f"{exp}" + "}"
            if index == 2:
                text = "\\sqrt{" + seed + "}"
            else:
                text = "\\sqrt[" + f"{index}" + "]{" + seed + "}"

            if not any(x in numeros for x in factors[:-1]):  # no hi ha més números després del primer (Escriu E<-D)
                punts = False
            else:
                punts = True
            for x in range(len(factors)):
                exp = random.randint(1, 3)
                if exp > 1:
                    exp = "^{" + f"{exp}" + "}"
                else:
                    exp = ""
                if x > 0:
                    if not punts or (factors[x] in lets and factors[x - 1] in lets):
                        pass
                    else:
                        text = "\\cdot " + text
                text = f"{factors[x]}" + exp + text

    elif tipus == 107:  # sumes i restes simplificant primer
        if nivell in [1, 11, 2, 12]:  # sense coefs, mateix rad / pot dif // amb coef, mat / pdif
            seed = random.choice([2, 2, 2, 3, 3, 5])
            if seed == 2:
                opcions = [1, 2, 3, 4, 5, 6, 7, 8, 10]
            elif seed == 3:
                opcions = [1, 2, 3, 4, 5, 6, 10]
            elif seed == 5:
                opcions = [1, 2, 3, 4, 5, 10]
            triats = random.sample(opcions, termes)
            text = ""
            mutat = False
            for x in range(len(triats)):
                if x > 0:
                    text += random.choice(["+", "-"])
                if nivell in [2, 12]:
                    coef = random.randint(1, random.choice([5, 10]))
                    if coef != 1:
                        text += f"{coef}"
                if nivell == 11 and not mutat and random.randint(1, 10) == 1:
                    altseed = [2, 3, 5]
                    altseed.remove(seed)
                    altseed = random.choice(altseed)
                    altop = random.choice([2, 3, 4, 5, 10])
                    text += "\\sqrt{" + f"{altseed * pow(altop, 2)}" + "}"
                    mutat = True
                else:
                    text += "\\sqrt{" + f"{seed * pow(triats[x], 2)}" + "}"

    elif tipus == 108:  # racionalitzar
        text = "\\frac{1}{\\sqrt{42}}"
        if nivell in [1, 2, 3]:  # denominador arrel quadrada
            num = random.randint(1, random.choice([5, 10]))
            den = random.randint(2, random.choice([5, 10]))
            if nivell == 1:
                text = "\\frac{" + f"{num}" + "}{\\sqrt{" + f"{den}" + "}}"
            else:
                index = random.randint(2, 5)
                if nivell == 3:
                    exp = random.randint(1, index - 1)
                    if exp != 1:
                        den = f"{den}^" + "{" + f"{exp}" + "}"
                if index == 2:
                    index = ""
                text = "\\frac{" + f"{num}" + "}{\\sqrt[" + f"{index}" + "]{" + f"{den}" + "}}"

        elif nivell in [11, 12]:  # denominador suma (√B+√C), una arrel / dues arrels
            a = random.randint(1, random.choice([5, 10]))
            if random.choice([0, 0, 1]):
                a = -a
            signe = random.choice(["+", "-"])
            if nivell == 11 or random.choice([0, 1, 1]):  # una arrel
                if moneda():  # B + √C
                    b = random.randint(1, 10)
                    opcions = [2, 3, 5, 6, 7, 8, 10]
                    if pow(b, 2) in opcions:
                        opcions.remove(pow(b, 2))
                    c = random.choice(opcions)
                    text = "\\frac{" + f"{a}" + "}{" + f"{b}" + signe + "\\sqrt{" + f"{c}" + "}}"
                else:  # √B + C
                    c = random.randint(1, 10)
                    opcions = [2, 3, 5, 6, 7, 8, 10]
                    if pow(c, 2) in opcions:
                        opcions.remove(pow(c, 2))
                    b = random.choice(opcions)
                    text = "\\frac{" + f"{a}" + "}{" + "\\sqrt{" + f"{b}" + "}" + signe + f"{c}" + "}"
            else:  # dues arrels
                opcions = [2, 3, 5, 6, 7, 8, 10]
                random.shuffle(opcions)
                b = opcions.pop()  # gets and removes last element
                c = opcions.pop()
                text = "\\frac{" + f"{a}" + "}{" + "\\sqrt{" + f"{b}" + "}" + signe + "\\sqrt{" + f"{c}" + "}}"

        elif nivell in [13, 14]:  # denominador i numerador conjugats, una arrel / dues arrels
            if nivell == 13 or moneda():  # una arrel
                if moneda():  # B + √C
                    b = random.randint(1, 10)
                    opcions = [2, 3, 5, 6, 7, 8, 10]
                    if pow(b, 2) in opcions:
                        opcions.remove(pow(b, 2))
                    c = random.choice(opcions)
                    signe = ["+", "-"]
                    random.shuffle(signe)
                    num = f"{b}" + signe[0] + "\\sqrt{" + f"{c}" + "}"
                    den = f"{b}" + signe[1] + "\\sqrt{" + f"{c}" + "}"
                else:  # √B + C
                    c = random.randint(1, 10)
                    opcions = [2, 3, 5, 6, 7, 8, 10]
                    if pow(c, 2) in opcions:
                        opcions.remove(pow(c, 2))
                    b = random.choice(opcions)
                    signe = ["+", "-"]
                    random.shuffle(signe)
                    num = "\\sqrt{" + f"{b}" + "}" + signe[0] + f"{c}"
                    den = "\\sqrt{" + f"{b}" + "}" + signe[1] + f"{c}"
            else:  # dues arrels (√A + √B)/(√A - √B)
                opcions = [2, 3, 5, 6, 7, 8, 10]
                random.shuffle(opcions)
                a = opcions.pop()
                b = opcions.pop()
                signe = ["+", "-"]
                random.shuffle(signe)
                num = "\\sqrt{" + f"{a}" + "}" + signe[0] + "\\sqrt{" + f"{b}" + "}"
                den = "\\sqrt{" + f"{a}" + "}" + signe[1] + "\\sqrt{" + f"{b}" + "}"

            text = "\\frac{" + num + "}{" + den + "}"

    if solucions:
        return text, solu
    return text


def idnotable(tipus, nivell=1, idnums=None, fcoefb=0, ordenat=True, ordre2=False, solucions=False):
    """genera exercicis d'identitats notables

    :param tipus: 1 calcular, 2 endevinar
    :param nivell: 1 (x+B) / 2 (Ax+B) / 3 (x^n+B) / 4 (Axy+B) / 5 (Ax+By) / 6 (Axy^n+Byz^m)
    :param idnums: llista de tipus possibles (o tipus demanat) ::  1 (a+b)^2 / 2 (a-b)^2 / 3 (a+b)(a-b)
    :param fcoefb: forçar coeficient b (número que tindrà el coeficient si el vull triar)
    :param ordenat: False permet desordre als tipus 2
    :param ordre2: Considera que "ordenat" vol dir a^2+b^2+2ab
    :param solucions: retornar també les solucions
    """
    if not idnums:  # si no venia res, poso [1, 2, 3]
        idnums = [1, 2, 3]

    text = "(x+42)^2"
    solu = ""
    try:
        idnum = random.choice(idnums)
    except TypeError:  # per quan només n'hi ha un però no està dins una llista
        idnum = idnums
    varops = random.choice([["x", "y", "z"], ["a", "b", "c"]])
    if tipus in [1, 2]:  # calcula la idnot / endevina enunciat
        if nivell in [1, 2, 3]:  # (x+3) sola + indep / (2x+3) coef + indep / (x^2+3) exp + indep
            # coefs
            if nivell in [1, 3]:
                a = 1
            else:
                a = random.randint(2, 5)
            if fcoefb:
                b = fcoefb
            else:
                b = random.randint(1, 10)
            if nivell == 3:  # pujo l'exponent de la a afegint zeros al mig del rufini
                zeros = [0 for _ in range(random.randint(1, 3))]
            else:
                zeros = []
            # tipus d'identitat
            if idnum == 2 or (idnum == 3 and moneda()):
                b = -b
            # càlcul
            base = [a] + zeros + [b]
            base2 = base[:]
            if idnum == 3:
                base2[-1] = -base2[-1]
            desenv = poli_op(3, base, base2)   # multiplico el quadrat
            # muntatge
            if idnum in [1, 2]:
                base = f"({polinomitza(base)})^2"
            else:
                base = f"({polinomitza(base)})({polinomitza(base2)})"
            desenv = polinomitza(desenv, ordenat, ordre2=ordre2)

        elif nivell in [4, 5, 6]:  # (2xy+3) multimonomi + indep / (2x+3y) dues variables / (5xy^2+3x^2y)
            ca = random.randint(1, 3)  # de moment els deixo tots positius els de davant
            cb = random.randint(1, 5)
            va, ea, vb, eb = [], [], [], []
            if nivell == 4:
                va = random.sample(varops, 2)
                ea = [1 for _ in range(len(va))]
                vb = [random.choice(varops)]
                eb = [0]
            elif nivell == 5:
                va, vb = random.sample(varops, 2)
                va = [va]
                vb = [vb]
                ea, eb = [[1], [1]]
            elif nivell == 6:
                va, vb = [random.sample(varops, 2) for _ in range(2)]
                ea, eb = [[1, random.randint(1, 3)] for _ in range(2)]
                random.shuffle(ea)
                random.shuffle(eb)
                if moneda():  # de tant en tant trec una de les dues variables d'un dels dos costats
                    if moneda():
                        va = va[1:]
                        ea = ea[1:]
                    else:
                        vb = vb[1:]
                        eb = eb[1:]
                if mumo_semblant([ca, va, ea], [cb, vb, eb]):  # si es podrien sumar, trenco la semblança
                    if ea[0] > 1:
                        ea[0] = 1
                    else:
                        ea[0] += 1
            # càlcul
            a = [ca, va, ea]
            b = [cb, vb, eb]
            if idnum == 2 or (idnum == 3 and moneda()):
                b[0] *= -1
            base = [a, b]
            base2 = deepcopy(base)  # sense deepcopy les llistes niades queden enllaçades
            if idnum == 3:
                base2[1][0] *= -1
            desenv = polimumo_op(3, base, base2)  # multiplico el quadrat
            # muntatge
            if idnum in [1, 2]:
                base = f"({polimumitza(base)})^2"
            else:
                base = f"({polimumitza(base)})({polimumitza(base2)})"
            if not ordenat:
                random.shuffle(desenv)
            elif ordre2:  # quan "ordenat" vol dir a^2+b^2+2ab
                desenv = [desenv[0]]+[desenv[2]]+[desenv[1]]
                print(desenv)
            desenv = polimumitza(desenv)
        if tipus == 1:
            text = base
            solu = desenv
        elif tipus == 2:
            text = desenv
            solu = base
    if solucions:
        return text, solu
    else:
        return text


def px(tipus, nivell=1, termes=[], noneg=False, solucions=False, par="k"):
    """genera polinomis i operacions amb polinomis

    :param tipus: operació / tipus d'exercici
    :param nivell: subtipus d'exercici
    :param termes: quants termes té cada polinomi (a les ops) / quants polinomis (al de factoritzar)
    :param noneg: evita doble negatiu restant
    :param solucions: incloure solució a l'exercici
    :param par: lletra que faré servir com a paràmetre (e.g. als exercicis de paràmetre tq residu)
    """
    text = "P(x)=42"
    solu = "(R: 42)"
    if tipus == 0:  # fcomú
        if not termes:
            termes = 3

        if nivell == 1:  # una variable
            xn = random.randint(1, 3)  # grau de la x fc
            k = random.randint(1, 5)
            rufipx = polinomi(random.choice([termes, termes+1]), termes, cmax=10, obliga=[0], rufinat=True)[1]
            for i in range(len(rufipx)):
                rufipx[i] *= k
            rufipx += [0 for _ in range(xn)]
            text = polinomitza(rufipx, False)

        elif nivell == 2:  # multivariable
            varopcions = ["a", "b", "c", "d", "x", "y", "z", "r", "s", "t"]
            variables = random.sample(varopcions, random.choice([3, 4]))  # trec unes quantes
            random.shuffle(variables)
            vcomuns = variables[:2]
            vopc = variables[2:]
            text = []
            k = random.randint(1, 5)
            signe = False
            for x in range(termes):
                coef = random.randint(1, random.choice([4, 10])) * k
                mvars = vcomuns + random.sample(vopc, 1)
                exps = [random.randint(1, random.choice([1, 4])) for _ in range(len(mvars))]
                text.append(multimonomi(coef, mvars, exps, signe))
                signe = True  # a partir de la segona vull signe obligat
            text = "".join(text)

    if tipus == 1:  # suma P(x)+Q(x)
        if not termes:
            termes = [4, 3]

        if nivell in [1, 2, 3]:  # ordenat complet / ordenat incomplet / qualsevol
            # opcions
            if nivell > 2:
                ordenat = False
            else:
                ordenat = True

            # graus
            gp = termes[0] - 1
            gq = termes[1] - 1
            if nivell > 1:
                gp += random.randint(0, random.randint(1, 2))
                gq += random.randint(0, random.randint(1, 2))

            # polinomis
            px, rufipx = polinomi(gp, termes[0], ordenat, rufinat=True)
            qx, rufiqx = polinomi(gq, termes[1], ordenat, rufinat=True)

            # solució
            if solucions:
                solu = polinomitza(poli_op(1, rufipx, rufiqx))

            text = f"({px})+({qx})"

    elif tipus == 2:  # resta P(x)-Q(x)
        if not termes:
            termes = [4, 3]

        if nivell in [1, 2, 3]:  # ordenat complet / ordenat incomplet / qualsevol
            # opcions
            if nivell > 2:
                ordenat = False
            else:
                ordenat = True

            if noneg:  # evita negatius al segon polinomi (per no fer -[-k])
                negatius = 0
            else:
                negatius = 1

            # graus
            gp = termes[0] - 1
            gq = termes[1] - 1
            if nivell > 1:
                gp += random.randint(0, random.randint(1, 2))
                gq += random.randint(0, random.randint(1, 2))

            # polinomis
            px, rufipx = polinomi(gp, termes[0], ordenat, rufinat=True)
            qx, rufiqx = polinomi(gq, termes[1], ordenat, negatius=negatius, rufinat=True)

            # solució
            if solucions:
                solu = polinomitza(poli_op(2, rufipx, rufiqx))

            text = f"({px})-({qx})"

    elif tipus == 3:  # multis P(x)*Q(x)
        if not termes:
            termes = [3, 2]

        if nivell in [1, 2, 3, 4, 5]:  # ord complets / ord incomplets // desord independent / pot sense
            # opcions
            if nivell > 2:
                ordenat = False
            else:
                ordenat = True

            # graus
            gp = termes[0] - 1
            gq = termes[1] - 1
            if nivell > 1:
                gp += random.randint(0, random.randint(1, 2))
                gq += random.randint(0, random.randint(1, 2))

            # control (vigilo que hi hagi terme independent)
            if nivell < 4:
                obligap = [0]
                obligaq = [0]
            elif nivell == 4:
                if moneda():
                    obligap = [0]
                    obligaq = []
                else:
                    obligaq = [0]
                    obligap = []
            else:
                obligaq = []
                obligap = []

            # polinomis
            px, rufipx = polinomi(gp, termes[0], ordenat, cmax=7, obliga=obligap, rufinat=True)
            qx, rufiqx = polinomi(gq, termes[1], ordenat, cmax=3, obliga=obligaq, rufinat=True)

            # solució
            if solucions:
                solu = polinomitza(poli_op(3, rufipx, rufiqx))

            text = f"({px})\\times ({qx})"

    elif tipus in [4, 5]:  # divis (rufini / normal)
        if not termes:
            termes = [random.choice([2, 3]), random.choice([2, 3])]  # quocient i divisor
        if nivell in [1, 2, 3, 4]:  # Exacte complet ordenat / complet ordenat / ordenat / qualsevol
            # opcions
            if nivell > 3:
                ordenat = False
            else:
                ordenat = True
            if nivell > 1:
                residu = True
            else:
                residu = False

            # graus (quocient, divisor)
            gq = termes[0] - 1
            gd = termes[1] - 1
            if nivell > 2:
                gq += random.randint(0, random.randint(1, 2))
                gd += random.randint(0, random.randint(1, 2))

            # polinomis
            qx, rufiqx = polinomi(gq, termes[0], ordenat=True, cmax=7, rufinat=True)  # quocient
            if tipus == 4:  # si és rufini faig un polinomi de rufini
                rufidx = [1, random.randint(1, random.choice([3, 5])) * random.choice([1, -1])]
                dx = polinomitza(rufidx, ordenat)
                gd = 1
            else:
                dx, rufidx = polinomi(gd, termes[1], ordenat, cmax=3, rufinat=True)  # divisor
            rufidend = poli_op(3, rufiqx, rufidx)  # dividend (multiplico)
            if residu:  # si tinc opció a residu, en poso
                rufisidu = [0 for _ in range(gd)]  # màxim un grau menys que el divisor
                tresidu = random.choice([0, 1, 2])  # quants termes pot tenir el residu (si 0: divi exacte)
                for x in range(len(rufisidu)):
                    if tresidu < 1:
                        break
                    if rufidend[-x-1] or tipus == 4:  # quan hi ha ruffini els forço encara que (termes + 1)
                        rcoef = random.randint(1, 10) * random.choice([1, 1, -1])
                        rufidend[-x-1] += rcoef
                        rufisidu[-x-1] = rcoef
                        tresidu -= 1
            else:
                rufisidu = []
                tresidu = 0
            dendx = polinomitza(rufidend, ordenat)

            # solució
            if solucions:
                if any([x for x in rufisidu]):
                    solu = f"${qx}$~(R:~${polinomitza(rufisidu)}$)"
                else:
                    solu = f"${qx}$~(R:~0)"

            text = f"({dendx})\\div ({dx})"

    elif tipus == 6:  # tª residu / avaluar
        # grau
        termes = random.randint(3, 4)
        gp = termes + random.choice([0, 1, 2])

        # punt x
        if gp < 5:
            x = random.randint(1, 3)
        elif gp < 2:
            x = random.randint(1, 5)
        else:  # 5+
            x = random.randint(1, 2)
        x *= random.choice([1, 1, -1])

        # polinomis
        px, rufipx = polinomi(gp, termes, True, cmax=5, obliga=[0], suavitzat=True, rufinat=True)
        dx = f"x{amb_signe(-x)}"

        # solució
        solu = poli_aval(rufipx, x)

        # muntatge
        text = en.px_residu(nivell, px, dx, x)

    elif tipus == 7:  # factoritzar TODO factors no simplificables de grau 2
        if not termes:
            termes = random.choice([2, 3])
        if nivell in [1, 2, 3]:  # sense fcomú ni k / sense k / amb tot
            if random.randint(0, 5) or nivell < 3:  # rufinable
                rufipx = frufinable()
            else:  # el freak de primer grau
                rufipx = [random.randint(1, 3), 1]
            solulist = ["(" + polinomitza(rufipx) + ")"]

            for x in range(termes-1):  # factors rufinables
                noufact = frufinable()
                rufipx = poli_op(3, rufipx, noufact)
                solulist.append("(" + polinomitza(noufact) + ")")

            soluxn = ""
            if nivell > 1:  # factor x^n
                if moneda():
                    exp = random.randint(1, 3)
                    rufipx = rufipx + [0 for _ in range(exp)]
                    soluxn = f"{monomi(1, exp)}"

            k = ""
            if nivell > 2:  # factor k
                if moneda():
                    k = random.randint(2, 5) * random.choice([1, 1, -1])
                    rufipx = [x * k for x in rufipx]

            # muntatge
            text = polinomitza(rufipx)

            # solució
            solu = f"{k}" + soluxn + "".join(solulist)

    elif tipus == 8:  # simplificar frac algebraiques
        if not termes:
            termes = [random.choice([2, 3]) for _ in range(2)]
        if nivell:
            rufinum = frufinable()
            rufiden = rufinum[:]  # crec que això és important pq no siguin dos sobrenoms de la mateixa llista
            hihatermes = [1, 1]

            if termes[0] > 2 or termes[1] > 2:  # extra tatxable (si algun té 3 factors (rufinables))
                nouterme = frufinable()
                rufinum = poli_op(3, rufinum, nouterme)
                rufiden = poli_op(3, rufiden, nouterme)
                hihatermes = [x + 1 for x in hihatermes]

            opcionsarrel = [1, -1, 2, -2, 3, -3, 4, -4, 5, -5]
            random.shuffle(opcionsarrel)

            solunum = []
            if hihatermes[0] < termes[0]:  # únics num
                for x in range(termes[0] - hihatermes[0]):
                    noufact = [1, opcionsarrel.pop()]  # pot donar error si la suma de termes > 12
                    rufinum = poli_op(3, rufinum, noufact)
                    hihatermes[0] += 1
                    solunum.append("(" + polinomitza(noufact) + ")")

            soluden = []
            if hihatermes[1] < termes[1]:  # únics den
                for x in range(termes[1] - hihatermes[1]):
                    noufact = [1, opcionsarrel.pop()]  # pot donar error si la suma de termes > 12
                    rufiden = poli_op(3, rufiden, noufact)
                    hihatermes[1] += 1
                    soluden.append("(" + polinomitza(noufact) + ")")

            if moneda():  # factor x^n compartit
                exp = random.randint(1, 2)
                rufinum = rufinum + [0 for _ in range(exp)]
                rufiden = rufiden + [0 for _ in range(exp)]

            soluxn = ["", ""]
            if moneda():  # factor x^n únic
                exp = random.randint(1, 2)
                if moneda():
                    rufinum = rufinum + [0 for _ in range(exp)]
                    soluxn[0] = f"{monomi(1, exp)}"
                else:
                    rufiden = rufiden + [0 for _ in range(exp)]
                    soluxn[1] = f"{monomi(1, exp)}"

            if moneda():  # factor k compartit
                k = random.randint(2, 5) * random.choice([1, 1, -1])
                rufinum = [x * k for x in rufinum]
                rufiden = [x * k for x in rufiden]

            k = ["", ""]
            if moneda():  # factor k únic
                if moneda():
                    k[0] = random.randint(2, 5) * random.choice([1, 1, -1])
                    rufinum = [x * k[0] for x in rufinum]
                else:
                    k[1] = random.randint(2, 5) * random.choice([1, 1, -1])
                    rufiden = [x * k[1] for x in rufiden]

            # muntatge
            text = "\\frac{" + polinomitza(rufinum) + "}{" + polinomitza(rufiden) + "}"

            # solució
            num = f"{k[0]}" + soluxn[0] + "".join(solunum)
            if not num:
                num = "1"
            den = f"{k[1]}" + soluxn[1] + "".join(soluden)
            if not den:
                den = "1"
            solu = ("\\frac{" + num + "}{" + den + "}")

    elif tipus == 106:  # paràmetre(s) tal que residu
        if nivell in [1, 2, 3, 4, 5, 6]:  # k tal que divi exacta
            # (Ax^2+Bx+C)*(x-D): un coef k / un coef ka / multi coefs / amb una suma (k+a)
            # coefs pre-multi
            a = random.randint(1, 2) * random.choice([-1, 1])
            b = random.randint(1, 3) * random.choice([-1, 1])
            c = random.randint(1, 4) * random.choice([-1, 1])
            d = random.randint(1, 3) * random.choice([-1, 1])  # important no 0
            # coef control (per dues k)
            if abs(c - d*b) > 10 and c*d*b < 0:
                c = -c
            if nivell == 3:
                if b % d and c % d:  # no hi ha múltiples
                    b = d * random.choice([1, 2, 3])
                    if a*d < 0:
                        b = -b
            # construeixo el polinomi (multiplicant)
            rufipx = poli_op(3, [a, b, c], [1, -d])

            if nivell == 1:  # subs pel num sencer
                i = random.randint(0, len(rufipx)-1)
                if moneda():
                    k, rufipx[i] = rufipx[i], par  # substitueixo per k
                else:
                    k, rufipx[i] = -rufipx[i], f"-{par}"  # substitueixo per -k

            elif nivell == 2:  # subs una part del num
                try:  # intento agafar un major que 1 si n'hi ha
                    i = random.choice([x for x in range(len(rufipx)) if abs(rufipx[x]) > 1])
                except:
                    i = random.choice([x for x in range(len(rufipx)) if rufipx[x]])
                divs = divisors(rufipx[i], True)
                ca = random.choice(divs) * random.choice([-1, 1])  # coef "a" que deixo davant la k
                if not ca:
                    ca = random.choice([-1, 1])
                k = rufipx[i] // ca  # per la solu
                if abs(ca) != 1:
                    rufipx[i] = f"{ca}{par}"
                elif ca > 0:
                    rufipx[i] = f"{par}"
                else:
                    rufipx[i] = f"-{par}"

            elif nivell == 3:  # multi coefs
                m2 = []
                m3 = []
                m4 = []
                m5 = []
                for i, x in enumerate(rufipx):
                    if not x:
                        continue
                    if not x % 4:  # múltiple de 4
                        m4.append(i)
                        m2.append(i)
                    elif not x % 2:  # múltiple de 2
                        m2.append(i)
                    if not x % 3:  # múltiple de 3
                        m3.append(i)
                    if not x % 5:  # múltiple de 5
                        m5.append(i)
                for i in reversed(range(0, 4)):  # llegiré de m5 a m2 perquè mola més com més gros
                    mn = [m2, m3, m4, m5][i]
                    if len(mn) > 1:
                        break
                if len(mn) < 2:
                    return genera_ex_px(tipus, 2, solucions=solucions, par=par)  # si no faig prou serà nivell 2
                elif len(mn) > 2:  # si en tinc molts en deixo 2 (que així també dissimulem una mica)
                    mn = random.sample(mn, 2)
                print(rufipx)
                i += 2  # adapto, que es deia i=0 però era m2 i per tant ha de ser i=2, etc
                k = random.choice([i, -i])
                totalk = 0
                for i in mn:
                    ca = rufipx[i] // k  # coeficient davant la k
                    if ca:
                        if abs(ca) != 1:
                            rufipx[i] = f"{ca}{par}"
                        elif ca > 0:
                            rufipx[i] = f"{par}"
                        else:
                            rufipx[i] = f"-{par}"
                    else:
                        rufipx[i] = 0
                    totalk += k*ca * d**(len(rufipx)-i-1)
                if not totalk:
                    k = r"${\rm I\!R}$"

            elif nivell == 4:  # subs un per sumes (k+1)
                i = random.randint(0, len(rufipx)-1)
                sa = random.randint(1, 2) * random.choice([-1, 1])  # sumand "a" (k+a)
                k, rufipx[i] = (rufipx[i]-sa), f"({par}{amb_signe(sa)})"

            elif nivell == 5:  # multisumes (k+a), (k+b)
                if d != -1:  # esquivo els indeterminats més obvis
                    i, j = random.sample(range(len(rufipx)), 2)
                else:
                    i, j = random.sample(range(len(rufipx))[random.choice([0, 1])::2], 2)  # agafa 2 imparells o parells
                if j < i:  # asseguro el sumand petit al grau gran (la i el porta escollit, la j calculat)
                    j, i = i, j
                sa = random.randint(1, 2) * random.choice([-1, 1])  # sumand "a" [i] = (k+a)
                k, rufipx[i] = (rufipx[i]-sa), f"({par}{amb_signe(sa)})"
                sb = rufipx[j] - k
                if sb:
                    rufipx[j] = f"({par}{amb_signe(sb)})"
                else:
                    rufipx[j] = par

                if not d**(len(rufipx)-i-1) + d**(len(rufipx)-j-1):
                    k = r"${\rm I\!R}$"

            elif nivell == 6:  # sumes i multis alhora
                i = random.choice([x for x in range(len(rufipx)) if rufipx[x]])
                j = random.choice([x for x in [len(rufipx)-1, len(rufipx)-2] if x != i])
                divs = divisors(rufipx[i], True)
                ca = random.choice(divs) * random.choice([-1, 1])  # coef "a" que deixo davant la k
                if not ca:
                    ca = random.choice([-1, 1])
                k = rufipx[i] // ca
                if abs(ca) != 1:
                    rufipx[i] = f"{ca}{par}"
                elif ca > 0:
                    rufipx[i] = f"{par}"
                else:
                    rufipx[i] = f"-{par}"

                if not ca * d**(len(rufipx)-1-i) + d**(len(rufipx)-1-j):  # em carrego la majoria d'indefinits
                    j = random.choice([x for x in range(len(rufipx)) if x != i and x%2 == i%2])
                sb = rufipx[j] - k
                if sb:
                    rufipx[j] = f"({par}{amb_signe(sb)})"
                else:
                    rufipx[j] = par

                if not ca * d**(len(rufipx)-1-i) + d**(len(rufipx)-1-j):  # indefinit (perdo les k)
                    k = r"${\rm I\!R}$"

            elif nivell == 10:  # TODO subs multivar (comparant amb residu ...de fet això amb rufini no es pot, no?)
                ...
            px = polinomitza(rufipx)
            dx = polinomitza([1, -d])

            text = squarebracketer(f"({px})\div ({dx})")
            solu = f"{k}"

    if solucions:
        return text, solu
    return text

genera_ex_px = px  # alias perquè sovint matxaco el nom de px amb altres coses perquè sóc un xungo suposo


def op_algeb(tipus, nivell=1, solucions=True, r=False):
    text = r"\frac{42x+42}{42x}"
    solu = r"\frac{42x}{42}"
    if tipus == 1:  # suma
        if nivell == 8:
            ...
        if nivell in [10, 11]:
            """ 
                Gx + C    Hx + D       Ex + F
                ------- + ------- + ------------
                 x + A     x + B    x2+(A+B)x+AB
            """
            # coef control
            g = random.randint(-3, 3)
            h = random.choice([h for h in range(-3, 4) if h != -g])  # evito g+h=0 (que mataria la solució)
            k = random.choice([k for k in range(-10, 10) if -20 < k*(g+h) < 20]
                              or [11])
            control = k*(g+h)
            a = random.randint(-5, 5)
            b = random.choice([b for b in range(-10, 10) if -10 < g*(a-b) + control < 10 and b != a]
                              or [11])
            control = g*(a-b) + control
            d = random.choice([d for d in range(-10, 10) if -10 < control - d < 10]
                              or [11])
            e = random.choice([e for e in range(-10, 10) if ((0 if g else 1) <= abs(control - (d + e)) < 10)]
                              or [11])
            # forced coefs
            c = control - (d + e)
            f = a*k*(g+h) - c*b - a*d
            fr1 = Fr(npx([c, g]), npx([a, 1]))
            fr2 = Fr(npx([d, h]), npx([b, 1]))
            fr3 = Fr(npx([f, e]), npx([a*b, a+b, 1]))
            text = [fr1, fr2, fr3]
            if nivell == 11:
                for fr in text:
                    if fr.num.termes[0].coef < 0:
                        fr.signe = -1
                        fr.num *= -1
            random.shuffle(text)
            fkey = 'r' if r else ''
            text = "".join(f"{t:{fkey}{'s' if i else ''}}" for i, t in enumerate(text))
            if k == b:
                solu = f"{g+h}"
            else:
                if g+h == 1 and k:
                    solu = f"{Fr(npx([k, 1]), npx([b, 1])):{fkey}}"
                else:
                    solu = f"{Fr(Mul([g+h, npx([k, 1])]), npx([b, 1])):{fkey}}"
    elif tipus == 2:  # resta
        ...
    elif tipus == 3:  # multi
        ...
    elif tipus == 4:  # divi
        ...

    if solucions:
        return text, solu
    return text


def frufinable(nmax=5):
    """Retorna un factor aleatori rufinable

    :param nmax: valor màxim de l'arrel (en valor absolut)
    """
    return [1, random.randint(1, random.choice([2, nmax])) * random.choice([1, -1])]


def polinomi(grau, termes=0, ordenat=True, cmax=15, obliga=[], negatius=1, suavitzat=False, rufinat=False):
    """Crea un polinomi aleatori amb els paràmetres proposats (i opcionalment llista de coefs)

    :param grau: grau del polinomi (grau del terme de grau més gran)
    :param termes: quantitat de termes que tindrà (incloent sempre el de grau més gran)
    :param ordenat: True vol dir de grau gran a grau petit
    :param cmax: coeficient màxim que apareixerà al polinomi (per fer una mica de coef control)
    :param obliga: llista de termes que cal incloure segur (perquè l'exercici en parla, o qui sap)
    :param negatius: 0 positiu tot, 1 qualsevol, 2 negatiu tot
    :param suavitzat: suavitza els coeficients (esp. dels graus més alts)
    :param rufinat: treu una llista amb només els coefs (posant zeros on calgui)
    """
    # opcions
    po = []
    for x in obliga:
        if x < grau:  # no incloc el grau del P(x) en sí pq ja era obligat (si no el tingués, no seria del grau adequat)
            po.append(x)  # graus obligats del polinomi

    if not termes:  # per defecte el faig complet
        termes = grau + 1

    # càlculs
    px = [x for x in range(grau+1) if x not in po and x != grau]
    try:
        px = [grau] + random.sample(px, termes-1-len(po)) + po  # agafo el grau màx, uns random, i els obligats
    except:
        print("S'han obligat massa coses.")
        px = [x for x in range(grau+1)]

    if ordenat:
        px.sort()
        px.reverse()
    else:
        random.shuffle(px)

    # muntatge
    coefs = [0 for _ in range(grau+1)]
    for i, grau in enumerate(px):
        if i == 0:
            signe = False
        else:
            signe = True
        if suavitzat:  # limita els coefs més alts
            if grau > 2:
                coef = random.randint(1, min(i+1, 2))
            else:
                coef = random.randint(1, 16//(grau+1))
        else:
            coef = random.randint(1, cmax)
        if negatius == 2 or (not negatius == 0 and not random.randint(0, 2)):
            coef *= -1
        coefs[-grau-1] = coef
        px[i] = monomi(coef, grau, signe)
    if rufinat:
        return "".join(px), coefs
    return "".join(px)


def polinomitza(rufinat, ordenat=True, ordre2=False):
    """escriu el polinomi a partir dels coefs (sense zeros)

    :param rufinat: polinomi donat com a llista de coeficients del rufini
    :param ordenat: de grau més gran a grau més petit
    :param ordre2: en id. notables significa escriure'l a^2+b^2+2ab
    """
    px = []
    for i, x in enumerate(rufinat):
        if x:
            px.append(monomi(x, len(rufinat)-i-1, True))
    if not ordenat:
        random.shuffle(px)
    elif ordre2 and len(px) == 3:
        px = [px[0]]+[px[2]]+[px[1]]
        print(px)
    if px[0].startswith("+"):
        px[0] = px[0][1:]
    return "".join(px)


def poli_op(op, px, qx):
    """Suma (op=1), resta (op=2) o multiplica (op=3) els polinomis donats

    :param op: 1 suma, 2 resta, 3 multiplica
    :param px: primer polinomi a operar, P(x) com a llista de coeficients
    :param qx: segon polinomi a operar, Q(x) com a llista de coeficients
    """
    if op == 1:  # suma
        sol = [0 for _ in range(max(len(px), len(qx)))]
        for x in range(len(sol)):  # això fa la suma. jo tampoc l'entendré d'aquí un mes, but it works
            if x < len(px):
                sol[-x-1] += px[-x-1]
            if x < len(qx):
                sol[-x-1] += qx[-x-1]

    elif op == 2:  # resta
        sol = [0 for _ in range(max(len(px), len(qx)))]
        for x in range(len(sol)):  # això fa la resta. jo tampoc l'entendré d'aquí un mes, but it works
            if x < len(px):
                sol[-x-1] += px[-x-1]
            if x < len(qx):
                sol[-x-1] -= qx[-x-1]

    elif op == 3:  # multi
        sol = [0 for _ in range(len(px) + len(qx) - 1)]
        for x in range(len(px)):
            for y in range(len(qx)):
                if px[-x-1] and qx[-y-1]:
                    sol[-(x+y)-1] += px[-x-1] * qx[-y-1]

    elif op == 4:  # divi
        ...

    return sol


def poli_aval(rufipx, x):
    suma = 0
    for i in range(len(rufipx)):
        if rufipx[-i-1]:
            suma += rufipx[-i-1] * pow(x, i)
    return suma


def eq_base(tipus, nivell=1, solucions=False, fid=0):
    """genera exercicis de base d'equacions (de moment, eq vs id)

    :param tipus: 10 eq vs id
    :param nivell: dificultat (estil d'equació) dins el tipus
    :param solucions: incloure solucions (si en té)
    :param fid: forçar identitat (0 no, 1 id, 2 eq)
    :return: text de l'exercici
    """
    text = "42+x=x+42"
    solu = "NI IDEA, NEN"

    if tipus == 10:  # equació vs identitat
        if fid == 1 or (fid == 0 and moneda()):
            ident = True
        else:
            ident = False

        if nivell == 1:
            # Ax+B = C(x+D)  ->   Ax+B = Cx+CD
            """ident: A=C, B=CD"""
            a, d = [random.randint(1, 7) * random.choice([1, -1]) for _ in range(2)]
            # coef control (ident)
            c = a
            b = c*d
            if not ident:
                c = random.randint(1, 7) * random.choice([1, -1])
            # muntatge
            if moneda():  # B amb A
                text1 = f"{polinomitza([a, b], False)}"
                text2 = f"{c}({polinomitza([1, d], False)})"
            else:
                if moneda():  # Ax sola
                    text1 = f"{monomi(a, 1)}"
                    if moneda():
                        text2 = f"{ncoef(c)}({polinomitza([1, d], False)}){signe(-b)}"
                    else:
                        text2 = f"{-b}{signe(c)}({polinomitza([1, d], False)})"
                else:  # B sola
                    text1 = f"{b}"
                    if moneda():
                        text2 = f"{ncoef(c)}({polinomitza([1, d], False)}){monomi(-a, 1, True)}"
                    else:
                        text2 = f"{monomi(-a, 1)}{signe(c)}({polinomitza([1, d], False)})"
            # solució
            if a == c and b == c*d:
                solu = "id"
            else:
                solu = "eq"

            text = random.choice([f"{text1}={text2}", f"{text2}={text1}"])

        elif nivell == 2:
            # A(x+B)+Cx = D(x+E)+Fx  ->  (A+C)x+AB = (D+F)x+DE
            """ident: C=D+F-A, AB=DE"""
            d, e, f = [random.randint(1, 7) * random.choice([1, -1]) for _ in range(3)]
            # coef control
            a = random.choice(divisors(d*e, True)) * random.choice([1, -1])
            if not a:
                a = 1
                print("OJUT")
            b = d*e // a
            c = d+f-a
            if not c:
                offset = random.choice([-1, 1, -2, 2])
                c += offset
                f += offset
            if not ident:
                aux = random.randint(1, 7) * random.choice([1, -1])
                if not random.randint(0, 2):
                    a = aux
                elif moneda():
                    b = aux
                else:
                    c = aux
            # muntatge
            if moneda():  # bloc+cx
                text1 = f"{ncoef(a)}({polinomitza([1, b], False)}){monomi(c, 1, True)}"
            else:  # cx+bloc
                text1 = f"{monomi(c, 1)}{ncoef(a, True)}({polinomitza([1, b], False)})"
            if moneda():  # bloc+fx
                text2 = f"{ncoef(d)}({polinomitza([1, e], False)}){monomi(f, 1, True)}"
            else:  # fx+bloc
                text2 = f"{monomi(f, 1)}{ncoef(d, True)}({polinomitza([1, e], False)})"
            # solució
            if c == d+f-a and a*b == d*e:
                solu = "id"
            else:
                solu = "eq"

            text = random.choice([f"{text1}={text2}", f"{text2}={text1}"])

        elif nivell == 3:
            # (x+A)(x-A)+B = x^2+C  ->   x^2-A^2+B=x^2+C
            """ident: C=B-A^2"""
            a = random.randint(1, 5) * random.choice([1, -1])
            b = random.randint(1, 7) * random.choice([1, -1])
            # coef control
            c = b - a*a
            if not ident:
                c += random.randint(1, 4) * random.choice([1, -1])
            if not c:
                offset = random.choice([-1, 1, -2, 2])
                c += offset
                b += offset
            # muntatge
            text1 = f"(x{signe(a)})(x{signe(-a)})"
            if moneda():
                text1 += f"{signe(b)}"
            else:
                text1 = f"{b}+{text1}"
            if moneda():
                text2 = f"x^2{signe(c)}"
            else:
                text2 = f"{c}+x^2"
            # solució
            if c == b - a*a:
                solu = "id"
            else:
                solu = "eq"

            text = random.choice([f"{text1}={text2}", f"{text2}={text1}"])

        elif nivell == 4:
            # (x+A)(x+B) = x^2+Cx+D  ->  x^2+(A+B)x+AB = x^2+Cx+D
            """ident: A+B=C, D=AB"""
            ...
    if solucions:
        return text, solu
    return text


def eq(tipus, nivell=1, solucions=False, totexist=False, x=-42, seed=None, ordenat=True):
    """
    :param tipus: 1, 2... lineals / 101, 102... quadràtiques / 201, 202... irracionals
    :param nivell: (subtipus)
    :param solucions: incloure solucions (els que en tenen)
    :param totexist: evitar arrels negatives
    :param x: solució escollida des de fora (per evitar massa repetits)
    :param seed: llavor de l'aleatori si ve de fora (biq.)
    :param ordenat: polinomi ordenat (per biquadrades)
    :return:
    """
    solus = "NOT DEF"
    text = "x=42"

    if tipus == 1:  # TIPUS x+B=C
        if nivell == 1 or nivell == 2:  # x esquerra (números petits) || x on sigui, (números petits)
            if x == -42:  # no en venia una de fora
                x = random.randint(-10, 10)
            b = random.randint(1, 5)
            print(x, b, "//", x+b, x-b)
            if (abs(x+b) < 11 and abs(x-b) < 11 and moneda()) or abs(x-b) < abs(x+b):
                b = -b
                print("canvi")
            c = x+b
            # muntatge
            if moneda():
                if nivell == 1 or moneda():
                    text = f"x{sig(b)}={c}"
                else:
                    text = f"{c}=x{sig(b)}"
            else:
                if nivell == 1 or moneda():
                    text = f"{b}+x={c}"
                else:
                    text = f'{c}={b}+x'

    elif tipus == 2:  # TIPUS Ax+B=C
        if nivell == 1:  # (innecessari) resultat enter positiu, no divideix per negatiu (a>0), coef max = 50
            x = random.randint(0, 9)
            a = random.randint(2, 9)
            b = random.randint(1, 9)  # límits estables per a*x<100 (aquí = 50)
            c = a * x + b
        elif nivell == 2:  # resultat enter, no divideix per negatiu (a>0) ,coef max = 50
            x = random.randint(-9, 9)
            a = random.randint(2, 9)
            b = random.randint(1, 9)
            if moneda():
                b = -b
            c = a * x + b
        else:  # resultat enter, coef max = 50
            x = random.randint(-9, 9)
            a = random.randint(2, 9)
            if moneda():
                a = -a
            b = random.randint(1, 9)
            if moneda():
                b = -b
            c = a * x + b
        if moneda():
            if b > 0:
                b = f'+{b}'
            text = f'{a}x{b}'
        else:
            if a > 0:
                a = f'+{a}'
            text = f'{b}{a}x'
        if moneda():
            text = text + f'={c}'
        else:
            text = f'{c}=' + text

    elif tipus == 3:  # lineals: opera i resol
        if nivell == 1:  # (6 termes) Ax + Bx + Cx + D + E + F = 0
            x = random.randint(-10, 10)
            # coeficients
            a, b, c = [random.choice([-1, 1]) * random.randint(1, 5) for _ in range(3)]
            if (a + b + c) == 0:  # evito indeterminat
                if a == 1 or moneda():
                    a += 1
                else:
                    a -= 1
            blocx = (a + b + c) * x
            if abs(blocx) > 50:  # si la F quedarà enorme, compenso amb signe contrari i restant gros
                d, e = [-abs(blocx) // blocx * random.randint(10, 20) for _ in range(2)]
            else:
                d, e = [random.choice([-1, 1]) * random.randint(1, 15) for _ in range(2)]
            f = -1 * ((a + b + c) * x + (d + e))
            # muntatge
            if moneda():  # faig al menys un de cada a cada costat
                etext = f"{monomi(a, 1) + signe(d)}"
            else:
                etext = f"{d}" + f"{monomi(a, 1, True)}"
            if moneda():
                dtext = f"{monomi(-b, 1) + signe(-e)}"
            else:
                dtext = f"{-e}" + f"{monomi(-b, 1, True)}"

            if moneda():
                etext += f"{monomi(c, 1, True)}"
            else:
                dtext += f"{monomi(-c, 1, True)}"
            if moneda():
                etext += f"{signe(f)}"
            else:
                dtext += f"{signe(-f)}"

            text = etext + "=" + dtext

    elif tipus == 4:  # lineals: amb parèntesis
        if nivell == 1:  # Ax+B = F(Cx+D)
            x = random.randint(-10, 10)
            c = random.randint(1, 5)
            f = random.randint(2, 3)
            a = random.randint(max(c, f), 10)
            if a == c * f:  # evito indefinit
                a += random.choice([-1, 1])  # això no és mai 0
            d = random.choice([-1, 1]) * random.randint(1, 5)
            b = (f * c - a) * x + f * d
            if random.randint(1, 3) == 1:
                if random.choice([0, 0, 1]):
                    swap = f"{monomi(-a, 1, True)}"
                    text2 = f"{b}"
                else:
                    swap = f"{signe(-b)}"
                    text2 = f"{monomi(a, 1)}"
            else:
                swap = ""
                text2 = f"{monomi(a, 1) + signe(b)}"
            if moneda():
                text = f"{f}({monomi(c, 1) + signe(d)}){swap}"
            else:
                text = f"{f}({d}{monomi(c, 1, True)}){swap}"
            if moneda():
                text += "=" + text2
            else:
                text = text2 + "=" + text

        elif nivell == 2:  # E(Ax+B) = F(Cx+D) + G
            x = random.randint(-10, 10)
            # coefs
            a, c = [random.choice([-1, 1]) * random.randint(1, 5) for _ in range(2)]
            e, f = [random.choice([-1, 1]) * random.randint(2, 4) for _ in range(2)]
            b, d = [random.choice([-1, 1]) * random.randint(1, 7) for _ in range(2)]
            # coef control
            if abs(abs(e * a) - abs(f * c)) * abs(x) > 45:  # la diferència entre EA i FC fa un blocx massa gran
                if abs(e * a) < abs(f * c):
                    if abs(e) < abs(a):
                        e = int(e * (abs(f * c) / abs(e * a)))
                    else:
                        a = int(a * (abs(f * c) / abs(e * a)))
                else:
                    if abs(f) < abs(c):
                        c = int(c * (abs(e * a) / abs(f * c)))
                    else:
                        f = int(f * (abs(e * a) / abs(f * c)))
            if e * a // abs(e * a) == -f * c // abs(f * c) and abs(
                    e * a - f * c) > 6:  # si sumen (i queda gros) faig que restin
                c = -c
            if e * a == f * c:  # evito indeterminat
                if a == 1 or moneda():
                    a += 1
                else:
                    a -= 1
            blocx = (e * a - f * c) * x
            if abs(blocx) > 40:  # si segueix mig gros, ajudo amb els independents
                if e * b * blocx > 0:  # mateix signe
                    b = -b
                if -f * d * blocx > 0:
                    d = -d
            else:
                if abs(abs(e * b) + abs(f * d)) > 10 and e * b * (
                        -f * d) > 0:  # si sumen bastant i els estic sumant, resto
                    b = -b
                if (abs(e * b) > abs(f * d) and e * b * blocx > 0) or (abs(f * d) > abs(e * b) and -f * d * blocx > 0):
                    b = -b
                    d = -d
            g = blocx + e * b - f * d
            # muntatge
            if moneda():
                text1 = f"{e}(" + monomi(a, 1) + signe(b) + ")"
            else:
                text1 = f"{e}({b}" + monomi(a, 1, True) + ")"
            if moneda():
                text2 = f"{f}(" + monomi(c, 1) + signe(d) + ")"
            else:
                text2 = f"{f}({d}" + monomi(c, 1, True) + ")"
            if random.randint(0, 4):  # de tant en tant els poso al mateix costat
                if text2.startswith("-"):
                    text1 = text1 + "+" + text2[1:]
                else:
                    text1 = text1 + "-" + text2
                text2 = f"{g}"
            else:
                if moneda():
                    text1 += f"{signe(-g)}"
                else:
                    text2 += f"{signe(g)}"
            if moneda():
                text = text1 + "=" + text2
            else:
                text = text2 + "=" + text1

    elif tipus == 5:  # lineals amb fraccions
        if nivell == 1:  # alguna cosa més senzilla
            ...
        elif nivell == 2:  # fraccions (resultat fracció) TODO entendre per què no surt enter
            x = random.randint(-10, 10)
            # coefs
            e = random.choice([2, 3])
            f = random.choice([2, 3, 4, 5, 6, 7])
            if moneda():
                e, f = f, e
            if random.randint(0, 4) and mcm(e, f) < 20:  # de tant en tant un dels dos és ja el mcm
                if moneda():
                    e = mcm(e, f)
                else:
                    f = mcm(e, f)
            a, c, g = [random.choice([-1, 1]) * random.randint(1, 5) for _ in range(3)]
            b, d = [random.choice([-1, 1]) * random.randint(0, 10) for _ in range(2)]  # permeto zeros als independents
            h = random.randint(-5, 5)
            # coef control
            na, nc, ng = a, c, g
            bestnum = 1000000
            for n in sorted([[1, 1, 1], [1, 1, -1], [1, -1, 1], [-1, 1, 1]]):  # trio signes per fer petit el denomin.
                num = abs(na * f + nc * e + ng * e * f)
                if num and num < bestnum:
                    a, c, g = na, nc, ng
            nb, nd = b, d
            bestnum = 1000000
            for n in sorted([[1, 1], [1, -1]]):  # trio signes per fer petit el numerador
                num = abs(nb * f + nd * e)
                if num and num < bestnum:
                    b, d = nb, nd
            bestmcd = 1
            for n in sorted(range(-5, 5)):  # trio la h que millor simplifica
                # n és h provisional
                num = b * f + d * e + n * e * f
                den = a * f + c * e + g * e * f
                if num and den:
                    elmcd = mcd(abs(num), abs(den))
                    if elmcd > bestmcd:
                        h = n
                        bestmcd = elmcd
            # simplificacions (si es pot)
            if b == 0:
                a, e = fracsimple(a, e)
            if d == 0:
                c, f = fracsimple(c, f)
            for k in reversed(divisors(e, True)):
                if not (a % k or b % k or e % k):
                    a = a // k
                    b = b // k
                    e = e // k
            for k in reversed(divisors(f)):
                if not (c % k or d % k or f % k):
                    c = c // k
                    d = d // k
                    f = f // k
            # muntatge
            m = monomi
            if a < 0 and b < 0:
                a = -a
                b = -b
                s = "-"
            else:
                s = ""
            if b == 0:
                frac1 = f"{m(a, 1)}"
            else:
                frac1 = random.choice([f"{m(a, 1)}{signe(b)}", f"{b}{m(a, 1, True)}"])
            if e != 1:
                frac1 = s + "\\frac{" + frac1 + "}{" + f"{e}" + "}"
            else:
                frac1 = s + "(" + frac1 + ")"

            if c < 0 and d < 0:
                c = -c
                d = -d
                s = "-"
            else:
                s = ""
            if d == 0:
                frac2 = f"{m(c, 1)}"
            else:
                frac2 = random.choice([f"{m(c, 1)}{signe(d)}", f"{d}{m(c, 1, True)}"])
            if f != 1:
                frac2 = s + "\\frac{" + frac2 + "}{" + f"{f}" + "}"
            else:
                frac2 = s + "(" + frac2 + ")"

            if h == 0:
                frach = ""
            else:
                frach = f"{h}"

            etext = frac1
            dtext = ""
            for x in sorted(range(4)):  # 0 CDF, 1 G, 2 HJ
                if x == 0:  # CDF
                    if moneda():  # esq
                        if frac2.startswith("-"):
                            etext += frac2
                        else:
                            etext += "+" + frac2
                    else:  # dr
                        if frac2.startswith("-"):
                            if not dtext:
                                dtext += frac2[1:]
                            else:
                                dtext += "+" + frac2[1:]
                        else:
                            dtext += "-" + frac2
                elif x == 1:  # G
                    if moneda():  # esq
                        if moneda():  # esq-e
                            if etext.startswith("-"):
                                etext = m(g, 1) + etext
                            else:
                                etext = m(g, 1) + "+" + etext
                        else:  # esq-d
                            etext += m(g, 1, True)
                    else:  # dr
                        if not dtext:
                            dtext = m(-g, 1)
                        else:
                            dtext += m(-g, 1, True)
                elif x == 2 and frach != "":  # H
                    if moneda():  # esq
                        if moneda():  # esq-e
                            if etext.startswith("-"):
                                etext = frach + etext
                            else:
                                etext = frach + "+" + etext
                        else:  # esq-d
                            if frach.startswith("-"):
                                etext += frach
                            else:
                                etext += "+" + frach
                    else:  # dr
                        if frach.startswith("-"):
                            if not dtext:
                                dtext += frach[1:]
                            else:
                                dtext += "+" + frach[1:]
                        else:
                            dtext += "-" + frach
            if not dtext:
                dtext = "0"
            text = etext + "=" + dtext
            print(text, "||", a, b, c, d, e, f, g, h)

        elif nivell == 9:  # (Ax+B)/E + (Cx+D)/F + Gx + H/J = 0;  [J = EF] [simplificat tot quan es pot]
            """AIXÒ NO HA FUNCIONAT BÉ. CREC QUE NO VAL LA PENA RESULTAT ENTER"""
            x = random.randint(-10, 10)
            # coefs
            e, f = random.sample(sorted([2, 3, 4, 5, 6, 7]), 2)
            if random.randint(0, 4) and mcm(e, f) < 20:  # de tant en tant un dels dos és ja el mcm
                if moneda():
                    e = mcm(e, f)
                else:
                    f = mcm(e, f)
            a, c, g = [random.choice([-1, 1]) * random.randint(1, 5) for _ in range(3)]
            b, d = [random.choice([-1, 1]) * random.randint(0, 10) for _ in range(2)]  # permeto zeros als independents
            # coef control
            print(a * f, c * e, g * e * f, ")", x, "// ", b * f, d * e, "||", g, "(", e, f)
            if abs(g * e * f) > 90 or (abs(g * e * f) > 40 and abs(x) > 3) or (abs(g * e * f) > 25 and abs(x) > 5):
                if abs(g) > 2:
                    if abs(g * e * f) < 200 and abs(e * f * 2) < 60 and x < 5:
                        g = random.choice([1, 2, -1, -2])
                    else:
                        g = random.choice([1, -1])
                if abs(g * e * b) > 42:
                    if abs(x) < 3:
                        lim = 7
                    else:
                        lim = 4
                    if abs(e) > abs(f):
                        e = e % lim + 1
                        if abs(e) == 1:
                            e += e
                    else:
                        f = f % lim + 1
                        if abs(f) == 1:
                            f += f
            print(a * f, c * e, g * e * f, ")", x, "// ", b * f, d * e, "||", g, "(", e, f)
            if abs(g * e * f) > 30 or x > 5 or abs(a * f + c * e + g * e * f) > 30:
                if a * f * c * e < 0:  # si no s'ajuden
                    if abs(abs(a * f) + abs(c * e) - abs(g * e * f)) < abs(g * e * f) \
                            and not max(abs(a * f), abs(c * e)) > abs(g * e * f):  # si no es desmadrarà
                        if a * g * e < 0:  # faig que s'ajudin contra el GEF
                            c = -c
                        else:
                            a = -a
                    else:  # poso el més gros en contra
                        if (abs(a * f) > abs(c * e) and a * g * e > 0) or (abs(c * e) > abs(a * f) and c * g * f > 0):
                            a = -a
                            c = -c
                else:  # si s'ajuden
                    if a * g * e > 0:
                        a = -a
                        c = -c
            print(a * f, c * e, g * e * f, ")", x, "// ", b * f, d * e, "||", g, "(", e, f)
            blocx = (a * f + c * e + g * e * f) * x
            print(x, blocx)
            if abs(blocx) > 60:
                x = max(1, x // 2)
            if abs(blocx) > 40:
                x = max(1, x - 2)
            blocx = (a * f + c * e + g * e * f) * x
            print(x, blocx)
            h = -(blocx + (b * f + d * e))
            print(h)
            j = e * f
            # simplificacions (si es pot)  # TODO no està bé quan una simplifica més que l'altra
            if fracsimple(a, e)[1] == fracsimple(b, e)[1]:
                a = fracsimple(a, e)[0]
                b, e = fracsimple(b, e)
            if fracsimple(c, f)[1] == fracsimple(d, f)[1]:
                c = fracsimple(c, f)[0]
                d, f = fracsimple(d, f)
            h, j = fracsimple(h, j)
            # muntatge
            m = monomi
            if a < 0 and b < 0:
                a = -a
                b = -b
                s = "-"
            else:
                s = ""
            frac1 = s + "\\frac{" + random.choice([f"{m(a, 1)}{signe(b)}", f"{b}{m(a, 1, True)}"]) + "}{" + f"{e}" + "}"
            if c < 0 and d < 0:
                c = -c
                d = -d
                s = "-"
            else:
                s = ""
            frac2 = s + "\\frac{" + random.choice([f"{m(c, 1)}{signe(d)}", f"{d}{m(c, 1, True)}"]) + "}{" + f"{f}" + "}"
            if h < 0:
                h = -h
                s = "-"
            else:
                s = ""
            if h == 0:
                frach = ""
            elif j == 1:
                frach = f"{h}"
            else:
                frach = s + "\\frac{" + f"{h}" + "}{" + f"{j}" + "}"

            etext = frac1
            dtext = ""
            for x in sorted(range(4)):  # 0 CDF, 1 G, 2 HJ
                if x == 0:  # CDF
                    if moneda():  # esq
                        if frac2.startswith("-"):
                            etext += frac2
                        else:
                            etext += "+" + frac2
                    else:  # dr
                        if frac2.startswith("-"):
                            if not dtext:
                                dtext += frac2[1:]
                            else:
                                dtext += "+" + frac2[1:]
                        else:
                            dtext += "-" + frac2
                elif x == 1:  # G
                    if moneda():  # esq
                        if moneda():  # esq-e
                            if etext.startswith("-"):
                                etext = m(g, 1) + etext
                            else:
                                etext = m(g, 1) + "+" + etext
                        else:  # esq-d
                            etext += m(g, 1, True)
                    else:  # dr
                        if not dtext:
                            dtext = m(-g, 1)
                        else:
                            dtext += m(-g, 1, True)
                elif x == 2:  # HJ
                    if moneda():  # esq
                        if moneda():  # esq-e
                            if etext.startswith("-"):
                                etext = frach + etext
                            else:
                                etext = frach + "+" + etext
                        else:  # esq-d
                            if frach.startswith("-"):
                                etext += frach
                            else:
                                etext += "+" + frach
                    else:  # dr
                        if frach.startswith("-"):
                            if not dtext:
                                dtext += frach[1:]
                            else:
                                dtext += "+" + frach[1:]
                        else:
                            dtext += "-" + frach
            if not dtext:
                dtext = "0"
            text = etext + "=" + dtext

    elif tipus == 101:  # x^2-C (treure l'arrel)
        nexist = False
        if nivell == 1:  # quadrat perfecte, x2 sense coef
            if x == -42:  # si no l'he definit des de fora la trio aquí
                x = random.randint(1, 10)
            text = f"x^2-{pow(x, 2)}=0"
        elif nivell == 2:  # pot sortir impossible (i zero a qualsevol costat)
            if x == -42:  # si no l'he definit des de fora la trio aquí
                x = random.randint(1, 10)
            if random.choice([0, 0, 1]) and not totexist:  # arrel neg
                nexist = True
                text = f"x^2+{pow(x, 2)}"
            else:
                text = f"x^2-{pow(x, 2)}"  # normal
            if random.choice([1, 1, 0]):
                text = text + "=0"
            else:
                text = "0=" + text

        elif nivell == 3:  # amb coef (ax^2-ac=0)
            if x == -42:  # si no l'he definit des de fora la trio aquí
                x = random.randint(1, 10)
            c = pow(x, 2)
            a = random.randint(-3, 3)
            if a == 0:
                a = random.choice([1, -1])

            if random.randint(0, 2) or totexist:  # normalment canviat de signe (arrel possible)
                tc = -a * c
            else:  # una de cada tres arrel impossible
                tc = a * c
                nexist = True

            if moneda():
                text = f"{monomi(a, 2)}{signe(tc)}"
            else:
                text = f"{tc}{monomi(a, 2, True)}"

            if random.randint(0, 2):
                text += "=0"
            else:
                text = "0=" + text

    elif tipus == 102:  # x^2+Bx (desacoblar)
        if x == -42:  # si no l'he donada, la trio
            x = random.randint(-10, 10)
        if x == 0:
            x = random.choice([1, -1])
        if nivell == 1 or nivell == 2:  # zero a la dreta, sense coef
            if x > 0:
                if x == 1:
                    text = f"x^2+x"
                else:
                    text = f"x^2+{x}x"
            else:
                if x == -1:
                    text = f"x^2-x"
                else:
                    text = f"x^2{x}x"
            if nivell == 1 or random.choice([1, 1, 0]):
                text = text + "=0"
            else:
                text = "0=" + text

        elif nivell == 3:  # amb coef
            a = random.randint(-3, 3)
            if a == 0:
                a = random.choice([-1, 1])
            tb = f"{a * x}x"
            if a == 1:
                ta = "x^2"
                if x == 1:
                    tb = "x"
                elif x == -1:
                    tb = "-x"
            elif a == -1:
                ta = "-x^2"
                if x == -1:
                    tb = "x"
                elif x == 1:
                    tb = "-x"
            else:
                ta = f"{a}x^2"
                tb = f"{a * x}x"

            if moneda():
                if a * x > 0:
                    text = f"{ta}+{tb}"
                else:
                    text = f"{ta}{tb}"
            else:
                if a > 0:
                    text = f"{tb}+{ta}"
                else:
                    text = f"{tb}{ta}"
            if random.choice([1, 1, 0]):
                text = text + "=0"
            else:
                text = "0=" + text

    elif tipus == 103:  # Ax^2+Bx+C (sencera)
        x1 = random.randint(-10, 10)
        if x1 == 0:
            x1 = random.choice([-1, 1])
        x2 = random.randint(-7, 7)
        if x2 == 0:
            x2 = random.choice([-1, 1])
        if x1 == -x2:  # evita b=0
            x1 = x2
        b = -x1 - x2
        c = x1 * x2

        if nivell == 1:  # sense coef A, ordenada
            if b > 0:
                if b == 1:
                    tb = "+x"
                else:
                    tb = f"+{b}x"
            else:
                if b == -1:
                    tb = "-x"
                else:
                    tb = f"{b}x"
            if c > 0:
                tc = f"+{c}"
            else:
                tc = f"{c}"
            text = f"x^2{tb}{tc}"
            if random.choice([1, 1, 0]):
                text = text + "=0"
            else:
                text = "0=" + text

        elif nivell == 2 or nivell == 3:  # A ±1 || amb coef A
            x1 = random.randint(-10, 10)
            if x1 == 0:
                x1 = random.choice([-1, 1])
            x2 = random.randint(-7, 7)
            if x2 == 0:
                x2 = random.choice([-1, 1])
            if x1 == -x2:  # evita b=0
                x1 = x2

            if nivell == 3:
                a = random.randint(-3, 3)
                if a == 0:
                    a = random.choice([-2, 2])
            else:
                a = random.choice([-1, 1])
            b = a * (-x1 - x2)
            c = a * (x1 * x2)
            primer = random.choice([2, 1, 0])

            if a > 0 and primer != 2:
                if a == 1:
                    ta = "+x^2"
                else:
                    ta = f"+{a}x^2"
            else:
                if a == -1:
                    ta = "-x^2"
                elif a == 1:
                    ta = "x^2"
                else:
                    ta = f"{a}x^2"
            if b > 0 and primer != 1:
                if b == 1:
                    tb = "+x"
                else:
                    tb = f"+{b}x"
            else:
                if b == -1:
                    tb = "-x"
                elif b == 1:
                    tb = "x"
                else:
                    tb = f"{b}x"
            if c > 0 and primer != 0:
                tc = f"+{c}"
            else:
                tc = f"{c}"

            if primer == 2:
                if moneda():
                    text = f"{ta}{tb}{tc}"
                else:
                    text = f"{ta}{tc}{tb}"
            elif primer == 1:
                if moneda():
                    text = f"{tb}{ta}{tc}"
                else:
                    text = f"{tb}{tc}{ta}"
            elif primer == 0:
                if moneda():
                    text = f"{tc}{ta}{tb}"
                else:
                    text = f"{tc}{tb}{ta}"
            if random.choice([1, 1, 0]):
                text = text + "=0"
            else:
                text = "0=" + text

    elif tipus == 104:  # opera i resol (6 termes)
        x1 = random.randint(-10, 10)
        if x1 == 0:
            x1 = random.choice([-1, 1])
        x2 = random.randint(-7, 7)
        if x2 == 0:
            x2 = random.choice([-1, 1])
        if x1 == -x2:  # evita b=0
            x1 = x2

        a = random.randint(-3, 3)
        if a == 0:
            a = random.choice([-1, 1])
        b = a * (-x1 - x2)
        c = a * (x1 * x2)
        # separa cada terme en dues parts
        a1 = random.randint(-10, +10)
        a2 = a - a1
        b1 = random.randint(-20, +20)
        b2 = b - b1
        c1 = random.randint(-30, +30)
        c2 = c - c1

        ordre = [0, 1, 2, 3, 4, 5]
        random.shuffle(ordre)
        text = "="
        dreta = False
        for x in ordre:
            if x == 0:  # a1
                n = a1
                g = "x^2"
            elif x == 1:
                n = b1
                g = "x"
            elif x == 2:
                n = c1
                g = ""
            elif x == 3:
                n = a2
                g = "x^2"
            elif x == 4:
                n = b2
                g = "x"
            elif x == 5:
                n = c2
                g = ""

            if n != 0:
                if moneda():  # esquerra
                    if abs(n) == 1 and n % 3 != 2:  # evita 1x etc
                        if n == 1:
                            text = f"{g}" + text
                        else:
                            text = f"-{g}" + text
                    else:
                        text = f"{n}{g}" + text
                    if n > 0:
                        text = "+" + text
                else:  # dreta
                    n = -n
                    if n > 0:
                        if dreta:
                            text += "+"
                    if abs(n) == 1 and n % 3 != 2:
                        if n == 1:
                            text += f"{g}"
                        else:
                            text += f"-{g}"
                    else:
                        text += f"{n}{g}"
                    dreta = True
        if text[0] == "+":
            text = text[1:]
        elif text[0] == "=":
            text = "0" + text
        elif text[-1] == "=":
            text += "0"

    elif tipus == 110:  # biquadrades
        a = 1
        if nivell in [1, 2, 3, 4]:  # quatre solucions / dues solucions // quatre amb rand a / dos amb rand a
            t1, t2 = 42, 42
            # càlculs
            if seed is None:
                if nivell in [1, 3]:
                    t1, t2 = random.sample([x ** 2 for x in range(1, 5)], 2)
                elif nivell in [2, 4]:
                    t2, t2 = random.sample([x ** 2 for x in range(1, 5)] + [x for x in range(1, 10)], 2)
                if nivell in [3, 4]:
                    a = random.randint(1, 3)*random.choice([-1, 1])
            else:
                if len(seed) == 3:
                    a = seed[-1]
                    seed = seed[:-1]
                if nivell == 1 and any(t < 0 for t in [t1, t2]):
                    print("Ei, la llavor no quadra amb el nivell")
                t1, t2 = seed

            # muntatge
            fkey = "" if ordenat else "d"
            text = f"{npx([-t1, 0, 1]) * npx([-t2, 0, 1]) * a:{fkey}}=0"

    elif tipus == 111:  # triquadrades
        if nivell == 1:
            a = 1
        else:
            a = random.choice([1, 2, 3]) * random.choice([-1, 1])
        if seed:
            if len(seed) == 3:
                a = seed[-1]
                x1, x2 = seed[:-1]
            else:
                x1, x2 = seed
        else:
            x1, x2 = random.sample([[x, y] for x in range(-4, 5) for y in range(x, 5)
                                    if x*y and abs(x**3 * y**3) < 100], 2)
        # muntatge
        fkey = "" if ordenat else "d"
        text = f"{npx([-x1 ** 3, 0, 0, 1]) * npx([-x2 ** 3, 0, 0, 1]) * a:{fkey}}=0"

    elif tipus == 201:  # irracionals TODO acabar i fer més variants d'enunciat
        if nivell in [1, 2]:  # √(Ax+B) = x+C
            """
            Operant queda x^2 + (2C-A)x + (C^2-B) = 0
            """
            xmax = 4
            # eq2
            x1 = random.randint(1, xmax)
            x2 = random.randint(1, xmax)
            if x1*x2 > 6 or moneda():
                x2 = -x2
            n = -x1-x2
            m = x1*x2
            # coef control
            c = isqrt(abs(n*m)) - random.choice([-1, 0, 1])
            if n == -2*c:
                c += random.choice([-1, 1])
            if n > 0:
                c = -abs(c)
            a = n + 2*c
            b = pow(c, 2) - m
            print(x1, x2, "/", n, m, "/", a, b, c)
            text = ("\\sqrt{" + random.choice([f"{monomi(a, 1)}{signe(b)}", f"{b}{monomi(a, 1, True)}"])
                    + "} = " + random.choice([f"x{signe(c)}", f"{c}{monomi(1, 1, True)}"]))

    if solucions:
        if tipus == 1:  # primer simple
            solus = f"{c - b}"
        elif tipus in [2, 3, 4]:  # primer
            solus = f"{x}"
        elif tipus == 5:  # fracs
            ...  # no tinc el resultat, crec, i no sé per què
        elif tipus == 101:  # treure l'arrel
            if nexist:
                solus = r"$\nexists$"
            else:
                solus = rf"$\pm ${x}"
        elif tipus == 102:  # inc. factoritzant
            solus = f"0,~{-x}"  # (m'he inventat el del factor, no pas l'arrel)
        elif tipus in [103, 104]:
            if x1 == x2:
                solus = f"{x1}"
            else:
                solus = f"{x1},~{x2}"  # el ~ fa l'espai intrencable
        elif tipus == 110:
            solus = ",~".join(fr"$\pm ${isqrt(t)}" for t in [t1, t2] if t > 0)
            print(solus)
        elif tipus == 111:
            solus = ",~".join(f"{x}" for x in [x1, x2])
        elif tipus == 201:
            s = []
            for x in [x1, x2]:
                if a * x + b >= 0:
                    s.append(f"{x}")
            if s:
                solus = ",~".join(s)
            else:
                solus = r"$\nexists$"
        return text, solus
    return text


def sisteq(tipus, nivell=1, nums=1, solucions=False):
    text = text = r"\begin{cases} x+y=42 \\ x+y=42 \end{cases}"
    solus = "NOT DEF"

    if tipus == 1:  # ax+by=c, dx+ey=f
        if nivell in [1, 2, 3]:  # primera x coef 1 || algun coef ±1 || reducció qualsevol
            eq1 = "x+y=42"
            eq2 = "x+y=42"
            x = random.randint(-10, 10)
            y = random.randint(-10, 10)
            coefs = [random.randint(1, 5) for _ in range(4)]
            for n in range(4):
                if moneda():
                    coefs[n] = -coefs[n]
            if nivell == 1:  # la primera x sense coef
                coefs[0] = 1
            elif nivell == 2:  # alguna incògnita unitària
                if not any(n in [1, -1] for n in coefs):
                    coefs[random.randint(0, 3)] = random.choice([1, -1])
            if round(coefs[0] * 1. / coefs[2], 7) == round(coefs[1] * 1. / coefs[3], 7):  # crec que això evita SCI
                coefs[0] = - coefs[0]

            # TODO afegir eqns amb les inc barrejades

            c = coefs[0] * x + coefs[1] * y
            f = coefs[2] * x + coefs[3] * y
            eq1 = systeq_text(coefs[0], coefs[1], c)
            eq2 = systeq_text(coefs[2], coefs[3], f)
            text = r"\begin{cases} " + eq1 + r" \\ " + eq2 + r" \end{cases}"
            solus = f"({x},~{y})"

    elif tipus == 2:  # lineals 2D gràficament (coef control per dibuix fàcil)
        """Trio el punt solució (prop de OY per pendents fàcils) i trio talls amb OY
           Punt solució: (x0, y0) :: pondero sobre tot x0 entre -1 i 1 (pendents enters), 
                                     accepto -2 a 2 (pendents múltiples de 1/2)
           Tall OY primera: (x1, y1) :: n = y1
           Tall OY segona: (x2, y2)  :: n = y2
           
           :: Muntatge ::
           Pendent: my/mx
           Equació:  -(my)x + (mx)y = (mx)*n
        """
        x0 = y0 = 0

        if nivell in [1, 2]:
            # resultat
            y0 = random.randint(-5, 5)
            if random.randint(0, 3):  # 1/4 de vegades cau a {-2, 2}
                if random.randint(0, 3):  # més a {-1, 1} que al 0
                    x0 = random.choice([-1, 1])
                else:
                    x0 = 0
            else:
                x0 = random.choice([-2, 2])
            # coef control
            if x0 in [-2, 2] and nivell == 1:  # nivell 1 sense meitats al pendent
                y1, y2 = random.sample([y0 + 2*i for i in range(-2, 2) if i != 0], 2)
            else:
                y1, y2 = random.sample([y0 + i for i in range(-4, 4) if i != 0], 2)
            # càlcul
            coefs = [[42, 42, 42], [42, 42, 42]]
            ys = [y1, y2]
            for eq in [0, 1]:
                if x0:
                    my = y0 - ys[eq]
                    mx = x0
                    n = ys[eq]
                else:
                    mx = 1
                    my = random.randint(1, 4) * random.choice([-1, 1])
                    n = y0
                coefs[eq] = [-my, mx, mx*n]
            eq1 = systeq_text(coefs[0][0], coefs[0][1], coefs[0][2])
            eq2 = systeq_text(coefs[1][0], coefs[1][1], coefs[1][2])
            text = r"\begin{cases} " + eq1 + r" \\ " + eq2 + r" \end{cases}"
            solus = f"({x0},~{y0})"

    elif tipus == 11:  # NO LINEALS: Ax+By=C, Dx*y=E (sense coef / un coef / dos dels tres coefs)
        # solucions
        x, y = [random.randint(1, 10) * random.choice([1, -1]) for _ in range(2)]
        # coefs
        a = 1
        b = 1
        d = 1
        if nivell == 1 and moneda():  # en algunes de l'1 canvio un signe
            b = -1
        elif nivell == 2:  # al segon introdueixo un número als factors
            a = random.randint(2, 5) * random.choice([-1, 1])
            if moneda():
                a, b = b, a
        elif nivell == 3:  # poso dos dels tres coeficients
            a, b = [random.randint(1, 5) * random.choice([1, -1]) for _ in range(2)]
            d = random.randint(1, 3)
            if not random.randint(0, 2):
                d = 1
            elif moneda():
                a = random.choice([1, -1])
            else:
                b = random.choice([1, -1])
        # càlcul
        c = a*x + b*y
        e = d * x*y
        # muntatge
        eq1 = f"{monomi(a, 1)}{monomi(b, 1, True, var='y')}={c}"
        eq2 = f"{multimonomi(d, exps=[1, 1])}={e}"
        text = r"\begin{cases} " + eq1 + r" \\ " + eq2 + r" \end{cases}"
        # solucions
        if solucions:
            x2 = fraconum(*fracsimple(b*y, a))  # la segona solució, que surt d'intercanviar les variables (Ax=By)
            y2 = fraconum(*fracsimple(a*x, b))  # el * desplega la llista en forma arguments individuals
            x = f"{x}"
            y = f"{y}"
            if x == x2 and y == y2:
                solus = f"({x},~{y})"
            else:
                solus = f"({x},~{y}),~({x2},~{y2})"

    elif tipus == 12:  # NO LINEALS: estil Ax^2+By^2=C, Dx+Ey=F
        """
        Ax^2+By^2=C, Dx+Ey=F
        - Hi ha segona solució si A*E^2+B*D^2 (és el coef del terme de segon grau)
        - La segona solució (aïllant de la fórmula quadràtica) és: 
                     x2 = 2BFD/(A*E^2+B*D^2) - x1
        """
        x, y = [random.randint(1, 6) * random.choice([1, -1]) for _ in range(2)]
        a, b, d, e = [1 for _ in range(4)]
        if nivell == 1:  # x^2-y^2=C, x+y=F (eq primer grau)
            """Unitaris amb un negatiu a la quadràtica: elimina el terme de 2n grau"""
            if random.randint(0, 3):
                b = -1
            else:
                a = -1
            if moneda():
                if random.randint(0, 3):
                    e = -1
                else:
                    d = -1

        elif nivell == 2:  # equació de segon grau (i en tot cas negatiu a sota)
            if moneda():
                if random.randint(0, 3):
                    e = -1
                else:
                    d = -1
        elif nivell == 3:  # Ax^2-By^2=C, Dx+Ey=F (coeficients "qualssevol")
            a, e = [random.randint(1, 3)*random.choice([-1, 1]) for _ in range(2)]
            # coef control
            """
            Busco opcions per resultat enter a 2BFD/(AE^2+BD^2)
            ...o eliminació del terme quadràtic
            """
            opcions = []
            primer = []
            for b in reversed(range(1, 4)):
                for d in reversed(range(1, 4)):
                    f = d*x + e*y
                    num = 2*b*f*d
                    den = a*e*e+b*d*d
                    if not den:  # equació de primer grau (em serveix de candidat també)
                        primer.append([b, d])
                    elif not num % den:  # si surt enter el guardo de candidat
                        opcions.append([b, d])
            if opcions or primer:  # tendeix a haver-hi molts enters (1-5) i algun primer (0-2)
                b, d = random.choice(opcions + primer)
        # càlcul
        c = a*x*x + b*y*y
        f = d*x + e*y
        # muntatge
        eq1 = f"{monomi(a, 2)}{monomi(b, 2, True, var='y')}={c}"
        eq2 = f"{monomi(d, 1)}{monomi(e, 1, True, var='y')}={f}"
        text = r"\begin{cases} " + eq1 + r" \\ " + eq2 + r" \end{cases}"
        # solucions
        ca = a*e*e + b*d*d
        if ca:  # equació de 2n grau
            # càlcul
            x2n = 2*b*f*d - ca*x
            x2d = ca
            y2n = f*x2d-d*x2n
            y2d = e*x2d
            # muntatge
            x = f"{x}"
            y = f"{y}"
            x2 = fraconum(*fracsimple(x2n, x2d))
            y2 = fraconum(*fracsimple(y2n, y2d))
            if y == y2 and x == x2:
                solus = f"({x},~{y})"
            else:
                solus = f"({x},~{y}),~({x2},~{y2})"
        else:  # primer grau (perd el terme de 2n)
            solus = f"({x},~{y})"

    elif tipus == 101:  # ax+by+cz=d, ex+fy+gz=h, ix+jy+kz=m
        if nivell in [1, 2, 3, 4]:  # escala de ±1 (primera x sola || qualsevol x) || alguna x ±1 || gauss normal
            eq1 = "x+y+z=42"
            eq2 = "x+y+z=42"
            x = random.randint(-10, 10)
            y = random.randint(-10, 10)
            z = random.randint(-10, 10)
            coefs = [random.randint(1, 5) for _ in range(9)]
            for n in range(9):
                if moneda():
                    coefs[n] = -coefs[n]
            if nivell in [1, 2]:
                coefs[0] = random.choice([1, -1])  # una de les x sola
                coefs[4] = coefs[3] * coefs[0] * coefs[1] + random.choice([1, -1])  # escalonat amb la segona
                if moneda():  # aleatori quina de les dues és l'escalonada
                    for n in range(3):
                        aux = coefs[n + 3]
                        coefs[n + 3] = coefs[n + 6]
                        coefs[n + 6] = aux
                if nivell == 2 and random.choice([True, True, False]):
                    fila = random.choice([1, 2])  # moc la fila de la x a qualsevol de les altres
                    for n in range(3):
                        aux = coefs[n]
                        coefs[n] = coefs[n + fila * 3]
                        coefs[n + fila * 3] = aux
            elif nivell == 3:
                if not any(n in [1, -1] for n in [coefs[0], coefs[3], coefs[6]]):
                    coefs[random.choice([0, 3, 6])] = random.choice([1, -1])

            # TODO afegir permetre icompatibles i indeterminats (seran botons com les taules)
            # TODO afegir fraccions

            d = coefs[0] * x + coefs[1] * y + coefs[2] * z
            h = coefs[3] * x + coefs[4] * y + coefs[5] * z
            m = coefs[6] * x + coefs[7] * y + coefs[8] * z
            eq1 = systeq3_text(coefs[0], coefs[1], coefs[2], d)
            eq2 = systeq3_text(coefs[3], coefs[4], coefs[5], h)
            eq3 = systeq3_text(coefs[6], coefs[7], coefs[8], m)
            text = r"\begin{cases} " + eq1 + r" \\ " + eq2 + r" \\ " + eq3 + r" \end{cases}"
            solus = f"({x},~{y},~{z})"
    if solucions:
        return text, solus
    return text


def systeq_text(a, b, c):
    """Retorna el text d'una equació tipus ax+by=c"""
    if a == 1:
        ax = 'x'
    elif a == -1:
        ax = '-x'
    else:
        ax = f'{a}x'
    if b >= 0:
        by = '+'
    else:
        by = ''
    if b == 1:
        by = by + 'y'
    elif b == -1:
        by = by + '-y'
    else:
        by = by + f'{b}y'
    return ax + by + f'={c}'


def systeq3_text(a, b, c, d):
    if a == 1:
        ax = 'x'
    elif a == -1:
        ax = '-x'
    elif a == 0:
        ax = ''
    else:
        ax = f'{a}x'
    if b > 0:
        by = '+'
    else:
        by = ''
    if b == 1:
        by = by + 'y'
    elif b == -1:
        by = by + '-y'
    elif b == 0:
        by = ''
    else:
        by = by + f'{b}y'
    if c > 0:
        cz = '+'
    else:
        cz = ''
    if c == 1:
        cz = cz + 'z'
    elif c == -1:
        cz = cz + '-z'
    elif c == 0:
        cz = ''
    else:
        cz = cz + f'{c}z'
    return ax + by + cz + f'={d}'


def success(tipus, nivell=1, variant=1):
    if tipus == 1:  # aritmètiques
        if nivell == 1 or nivell == 2:  # trobar an sabent a1 i d
            d = random.randint(2, 6)
            a1 = random.randint(1, 10)
            n = random.randint(2, 30 + 50 * (nivell - 1))
        elif nivell == 3 or nivell == 4:  # trobar alguna cosa sabent les altres (a1, an, n, d) | d pot ser negativa
            d = random.randint(2, 9)
            if nivell == 4 and moneda():
                d = -d
            # no faig if comú pq canvis independents
            if moneda():
                a1 = random.randint(-9, -1)
            else:
                a1 = random.randint(1, 15)
            n = random.randint(3, 40)
        elif nivell == 101:
            d = random.randint(2, 9)
            if moneda():
                d = -d
            if moneda():
                a1 = random.randint(-9, -1)
            else:
                a1 = random.randint(1, 15)
            n = random.randint(6, 60)
        an = a1 + (n - 1) * d
        return en.success(tipus, nivell, variant, d, a1, n, an)

    elif tipus == 2:  # geomètriques
        if nivell == 1 or nivell == 2:  # trobar an sabent a1 i r #TODO decimals/fraccions
            r = random.randint(2, 5)
            a1 = random.randint(1, 10)
            n = random.randint(2, 5 + 5 * (nivell - 1))
        elif nivell == 3 or nivell == 4:  # trobar alguna cosa sabent les altres (a1, an, n, d) | d pot ser negativa
            r = random.randint(2, 5)
            if nivell == 4 and moneda():
                r = -r
            # no faig if comú pq canvis independents
            if moneda():
                a1 = random.randint(-9, -1)
            else:
                a1 = random.randint(1, 15)
            n = random.randint(3, 10)
        elif nivell == 101:
            r = random.randint(2, 5)
            if moneda():
                r = -r
            if moneda():
                a1 = random.randint(-9, -1)
            else:
                a1 = random.randint(1, 15)
            n = random.randint(6, 10)
        an = a1 * pow(r, n - 1)
        return en.success(tipus, nivell, variant, r, a1, n, an)
    return "No existeix aquest tipus de problema de successions..."


def prop(tipus, nivell=1):
    if tipus == 1:  # proporcionalitat simple
        if nivell in [1, 2, 3]:  # només directa || només inversa || random
            x = random.randint(1, 16)
            ay = random.choice([1, 2, 3, 4])
            by = random.choice([1, 2, 3, 5])
            y = ay * by
            y2 = random.randint(1, 16)
            if y2 == y:
                y2 += 1
            if (y2 * x) % y:
                if moneda():
                    x *= ay
                    y2 *= by
                elif moneda():
                    x *= y
                else:
                    y2 *= y
            x2 = y2 * x // y
            if nivell == 1 or (nivell == 3 and moneda()):
                return en.propsimple(1, x, y, x2, y2)  # 1 marca directa
            else:
                return en.propsimple(2, x, y2, x2, y)  # la inversa només és canviar y2 per y
        else:
            return "NO HI HA RES AQUÍ 42"
    return "AQUEST TIPUS DE P NO EXISTEIX 42"


def limits(tipus, nivell=1, conv=3, ordenat=False, txto=True, var="x"):
    """
    Genera un límit del tipus escollit

    :param tipus: 0 Px, 1 frac, 2 fracs, 3 sqrts, 4 e
    :param nivell:
    :param conv: 0 zero, 1 num, 2 inf, 3 rand
    :param ordenat: termes ordenats
    :param txto: text 'x tendeix a' (e.g. x->inf)
    :return: text
    """

    text = "x^{42}"
    xto = "42"

    if tipus == 0:  # polinomi
        text = ""
        xto = random.choice(["", "-"]) + "\\infty"
        for x in range(random.choice([3, 4])):
            coef = random.randint(1, 6)
            if moneda():
                coef = -coef
            if x == 0:
                exp = ""
            elif x == 1:
                exp = "x"
            else:
                exp = "x^{" + f"{x}" + "}"

            if moneda() or x == 0 or ordenat:
                if x > 0:
                    if coef > 0:
                        text += "+"
                text += f"{coef}{exp}"
            else:
                if text[0] != "-":
                    text = "+" + text
                text = f"{coef}{exp}" + text

    if tipus == 1:  # frac (to infty)
        xto = random.choice(["", "-"]) + "\\infty"
        gnum = random.randint(2, 5)
        if conv == 1 or random.choice([0, 0, 1]):  # resultat num
            gden = gnum
        elif conv == 2 or moneda():  # resultat inf
            gden = max(1, random.randint(1, gnum - 1))
        else:  # resultat 0
            gden = gnum + random.randint(1, 3)

        tnum = ""
        ternums = 0
        quantsvull = random.choice([2, 3])
        for x in range(gnum + 1):
            coef = random.randint(1, 6)
            if moneda():
                coef = -coef
            if gnum - x > 0:
                exp = "x"
                if gnum - x > 1:
                    exp += "^{" + f"{gnum - x}" + "}"
            else:
                exp = ""

            if x == 0:
                tnum = f"{coef}" + exp
                ternums += 1
            else:
                if (random.randint(0, gnum) != 1 and not ternums >= quantsvull) or ternums + (gnum - x) <= quantsvull:
                    if moneda() or ordenat:  # dreta
                        if coef > 0:
                            tnum += "+"
                        tnum += f"{coef}" + exp
                        ternums += 1
                    else:  # esquerra
                        if tnum[0] != "-":
                            tnum = "+" + tnum
                        tnum = f"{coef}" + exp + tnum
                        ternums += 1

        tden = ""
        terdens = 0
        quantsvull = random.choice([2, 3])
        for x in range(gden + 1):
            coef = random.randint(1, 6)
            if moneda():
                coef = -coef
            if gden - x > 0:
                exp = "x"
                if gden - x > 1:
                    exp += "^{" + f"{gden - x}" + "}"
            else:
                exp = ""

            if x == 0:
                tden = f"{coef}" + exp
                terdens += 1
            else:
                if (random.randint(0, gden) == 1 and not terdens >= quantsvull) or terdens + (gden - x) <= quantsvull:
                    if moneda() or ordenat:  # dreta
                        if coef > 0:
                            tden += "+"
                        tden += f"{coef}" + exp
                        terdens += 1
                    else:  # esquerra
                        if tden[0] != "-":
                            tden = "+" + tden
                        tden = f"{coef}" + exp + tden
                        terdens += 1

        text = "\\frac{" + f"{tnum}" + "}{" + f"{tden}" + "}"

    elif tipus == 2:  # frac ± frac (to infty)
        if nivell in [1, 2]:  # num - num / inf - inf
            if nivell == 1:
                k = 0  # num - num
                if random.randint(1, 5) == 1:  # 0 - 0
                    k = random.randint(-1, -2)
                # TODO num - 0 and the vicerveza
                # TODO escriure les fraccions i tal estaria bé
            else:
                xto = "\\infty"
                signe = "-"  # entre fracs
                # diferència entre els graus de num i den
                k = random.randint(1, 2)  # inf - inf
                # graus dels altres termes (Ax^a+Bx^b)/(Cx^c+Dx^d) + (Ex^e+Fx^f)/(Gx^g+Hx^h)
                c = random.randint(1, 2)
                g = random.randint(0, 2)
                a = c + k
                e = g + k

                b = random.randint(0, c)
                f = random.randint(0, g)
                if c - k >= 0:
                    d = random.randint(0, c - k)
                else:
                    d = -42
                if g - k >= 0:
                    h = random.randint(0, g - k)
                else:
                    h = -42
                # comprovo que al menys n'hi ha un prou gros per convergent a núm
                if c > b and g > f and c - k > d and g - k > h:
                    if moneda():
                        b = c
                    else:
                        f = g
                # coeficients
                ca = random.randint(1, 3) * random.choice([1, -1])  # principals
                cg = random.randint(1, 3) * random.choice([1, -1])
                ce = random.choice(divisors(ca * cg))  # obligats
                if moneda():
                    ce = -ce
                    signe = "+"
                cc = ca * cg // ce
                cb = random.randint(1, 6) * random.choice([1, -1])  # lliures
                cf = random.randint(1, 6) * random.choice([1, -1])
                cd = random.randint(1, 6) * random.choice([1, -1])
                ch = random.randint(1, 6) * random.choice([1, -1])
                # muntem la fracció
                num1 = monomi(ca, a)
                if moneda() and not ordenat:
                    if num1[0] != "-":
                        num1 = monomi(cb, b) + "+" + num1
                    else:
                        num1 = monomi(cb, b) + num1
                else:
                    if cb > 0:
                        num1 += "+" + monomi(cb, b)
                    else:
                        num1 += monomi(cb, b)

                den1 = monomi(cc, c)
                if d != -42:
                    if moneda() and not ordenat:
                        if den1[0] != "-":
                            den1 = monomi(cd, d) + "+" + den1
                        else:
                            den1 = monomi(cd, d) + den1
                    else:
                        if cd > 0:
                            den1 += "+" + monomi(cd, d)
                        else:
                            den1 += monomi(cd, d)

                num2 = monomi(ce, e)
                if moneda() and not ordenat:
                    if num2[0] != "-":
                        num2 = monomi(cf, f) + "+" + num2
                    else:
                        num2 = monomi(cf, f) + num2
                else:
                    if cf > 0:
                        num2 += "+" + monomi(cf, f)
                    else:
                        num2 += monomi(cf, f)

                den2 = monomi(cg, g)
                if h != -42:
                    if moneda() and not ordenat:
                        if den2[0] != "-":
                            den2 = monomi(ch, h) + "+" + den2
                        else:
                            den2 = monomi(ch, h) + den2
                    else:
                        if ch > 0:
                            den2 += "+" + monomi(ch, h)
                        else:
                            den2 += monomi(ch, h)
                f1 = "\\frac{" + f"{num1}" + "}{" + f"{den1}" + "}"
                if den2 != "1":
                    f2 = "\\frac{" + f"{num2}" + "}{" + f"{den2}" + "}"
                else:
                    f2 = num2
                    if f2[0] == "-" or signe == "-":
                        f2 = f"({f2})"
                text = f1 + signe + f2

                """  # Això és un experiment fracassat però que seria útil per crear polinomis amb qtat de termes defin.
                gden1 = list(reversed(range(random.randint(1, 2) + 1)))  # P(x) de grau randint(1,2)
                gden2 = list(reversed(range(random.randint(0, 2) + 1)))  # P(x) de grau randint(0,2)
                gnum1 = list(reversed(range(gden1[0]+gdif + 1)))  # P(x) del grau que toqui segons dif
                gnum2 = list(reversed(range(gden2[0]+gdif + 1)))  # P(x) del grau que toqui segons dif
                
                # me'n quedo dos o tres (incl. el més gros)
                tden1 = random.randint(2, 3)
                tden2 = random.randint(2, 3)
                tnum1 = random.randint(2, 3)
                tnum2 = random.randint(2, 3)
                print(gden1, gden2, gnum1, gnum2)
                if len(gden1) > tden1:
                    gden1 = gden1[:1] + random.sample(gden1[1:], tden1-1)  # agafo el més alt i rand fins omplir termes
                if len(gden2) > tden2:
                    gden2 = gden2[:1] + random.sample(gden2[1:], tden2-1)
                if len(gnum1) > tnum1:
                    gnum1 = gnum1[:1] + random.sample(gnum1[1:], tnum1 - 1)
                if len(gnum2) > tnum2:
                    gnum2 = gnum2[:1] + random.sample(gnum2[1:], tnum2-1)
                print(gden1, gden2, gnum1, gnum2)
                """

    elif tipus == 3:  # sqrt ± sqrt (to infty)
        if nivell == 1:  # arrel - arrel
            """
            √(Ax^a+Bx^b)- √(Cx^c+Dx^d)
            
            Definició:
                a>b
                c>d
            Indet:
                a=c
                A=C
            Resultat número:
                a = c = 2 * max(b, d)
            """
            xto = "\\infty"
            # graus
            b = random.randint(0, 1)
            if b == 0:
                d = random.randint(1, 1)
            else:
                d = random.randint(0, 1)
            a = 2 * max(b, d)
            c = a
            # coefs
            ca = random.randint(1, 3)
            cc = ca
            cb = random.randint(1, random.choice([5, 15])) * random.choice([-1, 1])
            cd = random.randint(1, random.choice([5, 15])) * random.choice([-1, 1])
            # muntatge
            text = "\\sqrt{" + f"{monomi(ca, a)}{monomi(cb, b, True)}" + "}"
            text += "-\\sqrt{" + f"{monomi(cc, c)}{monomi(cd, d, True)}" + "}"

        elif nivell == 2:  # num - arrel
            """
            Ax^a+Bx^b - √(Cx^c+Dx^d)
            
            Definició:
                a>b, c>d, C>0
            Indet:
                c = 2a
                C = A^2
            Resultat número:
                b=0 or d=a
                    b=0 or B=0
                    d<=a
            """
            xto = "\\infty"
            # graus
            b = random.choice([-42, 0])
            d = random.randint(0, 2)
            if b == 0:  # b ja recolza el resultat enter
                a = random.randint(max(b + 1, d), 2)
            else:  # b no recolza, per tant d ha de recolzar
                a = d
            c = 2 * a
            # coefs
            ca = random.randint(1, 3)
            cc = pow(ca, 2)
            cb = random.randint(1, random.choice([5, 15])) * random.choice([-1, 1])
            cd = random.randint(1, random.choice([5, 15])) * random.choice([-1, 1])
            # muntatge
            if moneda():  # arrel a la dreta
                text = str(monomi(ca, a)) + str(monomi(cb, b, True))
                text += "-\\sqrt{" + str(monomi(cc, c) + str(monomi(cd, d, True))) + "}"
            else:  # arrel a l'esquerra
                text = "\\sqrt{" + str(monomi(cc, c) + str(monomi(cd, d, True))) + "}"
                if moneda() or b == -42 or a < 0:
                    ca = -ca
                    cb = -cb
                    text += str(monomi(ca, a, True)) + str(monomi(cb, b, True))
                else:
                    text += "-(" + str(monomi(ca, a)) + str(monomi(cb, b, True)) + ")"

    elif tipus == 4:  # 1^inf (coses de la e)
        text = "1^{\\infty}"
        xto = "\\infty"
        if nivell == 1:  # (1+frac)^(frac)
            """
                 Ax^a+Bx^b    Ex^e+Fx^f
            (1 + ---------) ^ ---------
                 Cx^c+Dx^d    Gx^g+Hx^h
            
            Definició:
                a>b, c>d, e>f, g>h
            Indet:
                c>a, e>g
            Resultat número: 
                c-a = e-g = dif
                Enter:
                    AE % CG = 0
            """
            # graus
            a = random.randint(0, 1)  # ??? Incrementar màx?
            g = random.randint(0, 1)
            dif = random.randint(1, 2)
            c = a + dif
            e = g + dif
            if a == 0 or moneda():
                b = -42
            else:
                b = random.randint(0, a - 1)
            if random.randint(1, 5) == 1:
                d = -42
            else:
                d = random.randint(0, c - 1)
            if g == 0 or moneda():
                h = -42
            else:
                h = random.randint(0, g - 1)
            if random.randint(1, 5) == 1:
                f = -42
            else:
                f = random.randint(0, e - 1)
            # coefs
            ca, ce, cb, cd, cf, ch = [random.choice([-1, 1]) * random.randint(1, 5) for _ in range(6)]
            if random.choice([0, 1, 1]):  # mig sovint forço resultat enter
                cc = random.choice(divisors(ca * ce))
                cg = ca * ce // cc  # aquí tinc resultat = 1 (cg és el divisor gros)
                for x in reversed(range(2, 6)):  # faig el cg una mica més petit si es pot
                    if cg % x == 0:
                        cg = cg // x
                        if moneda():
                            break
            else:
                cc, cg = [random.choice([-1, 1]) * random.randint(1, 5) for _ in range(2)]
            # muntatge
            signe = random.choice(["-", "+"])
            m = monomi
            base = ("(1" + signe + "\\frac{" + m(ca, a) + m(cb, b, True) + "}{" + m(cc, c) + m(cd, d, True) + "})")
            exp = ("^{" + "\\frac{" + m(ce, e) + m(cf, f, True) + "}{" + m(cg, g) + m(ch, h, True) + "}" + "}")
            text = base + exp

        elif nivell == 2:  # frac^frac
            """
             Ax^a+Bx^b    Ex^e+Fx^f
            (---------) ^ ---------
             Cx^c+Dx^d    Gx^g+Hx^h
            
            Definició:
                a>b, c>d, e>f, g>h
            Indet:
                a = c
                A = C
                e>g
            Resultat número: 
                e = c + g - max(b, d)
            """
            # graus
            g = random.randint(0, 1)
            a = c = random.randint(1, 3)
            d = random.choice([-42] + list(range(c)))  # de 0 a c-1, o bé inexistent.
            b = random.choice([-42] + list(range(a)))
            if d == -42 and b == -42:  # necessito algun dels dos per tenir resultat no 0
                if moneda():
                    d = 0
                else:
                    b = 0
            e = c + g - max(b, d)  # això assegura la proporció de graus correcta
            f = random.choice([-42] + list(range(e)))
            h = random.choice([-42] + list(range(g)))
            # coefs
            ca = cc = random.randint(1, 5) * random.choice([-1, 1])
            cb, cd, cf, ch = [random.choice([-1, 1]) * random.randint(1, 5) for _ in range(4)]
            if b == -42:
                cbd = cd
            elif d == -42:
                cbd = cb
            else:
                cbd = cb - cd
            if random.choice([0, 1, 1]):  # mig sovint forço resultat enter
                ce = random.randint(1, 2)
                gpossibles = divisors(cbd * ce)
                if len(gpossibles) > 2:
                    gpossibles = gpossibles[:2]  # si hi ha moltes opcions deixo les baixes (+ marge de maniobra per e)
                cg = random.choice(gpossibles)
                if cbd * ce % (cc * cg):  # no divideix exacte
                    ce *= fracsimple(cbd * ce // cg, cc)[1]  # multiplico a ce la part indivisible per cc
            else:
                ce, cg = [random.choice([-1, 1]) * random.randint(1, 5) for _ in range(2)]
            if cb == cd:
                cd = -cd
            # muntatge
            m = monomi
            base = "(\\frac{" + m(ca, a) + m(cb, b, True) + "}{" + m(cc, c) + m(cd, d, True) + "})"
            exp = "^{\\frac{" + m(ce, e) + m(cf, f, True) + "}{" + m(cg, g) + m(ch, h, True) + "}}"
            text = base + exp

    if txto:
        text = "\\lim\\limits_{x\\to " + xto + "}" + text
    else:
        text = "\\lim " + text
    return text


def amb_signe(num):
    return signe(num)


def sig(num):
    return signe(num)


def signe(num):
    """returna el número amb signe (retorna buit si és 0)"""
    if num == 0 or num == "":
        return ""
    elif num > 0:
        return f"+{num}"
    else:
        return f"{num}"


def ncoef(coef, signe=False):
    """Retorna el número com a coeficient d'alguna cosa (evita escriure 1 i -1)"""
    return monomi(coef, 1, signe=signe, var="")


def monomi(coef, exp, signe=False, allexps=False, var="x"):
    """Retorna el monomi muntat

    :param coef: coeficient
    :param exp: grau (-42 indica inexistent, excepte si allexps)
    :param signe: True escriu "+" davant els positius
    :param allexps: si és cert, -42 serà un exponent com els altres
    :param var: text de la variable (per defecte "x")
    :return: text del monomi
    """
    if (exp != -42 or allexps) and coef:
        # coeficient
        if coef in [1, -1] and exp != 0:  # coeficient unitari i hi ha x
            if coef < 0:
                text = "-"
            else:
                text = ""
        else:
            text = f"{coef}"
        # exponent
        if exp:
            text += f"{var}"
        if exp not in [0, 1]:
            text += "^{" + f"{exp}" + "}"
        if signe:
            try:
                if coef >= 0:
                    text = "+" + text
            except:
                if not f"{coef}".startswith("-"):
                    text = "+" + text
    else:
        text = ""
    return text


def rand_multimon(nvars=2):
    """inventa un monomi amb la quantitat de variables especificada"""
    # coef
    coef = random.randint(1, random.choice([10, random.choice([420, 4200])])) * random.choice([-1, 1])
    # vars
    varopcions = ["x", "y", "z", "t", "a", "b", random.choice(["c", "ç"]), random.choice(["d", "q"])]
    vars = random.sample(varopcions, nvars)
    # exps
    exps = [random.randint(1, random.choice([5, random.choice([15, 50])])) for _ in range(nvars)]
    return multimonomi(coef, vars, exps)


def multimonomi(coef, vars=["x", "y"], exps=[], signe=False):
    """retorna un monomi de múltiples variables

    :param coef: coeficient
    :param vars: llista dels noms de variable per utilitzar
    :param exps: llista dels exponents a utilitzar
    :param signe: incloure signe positiu al text
    """
    text = "42xy"

    if coef:

        if len(vars) > len(exps):
            return "Escolti, doni'm tots els exponents."

        if abs(coef) == 1 and any(exps):  # coef unitari i hi ha alguna variable té exponent
            if coef < 0:
                text = "-"
            else:
                text = ""
        else:
            text = f"{coef}"
        # exponent
        for i, x in enumerate(vars):
            if exps[i]:
                text += f"{vars[i]}"
            if exps[i] not in [0, 1]:
                text += "^{" f"{exps[i]}" "}"
        if signe:
            if coef > 0:
                text = "+" + text
    else:  # si no tinc coef no tinc monomi
        text = ""
    return text


def multimonitza(mumo, signe=False):
    """Crida multimonomi a partir de les dades agrupades: mumo = [coef, [vars], [exps]]"""
    return multimonomi(mumo[0], mumo[1], mumo[2], signe=signe)


def polimumitza(mumopx):
    """Escriu el text d'un polimultimonomi donat com a llista de mumos, on mumo = [coef, [vars], [exps]]"""
    mlist = []
    signe = False
    for mx in mumopx:
        mlist.append(multimonitza(mx, signe))
        signe = True
    return "".join(mlist)


def polimumo_op(op, mumopx, mumoqx):
    """Opera dos polimultimonomis donats com a llista de mumos, on cada mumo = [coef, [vars], [exps]]"""
    musol = []
    if op == 1:  # suma
        musol = "Això no existeix encara, gamarús"
    elif op == 2:  # resta
        musol = "Això no existeix encara, gamarús"
    elif op == 3:  # multi
        for mx in mumopx:
            for my in mumoqx:
                mnou = mumo_op(3, mx, my)
                afegit = False
                for ms in musol:  # miro si el puc sumar amb algun dels que ja tenia
                    if mumo_semblant(ms, mnou):
                        ms[0] += mnou[0]  # sumo coefs
                        afegit = True
                        break
                if not afegit:  # si no he pogut l'afegeixo al final
                    musol.append(mnou)
    return musol


def mumo_semblant(mp, mq):
    """Et diu si dos multimonomis es poden sumar"""
    for i, v in enumerate(mp[1]):  # per cada variable de mp
        if mp[2][i]:  # si la variable té exponent
            if v in mq[1]:  # i l'altre mumo també la té
                if mq[2][mq[1].index(v)] != mp[2][i]:  # si tenen exponents diferents plego
                    return False
            else:  # si l'altre no la té plego
                return False
    # i a la vicerveza (només miro si les té, perquè exponents iguals ja ho he vist abans)
    for i, v in enumerate(mq[1]):  # per cada variable de mp
        if mq[2][i]:  # si la variable té exponent
            if v not in mp[1]:  # si l'altre no la té plego
                return False
    # si sobreviu a tot és bona
    return True


def mumo_op(op, mp, mq):
    """Multiplica dos multimonomis donats en mumo = [coefs, [vars], [exps]]"""
    if op == 3:
        musol = [mp[0] * mq[0], mp[1][:], mp[2][:]]
        for i, v in enumerate(mq[1]):  # per cada variable del segon
            if v in musol[1]:  # si ja la tenia
                j = musol[1].index(v)  # miro on la tinc
                musol[2][j] += mq[2][i]  # sumo els graus
            else:  # no la tenia
                musol[1].append(mq[1][i])  # l'afegeixo
                musol[2].append(mq[2][i])
    else:
        musol = "No has pas definit res d'això..."
    return musol


def dx(inception=1, opcions=[1, 2, 3, 4, 5, 6, 7, 8], amaga=[], simples=False, inici=0):
    opcions = opcions[:]  # sense això estic passant la referència i afecta a fora de manera incontrolable
    amaga = amaga[:]
    text = "x"
    sumasegur = False
    if -7 in amaga:
        sumasegur = True
        amaga.remove(-7)
    else:
        if -8 in amaga:
            amaga.remove(-8)
            if moneda():
                sumasegur = True
    if -6 in amaga:
        impedeixsuma = True
        amaga.remove(-6)
    else:
        impedeixsuma = False

    if inception == 1:
        if 6 in opcions:
            opcions.remove(6)
        if 8 in opcions:
            opcions.remove(8)

    if inception < 1:
        inception = 0
        fx = 0
    else:  # si queda recursivitat encara
        if -4 in amaga:
            sensearrels = True
            amaga.remove(-4)
        else:
            sensearrels = False
        for x in amaga:
            if x in opcions:
                opcions.remove(x)
            else:
                amaga.remove(x)

        if inici != 0:
            fx = inici
            if fx not in opcions:
                opcions.append(fx)
        else:
            if opcions:
                fx = random.choice(opcions)
            else:
                fx = 0
        if amaga:  # retorno a la llista principal l'amagat
            opcions += amaga
            amaga = []

        if fx == 1:  # a^x / e^x
            if random.choice([0, 0, 1]):  # a^x
                n = random.randint(2, 9)
                text = f"{n}^" + "{" + f"{dx(inception - 1, opcions, [1], simples=simples)}" + "}"
            else:  # e^x
                text = "e^{" + f"{dx(inception - 1, opcions, [1], simples=simples)}" + "}"

        elif fx == 2:  # cos(x) / sin(x) / tg(x)
            if random.choice([0, 0, 1]):
                text = "cos"
                amaga += [5]
            elif moneda():
                text = "sin"
                amaga += [5]
            else:
                text = "tg"
                amaga += [2, 5]
            if random.randint(1, 5) == 1 and not simples:  # exponent intern
                text += f"^{random.randint(2, 4)}"
                inception -= 1
            text += "(" + f"{dx(inception - 1, opcions, amaga, simples=simples)}" + ")"

        elif fx == 3:
            if random.choice([0, 0, 1]):  # log_b x
                n = random.randint(1, 9)
                text = "log"
                if n > 1:
                    text += f"_{n}"
                if random.randint(1, 20) == 1 and not simples:  # exponent intern
                    text += f"^{random.randint(2, 4)}"
                    inception -= 1
            else:  # ln x
                text = "ln"
                if random.randint(1, 5) == 1 and not simples:  # exponent intern
                    text += f"^{random.randint(2, 4)}"
                    inception -= 1
            text += "(" + f"{dx(inception - 1, opcions, simples=simples)}" + ")"

        elif fx == 4:  # x^2 / sqrt
            if random.choice([0, 0, 0, 1]) and not sensearrels:  # sqrt
                if random.choice([0, 0, 1]):
                    text = "\\sqrt[" + f"{random.randint(3, 5)}" + "]{" + f"{dx(inception - 1, opcions, [-4], simples=simples)}" + "}"
                else:
                    text = "\\sqrt{" + f"{dx(inception - 1, opcions, [-4], simples=simples)}" + "}"
            else:  # pow
                text = f"{dx(inception - 1, opcions, [4], simples=simples)}"
                if text == "x":
                    text = "x^"
                else:
                    text = "(" + text + ")^"
                if moneda():
                    text += f"{random.randint(2, 7)}"
                elif moneda():
                    text += "{-" + f"{random.randint(2, 3)}" + "}"
                else:
                    text += "{\\frac{1}{" + f"{random.randint(2, 3)}" + "}}"

        elif fx == 5:  # arctg / arcsin / arccos
            opcions.remove(5)
            if moneda():
                text = "arctg"
            elif moneda():
                text = "arcsin"
            else:
                text = "arccos"
            if random.randint(1, 9) == 1 and not simples:  # exponent intern
                text += f"^{random.randint(2, 4)}"
                inception -= 1
            text += "(" + f"{dx(inception - 1, opcions, [5], simples=simples)}" + ")"

        elif fx == 6:  # f + g
            opcions.remove(6)
            t1 = f"{dx(inception - 1, opcions, simples=simples)}"
            if t1[0] != "-":
                t1 = "+" + t1
            text = f"{dx(inception - 1, opcions, [-6], simples=simples)}{t1}"

        elif fx == 7:  # f * g
            opcions.remove(7)
            if 8 in opcions:
                opcions.remove(8)
            t1 = f"{dx(inception - 2, opcions, simples=simples)}"
            for x in opcions:
                if x in [5]:  # si vols treure més coses al segon factor, és aquí
                    opcions.remove(x)

            if inception < 3:
                ss = [-7]
            else:
                ss = [-8]
            t2 = f"{dx(inception - 2, opcions, ss, simples=simples)}"
            if t1 not in ["x", "-x", "2x", "-2x", "3x", "-3x"]:
                t1 = f"({t1})"
            if t2 != "x":
                t2 = f"({t2})"
            text = t1 + t2

        elif fx == 8:  # f/g
            opcions.remove(8)
            if 7 in opcions:
                opcions.remove(7)
            if 5 in opcions:
                opcions.remove(5)

            if inception < 3:
                if moneda():
                    s1 = [-7]
                    s2 = [-8]
                else:
                    s1 = [-8]
                    s2 = [-7]
            else:
                s1 = []
                s2 = []
            t1 = f"{dx(inception - 2, opcions, s1, simples=simples)}"
            t2 = f"{dx(inception - 2, opcions, s2, simples=simples)}"
            text = "\\frac{" + t1 + "}{" + t2 + "}"

    # Les sumes i multis les pot fer sempre que no hi ha f+g
    if fx != 6 and fx != 8:
        n = 1
        if not (simples and inception < 1):  # multiplica quelcom?
            if random.randint(1, 2) == 1:
                n = random.randint(2, 3 * (inception + 1))
                if random.randint(1, 5) == 1:
                    n = -n

                if text[0] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                    if len(text) > 1:
                        if text[1] == "^":
                            text = f"{n}\\cdot " + text
                elif text[0] in ["x", "e"]:
                    text = f"{n}" + text
                elif text[0] == "-":
                    text = f"{n}(" + text + ")"
                else:
                    text = f"{n}\\, " + text
            elif random.randint(1, 5) == 1:
                n = -1
                if text[0] == "-":
                    text = "-(" + text + ")"
                else:
                    text = "-" + text

        if (random.randint(1, 5) == 1 or sumasegur) and not (simples and inception > 0) and not impedeixsuma:  # suma?
            m = random.randint(2, 9)
            if moneda():
                if moneda():
                    if moneda():
                        if moneda():
                            m = random.randint(2, 1080)
                        else:
                            m = random.randint(2, 216)
                    else:
                        m = random.randint(2, 54)
                else:
                    m = random.randint(2, 18)
            if random.randint(1, 5) == 1:
                m = -m
            if moneda():
                if n > 0:
                    text = f"{m}+" + text
                else:
                    text = f"{m}" + text
            else:
                if m > 0:
                    text += f"+{m}"
                else:
                    text += f"{m}"
    return text


def fxscale(text):  # TODO acabar de pensar cómo hacer esto, porque no tiene sentido
    if "frac" in text[0:8] or (text[0] != "x" and text[1] == "^") or "e" in text[0:4] or "cdot" in text[0:9]:
        return 1.2
    else:
        return 1

    """
    br = 0
    es = []
    emax = 0
    for x in range(len(text)):
        if text[x] == "{":
            br += 1
        elif text[x] == "}":
            br -= 1
            while len(es) > 0 and br <= es[-1]:
                es = es[:-1]
        elif text[x] in ["^"]:
            es.append(br)
            emax = max(emax, len(es))
        print(es)

    if emax > 1:
        return 1.2
    else:
        return 1
    """


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - debugging

p = "muldiv"
"""
if p == "eq":
    print("equacions 1-1")
    for x in range(0, 5):
        print(eq(1, 1))

    print("\nequacions 1-2")
    for x in range(0, 5):
        print(eq(1, 2))

    print("\nequacions 2-1")
    for x in range(0, 5):
        print(eq(2, 1))

    print("\nequacions 2-2")
    for x in range(0, 5):
        print(eq(2, 2))

    print("\nequacions 2-3")
    for x in range(0, 5):
        print(eq(2, 3))

elif p == "sumes":
    print("\ncombinades 1-1")
    for x in range(0, 5):
        print(comb(1, 1))
    print("\ncombinades 1-2-2")
    for x in range(0, 5):
        print(comb(1, 2, 2))
    print("\ncombinades 1-3-5")
    for x in range(0, 5):
        print(comb(1, 3, 5))
    print("\ncombinades 2-1-1")
    for x in range(0, 5):
        print(comb(2, 1, 1))
    print("\ncombinades 2-2-2")
    for x in range(0, 5):
        print(comb(2, 2, 2))
    print("\ncombinades 2-3-3")
    for x in range(0, 5):
        print(comb(2, 3, 3))

elif p == "muldiv":
    print("\ncombinades 3-1")
    for x in range(0, 5):
        print(comb(3, 1))
    print("\ncombinades 3-2-2")
    for x in range(0, 5):
        print(comb(3, 2, 2))
    print("\ncombinades 3-3-3")
    for x in range(0, 5):
        print(comb(3, 3, 3))
    print("\ncombinades 3-4")
    for x in range(0, 5):
        print(comb(3, 4))
    print("\ncombinades 3-5-2")
    for x in range(0, 5):
        print(comb(3, 5, 2))
    print("\ncombinades 3-6-3")
    for x in range(0, 5):
        print(comb(3, 6, 3))

for x in range(0, 5):
    print(taules(9, True))



print(sisteq(1, 1))
print(sisteq(1, 2))
print(sisteq(1, 3))
print(sisteq(101, 1))
print(sisteq(101, 2))
print(sisteq(101, 3))
print(sisteq(101, 4)+"\n")

print(apilades(3, 1, [3, 2]))
print(apilades(3, 2, [2, 1], [2, 2]))
print(apilades(2, 1, [2, 2]))
print(apilades(2, 2, [3, 2]))
print(apilades(2, 3, [3, 2], [2, 3]))
print(apilades(1, 1, [3, 2]))
print(apilades(1, 2, [3, 2], [2, 3]))
print(apilades(1, 2, [3, 2], [0, 0]) + "\n")



for x in range(1, 6):
    print(f"Exercici {x}:", prop(1, 1))
print("")
for x in range(1, 10):
    print(f"Exercici {x}:", prop(1, 2))
print("")
for x in range(1, 10):
    print(f"Exercici {x}:", prop(1, 3))
print("")



print(eq(101, 1))
print(eq(101, 1))
print(eq(101, 2))
print(eq(101, 2))
print(eq(101, 3))
print(eq(101, 3), "\n")
print(eq(102, 1))
print(eq(102, 1))
print(eq(102, 2))
print(eq(102, 2))
print(eq(102, 3))
print(eq(102, 3), "\n")
print(eq(103, 1))
print(eq(103, 1))
print(eq(103, 2))
print(eq(103, 2))
print(eq(103, 3))
print(eq(103, 3))


for x in range(5):
    print(success(1, 1))
for x in range(5):
    print(success(1, 2))
print("\n")
for x in range(5):
    print(success(1, 3))
for x in range(5):
    print(success(1, 4))
print("\n")
print("Troba la diferència, el terme general i el terme indicat de les successions següents:")
for x in range(5):
    print(success(1, 101))
print("\nGEOM")
for x in range(5):
    print(success(2, 1))
for x in range(5):
    print(success(2, 2))
print("\n")
for x in range(5):
    print(success(2, 3))
for x in range(5):
    print(success(2, 4))
print("\n")
print("Troba la diferència, el terme general i el terme indicat de les successions següents:")
for x in range(5):
    print(success(2, 101))

print("\n")
print("Digues si les següents successions són aritmètiques o geomètriques,\n"
      "i calcula'n la distància o raó en cada cas.")
for x in range(12):
    print(success(random.choice([1, 2]), 101, random.choice([1, 2, 3, 4])))

for x in range(6):
    print(powsqr(103, 2, 2))

for x in range(10):
    print(powsqr(103, 2, 3))

for x in range(12):
    #print(powsqr(2, 3, termes=4), "\\\\ \\\\")
    print(powsqr(2, 4), "\\\\ \\\\")
    print("\\\\")"""


if __name__ == "__main__":
    # aquesta secció la faig servir per fer debugging dels tipus d'exercici
    print("running generator...")
    for x in range(50):
        print(eq(110, x // 13+1, solucions=True))
        # print(op_algeb(1, 10, solucions=True))
