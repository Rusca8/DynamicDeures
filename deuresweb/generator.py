import random, math
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
    if tipus == 2: # A±(±B)
        if nivell == 1 or nivell == 2:  # A positiva, sense -(-B) || amb -(-B)
            a = random.randint(1, 10*nums)
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
                    a == random.randint(1,10+2*(nums-1))
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


def taules(taula, div=False):
    a = random.randint(1,10)
    if div:
        return fr'{a*taula}\div {a}='
    else:
        if moneda():
            return fr'{taula}\times {a}='
        else:
            return fr'{a}\times {taula}='


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
            na=""
            nb=""
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
            c = pow(x,2)
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
            if nivell == 3:
                a = random.randint(-3, 3)
                if a == 0:
                    a = random.choice([-1, 1])
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
            if nivell == 1:
                coefs[0] = 1
            elif nivell == 2:
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


def systeq3_text (a,b,c,d):
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

"""

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