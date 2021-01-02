import random
import re  # regex


def fc_frase(text):
    """Converteix un text qualsevol en un exercici de factor comú"""
    try:
        text = fc_split(text)
        text = fc_subsplit(text)
        text = fc_lparent(text)
        text = fc_ldistrib(text)
        text = fc_merge(text)
    except:
        text = "hi ha hagut un problema generant la frase oculta..."
    return text


def fc_split(text):
    """Neteja, retalla i agrupa un text per fer-hi factor comú"""
    text = ' '.join(text.split())
    text = neteja(text).lower()
    text = text.split()

    minlen = 5
    llista = []
    b = ["", "", ""]  # buffer
    for x in text:
        b = [b[1], b[2], x]  # van entrant per la dreta...
        if b[0]:
            if len(b[0]) < minlen or (b[1] and len(b[1]) < minlen):  # si una de les dues és petita, van juntes
                llista.append(b[0] + random_signe() + b[1])
                if b[2] and len(b[0]) + len(b[1]) < 4:  # això hi enganxa la tercera si les altres són massa curtes
                    llista[-1] += random_signe() + b[2]
                    b[2] = ""
                b[0] = ""
                b[1] = ""
            else:
                llista.append(b[0])
                b[0] = ""
    if b[1] or b[2]:
        if len(b[1]) >= minlen and len(b[2]) >= minlen:  # independents
            llista.append(b[1])
            llista.append(b[2])
        elif b[1] and b[2]:
            llista.append(b[1] + random_signe() + b[2])
        else:
            llista.append(b[1] + b[2])

    if len(llista[-1]) == 1:  # si l'última ha quedat sola l'enganxo a l'anterior
        if len(llista) > 1:
            llista[-2] += random_signe() + llista[-1]
            llista = llista[:-1]
    return llista


def fc_subsplit(llista):
    """Agafa un fc_split i el separa en forma de llista, i cada paraula de la llista la retalla amb fc_break
    """
    for k, x in enumerate(llista):
        # retalla les separacions que ja tenia
        xnou = []
        for i, y in enumerate(x.split("+")):
            if i > 0:
                xnou.append("+")
            for j, z in enumerate(y.split("-")):
                if j > 0:
                    xnou.append("-")
                for part in fc_break(z):  # retallo la paraula
                    xnou.append(part)
        # separacions extra
        llista[k] = xnou

    return llista


def fc_break(paraula):
    """Retalla una paraula donada de manera que no quedin lletres repes a cada tall
       (...i també retalla si el tall és massa llarg)
    """
    # anàlisi
    tinc = {}
    talls = [0]
    for i, c in enumerate(paraula):
        if c not in tinc:
            tinc[c] = i
        else:
            if tinc[c] >= talls[-1]:  # si queda a la dreta del tall (si no no m'afecta)
                talls.append(random.randint(tinc[c] + 1, i))  # tallaré a l'esquerra de la posició que surti
            tinc[c] = i  # renovo
        if i - talls[-1] > 2:
            talls.append(i)
    # retallant
    separada = []
    for i, x in enumerate(talls):
        if i > 0:
            separada.append(paraula[talls[i - 1]:talls[i]])
            separada.append(random_signe())
    separada.append(paraula[talls[i]:])
    return separada


def fc_lparent(llista):
    """Fa fc_parent sobre tots els elements de la llista"""
    for i, x in enumerate(llista):
        llista[i] = fc_parent(x)
    return llista


def fc_parent(bloc):
    """Tria on posar el parèntesis d'un bloc donat de paraules de factor comú"""
    blocnou = []
    if len(bloc) < 2:  # ["no"] / ["i"]
        blocnou.append(bloc[0])
    elif len(bloc) < 4:  # ["co", "+", "ses"] (dos talls)
        if len(bloc[0]) < 2 and len(bloc[2]) < 2:  # ["i", "+", "o"] (mono)
            for x in bloc:
                blocnou.append(x)
        elif len(bloc[0]) < 2 or (moneda() and not len(bloc[2]) < 2):  # ["i", "+", "cosa"] (retallo cosa, parent al +)
            blocnou.append(bloc[0])
            blocnou.append("(")
            tall = random.randint(1, len(bloc[2]) - 1)
            blocnou.append(bloc[2][0:tall])
            blocnou.append("+")
            blocnou.append(bloc[2][tall:])
            blocnou.append(")")
        else:  # ["cosa", "+", "i"] (retallo cosa per intercalar-hi el parent)
            blocnou.append(bloc[0][:-1])  # tallo per la última pq així faig més distributiva després
            blocnou.append("(")
            blocnou.append(bloc[0][-1])
            blocnou.append(bloc[1])
            blocnou.append(bloc[2])
            blocnou.append(")")
    else:  # ["ei", "+", "com", "+", "estàs"] el primer "+" passa a parèntesi
        blocnou.append(bloc[0])
        blocnou.append("(")
        for x in bloc[2:]:
            blocnou.append(x)
        blocnou.append(")")
    # evita que més lletres del compte siguin comuns
    if "(" in blocnou:  # just in case
        facts = [blocnou[i] for i in range(len(blocnou)) if (i > 1 and not i % 2)]  # agafo els que no són símbols
        for c in facts[0]:
            if all([c in x for x in facts[1:]]):  # una lletra surt a tots els factors => separo l'últim caràcter
                blocnou = blocnou[:-2] + [blocnou[-2][:-1]] + [random_signe()] + [blocnou[-2][-1]] + [blocnou[-1]]
    return blocnou


