"""
La meva pròpia implementació d'algunes funcions LaTeX que jo necessitava i PyLaTeX no tenia.
(...o que eren molt difícils de trobar perquè la documentació de PyLaTeX és bastant pèssima)
"""

from pylatex import NoEscape, Command, Package


# ***************************************** ESTRUCTURA BÀSICA ******************************************** #


def begin(doc, tag, extra=""):  # TODO canviar per Command (una instrucció genèrica LaTeX que ja existeix), boig
    """Inicia una secció del LaTeX amb la comanda 'Begin' """
    if tag == "solution" and not extra == "":
        doc.append(NoEscape(r'\begin{%s}[%s]' % (tag, extra)))
    elif tag == "multicols":
        doc.append(NoEscape(r'\setlength{\parskip}{0pt}'))  # elimina la flexibilitat entre punts (espaiat molt millor)
        doc.append(NoEscape(r'\begin{%s}{%s}' % (tag, extra)))
    else:
        doc.append(NoEscape(r'\begin{%s}' % (tag,)))
    return


def end(doc, tag):
    """Tanca una secció del LaTeX amb la comanda 'End' """
    doc.append(NoEscape(r'\end{%s}' % (tag,)))
    return


def part(doc, punts=""):
    """Afegeix un apartat dins la pregunta actual, amb la comanda 'Part'
    (no cal tancar-les)
    """
    if punts == "":
        doc.append(NoEscape(r'\part'))
    else:
        doc.append(NoEscape(r'\part[%s]' % (punts,)))
    return


def space(doc, size):
    """Afegeix espai vertical entre la línia actual i la següent amb la comanda 'VSpace' """
    doc.append(NoEscape(r'\vspace{%s}' % (size,)))
    return


def stretch(doc, relsize):  # crec que no ho faig servir enlloc
    doc.append(NoEscape(r'\vspace{\stretch{%s}}' % (relsize,)))


def lines(doc, size):
    """Converteix la zona de la resposta en paper pautat, amb la comanda 'FillWithLines' """
    doc.append(NoEscape(r'\fillwithlines{%s}' % (size,)))
    return


def br(doc):
    """Introdueix un salt de línia 'NewLine' """
    doc.append(NoEscape(r'\newline'))


def pagebreak(doc, priority="4"):
    """Introdueix una suggerència de salt de pàgina pel LaTeX, amb la comanda 'PageBreak' """
    doc.append(NoEscape(r'\pagebreak[%s]' % priority))


def needspace(doc, height=8, cms=0):
    """uses needspace package to force page break if there's not enough space

    [[[[[[[[ REQUIRES needspace package ]]]]]]]

    :param doc: current doc
    :param height: height of the needed space (approx, measured in lines of text)
    :param cms: height of the needed space in cm
    """
    if cms:
        doc.append(NoEscape(r'\needspace{%scm}' % cms))
    else:
        doc.append(NoEscape(r'\needspace{%s\baselineskip}' % height))


def bloctitle(doc, text):
    """Escriu un títol amb el text donat (dóna format: negreta i gros) """
    doc.append(Command("fullwidth", NoEscape(r"\bfseries \large %s" % (text,))))


def question(doc, punts=""):
    """Comença un exercici, posant el número i la quantitat de punts, amb la comanda 'Question'
    (com amb les parts, no cal tancar-ho)
    """
    if punts == "":
        doc.append(NoEscape(r'\question'))
    else:
        doc.append(NoEscape(r'\question[%s]' % (punts,)))
    return


def choice(doc, text, corregir=False):  # ?
    if corregir:
        doc.append(NoEscape(r'\CorrectChoice %s' % (text,)))
    else:
        doc.append(NoEscape(r'\choice %s' % (text,)))
    return


def prepkg(doc, pkg):
    """Afegeix un paquet a la llista de paquets que calen pels exercicis escullits"""
    try:
        doc.prepkg.add(pkg)
    except AttributeError:
        doc.prepkg = set()
        doc.prepkg.add(pkg)
    return


def prepkgs(doc, pkgs):
    """Afegeix múltiples paquets a la llista de paquets que calen pels exercicis escollits"""
    for pkg in pkgs:
        prepkg(doc, pkg)
    return


