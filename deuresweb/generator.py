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

        text = (r"\begin{array}{c}\phantom{\times" + na + "}" + f"{a}" + r"\\ \underline{\times\phantom{" + nb + "}"
                f"{b}" + r"}\\ \end{array}")
    else:  # divis
        text = "42/42"
    return text


def powsqr(tipus, nivell=1, termes=2, lletres=0):
    """

    :param tipus:
    :param nivell:
    :param termes: quantitat de termes
    :param lletres: 0 = nums / 1 = nums i llet / 2 = llet
    :return: text en LaTeX
    """

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
        pass
    elif tipus == 102:  # arrels, mateixa base (té sentit?)
        pass
    elif tipus == 103:  # arrels, índex comú
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
                if nivell > 1 and x < termes-1 and moneda():
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
                    if not punts or (factors[x][0] in lets and factors[x-1][0] in lets):
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
            for x in range(random.randint(3, 5)-factors):
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
                    if not punts or (factors[x] in lets and factors[x-1] in lets):
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
                    exps[x] = exps[x]-1  # rebaixo els múltiples de l'arrel (així no es poden treure fora)
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
                    text += "\\sqrt{" + f"{altseed*pow(altop, 2)}" + "}"
                    mutat = True
                else:
                    text += "\\sqrt{" + f"{seed*pow(triats[x], 2)}" + "}"

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
                    exp = random.randint(1, index-1)
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

    elif tipus == 3:  # lineals: opera i resol
        if nivell == 1:  # (6 termes) Ax + Bx + Cx + D + E + F = 0
            x = random.randint(-10, 10)
            # coeficients
            a, b, c = [random.choice([-1, 1]) * random.randint(1, 5) for _ in range(3)]
            if (a+b+c) == 0:  # evito indeterminat
                if a == 1 or moneda():
                    a += 1
                else:
                    a -= 1
            blocx = (a+b+c)*x
            if abs(blocx) > 50:  # si la F quedarà enorme, compenso amb signe contrari i restant gros
                d, e = [-abs(blocx)//blocx * random.randint(10, 20) for _ in range(2)]
            else:
                d, e = [random.choice([-1, 1]) * random.randint(1, 15) for _ in range(2)]
            f = -1 * ((a+b+c)*x + (d+e))
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
            if a == c*f:  # evito indefinit
                a += random.choice([-1, 1])  # això no és mai 0
            d = random.choice([-1, 1]) * random.randint(1, 5)
            b = (f*c - a)*x + f*d
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
            if abs(abs(e*a) - abs(f*c)) * abs(x) > 45:  # la diferència entre EA i FC fa un blocx massa gran
                if abs(e*a) < abs(f*c):
                    if abs(e) < abs(a):
                        e = int(e * (abs(f*c) / abs(e*a)))
                    else:
                        a = int(a * (abs(f*c) / abs(e*a)))
                else:
                    if abs(f) < abs(c):
                        c = int(c * (abs(e*a) / abs(f*c)))
                    else:
                        f = int(f * (abs(e*a) / abs(f*c)))
            if e*a//abs(e*a) == -f*c//abs(f*c) and abs(e*a-f*c) > 6:  # si sumen (i queda gros) faig que restin
                c = -c
            if e*a == f*c:  # evito indeterminat
                if a == 1 or moneda():
                    a += 1
                else:
                    a -= 1
            blocx = (e*a - f*c)*x
            if abs(blocx) > 40:  # si segueix mig gros, ajudo amb els independents
                if e*b * blocx > 0:  # mateix signe
                    b = -b
                if -f*d * blocx > 0:
                    d = -d
            else:
                if abs(abs(e*b) + abs(f*d)) > 10 and e*b * (-f*d) > 0:  # si sumen bastant i els estic sumant, resto
                    b = -b
                if (abs(e*b) > abs(f*d) and e*b * blocx > 0) or (abs(f*d) > abs(e*b) and -f*d * blocx > 0):
                    b = -b
                    d = -d
            g = blocx + e*b - f*d
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
            pass
        elif nivell == 2:  # fraccions (resultat fracció)
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
                num = abs(nb*f + nd*e)
                if num and num < bestnum:
                    b, d = nb, nd
            bestmcd = 1
            for n in sorted(range(-5, 5)):  # trio la h que millor simplifica
                # n és h provisional
                num = b*f + d*e + n*e*f
                den = a*f + c*e + g*e*f
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
            a, c, g = [random.choice([-1, 1])*random.randint(1, 5) for _ in range(3)]
            b, d = [random.choice([-1, 1]) * random.randint(0, 10) for _ in range(2)]  # permeto zeros als independents
            # coef control
            print(a*f, c*e, g*e*f, ")", x,"// ", b*f, d*e, "||", g, "(", e, f)
            if abs(g*e*f) > 90 or (abs(g*e*f) > 40 and abs(x) > 3) or (abs(g*e*f) > 25 and abs(x) > 5):
                if abs(g) > 2:
                    if abs(g*e*f) < 200 and abs(e*f*2) < 60 and x < 5:
                        g = random.choice([1, 2, -1, -2])
                    else:
                        g = random.choice([1, -1])
                if abs(g*e*b) > 42:
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
            print(a*f, c*e, g*e*f, ")", x,"// ", b*f, d*e, "||", g, "(", e, f)
            if abs(g*e*f) > 30 or x > 5 or abs(a*f + c*e + g*e*f) > 30:
                if a*f * c*e < 0:  # si no s'ajuden
                    if abs(abs(a*f) + abs(c*e) - abs(g*e*f)) < abs(g*e*f) \
                           and not max(abs(a*f), abs(c*e)) > abs(g*e*f):  # si no es desmadrarà
                        if a * g*e < 0:  # faig que s'ajudin contra el GEF
                            c = -c
                        else:
                            a = -a
                    else:  # poso el més gros en contra
                        if (abs(a*f) > abs(c*e) and a * g*e > 0) or (abs(c*e) > abs(a*f) and c * g*f > 0):
                            a = -a
                            c = -c
                else:  # si s'ajuden
                    if a * g*e > 0:
                        a = -a
                        c = -c
            print(a * f, c * e, g * e * f, ")", x, "// ", b * f, d * e, "||", g, "(", e, f)
            blocx = (a*f + c*e + g*e*f)*x
            print(x, blocx)
            if abs(blocx) > 60:
                x = max(1, x // 2)
            if abs(blocx) > 40:
                x = max(1, x-2)
            blocx = (a*f + c*e + g*e*f)*x
            print(x, blocx)
            h = -(blocx + (b*f+d*e))
            print(h)
            j = e*f
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


import random


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
        for x in range(gnum+1):
            coef = random.randint(1, 6)
            if moneda():
                coef = -coef
            if gnum-x > 0:
                exp = "x"
                if gnum-x > 1:
                    exp += "^{" + f"{gnum-x}" + "}"
            else:
                exp = ""

            if x == 0:
                tnum = f"{coef}" + exp
                ternums += 1
            else:
                if (random.randint(0, gnum) != 1 and not ternums >= quantsvull) or ternums + (gnum-x) <= quantsvull:
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
        for x in range(gden+1):
            coef = random.randint(1, 6)
            if moneda():
                coef = -coef
            if gden-x > 0:
                exp = "x"
                if gden - x > 1:
                    exp += "^{" + f"{gden - x}" + "}"
            else:
                exp = ""

            if x == 0:
                tden = f"{coef}" + exp
                terdens += 1
            else:
                if (random.randint(0, gden) == 1 and not terdens >= quantsvull) or terdens + (gden-x) <= quantsvull:
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
                if c-k >= 0:
                    d = random.randint(0, c-k)
                else:
                    d = -42
                if g-k >= 0:
                    h = random.randint(0, g-k)
                else:
                    h = -42
                # comprovo que al menys n'hi ha un prou gros per convergent a núm
                if c>b and g>f and c-k>d and g-k>h:
                    if moneda():
                        b = c
                    else:
                        f = g
                # coeficients
                ca = random.randint(1, 3) * random.choice([1, -1])  # principals
                cg = random.randint(1, 3) * random.choice([1, -1])
                ce = random.choice(divisors(ca*cg))  # obligats
                if moneda():
                    ce = -ce
                    signe = "+"
                cc = ca*cg // ce
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
            a = 2*max(b, d)
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
                a = random.randint(max(b+1, d), 2)
            else:  # b no recolza, per tant d ha de recolzar
                a = d
            c = 2*a
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
                b = random.randint(0, a-1)
            if random.randint(1, 5) == 1:
                d = -42
            else:
                d = random.randint(0, c-1)
            if g == 0 or moneda():
                h = -42
            else:
                h = random.randint(0, g-1)
            if random.randint(1, 5) == 1:
                f = -42
            else:
                f = random.randint(0, e-1)
            # coefs
            ca, ce, cb, cd, cf, ch = [random.choice([-1, 1]) * random.randint(1, 5) for _ in range(6)]
            if random.choice([0, 1, 1]):  # mig sovint forço resultat enter
                cc = random.choice(divisors(ca*ce))
                cg = ca*ce // cc  # aquí tinc resultat = 1 (cg és el divisor gros)
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
                gpossibles = divisors(cbd*ce)
                if len(gpossibles) > 2:
                    gpossibles = gpossibles[:2]  # si hi ha moltes opcions deixo les baixes (+ marge de maniobra per e)
                cg = random.choice(gpossibles)
                if cbd*ce % (cc*cg):  # no divideix exacte
                    ce *= fracsimple(cbd*ce//cg, cc)[1]  # multiplico a ce la part indivisible per cc
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


def signe(num):
    """returna el número amb signe (retorna buit si és 0)"""
    if num == 0 or num == "":
        return ""
    elif num > 0:
        return f"+{num}"
    else:
        return f"{num}"


def monomi(coef, exp, signe=False, allexps=False):
    """Retorna el monomi muntat

    :param coef: coeficient
    :param exp: grau (-42 indica inexistent, excepte si allexps)
    :param signe: True escriu "+" davant els positius
    :param allexps: si és cert, -42 serà un exponent com els altres
    :return: text del monomi
    """
    if (exp != -42 or allexps) and coef:
        # coeficient
        if abs(coef) == 1 and exp != 0:  # coeficient unitari i hi ha x
            if coef < 0:
                text = "-"
            else:
                text = ""
        else:
            text = f"{coef}"
        # exponent
        if exp:
            text += "x"
        if exp not in [0, 1]:
            text += "^{" + f"{exp}" + "}"
        if signe:
            if coef > 0:
                text = "+" + text
    else:
        text = ""
    return text


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
print("Digues si les següents successions són aritmètiques o geomètriques,\n"
      "i calcula'n la distància o raó en cada cas.")
for x in range(12):
    print(success(random.choice([1, 2]), 101, random.choice([1, 2, 3, 4])))

for x in range(6):
    print(powsqr(103, 2, 2))

for x in range(10):
    print(powsqr(103, 2, 3))
"""
"""
for x in range(20):
    print(eq(5, 2))"""

