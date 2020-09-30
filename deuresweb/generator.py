import math
import random

import enunciats as en


def moneda():
    return bool(random.getrandbits(1))


def comb(tipus, nivell=1, nums=1):
    text = "42"
    if tipus == 1:  # A+B
        if nivell == 1:  # (innecessari) A positiva, resultat positiu
            a = random.randint(1, 9*nums)
            b = random.randint(-a, 10*nums)
            if b >= 0:

                b = f'+{b}'
            text = f'{a}{b}='
        elif nivell == 2:  # A positiva
            a = random.randint(1, 10*nums)
            b = random.randint(-10*nums, 8*nums)
            if b >= 0:
                b = f'+{b}'
            text = f'{a}{b}='
        elif nivell == 3:  # nums qualssevol
            a = random.randint(-10*nums, 10*nums)
            b = random.randint(-10*nums, 10*nums)
            if b >= 0:
                b = f'+{b}'
            text = f'{a}{b}='
    if tipus == 2:  # A±(±B)
        if nivell == 1 or nivell == 2:  # A positiva, sense -(-B) || amb -(-B)
            a = random.randint(1, 10*nums)
            b = random.randint(-10*nums, 10*nums)
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
            a = random.randint(-10*nums, 10*nums)
            b = random.randint(-10*nums, 10*nums)
            if b>0:
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
                taula = random.randint(1, 10+2*(nums-1))  # nums inclou 11 i 12...
                text = taules(taula)
            else:  # div
                b = random.randint(1, 10+2*(nums-1))
                a = random.randint(1,10)
                text = fr'{a*b}\div {a}'
        elif (nivell == 2 or nivell == 3) or (nivell == 5 or nivell == 6):  # (taules amb un signe || amb dos signes) || divisions
            a = random.randint(-10-2*(nums-1), 10+2*(nums-1))
            b = random.randint(1, 10)
            symbol = r'\times '
            if nivell == 5 or nivell == 6:  # adapto per div
                if a == 0:  # evito dividir per zero
                    a = random.randint(1, 10+2*(nums-1))
                aux = a
                a = a*b
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
                if a>0:
                    text = fr'(+{a}){symbol}{b}='
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

            t1 = f"{mixcomb(a, inception-1, 0, 1, doblesigne, out, ops)}"
            t2 = f"{mixcomb(b, inception-1, 0, 1, doblesigne, out, ops)}"
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
                    a = random.randint(1, maxn*inception)
                else:
                    a = random.choice(divisors(abs(num)))
                if random.choice([0, 0, 1]):
                    a = -a
                if moneda():
                    b = a
                    a = num // b
                else:
                    b = num // a
                t1 = f"{mixcomb(a, inception-1, 0, 2, doblesigne, out, ops)}"
                t2 = f"{mixcomb(b, inception-1, 0, 2, doblesigne, out, ops)}"
                if t2[0] == "-":  # ±A*(-B)
                    text = f"{t1}\\cdot ({t2})"
                else:  # ±A*B
                    text = f"{t1}\\cdot {t2}"

            if previ == 3:
                text = f"({text})"

        elif op == 3:  # divi
            b = random.randint(2, maxn // 2)
            if random.choice([0, 0, 1]):
                b = -b
            a = num * b

            t1 = f"{mixcomb(a, inception-1, 0, 3, doblesigne, out, ops)}"
            t2 = f"{mixcomb(b, inception-1, 0, 3, doblesigne, out, ops)}"
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


def frac(tipus, nivell=1, termes=2, dmax=6, divis=0):
    """
    Exercicis de fraccions

    tipus = 1 sum/rest, 2 mul/div

    nivell = 1 positiu, 2 pos/neg, 3 pot doble neg

    termes = quantes fraccions

    dmax = màx denom. (sum/rest), màx número (mul/div)

    divis = 0 no, 1 random, 2 sempre
    """

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
                            text += "-"
                            a = -a
                        else:
                            text += "+"
                    else:
                        if moneda():
                            text += "-"
                        else:
                            text += "+"
                            a = -a
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
                    else:
                        text += "\\div "
                    if nivell == 1 or moneda():
                        if nivell == 3 and moneda():  # doble neg
                            a = -a
                            b = -b
                    else:
                        if moneda():
                            a = -a
                        else:
                            b = -b
                text += "\\frac{" + f"{a}" + "}{" + f"{b}" + "}"
    return text


def fracmix(num, den, inception=1, op=0, previ=0, doblesigne=True, out=0, segona=False):
    text = "4/2+42/6*3/42"
    if out == 0:
        out = inception

    if inception < 1:
        inception = 0
        if den == 1:
            text = f"{num}"
            if previ in [2, 3] and num < 0 and segona:
                text = "(" + text + ")"
        else:
            text = "\\frac{" + f"{num}" + "}{" + f"{den}" + "}"

    else:
        if op == 0:
            if previ == 1:
                op = 2
            else:
                op = random.randint(1, 2)

        if op == 1:  # sum/rest  (a/b + c/d (+e/f)) -> N = ad+cb (+e), D = bd
            # denominador
            b = random.choice(divisors(den))
            d = den // b
            # numerador
            c = 0
            exactes = []
            for x in range(-2, 3):  # -2 -> 2
                a = (num // d) + x
                if (num - a*d) % b == 0:  # si surt exacte (dues fraccions fan prou)
                    c = (num - a*d) // b
                    if a:
                        exactes.append([a, c])  # guardo les opcions
            if exactes:
                for x in exactes:  # faig una mica de neteja d'uns i números primers lletjos
                    if len(exactes) < 2:
                        break
                    if abs(x[0]) in [1, 13, 17, 19] or abs(x[1] in [1, 13, 17, 19]):
                        exactes.remove(x)
                a, c = random.choice(exactes)  # i en trio una (si no trio quedarà la última a, que ja em serveix)
            if c == 0:
                c = (num - a*d) // b + random.choice([-1, 1])
            if c == 0:
                c = random.choice([-1, 1])
            diff = num - (a*d + c*b)
            if diff:
                f = b*d
                e = diff
                e, f = fracsimple(e, f)
            a, b = fracsimple(a, b)
            c, d = fracsimple(c, d)
            if b == 1 or d == 1:
                q = random.randint(2, 3)
                k = random.choice([-1, 1])
                a = q*a + k
                b = q*b
                c = q*c - k
                d = q*d

            text = f"{fracmix(a, b, inception-1, previ=op)}"
            if c*d < 0:  # frac negativa
                text += f"-{fracmix(-c, d, inception-1, previ=op)}"
            else:  # frac positiva
                text += f"+{fracmix(c, d, inception-1, previ=op)}"

            if diff:
                if e*f < 0:
                    text += f"-{fracmix(-e, f, 0, previ=op)}"
                else:
                    text += f"+{fracmix(e, f, 0, previ=op)}"
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
                if a*k == b or d*k == c or (moneda() and not (b*k == a or c*k == d)):
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
                        if c*k % d != 0:  # no causaré enter a la dreta
                            b *= k
                            c *= k
                for k in [2, 3, 4, 5, 7]:
                    if c % d != 0 or random.randint(1, 30) == 1:  # (ja) no tinc enter a la dreta (excepte alguns)
                        break
                    else:
                        if a*k % b != 0:
                            a *= k
                            d *= k

            a, b = fracsimple(a, b)
            c, d = fracsimple(c, d)

            text = f"{fracmix(a, b, inception - 1, previ=op)}"
            if (moneda() or c in [0, 1]) and not d == 0:  # no volem dividir per zero (ni fer un enter a la divisió)
                text += f"\\cdot {fracmix(c, d, inception - 1, previ=op, segona=True)}"
            else:
                text += f": {fracmix(d, c, inception - 1, previ=3, segona=True)}"

            if previ == 3:
                text = "(" + text + ")"

    if inception == out:
        return squarebracketer(text)
    else:
        return text


def randomfracnum(n):
    num = random.choice([2, 3, 5, 7])
    for x in range(n):
        if moneda():
            num *= random.choice([1, 2])
        else:
            if moneda():
                num *= random.choice([1, 2, 3])
            else:
                num *= random.choice([2, 3, 5])
    return num


def fracsimple(n, d):
    """Retorna [n, d] = fracció (n/d) simplificada"""
    divis = divisors(d, True)
    for x in divis:
        if n % x == 0 and d % x == 0:
            n = n // x
            d = d // x
    if d < 0:
        d = -d
        n = -n
    return [n, d]


def taules(taula, div=False):
    a = random.randint(1, 10)
    if div:
        return fr'{a*taula}\div {a}='
    else:
        if moneda():
            return fr'{taula}\times {a}='
        else:
            return fr'{a}\times {taula}='


def divisors(num, tots=False):
    div = [1]
    for x in range(2, isqrt(num)+1):
        if num % x == 0:
            div.append(x)
    if len(div) > 1 and not tots:
        div.remove(1)
    if tots:
        extra = []
        for x in div:
            extra.append(num // x)
        div += extra
    return div


def isqrt(n):  # newton (from stackoverflow)
    """Part entera de l'arrel quadrada de n"""
    x = n
    y = (x + 1) // 2
    while y < x:
        x = y
        y = (x + n // x) // 2
    return x


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
        text = text[:x[1]] + "\\rbrack " + text[x[1]+1:]
        text = text[:x[0]] + "\\lbrack " + text[x[0] + 1:]

    return text


def apilades(tipus, nivell=1, digits=[2, 1], decimals=[0, 0]):
    text = r"\begin{array}{c}\phantom{\times99}42\\ \underline{\times\phantom{99}42}\\ \end{array}"
    if tipus == 1:  # sumes
        if nivell == 1:  # sense decimals
            text = "42+42"
            a = random.randint(max(2, pow(10, digits[0]-1)), pow(10, digits[0])-1)
            b = random.randint(max(2, pow(10, digits[1]-1)), pow(10, digits[1])-1)
            digitsc = math.ceil(math.log(a+b, 10))
            na = ""
            nb = ""
            for n in range(digitsc-digits[0]):
                na += "9"
            for n in range(digitsc-digits[1]):
                nb += "9"
            text = r"\begin{array}{c}\phantom{+" + na + "}" + f"{a}" + r"\\ \underline{+\phantom{" + nb + "}" + f"{b}" + r"}\\ \end{array}"
        else:  # amb decimals
            text = "4.2+4.2"
            xa = digits[0] + decimals[0]
            prea = random.randint(max(2, pow(10, xa - 1)), pow(10, xa) - 1)
            a = prea / pow(10, decimals[0])

            xb = digits[1] + decimals[1]
            preb = random.randint(max(2, pow(10, xb - 1)), pow(10, xb) - 1)
            b = preb / pow(10, decimals[1])

            res = a+b
            rdigits = math.ceil(math.log(math.floor(res), 10))
            partdecimal = round(res-math.floor(res), 7)  # cal truncar els glitches de binari (fa 2.3560000000023)
            rdecimals = 0
            while partdecimal - math.floor(partdecimal) != 0:
                partdecimal = round(partdecimal*10, 7)
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
            text = r"\begin{array}{c}\phantom{+" + nae + "}" + f"{a}" + r"\phantom{" + nad + r"}\\ \underline{+\phantom{" + nbe + "}" + f"{b}" + r"\phantom{" + nbd + r"}}\\ \end{array}"
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
            text = r"\begin{array}{c}\phantom{-" + na + "}" + f"{a}" + r"\\ \underline{-\phantom{" + nb + "}" + f"{b}" + r"}\\ \end{array} "
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
            text = r"\begin{array}{c}\phantom{-" + nae + "}" + f"{a}" + r"\phantom{" + nad + r"}\\ \underline{" \
                                                                                             r"-\phantom{" + nbe + \
                   "}" + f"{b}" + r"\phantom{" + nbd + r"}}\\ \end{array} "
    elif tipus == 3:  # multis a x b = c
        if nivell == 1:  # sense decimals
            text = "42x42"
            a = random.randint(max(2, pow(10, digits[0]-1)), pow(10, digits[0])-1)
            b = random.randint(max(2, pow(10, digits[1]-1)), pow(10, digits[1])-1)
            digitsc = math.ceil(math.log(a*b, 10))
            na = ""
            nb = ""
            for n in range(digitsc-digits[0]):
                na += "9"
            for n in range(digitsc-digits[1]):
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

        text = r"\begin{array}{c}\phantom{\times" + na + "}" + f"{a}" + r"\\ \underline{\times\phantom{" + nb + "}" + f"{b}" + r"}\\ \end{array}"
    else:  # divis
        text = "42/42"
    return text


def powsqr(tipus, nivell=1, termes=2):
    text = "42^6"
    if tipus == 1:  # potències, mateix exponent
        if nivell == 1:  # multiplicant
            text = ""
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
                    base = f"{random.randint(2, 6)}"
                    if random.randint(1, 4) == 4:
                        base = f"(-{base})"
                    text += f"{base}" + "^{" + f"{exp}" + "}"

        elif nivell == 2:  # multiplicant i dividint
            text = ""
            exp = random.randint(2, 9)
            if random.randint(1, 4) == 4:
                exp = -exp
            if random.randint(1, 20) == 1:
                exp = random.randint(300, 1458)  # mutació exp enorme
            bloc = ""
            multigastada = False  # asseguro 1 div mínim
            for x in range(termes):
                if x % 3 == 0:  # primera
                    a = random.randint(2, 5)
                    if x != 0:
                        text += "\\cdot "
                else:
                    b = random.randint(2, 9)
                    if moneda() and not multigastada:
                        if random.randint(1, 10) == 1:  # mutació 1^27482
                            bloc += "\\cdot 1^{" + f"{random.randint(1,  random.choice([9, 14958]))}" + "}"
                        elif random.randint(1, 10) == 1:
                            bloc += f"\\cdot {random.randint(2, random.choice([9, 9637]))}" + "^0"
                        else:
                            if random.randint(1, 4) == 1:
                                b = f"(-{b})"
                            bloc += f"\\cdot {b}^" + "{" + f"{exp}" + "}"
                        multigastada = True
                    else:
                        a *= b
                        if random.randint(1, 4) == 1:
                            b = f"(-{b})"
                        bloc += f"\\div {b}^" + "{" + f"{exp}" + "}"
                if x % 3 == 2 or x == (termes - 1):  # última
                    text += f"{a}^" + "{" + f"{exp}" + "}" + bloc
                    bloc = ""
                    multigastada = False

    elif tipus == 2:  # potències, mateixa base
        if nivell == 1 or nivell == 2:  # multiplicant // mul i div
            text = ""
            base = random.randint(2, 14)
            if random.randint(1, 4) == 1:
                base = f"(-{base})"
            if random.randint(1, 20) == 1:
                base = random.randint(32, 265)  # mutació base enorme

            for x in range(termes):
                if x > 0:
                    if nivell == 1 or moneda():
                        text += r"\cdot "
                    else:
                        text += r"\div "
                if random.randint(1, 15) == 1:  # mutació 1^27482
                    text += "1^{" + f"{random.randint(1, random.choice([9, 14958]))}" + "}"
                elif random.randint(1, 15) == 1:
                    text += f"{random.randint(2, random.choice([9, 9637]))}" + "^0"
                else:
                    exp = random.randint(1, 10)
                    if random.randint(1, 4) == 1:
                        exp = -exp
                    if exp == 1:
                        text += f"{base}"
                    else:
                        text += f"{base}" + "^{" + f"{exp}" + "}"

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
                if exp == 0 and moneda():
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
            if moneda() or termes < 5:
                bases = primers[:2]  # agafa 0-1
            else:
                bases = primers[:3]  # agafa 0-2
            gastat = []
            for x in range(termes):
                if x == termes - 1 and len(gastat) == 1:  # si és l'últim i només he posat una base, forço un altre
                    bases.remove(gastat[0])
                base = random.choice(bases)
                if base not in gastat:
                    gastat.append(base)
                exp = random.randint(random.choice([-7, -5, -3]), random.choice([3, 5, 7]))
                if exp == 0 and moneda():
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
                        tnum.append(random.choice(primers))
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
        pass
    elif tipus == 102:  # arrels, mateixa base
        pass
    elif tipus == 103:  # arrels, MCM
        if nivell == 1:  # multiplicant, sense exponent
            text = ""
            for x in range(termes):
                b = random.randint(2, 7)
                ind = random.randint(2, 6)
                if ind == 2:
                    ind = ""
                if x > 0:
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
                    text += "\\cdot "
                text += "\\sqrt[" + f"{ind}" + "]{" + f"{b}^" + "{" + f"{e}" + "}" + "}"
    return text


def eq(tipus, nivell=1):  # de moment tot (2,1)
    x = 1
    text = "x=42"

    if tipus == 1:  # TIPUS x+B=C
        if nivell == 1 or nivell == 2:  # resultat positiu (x esquerra, números petits || x on sigui, números petits)
            b = random.randint(1, 5)
            if moneda():
                b = -b
            c = random.randint(-5, 5)
            if moneda():
                if b >= 0:
                    b = f'+{b}'
                text = f'x{b}'
                if nivell == 1 or moneda():
                    text = text + f'={c}'
                else:
                    text = f'{c}=' + text
            else:
                text = f'{b}+x'
                if nivell == 1 or moneda():
                    text = text + f'={c}'
                else:
                    text = f'{c}=' + text
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

    elif tipus == 101:  # x^2-C (treure l'arrel)
        if nivell == 1:  # quadrat perfecte, x2 sense coef
            x = random.randint(1, 10)
            text = f"x^2-{pow(x,2)}=0"
        elif nivell == 2:  # pot sortir impossible
            x = random.randint(1, 10)
            if random.choice([0, 0, 1]):  # arrel neg
                text = f"x^2+{pow(x,2)}"
            else:
                text = f"x^2-{pow(x,2)}"  # normal
            if random.choice([1, 1, 0]):
                text = text + "=0"
            else:
                text = "0=" + text
        elif nivell == 3:  # amb coef
            x = random.randint(1, 10)
            c = pow(x, 2)
            a = random.randint(-3, 3)
            if a == 0:
                a = random.choice([1, -1])
            if a > 0:
                if moneda():
                    if a == 1:
                        text = f"x^2+{c*a}"
                    else:
                        text = f"{a}x^2+{c*a}"
                else:
                    if a == 1:
                        text = f"{c*a}+x^2"
                    else:
                        text = f"{c*a}+{a}x^2"
            else:
                if moneda():
                    if a == -1:
                        text = f"-x^2{c*a}"
                    else:
                        text = f"{a}x^2{c * a}"
                else:
                    if a == -1:
                        text = f"{c*a}-x^2"
                    else:
                        text = f"{c * a}{a}x^2"
            if random.choice([1, 1, 0]):
                text = text + "=0"
            else:
                text = "0=" + text

    elif tipus == 102:  # x^2+Bx (desacoblar)
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
                text = "0="+text

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
                if a*x > 0:
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
        c = x1*x2

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
            b = a * (-x1-x2)
            c = a * (x1*x2)
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

    elif tipus == 104:  # de moment completes però polinomi (6 termes)
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

    return text


def sisteq(tipus, nivell=1, nums=1):
    text = text = r"\begin{cases} x+y=42 \\ x+y=42 \end{cases}"

    if tipus == 1:  # ax+by=c, dx+ey=f
        if nivell == 1 or nivell == 2 or nivell == 3:  # primera x coef 1 || algun coef ±1 || reducció qualsevol
            eq1 = "x+y=42"
            eq2 = "x+y=42"
            x = random.randint(-10, 10)
            y = random.randint(-10, 10)
            coefs = [random.randint(1, 5) for _ in range(4)]
            for n in range(4):
                if moneda():
                    coefs[n] = -coefs[n]
            if round(coefs[0]*1./coefs[2], 7) == round(coefs[1]*1./coefs[3], 7):  # crec que això evita SCI
                coefs[0] = - coefs[0]
            if nivell == 1:  # la primera x sense coef
                coefs[0] = 1
            elif nivell == 2:  # alguna incògnita unitària
                if not any(n in [1, -1] for n in coefs):
                    coefs[random.randint(0, 3)] = random.choice([1, -1])

            # TODO afegir eqns amb les inc barrejades

            c = coefs[0]*x + coefs[1]*y
            f = coefs[2]*x + coefs[3]*y
            eq1 = systeq_text(coefs[0], coefs[1], c)
            eq2 = systeq_text(coefs[2], coefs[3], f)
            text = r"\begin{cases} " + eq1 + r" \\ " + eq2 + r" \end{cases}"

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
                coefs[4] = coefs[3]*coefs[0]*coefs[1]+random.choice([1, -1])  # escalonat amb la segona
                if moneda():  # aleatori quina de les dues és l'escalonada
                    for n in range(3):
                        aux = coefs[n+3]
                        coefs[n+3] = coefs[n+6]
                        coefs[n+6] = aux
                if nivell == 2 and random.choice([True, True, False]):
                    fila = random.choice([1, 2])  # moc la fila de la x a qualsevol de les altres
                    for n in range(3):
                        aux = coefs[n]
                        coefs[n] = coefs[n+fila*3]
                        coefs[n+fila*3] = aux
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
    return text


def systeq_text(a, b, c):
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


def systeq3_text (a, b, c, d):
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
    if c >= 0:
        cz = '+'
    else:
        cz = ''
    if c == 1:
        cz = cz + 'z'
    elif c == -1:
        cz = cz + '-z'
    else:
        cz = cz + f'{c}z'
    return ax + by + cz + f'={d}'


def success(tipus, nivell=1, variant=1):
    if tipus == 1:  # aritmètiques
        if nivell == 1 or nivell == 2:  # trobar an sabent a1 i d
            d = random.randint(2, 6)
            a1 = random.randint(1, 10)
            n = random.randint(2, 30 +50*(nivell-1))
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
        an = a1+(n-1)*d
        return en.success(tipus, nivell, variant, d, a1, n, an)

    elif tipus == 2:  # geomètriques
        if nivell == 1 or nivell == 2:  # trobar an sabent a1 i r #TODO decimals/fraccions
            r = random.randint(2, 5)
            a1 = random.randint(1, 10)
            n = random.randint(2, 5 + 5*(nivell-1))
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
        an = a1 * pow(r, n-1)
        return en.success(tipus, nivell, variant, r, a1, n, an)
    return "No existeix aquest tipus de problema de successions..."


def prop(tipus, nivell=1):
    if tipus == 1:  # proporcionalitat simple
        if nivell in [1, 2, 3]:  # només directa || només inversa || random
            x = random.randint(1, 16)
            ay = random.choice([1, 2, 3, 4])
            by = random.choice([1, 2, 3, 5])
            y = ay*by
            y2 = random.randint(1, 16)
            if y2 == y:
                y2 += 1
            if (y2*x) % y:
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
                text = f"{n}^" + "{" + f"{dx(inception-1, opcions, [1], simples=simples)}" + "}"
            else:  # e^x
                text = "e^{" + f"{dx(inception-1, opcions, [1], simples=simples)}" + "}"

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
            text += "(" + f"{dx(inception-1, opcions, amaga, simples=simples)}" + ")"

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
            text += "(" + f"{dx(inception-1, opcions, simples=simples)}" + ")"

        elif fx == 4:  # x^2 / sqrt
            if random.choice([0, 0, 0, 1]) and not sensearrels:  # sqrt
                if random.choice([0, 0, 1]):
                    text = "\\sqrt[" + f"{random.randint(3, 5)}" + "]{" + f"{dx(inception-1, opcions, [-4], simples=simples)}" + "}"
                else:
                    text = "\\sqrt{" + f"{dx(inception-1, opcions, [-4], simples=simples)}" + "}"
            else:  # pow
                text = f"{dx(inception-1, opcions, [4], simples=simples)}"
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
            text += "(" + f"{dx(inception-1, opcions, [5], simples=simples)}" + ")"

        elif fx == 6:  # f + g
            opcions.remove(6)
            t1 = f"{dx(inception-1, opcions, simples=simples)}"
            if t1[0] != "-":
                t1 = "+" + t1
            text = f"{dx(inception-1, opcions, [-6], simples=simples)}{t1}"

        elif fx == 7:  # f * g
            opcions.remove(7)
            if 8 in opcions:
                opcions.remove(8)
            t1 = f"{dx(inception-2, opcions, simples=simples)}"
            for x in opcions:
                if x in [5]:  # si vols treure més coses al segon factor, és aquí
                    opcions.remove(x)

            if inception < 3:
                ss = [-7]
            else:
                ss = [-8]
            t2 = f"{dx(inception-2, opcions, ss, simples=simples)}"
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
            t1 = f"{dx(inception-2, opcions, s1, simples=simples)}"
            t2 = f"{dx(inception-2, opcions, s2, simples=simples)}"
            text = "\\frac{" + t1 + "}{" + t2 + "}"

    # Les sumes i multis les pot fer sempre que no hi ha f+g
    if fx != 6 and fx != 8:
        n = 1
        if not (simples and inception < 1):  # multiplica quelcom?
            if random.randint(1, 2) == 1:
                n = random.randint(2, 3*(inception+1))
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
print("Digues si les següents successions són aritmètiques o geomètriques,\n" + \
      "i calcula'n la distància o raó en cada cas.")
for x in range(12):
    print(success(random.choice([1, 2]), 101, random.choice([1, 2, 3, 4])))

for x in range(6):
    print(powsqr(103, 2, 2))

for x in range(10):
    print(powsqr(103, 2, 3))
"""

for x in range(6):
    print(fracmix(random.choice([-1, 1])*randomfracnum(3), randomfracnum(3), 3))