def pre2pkg(doc):
    """Afegeix al document els paquets especials que he demanat des dels exercicis.
        ...això que diu llista de pkgs estranys vull dir els que necessiten opcions i tal (e.g. babel)

        Packages:
            'graphicx' - Per fer més grans o petits els textos de mates (scalebox)
            'amssymb' - Per tenir el símbol \nexists
    """
    try:
        for pkg in doc.prepkg:
            print(f"Adding pkg... ({pkg})")
            if pkg in ["llista_de_pkgs_estranys"]:
                ...
            else:
                doc.packages.append(Package(f'{pkg}'))
    except AttributeError:  # cap exercici necessitava coses extra
        pass

# ***************************************** TAULES ******************************************** #


def taulaconfig(ncols, align, dobles=[]):
    """Genera el text que li diu al LaTeX quin format tindrà la taula

    [[[[[[[[[ REQUIRES array package (if the 'm' alignment is used) ]]]]]]]]]]

    :param ncols: quantes columnes
    :param align:
    """
    if align == "m":  # compte a tenir el paquet array
        align = r"m{5cm}"
    config = ['|']
    for c in range(ncols):
        if c in dobles:
            config.append('|')
        config.append(fr"{align}|")
    if c+1 in dobles or -1 in dobles:
        config.append('|')
    return "".join(config)


def obretaula(doc, estructura, vorasobre=True, header=[], longtable=True):
    """Inicia una taula, que pot ser llarga o no.

    [[[[[[[[ REQUIRES longtable package if longtable ]]]]]]]]]]

    :param doc: document on posarem la taula
    :param estructura: format de la taula (el que surt de taulaconfig)
    :param vorasobre: si vull vora al costat superior de la capçalera
    :param header: elements de la capçalera (si faig servir longtable)
    :param longtable: si és una taula llarga o no
    """
    if longtable:
        obrellarga(doc, estructura, vorasobre, header=header)
    else:
        doc.append(NoEscape(r"\begin{tabular}[b]{" + estructura + "}"))  # la b ajuda amb l'espai sota l'enunciat (o no...)
        if vorasobre:
            doc.append(NoEscape(r"\hline"))


def obrellarga(doc, estructura, vorasobre=True, header=[]):
    """inicia taula multipaginable (cal 'longtable' package)

    :param doc: document on posarem la taula llarga
    :param estructura: format de la taula (el que surt de taulaconfig)
    :param vorasobre: si vull vora al costat superior de la capçalera
    :param header: elements de la capçalera (títols de les columnes, vaja)
    """
    # estructura de la taula
    doc.append(NoEscape(r"\begin{longtable}[b]{" + estructura + "}"))
    if vorasobre:
        doc.append(NoEscape(r"\hline"))
    # capçalera inici
    filataula(doc, header)
    doc.append(NoEscape(r"\endfirsthead"))
    if vorasobre:
        doc.append(NoEscape(r"\hline"))
    # capçalera cont
    filataula(doc, header)
    doc.append(NoEscape(r"\endhead"))
    # peu trencat
    filataula(doc, ["..." for _ in header], False)
    doc.append(NoEscape(r"\hline"))
    doc.append(NoEscape(r"\endfoot"))
    # últim peu
    doc.append(NoEscape(r"\hline"))
    doc.append(NoEscape(r"\endlastfoot"))


def filataula(doc, caselles, vorasota=True, py=0):
    """afegeix una fila a la taula, donades les caselles

    :param doc: document al qual afegir la taula
    :param caselles: llista amb les caselles de la taula
    :param vorasota: marcar la vora sota cada fila
    :param py: padding vertical (en desenes d'alçada de la x minúscula: py=35 és padding de '3.5ex')
    """
    # càlculs padding
    if py:
        pt = py + 22  # corregeixo la pròpia alçada del text (la implementació de pt que tinc compta des de baseline)
        pt = r" \rule{0pt}{" + f"{pt // 10}.{pt % 10}ex" + "} "
        pb = f"[{py // 10}.{py % 10}ex]"
    else:
        pt = ""
        pb = ""
    # muntatge
    doc.append(NoEscape(pt + r" & ".join(caselles) + rf"\\" + pb))  # \\[3ex] fa espai a sota
    if vorasota:
        doc.append(NoEscape(r"\hline"))