def fc_distrib(bloc):
    blocnou = []
    if "(" in bloc:
        partcomu = fc_varexp(bloc[0])
        for i, x in enumerate(bloc):
            if i > 0 and not (i % 2):  # els que tenen lletres a partir del segon
                part = fc_varexp(x)
                # distributiva
                pendents = [[], []]
                for j, y in enumerate(partcomu[0]):
                    if y in part[0]:  # si ja hi és pujo exp
                        part[1][part[0].index(y)] += 1
                    else:  # si no hi és la deixo pendent d'intercalar
                        pendents[0].append(y)
                        pendents[1].append(partcomu[1][j])
                if i > 2:
                    part = fc_intercala(pendents, part, False)  # a partir del segon bloc no comú: p. comuna desordenada
                else:
                    part = fc_intercala(pendents, part)  # el primer bloc no comú respecta l'ordre original
                blocnou.append("".join([exp(part[0][n], part[1][n]) for n in range(len(part[0]))]))

            elif 2 < i < len(bloc) - 1:  # això ho ha proposat pycharm, que es veu que es pot fer ("i" entre tal i tal)
                blocnou.append(x)
    else:
        blocnou = "".join(bloc)
    return blocnou


def fc_ldistrib(llista):
    """Fa fc_distrib sobre tots els elements de la llista"""
    for i, x in enumerate(llista):
        llista[i] = fc_distrib(x)
    return llista


def fc_merge(llista):
    """Ajunta cada bloc del factor comú en un sol element de text"""
    for i, x in enumerate(llista):
        llista[i] = "".join(x)
    return llista


def fc_intercala(comuns, part, ordenats=True):
    if not ordenats:
        comuns = fc_barreja(comuns)
    seguits = 0
    ic = 0
    ip = 0
    partnova = [[], []]
    for x in range(len(comuns[0]) + len(part[0])):
        if ip >= len(part[0]) or (ic < len(comuns[0])
                and random.choice([1 for _ in range(len(comuns[0])-ic)] + [0 for _ in range(len(part[0])-ip)])):
            partnova[0].append(comuns[0][ic])
            partnova[1].append(comuns[1][ic])
            ic += 1
            if seguits > 0:
                seguits = -1
            else:
                seguits -= 1
        else:
            partnova[0].append(part[0][ip])
            partnova[1].append(part[1][ip])
            ip += 1
            if seguits > 0:
                seguits = +1
            else:
                seguits += 1
    return partnova


def fc_barreja(part):
    """Donada una part de factor comú [[vars], [exps]], la retorna barrejada"""
    novapart = [[], []]
    ordre = list(range(len(part[0])))
    random.shuffle(ordre)
    for x in ordre:
        novapart[0].append(part[0][x])
        novapart[1].append(part[1][x])
    return novapart


def fc_varexp(part):
    var = [c for c in part]  # no n'hi ha mai de repetides, així que bé
    exp = [1 for _ in part]
    return [var, exp]


def random_signe():
    return random.choice(["-", "+"])


def neteja(text, accents=False):
    if not accents:
        text = re.sub('[àá]+', 'a', text)
        text = re.sub('[ÀÁ]+', 'A', text)
        text = re.sub('[éè]+', 'e', text)
        text = re.sub('[ÉÈ]+', 'E', text)
        text = re.sub('[íï]+', 'i', text)
        text = re.sub('[ÍÏ]+', 'I', text)
        text = re.sub('[óò]+', 'o', text)
        text = re.sub('[ÓÒ]+', 'O', text)
        text = re.sub('[úü]+', 'u', text)
        text = re.sub('[ÚÜ]+', 'U', text)
        text = re.sub('[ñ]+', 'n', text)
        text = re.sub('[Ñ]+', 'N', text)
        text = re.sub('[ç]+', 'c', text)
        text = re.sub('[Ç]+', 'C', text)
        return re.sub('[^a-zA-Z -]+', '', text)  # canvia el que no és alfabet per res de res
    else:
        return re.sub('[^a-zA-ZàáéèíïóòúüÀÁÈÉÍÏÓÒÚÜ çñÇÑ-]+', '', text)


def exp(b, e):
    if e > 1:
        return f"{b}^" "{" f"{e}" "}"
    else:
        return f"{b}"


def moneda():
    return bool(random.getrandbits(1))
