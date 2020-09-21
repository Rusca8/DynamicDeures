import random

from pylatex import Document, Section
from pylatex import Command, NoEscape, Math, Tabular, Package

import generator as gen


def combinades(opcions, solucions=False):  # - - - - - - - - - - - - - - - - - - - - - COMBINADES
    tema = "comb"

    # getting opcions
    curs = opcions["curs"]

    if "sumes" in opcions:
        sumes = True
        qsumes = quantesson(opcions["qsumes"], "sumes")
        qpsumes = quantesson(opcions["qpsumes"], "psumes")
    else:
        sumes = False
        qsumes = 0
        qpsumes = 0
    print(f"A+B = {qsumes}, A+(+B) = {qpsumes}")

    if "multiplicacions" in opcions:
        multis = True
        qmultis = quantesson(opcions["qmultis"], "multis")
        qsmultis = quantesson(opcions["qsmultis"], "smultis")
        taules = []
        for x in range(1, 13):
            if f"t{x}" in opcions:
                taules.append(x)
        if len(taules) == 0:
            taules = list(range(1, 11))
        print("M.Taules: ", taules)

    else:
        multis = False
        qmultis = 0
        qsmultis = 0
    print(f"A*B = {qmultis}, A*(-B) = {qsmultis}")

    if "divisions" in opcions:
        divis = True
        qdivis = quantesson(opcions["qdivis"], "divis")
        qsdivis = quantesson(opcions["qsdivis"], "sdivis")
        dtaules = []
        if multis and opcions["copymult"] == "com":  # si estic copiant les multis, copio les taules
            dtaules = taules
        else:
            for x in range(1, 13):
                if f"td{x}" in opcions:
                    dtaules.append(x)
            if len(dtaules) == 0:
                dtaules = list(range(1, 11))
        print("D.Taules: ", dtaules)
    else:
        divis = False
        qdivis = 0
        qsdivis = 0
    print(f"A/B = {qdivis}, A/(-B) = {qsmultis}")

    print("Generant pdf: {} ({})".format(temallarg(tema), curs))

    # PyLaTeX code
    geometry = margins()
    doc = Document(documentclass="exam", geometry_options=geometry)
    doc.packages.append(Package('multicol'))
    doc.packages.append(Package('alphalph'))  # per permetre aa bb cc

    headfoot(doc, opcions, tema)
    myconfig(doc, solucions)

    # doc.append(NoEscape(r'\renewcommand{\partlabel}{\thepartno)}')) # canvia l'embolcall del número d'apartat
    doc.append(NoEscape(
        r'\renewcommand{\thepartno}{\alphalph{\value{partno}}}'))  # per permetre doble lletra, 26*26 = 676 apartats max

    # preguntes

    if sumes or multis or divis:
        if any([qsumes, qpsumes, qmultis, qsmultis, qdivis, qsdivis]):
            begin(doc, 'questions')

            if sumes:

                bloctitle(doc, "Sumes i restes amb enters")

                if qsumes != 0:
                    n = qsumes
                    question(doc, f"{n // 4}")
                    doc.append("Calcula les següents sumes i restes sense parèntesis.")
                    begin(doc, 'parts')
                    begin(doc, "multicols", "4")
                    for x in range(0, n // 4):
                        uncalcul(doc, [1, 1], "0.2cm")  # resultat positiu
                    for x in range(0, n // 4):
                        uncalcul(doc, [1, 2], "0.2cm")  # a positiva
                    for x in range(0, n // 2):
                        uncalcul(doc, [1, 3], "0.2cm")  # normal
                    end(doc, "multicols")
                    end(doc, 'parts')

                pagebreak(doc, 3)

                if qpsumes != 0:
                    n = qpsumes
                    question(doc, f"{n // 2}")
                    doc.append("Calcula les següents sumes i restes amb parèntesis.")
                    begin(doc, 'parts')
                    begin(doc, "multicols", "3")
                    for x in range(0, n // 3):
                        uncalcul(doc, [2, 1], "0.2cm")  # a positiva
                    for x in range(0, n // 3):
                        uncalcul(doc, [2, 2], "0.2cm")  # no doble neg
                    for x in range(0, n // 3):
                        uncalcul(doc, [2, 3], "0.2cm")  # normal
                    end(doc, "multicols")
                    end(doc, 'parts')

                if qsumes == 0 and qpsumes == 0:
                    doc.append("Que diu que en vol, però no en vol.")

            pagebreak(doc, 2)

            if multis or divis:
                if multis and divis:
                    bTitle = "Multiplicacions i divisions amb enters"
                elif multis:
                    bTitle = "Multiplicacions amb enters"
                else:
                    bTitle = "Divisions amb enters"
                bloctitle(doc, bTitle)

                if qmultis or qdivis:
                    if qmultis:
                        if qdivis:
                            question(doc, f"{qmultis // 2}")
                            doc.append("Calcula les següents multiplicacions i divisions sense signes")
                        else:
                            question(doc, f"{qmultis // 2}")
                            doc.append("Calcula les següents multiplicacions sense signes")
                    else:
                        question(doc, f"{qdivis // 2}")
                        doc.append("Calcula les següents divisions sense signes")

                    begin(doc, 'parts')
                    begin(doc, "multicols", "4")

                    if qmultis != 0 and qdivis != 0:
                        n = qmultis // 2
                    elif qmultis != 0:
                        n = qmultis
                    else:
                        n = qdivis

                    if qmultis != 0:
                        for x in range(0, n):
                            part(doc)
                            doc.append(NoEscape(r'$%s$' % gen.taules(random.choice(taules))))
                            space(doc, "0,2cm")
                    if qdivis != 0:
                        for x in range(0, n):
                            part(doc)
                            doc.append(NoEscape(r'$%s$' % gen.taules(random.choice(dtaules), True)))  # true és divis
                            space(doc, "0,2cm")
                    end(doc, "multicols")
                    end(doc, 'parts')

                pagebreak(doc, 1)

                if qsmultis != 0 or qsdivis != 0:
                    if qsmultis != 0:
                        if qsdivis != 0:
                            question(doc, f"{qsmultis}")
                            doc.append(
                                "Calcula les següents multiplicacions i divisions amb signes")  # TODO afegir suport per nums grans
                        else:
                            question(doc, f"{qsmultis}")
                            doc.append("Calcula les següents multiplicacions amb signes")
                    else:
                        question(doc, f"{qsdivis}")
                        doc.append("Calcula les següents divisions amb signes")

                    if qsmultis != 0 or qsdivis != 0:
                        begin(doc, 'parts')
                        begin(doc, "multicols", "3")

                        if qsmultis != 0:
                            n = qsmultis
                        else:
                            n = qsdivis

                        for x in range(0, n // 2):  # meitat sense doble negatiu
                            if qsmultis != 0 and not qsdivis != 0:
                                uncalcul(doc, [3, 2], "0,2cm")  # mult
                            elif qsdivis != 0 and not qsmultis != 0:
                                uncalcul(doc, [3, 5], "0,2cm")  # div
                            else:
                                uncalcul(doc, [3, random.choice([2, 5])], "0,2cm")  # mult i div

                        for x in range(0, n // 2):
                            if qsmultis != 0 and not qsdivis != 0:
                                uncalcul(doc, [3, 3], "0,2cm")  # mult
                            elif qsdivis != 0 and not qsmultis != 0:
                                uncalcul(doc, [3, 6], "0,2cm")  # div
                            else:
                                uncalcul(doc, [3, random.choice([3, 6])], "0,2cm")  # mult i div

                        end(doc, "multicols")
                        end(doc, 'parts')

                if qmultis == 0 and qdivis == 0 and qsmultis == 0 and qsdivis == 0:
                    doc.append("Potser que triïs alguna cosa... (o no diguis que vols multiplicar i dividir)")

            end(doc, 'questions')
        else:
            doc.append("Calia tirar-se tanta estona per no posar res? Potser no")
    else:
        doc.append("haha.. quina gràcia.. has fet un pdf sense res, que original...")

    doc.generate_pdf("deuresweb/static/pdfs/" + temallarg(tema))
    print("PDF generat.")

    return


def apilades(opcions, solucions=False):  # - - - - - - - - - - - - - - - - - - - - - APILADES
    tema = "api"

    # getting opcions
    curs = opcions["curs"]
    print("Generant pdf: {} ({})".format(temallarg(tema), curs))

    if "sumes" in opcions:
        sumes = True
        qsumes = quantesson(opcions["qsumes"], "v_sumes")
        qdsumes = quantesson(opcions["qdsumes"], "v_dsumes")

        # sense decimals
        sdalt = []
        for n in range(6, 1, -1):  # l'últim no el fa
            if f"sdalt{n}" in opcions:
                sdalt.append(n)
        if not sdalt:
            sdalt = [5, 4, 3, 2]  # si no hay arqueólogos me lo invento

        sbaix = []
        for n in range(5, 1, -1):  # l'últim no el fa
            if f"sbaix{n}" in opcions:
                sbaix.append(n)
        if not sbaix:
            sbaix = [4, 3, 2]

        # amb decimals
        sddalt = []
        for n in range(6, 0, -1):  # l'últim no el fa
            if f"sddalt{n}" in opcions:
                sddalt.append(n)
        if not sddalt:
            sddalt = [3, 2, 1]

        sdecidalt = []
        for n in range(0, 3):  # l'últim no el fa
            if f"sdecidalt{n}" in opcions:
                sdecidalt.append(n)
        if not sdecidalt:
            sdecidalt = [1, 2]

        sdbaix = []
        for n in range(5, 0, -1):  # l'últim no el fa
            if f"sdbaix{n}" in opcions:
                sdbaix.append(n)
        if not sdbaix:
            sdbaix = [2, 1]

        sdecibaix = []
        for n in range(0, 3):  # l'últim no el fa
            if f"sdecibaix{n}" in opcions:
                sdecibaix.append(n)
        if not sdecibaix:
            sdecibaix = [1, 2]

    else:
        sumes = False
        qsumes = 0
        qdsumes = 0
    print(f"42+42 {qsumes}, 4.2+4.2 {qdsumes}")

    if "restes" in opcions:
        restes = True
        qrestes = quantesson(opcions["qrestes"], "v_restes")
        qdrestes = quantesson(opcions["qdrestes"], "v_drestes")

        # sense decimals
        rdalt = []
        for n in range(6, 1, -1):  # l'últim no el fa
            if f"rdalt{n}" in opcions:
                rdalt.append(n)
        if not rdalt:
            rdalt = [5, 4, 3, 2]  # si no hay arqueólogos me lo invento

        rbaix = []
        for n in range(5, 1, -1):  # l'últim no el fa
            if f"rbaix{n}" in opcions:
                rbaix.append(n)
        if not rbaix:
            rbaix = [4, 3, 2]

        # amb decimals
        rddalt = []
        for n in range(6, 0, -1):  # l'últim no el fa
            if f"rddalt{n}" in opcions:
                rddalt.append(n)
        if not rddalt:
            rddalt = [3, 2, 1]

        rdecidalt = []
        for n in range(0, 3):  # l'últim no el fa
            if f"rdecidalt{n}" in opcions:
                rdecidalt.append(n)
        if not rdecidalt:
            rdecidalt = [1, 2]

        rdbaix = []
        for n in range(5, 0, -1):  # l'últim no el fa
            if f"rdbaix{n}" in opcions:
                rdbaix.append(n)
        if not rdbaix:
            rdbaix = [2, 1]

        rdecibaix = []
        for n in range(0, 3):  # l'últim no el fa
            if f"rdecibaix{n}" in opcions:
                rdecibaix.append(n)
        if not rdecibaix:
            rdecibaix = [1, 2]

    else:
        restes = False
        qrestes = 0
        qdrestes = 0
    print(f"42-42 {qrestes}, 4.2-4.2 {qdrestes}")

    if "multiplicacions" in opcions:
        multis = True
        qmultis = quantesson(opcions["qmultis"], "v_multis")
        qdmultis = quantesson(opcions["qdmultis"], "v_dmultis")

        # sense decimals
        mdalt = []
        for n in range(6, 1, -1):  # l'últim no el fa
            if f"mdalt{n}" in opcions:
                mdalt.append(n)
        if not mdalt:
            mdalt = [5, 4, 3, 2]  # si no hay arqueólogos me lo invento

        mbaix = []
        for n in range(4, 0, -1):  # l'últim no el fa
            if f"mbaix{n}" in opcions:
                mbaix.append(n)
        if not mbaix:
            mbaix = [2, 1]

        # amb decimals
        mddalt = []
        for n in range(6, 1, -1):  # l'últim no el fa
            if f"mddalt{n}" in opcions:
                mddalt.append(n)
        if not mddalt:
            mddalt = [4, 3, 2]

        mdecidalt = []
        for n in range(0, 3):  # l'últim no el fa
            if f"mdecidalt{n}" in opcions:
                mdecidalt.append(n)
        if not mdecidalt:
            mdecidalt = [1, 2]

        mdbaix = []
        for n in range(4, 0, -1):  # l'últim no el fa
            if f"mdbaix{n}" in opcions:
                mdbaix.append(n)
        if not mdbaix:
            mdbaix = [1]

        mdecibaix = []
        for n in range(0, 3):  # l'últim no el fa
            if f"mdecibaix{n}" in opcions:
                mdecibaix.append(n)
        if not mdecibaix:
            mdecibaix = [1]

        print(mdecidalt, mdecibaix)

    else:
        multis = False
        qmultis = 0
        qdmultis = 0
    print(f"42*42 {qmultis} 4.2*4.2 {qdmultis}")

    divis = False
    """
    if "divis" in opcions:
        sistemes3 = True
        qsist3 = quantesson(opcions["qsist3"], "sistemes3")
    else:
        sistemes3 = False
        qsist3 = 0
    print(f"Ax+By+Cz=D ... etc que em fa mandra copiar {qsist}")
    """

    # PyLaTeX code
    geometry = margins()
    doc = Document(documentclass="exam", geometry_options=geometry)
    doc.packages.append(Package('multicol'))
    doc.packages.append(Package('amsmath'))
    doc.packages.append(Package('alphalph'))

    headfoot(doc, opcions, tema)
    myconfig(doc, solucions)

    doc.append(NoEscape(
        r'\renewcommand{\thepartno}{\alphalph{\value{partno}}}'))  # per permetre doble lletra, 26*26 = 676 apartats max

    # preguntes
    if sumes or restes or multis or divis:  # aquí van totes les grans
        if any([qsumes, qdsumes, qrestes, qdrestes, qmultis, qdmultis]):  # aquí van totes les petites
            begin(doc, 'questions')

            if sumes:
                bloctitle(doc, "Sumes")

            if qsumes:
                n = qsumes
                question(doc, f"{n}")
                doc.append("Resol les següents sumes apilades (sense decimals).")
                begin(doc, 'parts')
                begin(doc, "multicols", "4")
                for x in range(0, n):
                    part(doc)
                    a = random.choice(sdalt)
                    b = random.choice(sbaix)
                    doc.append(NoEscape(r'\Large $%s$\normalsize' % gen.apilades(1, 1, [a, b])))
                    space(doc, "1cm")
                end(doc, "multicols")
                end(doc, 'parts')
                space(doc, "1cm")

            if qdsumes:
                n = qdsumes
                question(doc, f"{2 * n}")
                doc.append("Resol les següents sumes apilades (amb decimals).")
                begin(doc, 'parts')
                begin(doc, "multicols", "4")
                for x in range(0, n):
                    part(doc)
                    a = random.choice(sddalt)
                    b = random.choice(sdbaix)
                    c = random.choice(sdecidalt)
                    d = random.choice(sdecibaix)
                    doc.append(NoEscape(r'\Large $%s$\normalsize' % gen.apilades(1, 2, [a, b], [c, d])))
                    space(doc, "1cm")
                end(doc, "multicols")
                end(doc, 'parts')
                space(doc, "1cm")

            if restes:
                bloctitle(doc, "Restes")

            if qrestes:
                n = qrestes
                question(doc, f"{n}")
                doc.append("Resol les següents restes apilades (sense decimals).")
                begin(doc, 'parts')
                begin(doc, "multicols", "4")
                for x in range(0, n):
                    part(doc)
                    a = random.choice(rdalt)
                    b = random.choice(rbaix)
                    doc.append(NoEscape(r'\Large $%s$\normalsize' % gen.apilades(2, x // n + 1, [a, b])))
                    space(doc, "1cm")
                end(doc, "multicols")
                end(doc, 'parts')
                space(doc, "1cm")

            if qdrestes:
                n = qdrestes
                question(doc, f"{2 * n}")
                doc.append("Resol les següents restes apilades (amb decimals).")
                begin(doc, 'parts')
                begin(doc, "multicols", "4")
                for x in range(0, n):
                    part(doc)
                    a = random.choice(rddalt)
                    b = random.choice(rdbaix)
                    c = random.choice(rdecidalt)
                    d = random.choice(rdecibaix)
                    doc.append(NoEscape(r'\Large $%s$\normalsize' % gen.apilades(2, 3, [a, b], [c, d])))
                    space(doc, "1cm")
                end(doc, "multicols")
                end(doc, 'parts')
                space(doc, "1cm")

            if multis:
                bloctitle(doc, "Multiplicacions")

            if qmultis:
                n = qmultis
                question(doc, f"{n}")
                doc.append("Resol les següents multiplicacions apilades (sense decimals).")
                begin(doc, 'parts')
                begin(doc, "multicols", "4")
                for x in range(0, n):
                    part(doc)
                    a = random.choice(mdalt)
                    b = random.choice(mbaix)
                    doc.append(NoEscape(r'\Large $%s$\normalsize' % gen.apilades(3, 1, [a, b])))
                    space(doc, "1.6cm")
                end(doc, "multicols")
                end(doc, 'parts')
                space(doc, "1.6cm")

            if qdmultis:
                n = qdmultis
                question(doc, f"{2 * n}")
                doc.append("Resol les següents multiplicacions apilades (amb decimals).")
                begin(doc, 'parts')
                begin(doc, "multicols", "4")
                for x in range(0, n):
                    part(doc)
                    a = random.choice(mddalt)
                    b = random.choice(mbaix)
                    c = random.choice(mdecidalt)
                    d = random.choice(mdecibaix)
                    doc.append(NoEscape(r'\Large $%s$\normalsize' % gen.apilades(3, 2, [a, b], [c, d])))
                    space(doc, "2.1cm")
                end(doc, "multicols")
                end(doc, 'parts')
                space(doc, "2.1cm")

            end(doc, 'questions')
        else:
            doc.append("Calia tirar-se tanta estona per no posar res? Potser no")
    else:
        doc.append("haha.. quina gràcia.. has fet un pdf sense res, que original...")

    doc.generate_pdf("deuresweb/static/pdfs/" + temallarg(tema))
    print("PDF generat.")

    return


def equacions(opcions, solucions=False):  # - - - - - - - - - - - - - - - - - - - - - EQUACIONS
    tema = "eq"

    # getting opcions
    curs = opcions["curs"]
    print("Generant pdf: {} ({})".format(temallarg(tema), curs))

    if "primer" in opcions:
        primer = True
        qsimples = quantesson(opcions["qsimples"], "simples")
        qdsimples = quantesson(opcions["qdsimples"], "dsimples")
    else:
        primer = False
        qsimples = 0
        qdsimples = 0
    print(f"x+B=C {qsimples}, Ax+b=C {qdsimples}")

    if "segon" in opcions:
        segon = True
        qincomps = quantesson(opcions["qincomps"], "incomps")
        qcompletes = quantesson(opcions["qcompletes"], "completes")
        qpolis = quantesson(opcions["qpolis"], "polis")
    else:
        segon = False
        qincomps = 0
        qcompletes = 0
        qpolis = 0
    print(f"Ax^2+Bx {qincomps}, Ax^2+Bx+C {qcompletes}, P(x)=Q(x) {qpolis}")

    if "sistemes" in opcions:
        sistemes = True
        qsist = quantesson(opcions["qsist"], "sistemes")
    else:
        sistemes = False
        qsist = 0
    print(f"Ax+By=C i Dx+Ey=F {qsist}")

    if "sistemes3" in opcions:
        sistemes3 = True
        qsist3 = quantesson(opcions["qsist3"], "sistemes3")
    else:
        sistemes3 = False
        qsist3 = 0
    print(f"Ax+By+Cz=D ... etc que em fa mandra copiar {qsist}")

    # PyLaTeX code
    geometry = margins()
    doc = Document(documentclass="exam", geometry_options=geometry)
    doc.packages.append(Package('multicol'))
    doc.packages.append(Package('amsmath'))
    doc.packages.append(Package('alphalph'))

    headfoot(doc, opcions, tema)
    myconfig(doc, solucions)

    doc.append(NoEscape(
        r'\renewcommand{\thepartno}{\alphalph{\value{partno}}}'))  # per permetre doble lletra, 26*26 = 676 apartats max

    # preguntes
    if primer or segon or sistemes or sistemes3:
        if any([qsimples, qdsimples, qsist, qsist3, qincomps, qcompletes, qpolis]):
            begin(doc, 'questions')

            if primer:
                bloctitle(doc, "Equacions de primer grau")

            if qsimples != 0:
                n = qsimples
                question(doc, f"{n // 2}")
                doc.append("Resol les següents equacions de primer grau (sense coeficient a la x).")
                begin(doc, 'parts')
                begin(doc, "multicols", "3")
                for x in range(0, n // 2):
                    part(doc)
                    doc.append(NoEscape(r'$%s$' % gen.eq(1, 1)))  # faig meitat de cada
                    space(doc, "0.7cm")
                for x in range(0, n // 2):
                    part(doc)
                    doc.append(NoEscape(r'$%s$' % gen.eq(1, 2)))  # faig meitat de cada
                    space(doc, "0.7cm")
                end(doc, "multicols")
                end(doc, 'parts')
                space(doc, "0.7cm")

            if qdsimples != 0:
                n = qdsimples
                question(doc, f"{qdsimples}")
                doc.append("Resol les següents equacions de primer grau (amb coeficient).")
                begin(doc, 'parts')
                begin(doc, "multicols", "3")
                for x in range(0, n):
                    part(doc)
                    if x < n // 2:
                        doc.append(NoEscape(r'$%s$' % gen.eq(2, 2)))  # positiu
                    else:
                        doc.append(NoEscape(r'$%s$' % gen.eq(2, 3)))  # enter
                    space(doc, "1.4cm")
                end(doc, "multicols")
                end(doc, 'parts')
                space(doc, "1cm")

            if segon:
                bloctitle(doc, "Equacions de segon grau")

            if qincomps:
                n = qincomps
                question(doc, f"{n // 2}")
                doc.append("Resol les següents equacions de segon grau (incompletes).")
                begin(doc, 'parts')
                begin(doc, "multicols", "3")
                for x in range(0, n):
                    part(doc)
                    if x < n // 4:
                        if x < 2:
                            doc.append(NoEscape(r'$%s$' % gen.eq(101, 1)))
                        else:
                            doc.append(NoEscape(r'$%s$' % gen.eq(101, random.choice([2, 3]))))
                    elif x < n * 3 // 4:
                        doc.append(NoEscape(r'$%s$' % gen.eq(102, random.choice([2, 3]))))
                    else:
                        doc.append(NoEscape(r'$%s$' % gen.eq(random.choice([101, 102]), 3)))
                    space(doc, "0.7cm")
                end(doc, "multicols")
                end(doc, 'parts')
                space(doc, "0.7cm")

            if qcompletes:
                n = qcompletes
                question(doc, f"{n}")
                doc.append("Resol les següents equacions de segon grau (completes).")
                begin(doc, 'parts')
                begin(doc, "multicols", "3")
                for x in range(0, n):
                    part(doc)
                    if x < n // 4:
                        doc.append(NoEscape(r'$%s$' % gen.eq(103, 1)))
                    elif x < n * 3 // 4:
                        doc.append(NoEscape(r'$%s$' % gen.eq(103, 2)))
                    else:
                        doc.append(NoEscape(r'$%s$' % gen.eq(103, random.choice([2, 3]))))
                    space(doc, "1.4cm")
                end(doc, "multicols")
                end(doc, 'parts')
                space(doc, "1.4cm")

            if qpolis:
                n = qpolis
                question(doc, f"{2 * n}")
                doc.append("Opera i resol les següents equacions de segon grau (polinòmiques).")
                begin(doc, 'parts')
                begin(doc, "multicols", "2")
                for x in range(0, n):
                    part(doc)
                    doc.append(NoEscape(r'$%s$' % gen.eq(104)))
                    space(doc, "1.4cm")
                end(doc, "multicols")
                end(doc, 'parts')
                space(doc, "1.4cm")

            if sistemes:
                bloctitle(doc, "Sistemes d'equacions de dues incògnites")

            if qsist != 0:
                n = qsist
                question(doc, f"{n * 2}")
                doc.append("Resol els següents sistemes d'equacions lineals de dues incògnites.")
                begin(doc, 'parts')
                begin(doc, "multicols", "3")
                for x in range(0, n):
                    part(doc)
                    if x < n // 3:
                        doc.append(NoEscape(
                            r'$%s$' % gen.sisteq(1, 1)))  # pels sistemes (per la clau de l'esquerra) cal msmath
                    elif x < 2 * n // 3:
                        doc.append(NoEscape(r'$%s$' % gen.sisteq(1, 2)))
                    else:
                        doc.append(NoEscape(r'$%s$' % gen.sisteq(1, 3)))
                    space(doc, "1.6cm")
                end(doc, "multicols")
                end(doc, 'parts')
                space(doc, "1.6cm")

            if sistemes3:
                bloctitle(doc, "Sistemes d'equacions de tres incògnites")

            if qsist3 != 0:
                n = qsist3
                question(doc, f"{n * 5}")
                doc.append("Resol els següents sistemes d'equacions lineals de dues incògnites.")
                begin(doc, 'parts')
                begin(doc, "multicols", "3")
                for x in range(0, n):
                    part(doc)
                    if x < n // 4 or n == 0:
                        doc.append(NoEscape(r'$%s$' % gen.sisteq(101, 1)))  # escalonat, x a dalt
                    elif x < n // 3:
                        doc.append(NoEscape(r'$%s$' % gen.sisteq(101, 2)))  # escalonat, x on sigui
                    elif x < 2 * n // 3:
                        doc.append(NoEscape(r'$%s$' % gen.sisteq(101, 3)))  # un coeficient 1
                    else:
                        doc.append(NoEscape(r'$%s$' % gen.sisteq(101, 4)))  # com sigui
                    space(doc, "0.5cm")
                end(doc, "multicols")
                end(doc, 'parts')

            end(doc, 'questions')
        else:
            doc.append("Calia tirar-se tanta estona per no posar res? Potser no")
    else:
        doc.append("haha.. quina gràcia.. has fet un pdf sense res, que original...")

    doc.generate_pdf("deuresweb/static/pdfs/" + temallarg(tema))
    print("PDF generat.")

    return


def proporcionalitat(opcions, solucions=False):
    tema = "prop"

    # getting opcions
    curs = opcions["curs"]
    print("Generant pdf: {} ({})".format(temallarg(tema), curs))

    if "simple" in opcions:
        simple = True
        qdirectes = quantesson(opcions["qdirectes"], "directes")
        qinverses = quantesson(opcions["qinverses"], "inverses")
        qbarrejades = quantesson(opcions["qbarrejades"], "barrejades")
    else:
        simple = False
        qdirectes = 0
        qinverses = 0
        qbarrejades = 0
    print(f"S.Directa {qdirectes}, S.Inversa {qinverses}, S. Barrejades {qbarrejades}")

    composta = False

    # PyLaTeX code
    geometry = margins()
    doc = Document(documentclass="exam", geometry_options=geometry)
    doc.packages.append(Package('multicol'))
    doc.packages.append(Package('amsmath'))
    doc.packages.append(Package('alphalph'))

    headfoot(doc, opcions, tema)
    myconfig(doc, solucions)

    doc.append(NoEscape(
        r'\renewcommand{\thepartno}{\alphalph{\value{partno}}}'))  # per permetre doble lletra, 26*26 = 676 apartats max

    # preguntes
    if simple or composta:
        if any([qdirectes, qinverses, qbarrejades]):
            begin(doc, 'questions')

            if simple:
                bloctitle(doc, "Proporcionalitat simple")

            if qdirectes:
                n = qdirectes
                question(doc, f"{n}")
                doc.append("Resol els següents problemes de proporcionalitat directa.")
                begin(doc, 'parts')
                for x in range(0, n):
                    part(doc)
                    doc.append(NoEscape(r'%s' % gen.prop(1, 1)))
                    space(doc, "1cm")
                end(doc, 'parts')

            if qinverses != 0:
                n = qinverses
                question(doc, f"{n}")
                doc.append("Resol els següents problemes de proporcionalitat inversa.")
                begin(doc, 'parts')
                for x in range(0, n):
                    part(doc)
                    doc.append(NoEscape(r'%s' % gen.prop(1, 2)))
                    space(doc, "1cm")
                end(doc, 'parts')

            if qbarrejades != 0:
                n = qbarrejades
                question(doc, f"{n}")
                doc.append("Resol els següents problemes de proporcionalitat simple (directa i inversa).")
                begin(doc, 'parts')
                for x in range(0, n):
                    part(doc)
                    doc.append(NoEscape(r'%s' % gen.prop(1, 3)))
                    space(doc, "1cm")
                end(doc, 'parts')

            end(doc, 'questions')
        else:
            doc.append("Calia tirar-se tanta estona per no posar res? Potser no")
    else:
        doc.append("haha.. quina gràcia.. has fet un pdf sense res, que original...")

    doc.generate_pdf("deuresweb/static/pdfs/" + temallarg(tema))
    print("PDF generat.")

    return


def powsqr(opcions, solucions=False):
    tema = "powsqr"

    # getting opcions
    curs = opcions["curs"]
    print("Generant pdf: {} ({})".format(temallarg(tema), curs))

    if "pot" in opcions:
        pot = True
        qmexp = quantesson(opcions["qmexp"], "p_mexp")
        qmbase = quantesson(opcions["qmbase"], "p_mbase")
    else:
        pot = False
        qmexp = 0
        qmbase = 0
    print(f"Mateix exp {qmexp}, Mateixa base {qmbase}")

    if "sqrt" in opcions:
        sqrt = True
        qarrels = quantesson(opcions["qarrels"], "arrels")
        qearrels = quantesson(opcions["qearrels"], "earrels")
    else:
        pot = False
        qarrels = 0
        qearrels = 0
    print(f"Arrels s/ exp {qearrels}, Arrels amb exp {qmbase}")

    # PyLaTeX code
    geometry = margins()
    doc = Document(documentclass="exam", geometry_options=geometry)
    doc.packages.append(Package('multicol'))
    doc.packages.append(Package('amsmath'))
    doc.packages.append(Package('alphalph'))

    headfoot(doc, opcions, tema)
    myconfig(doc, solucions)

    doc.append(NoEscape(
        r'\renewcommand{\thepartno}{\alphalph{\value{partno}}}'))  # per permetre doble lletra, 26*26 = 676 apartats max

    # preguntes
    if pot or sqrt:
        if any([qmexp, qmbase, qarrels, qearrels]):
            begin(doc, 'questions')

            if pot:
                bloctitle(doc, "Potències")

            if qmexp:
                n = qmexp
                question(doc, f"{n}")
                doc.append("Expressa com un sol exponent.")
                begin(doc, 'parts')
                begin(doc, 'multicols', 3)
                for x in range(0, n):
                    part(doc)
                    if x < (n // 2):
                        doc.append(NoEscape(r'$%s$' % gen.powsqr(1, 1, 2)))
                    else:
                        doc.append(NoEscape(r'$%s$' % gen.powsqr(1, 2, 3)))
                    space(doc, "1cm")
                end(doc, 'multicols')
                end(doc, 'parts')

            if qmbase:
                n = qmbase
                question(doc, f"{n}")
                doc.append("Expressa com un sol exponent.")
                begin(doc, 'parts')
                begin(doc, 'multicols', 3)
                for x in range(0, n):
                    part(doc)
                    if x < (n // 2):
                        doc.append(NoEscape(r'$%s$' % gen.powsqr(2, 1, 2)))
                    else:
                        doc.append(NoEscape(r'$%s$' % gen.powsqr(2, 2, 3)))
                    space(doc, "1cm")
                end(doc, 'multicols')
                end(doc, 'parts')

            if sqrt:
                bloctitle(doc, "Arrels")

            if qarrels:
                n = qarrels
                question(doc, f"{n}")
                doc.append("Expressa com una sola arrel.")
                begin(doc, 'parts')
                begin(doc, 'multicols', 3)
                for x in range(0, n):
                    part(doc)
                    if x < (n // 2):
                        doc.append(NoEscape(r'$%s$' % gen.powsqr(103, 1, 2)))
                    else:
                        doc.append(NoEscape(r'$%s$' % gen.powsqr(103, 1, 3)))
                    space(doc, "1cm")
                end(doc, 'multicols')
                end(doc, 'parts')

            if qearrels:
                n = qearrels
                question(doc, f"{n}")
                doc.append("Expressa com una sola arrel.")
                begin(doc, 'parts')
                begin(doc, 'multicols', 3)
                for x in range(0, n):
                    part(doc)
                    if x < (n // 2):
                        doc.append(NoEscape(r'$%s$' % gen.powsqr(103, 2, 2)))
                    else:
                        doc.append(NoEscape(r'$%s$' % gen.powsqr(103, 2, 3)))
                    space(doc, "1cm")
                end(doc, 'multicols')
                end(doc, 'parts')

            end(doc, 'questions')
        else:
            doc.append("Calia tirar-se tanta estona per no posar res? Potser no")
    else:
        doc.append("haha.. quina gràcia.. has fet un pdf sense res, que original...")

    doc.generate_pdf("deuresweb/static/pdfs/" + temallarg(tema))
    print("PDF generat.")

    return


def successions(opcions, solucions=False):
    tema = "succ"

    # getting opcions
    curs = opcions["curs"]
    print("Generant pdf: {} ({})".format(temallarg(tema), curs))

    if "arit" in opcions:
        arit = True
        qtermen = quantesson(opcions["qtermen"], "termen")
        qdades = quantesson(opcions["qdades"], "dades")
        qextreure = quantesson(opcions["qextreure"], "extreure")
    else:
        arit = False
        qtermen = 0
        qdades = 0
        qextreure = 0

    aGeneral = False
    aAn = False
    aSn = False
    if qextreure:
        if "aGeneral" in opcions:
            aGeneral = True
        if "aAn" in opcions:
            aAn = True
        if "aSn" in opcions:
            aSn = True

    aextron = opcions["aextron"]

    print(
        f"Aritmètiques: Terme n {qtermen}, Dades {qdades}, Extreure {qextreure} (G: {aGeneral} | An: {aAn} | Sn: {aSn})")

    if "geom" in opcions:
        geom = True
        qgtermen = quantesson(opcions["qgtermen"], "gtermen")
        qgdades = quantesson(opcions["qgdades"], "gdades")
        qgextreure = quantesson(opcions["qgextreure"], "gextreure")
    else:
        geom = False
        qgtermen = 0
        qgdades = 0
        qgextreure = 0

    gGeneral = False
    gAn = False
    gSn = False
    if qgextreure:
        if "gGeneral" in opcions:
            gGeneral = True
        if "gAn" in opcions:
            gAn = True
        if "gSn" in opcions:
            gSn = True

    gextron = opcions["gextron"]

    print(
        f"Geomètriques: Terme n {qgtermen}, Dades {qgdades}, Extreure {qgextreure} (G: {gGeneral} | An: {gAn} | Sn: {gSn})")

    barreja = False

    # PyLaTeX code
    geometry = margins()
    doc = Document(documentclass="exam", geometry_options=geometry)
    doc.packages.append(Package('multicol'))
    doc.packages.append(Package('amsmath'))
    doc.packages.append(Package('alphalph'))

    headfoot(doc, opcions, tema)
    myconfig(doc, solucions)

    doc.append(NoEscape(
        r'\renewcommand{\thepartno}{\alphalph{\value{partno}}}'))  # per permetre doble lletra, 26*26 = 676 apartats max

    # preguntes
    if arit or geom or barreja:
        if any([qtermen, qdades, qextreure, qgtermen, qgdades, qgextreure]):
            begin(doc, 'questions')

            # Aritmètiques
            if arit:
                bloctitle(doc, "Successions aritmètiques")

            if qtermen:
                n = qtermen
                question(doc, f"{n}")
                doc.append("Exercicis de trobar el terme n:")
                begin(doc, 'parts')
                for x in range(0, n):
                    part(doc)
                    doc.append(
                        NoEscape(r'%s' % gen.success(1, min(x // (n // 2) + 1, 2))))  # segona meitat un pèl més alts
                    space(doc, "1cm")
                end(doc, 'parts')

            if qdades:
                n = qdades
                question(doc, f"{2 * n}")
                doc.append("Exercicis de trobar la dada que falta:")
                begin(doc, 'parts')
                for x in range(0, n):
                    part(doc)
                    doc.append(NoEscape(r'%s' % gen.success(1, min(x // (n // 2) + 3, 4))))  # nivells 3 i 4
                    space(doc, "1.05cm")
                end(doc, 'parts')

            if qextreure:
                n = qextreure
                question(doc, f"{3 * n}")
                if aextron == "alhora" or aextron == "seguit":
                    t = "Calcula"
                    if aGeneral:
                        t += " el terme general"
                        if aAn or aSn:
                            if aAn and aSn:
                                t += ","
                            else:
                                if aextron == "alhora":
                                    t += " i"
                                else:
                                    t += " o"
                    if aAn:
                        t += " el terme $A_n$"
                        if aextron == "alhora":
                            t += " indicat"
                        if aSn:
                            if aextron == "alhora":
                                t += " i"
                            else:
                                t += " o"
                    if aSn:
                        t += r" la suma dels n primers termes $S_n$"
                        if aextron == "alhora":
                            t += " indicada"
                    if not (aGeneral or aAn or aSn):
                        t += " la diferència (d)"
                    if aextron == "seguit":
                        if (aGeneral and (aAn or aSn)) or (aAn and aSn):
                            t += " segons s'indiqui en cada cas"
                        else:
                            t += " de cada successió"
                    t += "."
                    doc.append(NoEscape(t))

                    avar = []  # per seguit
                    if aGeneral:
                        avar.append(1)
                    if aAn:
                        avar.append(2)
                    if aSn:
                        avar.append(3)

                    if aAn:  # per alhora
                        if aSn:
                            variant = 4
                        else:
                            variant = 2
                    elif aSn:
                        variant = 3
                    else:
                        variant = 1

                    begin(doc, 'parts')
                    begin(doc, "multicols", "2")
                    for x in range(0, n):
                        part(doc)
                        if aextron == "alhora":
                            doc.append(NoEscape(r'$%s$' % gen.success(1, 101, variant)))
                        else:  # seguit
                            # print(x, n, len(avar), n // len(avar), x // (n//len(avar)), avar[min(x // (n//len(avar)), len(avar)-1)])
                            doc.append(NoEscape(
                                r'$%s$' % gen.success(1, 101, avar[min(x // (n // len(avar)), len(avar) - 1)])))
                        space(doc, "1cm")
                    end(doc, "multicols")
                    space(doc, "1cm")
                    end(doc, 'parts')
                else:
                    if aGeneral:
                        doc.append("Calcula el terme general de les següents successions:")
                    elif not (aAn or aSn):
                        doc.append("Calcula la diferència (d) de les següents successions:")
                    if aGeneral or not (aAn or aSn):
                        begin(doc, 'parts')
                        begin(doc, 'multicols', 2)
                        for x in range(0, n):  # TODO ojo els punts totals de l'ex (ajustar)
                            part(doc)
                            doc.append(NoEscape(r'$%s$' % gen.success(1, 101, 1)))
                            space(doc, "1cm")
                        end(doc, 'multicols')
                        space(doc, "1.2cm")
                        end(doc, 'parts')

                    if aAn:
                        doc.append(NoEscape(r"Calcula per a cada successió el terme $a_n$ indicat:"))
                        begin(doc, 'parts')
                        begin(doc, 'multicols', 2)
                        for x in range(0, n):
                            part(doc)
                            doc.append(NoEscape(r'$%s$' % gen.success(1, 101, 2)))
                            space(doc, "1cm")
                        end(doc, 'multicols')
                        space(doc, "1.2cm")
                        end(doc, 'parts')

                    if aSn:
                        doc.append(NoEscape("Calcula per a cada successió la suma dels n primers termes $(S_n)$:"))
                        begin(doc, 'parts')
                        begin(doc, 'multicols', 2)
                        for x in range(0, n):
                            part(doc)
                            doc.append(NoEscape(r'$%s$' % gen.success(1, 101, 3)))
                            space(doc, "1cm")
                        end(doc, 'multicols')
                        space(doc, "1.2cm")
                        end(doc, 'parts')

            # Geomètriques
            if geom:
                bloctitle(doc, "Successions geomètriques")

            if qgtermen:
                n = qgtermen
                question(doc, f"{n}")
                doc.append("Exercicis de trobar el terme n:")
                begin(doc, 'parts')
                for x in range(0, n):
                    part(doc)
                    doc.append(NoEscape(r'%s' % gen.success(2, min(x // (n // 2) + 1, 2))))  # segona meitat un pèl més
                    space(doc, "1cm")
                end(doc, 'parts')

            if qgdades:
                n = qgdades
                question(doc, f"{2 * n}")
                doc.append("Exercicis de trobar la dada que falta:")
                begin(doc, 'parts')
                for x in range(0, n):
                    part(doc)
                    doc.append(NoEscape(r'%s' % gen.success(2, min(x // (n // 2) + 3, 4))))  # nivells 3 i 4
                    space(doc, "1.05cm")
                end(doc, 'parts')

            if qgextreure:
                n = qgextreure
                question(doc, f"{3 * n}")
                if gextron == "alhora" or gextron == "seguit":
                    t = "Calcula"
                    if gGeneral:
                        t += " el terme general"
                        if gAn or gSn:
                            if gAn and gSn:
                                t += ","
                            else:
                                if gextron == "alhora":
                                    t += " i"
                                else:
                                    t += " o"
                    if gAn:
                        t += " el terme $a_n$"
                        if gextron == "alhora":
                            t += " indicat"
                        if gSn:
                            if gextron == "alhora":
                                t += " i"
                            else:
                                t += " o"
                    if gSn:
                        t += r" la suma dels n primers termes $S_n$"
                        if gextron == "alhora":
                            t += " indicada"
                    if not (gGeneral or gAn or gSn):
                        t += " la raó (r)"
                    if gextron == "seguit":
                        if (gGeneral and (gAn or gSn)) or (gAn and gSn):  # si hi ha dues preguntes
                            t += " segons s'indiqui en cada cas"
                        else:
                            t += " de cada successió"
                    t += "."
                    doc.append(NoEscape(t))  # NoEscape fa que entrin els $ (i pugui interpretar-ho com inline maths)

                    avar = []  # per seguit
                    if gGeneral:
                        avar.append(1)
                    if gAn:
                        avar.append(2)
                    if gSn:
                        avar.append(3)

                    if gAn:  # per alhora
                        if gSn:
                            variant = 4
                        else:
                            variant = 2
                    elif gSn:
                        variant = 3
                    else:
                        variant = 1

                    begin(doc, 'parts')
                    begin(doc, "multicols", "2")
                    for x in range(0, n):
                        part(doc)
                        if aextron == "alhora":
                            doc.append(NoEscape(r'$%s$' % gen.success(2, 101, variant)))
                        else:  # seguit
                            # print(x, n, len(avar), n // len(avar), x // (n//len(avar)), avar[min(x // (n//len(avar)), len(avar)-1)])
                            doc.append(NoEscape(
                                r'$%s$' % gen.success(2, 101, avar[min(x // (n // len(avar)), len(avar) - 1)])))
                        space(doc, "1cm")
                    end(doc, "multicols")
                    space(doc, "1cm")
                    end(doc, 'parts')
                else:
                    if gGeneral:
                        doc.append("Calcula el terme general de les següents successions:")
                    elif not (gAn or gSn):
                        doc.append("Calcula la raó (r) de les següents successions:")
                    if aGeneral or not (gAn or gSn):
                        begin(doc, 'parts')
                        begin(doc, 'multicols', 2)
                        for x in range(0, n):  # TODO ojo els punts totals de l'ex (ajustar)
                            part(doc)
                            doc.append(NoEscape(r'$%s$' % gen.success(2, 101, 1)))
                            space(doc, "1cm")
                        end(doc, 'multicols')
                        space(doc, "1.2cm")
                        end(doc, 'parts')

                    if gAn:
                        doc.append(NoEscape(r"Calcula per a cada successió el terme $a_n$ indicat:"))
                        begin(doc, 'parts')
                        begin(doc, 'multicols', 2)
                        for x in range(0, n):
                            part(doc)
                            doc.append(NoEscape(r'$%s$' % gen.success(2, 101, 2)))
                            space(doc, "1cm")
                        end(doc, 'multicols')
                        space(doc, "1.2cm")
                        end(doc, 'parts')

                    if gSn:
                        doc.append(NoEscape("Calcula per a cada successió la suma dels n primers termes $(S_n)$:"))
                        begin(doc, 'parts')
                        begin(doc, 'multicols', 2)
                        for x in range(0, n):
                            part(doc)
                            doc.append(NoEscape(r'$%s$' % gen.success(2, 101, 3)))
                            space(doc, "1cm")
                        end(doc, 'multicols')
                        space(doc, "1.2cm")
                        end(doc, 'parts')

            end(doc, 'questions')
        else:
            doc.append("Calia tirar-se tanta estona per no posar res? Potser no")
    else:
        doc.append("haha.. quina gràcia.. as fet un pdf sense res, que original...")

    doc.generate_pdf("deuresweb/static/pdfs/" + temallarg(tema))
    print("PDF generat.")

    return


def derivades(opcions, solucions=False):
    tema = "dx"

    # getting opcions
    curs = opcions["curs"]
    print("Generant pdf: {} ({})".format(temallarg(tema), curs))

    if "rd" in opcions:
        rd = True
        qsimples = quantesson(opcions["qsimples"], "dx_simples")
        qcadena = quantesson(opcions["qcadena"], "dx_cadena")
        qmuldiv = quantesson(opcions["qmuldiv"], "dx_muldiv")
    else:
        rd = False
        qsimples = 0
        qmuldiv = 0
        qcadena = 0

    funcions = []
    for x in range(1, 9):  # 1-8
        if f"fx{x}" in opcions:
            funcions.append(x)
    if len(funcions) == 0:
        funcions = list(range(1, 9))  # 1-8

    print(f"Simples {qsimples}, Muldiv {qmuldiv} Amb Cadena {qcadena} || {funcions}")

    propietats = []
    for x in range(6, 9):  # 6-8 (sum mul div)
        if f"p{x}" in opcions:
            propietats.append(x)
    if len(propietats) == 0:
        propietats = list(range(7, 9))  # 7-8 (mul div)

    # PyLaTeX code
    geometry = margins()
    doc = Document(documentclass="exam", geometry_options=geometry)
    doc.packages.append(Package('multicol'))
    doc.packages.append(Package('amsmath'))
    doc.packages.append(Package('alphalph'))

    headfoot(doc, opcions, tema)
    myconfig(doc, solucions)

    doc.append(NoEscape(
        r'\renewcommand{\thepartno}{\alphalph{\value{partno}}}'))  # per permetre doble lletra, 26*26 = 676 apartats max

    # preguntes
    if rd:  # aquí tots els botons grossos
        if any([qsimples, qmuldiv, qcadena]):  # aquí tots els tipus d'exercici
            begin(doc, 'questions')

            if rd:
                bloctitle(doc, "Regles de Derivació")

            if qsimples:
                n = qsimples
                question(doc, f"{n}")
                doc.append("Resol les següents derivades sense regla de la cadena.")
                begin(doc, 'parts')
                begin(doc, 'multicols', 3)
                for x in range(0, n):
                    part(doc)
                    doc.append(NoEscape(r'$%s$' % gen.dx(1, [1, 2, 3, 4, 5], simples=True)))
                    space(doc, "1cm")
                end(doc, 'multicols')
                end(doc, 'parts')

            if qmuldiv != 0:
                n = qmuldiv
                question(doc, f"{2*n}")
                t = "Deriva les següents "
                if 6 in propietats:
                    t += "sumes"
                    if 7 in propietats and 8 in propietats:
                        t += ", "
                    elif len(propietats) > 1:
                        t += "i "
                if 7 in propietats:
                    if 8 in propietats:
                        t += "multiplicacions i divisions."
                    else:
                        t += "multiplicacions."
                elif 8 in propietats:
                    t += "divisions."
                doc.append(t)

                begin(doc, 'parts')
                begin(doc, 'multicols', 2)
                for x in range(0, n):
                    part(doc)
                    if x < (n // 3):
                        doc.append(NoEscape(r'$%s$' % gen.dx(2, [1, 2, 3, 4, 5, 6, 7, 8],
                                                             simples=True, inici=random.choice(propietats))))
                    else:
                        doc.append(NoEscape(r'$%s$' % gen.dx(3, [1, 2, 3, 4, 5, 6, 7, 8],
                                                             simples=True, inici=random.choice(propietats))))
                    space(doc, "1cm")
                end(doc, 'multicols')
                end(doc, 'parts')

            if qcadena != 0:
                n = qcadena
                question(doc, f"{3*n}")
                doc.append("Resol les següents derivades (amb regla de la cadena).")
                begin(doc, 'parts')
                begin(doc, 'multicols', 2)
                for x in range(0, n):
                    part(doc)
                    if x < (n // 2):
                        doc.append(NoEscape(r'$%s$' % gen.dx(2, funcions)))
                    else:
                        doc.append(NoEscape(r'$%s$' % gen.dx(3, funcions)))
                    print("funcions ara és ", funcions)
                    space(doc, "1cm")
                end(doc, 'multicols')
                end(doc, 'parts')

            end(doc, 'questions')
        else:
            doc.append("Calia tirar-se tanta estona per no posar res? Potser no")
    else:
        doc.append("haha.. quina gràcia.. has fet un pdf sense res, que original...")

    doc.generate_pdf("deuresweb/static/pdfs/" + temallarg(tema))
    print("PDF generat.")

    return


# - - - - - - - - - - - - - - - - - - - - - - - - Playground - - - - - - - - - - - - - - - - - - - - - - - - #


def playground(opcions, solucions=False):
    curs = opcions["curs"]
    print(f"Generant pdf d'equacions ({curs})")

    # PyTeX code
    geometry = {"tmargin": "40mm", "lmargin": "15mm", "bmargin": "20mm", "rmargin": "15mm"}
    doc = Document(documentclass="exam", geometry_options=geometry)
    doc.packages.append(Package('multicol'))
    doc.packages.append(Package('amsmath'))

    # header and footer
    doc.preamble.append(Command('pagestyle', "headandfoot"))
    doc.preamble.append(Command('runningheadrule'))
    doc.preamble.append(Command('footrule'))
    doc.preamble.append(Command('firstpageheadrule'))
    doc.preamble.append(NoEscape(
        r"\firstpageheader{}{\hrulefill \\ \bfseries\LARGE Fitxa d'Equacions\\ \large Matemàtiques - %s \scriptsize \\ \hrulefill \\  \small\mdseries fitxa generada automàticament amb Dynamic Deures (quan tinguin codi anirà aquí)}{}" % (
        curs,)))
    doc.preamble.append(NoEscape(r"\runningheader{Mates de %s}{Fitxa d'Equacions}{Dynamic Deures}" % (curs,)))
    doc.preamble.append(NoEscape(r"\footer{Total: \numpoints punts}{Pàgina \thepage /\numpages}{David Ruscalleda}"))

    # titles
    '''
    doc.preamble.append(Command('title', NoEscape(r'\vspace{-1cm}' + f"Exercicis d'Equacions ({curs})" + r'\vspace{-2ex}')))
    doc.preamble.append(Command('author', "Cortesia de Dynamic Deures"))
    doc.preamble.append(Command('date', NoEscape(r'\vspace{-5ex}')))
    doc.append(NoEscape(r'\maketitle'))
    '''

    # doc.append(Command("hrulefill"))

    # myconfig
    doc.append(NoEscape(r'\pointpoints{punt}{punts}'))
    doc.append(NoEscape(r'\bracketedpoints'))
    doc.append(NoEscape(r'\addpoints'))
    doc.append(NoEscape(r'\renewcommand{\solutiontitle}{\noindent\textbf{Solució:}\par\noindent}'))
    if solucions:
        doc.append(NoEscape(
            r'\printanswers'))  # Marca les respostes correctes dels multiopció (i m'imagino que altres coses si vull)

    # preguntes
    begin(doc, 'questions')
    question(doc, "10")  # Pregunta que val 10 punts
    doc.append("Quina és la resposta a la vida, a l'univers i a tot?")
    br(doc)
    begin(doc, 'oneparcheckboxes')
    choice(doc, '15')
    choice(doc, '35')
    choice(doc, '42', True)
    choice(doc, '1953405938275821')
    end(doc, 'oneparcheckboxes')

    question(doc)  # Pregunta sense punts
    doc.append("Creus que està bé això que has fet?")
    begin(doc, 'parts')

    part(doc, '3')  # Part de pregunta que val 5
    doc.append("Aquesta cosa és una part de la pregunta.")
    space(doc, '1cm')

    part(doc, '7')
    doc.append("Aquesta cosa és una altra part de la pregunta.")
    begin(doc, 'choices')  # choices per ABC vertical, oneparchoices per ABC paral·lel, checkboxes per radio
    choice(doc, "Pernil i coses variades")
    choice(doc, "No tinc gaire gana ara")
    choice(doc, "Però què t'empatolles penjat de la vida")
    choice(doc, "Potser que posis cometes en lloc d'apòstrofs si vols sobreviure")
    end(doc, 'choices')
    space(doc, '1cm')

    part(doc)
    doc.append("Aquesta no puntua.")
    space(doc, '1cm')
    begin(doc, 'solution', '2cm')
    doc.append("Perquè evidentment, si te la dono solucionada no et donaré punts per fer-la.")
    end(doc, 'solution')

    part(doc)
    doc.append(NoEscape(r"A viam si deixa espai... Ah mira, \fillin[Sí] que n'ha deixat"))
    end(doc, 'parts')

    question(doc, NoEscape(r"12034\half"))
    doc.append("Sí que val punts aquesta cosa maremeva. Explica'm per què")
    lines(doc, '2cm')

    question(doc, "20")
    doc.append("Resol les següents equacions de primer grau.")
    begin(doc, 'parts')
    begin(doc, "multicols", "2")
    for x in range(0, 8):
        part(doc)
        doc.append(NoEscape(r'%s' % gen.eq(2, 1)))
        space(doc, "1cm")
    end(doc, "multicols")
    end(doc, 'parts')

    question(doc, "20")  # pels sistemes (per la clau de l'esquerra) cal msmath
    doc.append("Resol aquests sistemes d'equacions de dues incògnites.")
    begin(doc, 'parts')
    begin(doc, "multicols", "3")
    for x in range(0, 9):
        part(doc)
        doc.append(NoEscape(r'$%s$' % gen.sisteq(1, (x // 3) + 1)))
        space(doc, "1cm")
    end(doc, "multicols")
    end(doc, 'parts')

    question(doc, "42")  # pels sistemes (per la clau de l'esquerra) cal msmath
    doc.append("Mira quines operacions apilades més maques.")
    begin(doc, 'parts')
    begin(doc, "multicols", "4")

    text = NoEscape(
        r'\begin{array}{c}\phantom{\times99}384\\ \underline{\times\phantom{999}56}\\ \phantom{\times9}2304\\ \underline{\phantom\times1920\phantom9}\\ \phantom\times21504 \end{array}')
    part(doc)
    doc.append(NoEscape(fr'${text}$'))
    space(doc, "1cm")

    part(doc)
    doc.append(NoEscape(fr'Si vols demostrat com la a, \\ hi ha el paq xlop que ho fa sol'))
    space(doc, "1cm")
    for x in range(0, 12):
        part(doc)
        doc.append(NoEscape(r'${%s}$' % (gen.apilades(3, [(x // 3) + 1, (x % 3) + 1]))))
        space(doc, "1cm")

    end(doc, "multicols")
    end(doc, 'parts')

    end(doc, 'questions')

    for x in range(0, 10):
        doc.append("Bon dia catalunya són les 16:30")
        space(doc, "5cm")

    doc.generate_pdf("deuresweb/static/pdfs/successions")
    print("PDF generat.")

    return


# - - - - - - - - - - - - - - - - - - - - - - - - Old Test #1 - - - - - - - - - - - - - - - - - - - - - - - - #

def old_equacions(opcions):
    curs = opcions["curs"]
    print(f"Generant pdf d'equacions ({curs})")

    # PyTeX code
    geometry = {"tmargin": "10mm", "lmargin": "25mm", "bmargin": "20mm", "rmargin": "25mm"}
    doc = Document(geometry_options=geometry)

    # titles
    doc.preamble.append(
        Command('title', NoEscape(r'\vspace{-1cm}' + f"Exercicis d'Equacions ({curs})" + r'\vspace{-2ex}')))
    doc.preamble.append(Command('author', "Cortesia de Dynamic Deures"))
    doc.preamble.append(Command('date', NoEscape(r'\vspace{-5ex}')))
    doc.append(NoEscape(r'\maketitle'))

    doc.append(Command("hrulefill"))

    title = "Equacions de primer grau"
    text = "Aquí aniran les equacions "
    with doc.create(Section(title)):
        doc.append(text)
        doc.append(curs)
        doc.append(Math(data=['2*3', '=', '6x']))

        with doc.create(Tabular('l|l')) as table:  # l = left, c = centered, r = right, | = barra
            table.add_row((1, 2))
            table.add_empty_row()
            table.add_row((3, 4))

    doc.generate_pdf("deuresweb/pdfs/equacions")
    print("PDF generat.")

    return


# *********************** Functions ************************* #


def temallarg(tema="no"):
    if tema == "eq":
        return "equacions"
    elif tema == "comb":
        return "combinades"
    elif tema == "api":
        return "apilades"
    elif tema == "powsqr":
        return "powsqr"
    elif tema == "prop":
        return "proporcionalitat"
    elif tema == "succ":
        return "successions"
    elif tema == "dx":
        return "derivades"
    else:
        return tema


def tematitol(tema="no"):
    if tema == "eq":
        return "d'Equacions"
    elif tema == "comb":
        return "d'Operacions amb Enters"
    elif tema == "api":
        return "d'Operacions amb Més Xifres"
    elif tema == "powsqr":
        return "de Potències i Arrels"
    elif tema == "prop":
        return "de Proporcionalitat"
    elif tema == "succ":
        return "de Successions"
    elif tema == "dx":
        return "de Derivades"
    elif tema == "no":
        return "de Qui sap què"
    else:
        return "de " + tema


def quantesson(value, op):
    n = ["no", "poques", "normal", "moltes", "mitja", "plana", "doble"].index(value)
    print(op, value)
    # enters
    if op == "sumes":
        quantitats = [0, 8, 20, 32, 48, 112, 200]
    elif op == "psumes":
        quantitats = [0, 9, 18, 27, 42, 87, 174]
    elif op in ["multis", "divis"]:
        quantitats = [0, 8, 20, 32, 48, 104, 200]
    elif op in ["smultis", "sdivis"]:
        quantitats = [0, 8, 15, 27, 42, 87, 174]
    # més xifres
    elif op == "v_sumes":
        quantitats = [0, 4, 8, 12, 16, 35, 64]
    elif op == "v_dsumes":
        quantitats = [0, 4, 8, 12, 16, 35, 64]
    elif op == "v_restes":
        quantitats = [0, 4, 8, 12, 16, 35, 64]
    elif op == "v_drestes":
        quantitats = [0, 4, 8, 12, 16, 35, 64]
    elif op == "v_multis":
        quantitats = [0, 3, 6, 9, 12, 28, 64]
    elif op == "v_dmultis":
        quantitats = [0, 3, 6, 9, 12, 24, 64]
    # potències i arrels
    elif op in ["p_mexp", "p_mbase" ,"arrels", "earrels"]:
        quantitats = [0, 6, 9, 12, 18, 39, 81]
    # equacions
    elif op in ["simples", "dsimples"]:
        quantitats = [0, 8, 12, 26, 42, 86, 174]  # arrodonit avall per evitar migpunts
    elif op == "incomps":
        quantitats = [0, 8, 12, 20, 25, 50, 100]
    elif op == "completes":
        quantitats = [0, 6, 9, 15, 20, 33, 66]
    elif op == "polis":
        quantitats = [0, 4, 6, 10, 14, 22, 44]
    elif op == "sistemes":
        quantitats = [0, 3, 6, 9, 12, 21, 45]
    elif op == "sistemes3":
        quantitats = [0, 3, 6, 9, 12, 27, 56]
    # proporcionalitat
    elif op == "directes":
        quantitats = [0, 3, 4, 5, 6, 12, 25]
    elif op == "inverses":
        quantitats = [0, 3, 4, 5, 6, 11, 22]
    elif op == "barrejades":
        quantitats = [0, 3, 4, 5, 6, 11, 23]
    # successions
    elif op in ["termen", "gtermen"]:
        quantitats = [0, 3, 5, 6, 6, 13, 27]
    elif op in ["dades", "gdades"]:
        quantitats = [0, 3, 5, 7, 7, 14, 27]
    elif op in ["extreure", "gextreure"]:
        quantitats = [0, 3, 4, 8, 12, 29, 56]
    # derivades
    elif op == "dx_simples":
        quantitats = [0, 6, 9, 12, 18, 39, 81]
    elif op in ["dx_cadena", "dx_muldiv"]:
        quantitats = [0, 4, 6, 8, 12, 26, 54]
    else:
        quantitats = [0, 8, 20, 32, 48, 112, 200]
        print("no he trobat el codi")
    return quantitats[n]


# *************************** Common Blocks ******************************* #

def margins():
    return {"tmargin": "40mm", "lmargin": "15mm", "bmargin": "20mm", "rmargin": "15mm"}


def headfoot(doc, opcions, tema="no"):
    tema = tematitol(tema)
    # header and footer
    doc.preamble.append(Command('pagestyle', "headandfoot"))
    doc.preamble.append(Command('runningheadrule'))
    doc.preamble.append(Command('footrule'))
    doc.preamble.append(Command('firstpageheadrule'))
    doc.preamble.append(NoEscape(
        r"\firstpageheader{}{\hrulefill \\ \bfseries\LARGE Fitxa %s\\ \large Matemàtiques - %s \scriptsize \\ \hrulefill \\  \small\mdseries Fitxa generada automàticament amb Dynamic Deures (http://bit.ly/DynamicDeures)}{}" % (
        tema, opcions["curs"],)))
    doc.preamble.append(NoEscape(r"\runningheader{Mates de %s}{Fitxa %s}{Dynamic Deures}" % (opcions["curs"], tema)))
    doc.preamble.append(NoEscape(r"\footer{Total: \numpoints\ punts}{Pàgina \thepage /\numpages}{David Ruscalleda}"))

    return


def myconfig(doc, solucions=False):
    doc.append(NoEscape(r'\pointpoints{punt}{punts}'))
    doc.append(NoEscape(r'\bracketedpoints'))
    doc.append(NoEscape(r'\addpoints'))
    doc.append(NoEscape(r'\renewcommand{\solutiontitle}{\noindent\textbf{Solució:}\par\noindent}'))
    if solucions:
        doc.append(NoEscape(
            r'\printanswers'))  # Marca les respostes correctes dels multiopció i mostra les respostes definides
    return


# ********************* Aliases PyLaTeX **********************#


def begin(doc, tag, extra=""):  # TODO canviar per Command (una instrucció genèrica LaTeX que ja existeix), boig
    if tag == "solution" and not extra == "":
        doc.append(NoEscape(r'\begin{%s}[%s]' % (tag, extra)))
    elif tag == "multicols":
        doc.append(NoEscape(r'\begin{%s}{%s}' % (tag, extra)))
    else:
        doc.append(NoEscape(r'\begin{%s}' % (tag,)))
    return


def end(doc, tag):
    doc.append(NoEscape(r'\end{%s}' % (tag,)))
    return


def space(doc, size):
    doc.append(NoEscape(r'\vspace{%s}' % (size,)))
    return


def stretch(doc, relsize):
    doc.append(NoEscape(r'\vspace{\stretch{%s}}' % (relsize,)))


def lines(doc, size):
    doc.append(NoEscape(r'\fillwithlines{%s}' % (size,)))
    return


def br(doc):
    doc.append(NoEscape(r'\newline'))


def pagebreak(doc, priority="4"):
    doc.append(NoEscape(r'\pagebreak[%s]' % (priority)))


def bloctitle(doc, text):
    doc.append(Command("fullwidth", NoEscape(r"\bfseries \large %s" % (text,))))


def part(doc, punts=""):
    if punts == "":
        doc.append(NoEscape(r'\part'))
    else:
        doc.append(NoEscape(r'\part[%s]' % (punts,)))
    return


def question(doc, punts=""):
    if punts == "":
        doc.append(NoEscape(r'\question'))
    else:
        doc.append(NoEscape(r'\question[%s]' % (punts,)))
    return


def choice(doc, text, corregir=False):
    if corregir:
        doc.append(NoEscape(r'\CorrectChoice %s' % (text,)))
    else:
        doc.append(NoEscape(r'\choice %s' % (text,)))
    return


def uncalcul(doc, quin=[1, 1], sp="0.7cm"):  # op és llista d'opcions del generador
    part(doc)
    doc.append(NoEscape(r'$%s$' % gen.comb(*quin)))  # asterisc separa la llista i els envia individualment
    space(doc, sp)

    return