def tancataula(doc, longtable=True):
    """Tanca una taula (o una taula llarga si longtable)"""
    if longtable:
        end(doc, "longtable")
    else:
        end(doc, "tabular")


def envt(text, qtat=4):
    """Afegeix espais al voltant d'un text
    (per evitar que la columna quedi estreta si té títol curt però espera una resposta llarga de l'alumne)
    """
    return "".join(['\\ ' for _ in range(qtat)] + [text] + ['\\ ' for _ in range(qtat+1)])


# ***************************************** SOLUCIONS ******************************************** #


def escriusolus(llista, mates=False):
    """fa una llista numerada amb totes les solucions de la llista

    :param llista: llista de solucions (que genera el propi generador)
    :param mates: cal afegir entorn matemàtic a les solucions
    """
    llista = llista[:]  # evito problemes amb mutable
    for x in range(len(llista)):
        if x < 26:
            apartat = f"{chr(x+97)}"  # a-z
        else:
            apartat = f"{chr(x//26+96)+chr(x%26+97)}"  # aa-zz
        if mates:
            llista[x] = r"\textbf{" + apartat + ":}~" f"${llista[x]}$"
        else:
            llista[x] = r"\textbf{" + apartat + ":}~" f"{llista[x]}"
    return r"; \penalty-300 ".join(llista)


def blocsolus(doc, solucions, llista, mates=False, stretch=False):  # stretch necessita package
    """Escriu les solucions al document en cas que s'hagi escollit que n'hi hagi

    [[[[[[[[[[[[[[[[[[ stretch necessita setspace package ]]]]]]]]]]]]]]]]]]]

    :param doc: document LaTeX on escriure-ho.
    :param solucions: bool, diu si hi ha d'haver o no solucions al document.
    :param llista: llista de solucions de l'exercici.
    :param mates: true si cal posar $$ a cada apartat / false si és text pla
    :param stretch: interlineat extra (cal needspace package).
    """
    if solucions:
        doc.append(NoEscape(r'\begin{solution}'))
        if stretch:
            prepkg(doc, "setspace")
            doc.append(NoEscape(r'\setstretch{' f"{stretch}" '}'))
        doc.append(NoEscape(r'%s\par' % escriusolus(llista, mates)))
        doc.append(NoEscape(r'\end{solution}'))
    return


def blocsolucions(doc, llista, mates=False, stretch=False):
    """Versió nova de blocsolus (no demana el bool solucions, perquè sempre serà sí).
    """
    blocsolus(doc, solucions=True, llista=llista, mates=mates, stretch=stretch)
    return


def textsolucions(doc, llista, mates=False, stretch=False):
    """Prepara el text per una solució (sense generar el bloc de solucions de LaTeX)

    [[[[[[[[[[ stretch necesssita setspace package ]]]]]]]]]]

    :param doc: cal el doc per passar-li el setspace si faig stretch
    :param llista: llista de solus
    :param mates: True si cal fer '$text$' en lloc de 'text'
    :param stretch: estirar l'interlineat del text
    """
    text = ["\\begin{quote} {"]
    if stretch:
        prepkg(doc, "setspace")
        text.append(r'\setstretch{' f"{stretch}" '} ')
    text.append(r'%s\par' % escriusolus(llista, mates))
    text.append("} \\end{quote}")
    return "".join(text)


def metasolucions(doc, llista, breakpage=True):
    """Agafa una llista amb les solucions de tots els exercicis que en tenen i escriu totes les solucions
    amb el número de l'exercici al qual pertanyen  (per quan les poso totes al final de la fitxa).

    :param doc: Document on afegirem les coses
    :param llista: Llista de solucions. Cada solució de la llista té l'estructura [qnum, [enunciat, solu<text>]]
    :param breakpage: True = començar les solucions en plana nova
    """
    if breakpage:
        doc.append(NoEscape(r"\newpage"))
    bloctitle(doc, "Solucions dels exercicis")

    for ex in llista:
        if ex[1][1]:
            doc.append(NoEscape(f"{ex[0]}. {ex[1][0]}"))
            doc.append(NoEscape(r"\par"))
            doc.append(NoEscape(f"{ex[1][1]}"))
            doc.append(NoEscape(r"\par"))
    return
