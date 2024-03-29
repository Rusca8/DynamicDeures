import random

from pylatex import Document, Section
from pylatex import Command, NoEscape, Math, Tabular, Package
from rpylatex import (begin, end, part, space, lines, br, needspace, bloctitle, question, choice,
                      taulaconfig, obretaula, obrellarga, filataula, tancataula, envt,
                      escriusolus, blocsolus, metasolucions,
                      pre2pkg)
import rpylatex as rpy

import generator as gen
import q_generator as qgen
import exercicitator as mexs  # modular exercicis
import picturator as pic  # imatges
from noms import nom_apartat, nom_tema
import wolframator as w


def exemple(opcions, solucions=False):
    tema = "fex"

    # getting opcions
    curs = opcions["curs"]
    print("Generant pdf: {} ({})".format(temallarg(tema), curs))

    if "apartat1" in opcions:
        apartat1 = True
        qexercici1 = quantesson(opcions["qexercici1"], "exercici1")
        qexercici2 = quantesson(opcions["qexercici2"], "exercici2")
        # ...
        print(f"Exercici 1 {qexercici1}, Exercici 2 {qexercici2} ...")
    else:
        apartat1 = False
        qexercici1 = 0
        qexercici2 = 0
        # ...

    if "apartat2" in opcions:
        apartat2 = True
        # ...
    else:
        apartat2 = False
        # ...

    # PyLaTeX code
    geometry = margins()
    doc = Document(documentclass="exam", geometry_options=geometry)
    doc.packages.append(Package('multicol'))
    doc.packages.append(Package('amsmath'))
    doc.packages.append(Package('alphalph'))
    doc.packages.append(Package('needspace'))  # per arrossegar coses si salta de línia
    # doc.packages.append(Package('graphicx'))  # això és per scalebox (fer les mates més grans)
    # doc.packages.append(Package('hyperref'))  # això és per links (ha de ser l'últim paquet)

    headfoot(doc, opcions, tema)
    myconfig(doc, solucions)

    doc.append(NoEscape(
        r'\renewcommand{\thepartno}{\alphalph{\value{partno}}}'))  # per permetre doble lletra, 26*26 = 676 apartats max

    # preguntes
    if any([apartat1, apartat2]):  # aquí tots els botons grossos
        if any([qexercici1, qexercici2]):  # aquí tots els tipus d'exercici
            begin(doc, 'questions')

            if apartat1:
                needspace(doc, 12)
                bloctitle(doc, "Primer Apartat")

            if qexercici1:
                n = qexercici1
                needspace(doc, 8)
                question(doc, f"{n}")  # puntuació de l'exercici
                doc.append("Resol el següent exercici que va de què sé jo.")
                begin(doc, 'parts')
                begin(doc, 'multicols', 3)  # columnes
                for x in range(0, n):
                    part(doc)
                    text = gen.dx(1, [1, 2, 3, 4, 5], simples=True)  # operació whatever que ve del generator
                    if solucions:
                        doc.append(NoEscape(r'\href{%s}{$%s$}' % (w.urlfor(text, t="dx"), text)))
                    else:
                        doc.append(NoEscape(r'$%s$' % text))
                    space(doc, "1cm")
                end(doc, 'multicols')
                end(doc, 'parts')

            if qexercici2 != 0:
                n = qexercici2
                needspace(doc, 8)
                question(doc, f"{2 * n}")
                doc.append("Resol el següent exercici que va de què sé jo.")
                begin(doc, 'parts')
                begin(doc, 'multicols', 2)
                scale = 1.3  # exemple amb fraccions per engrandir
                for x in range(0, n):
                    part(doc)
                    if solucions:
                        doc.append(NoEscape(r'\href{%s}{\scalebox{%s}{$%s$}}' % (w.urlfor(text, t="dx"), scale, text)))
                    else:
                        doc.append(NoEscape(r'\scalebox{%s}{$%s$}' % (scale, text)))
                    space(doc, "1cm")
                end(doc, 'multicols')
                end(doc, 'parts')

            if apartat2:
                needspace(doc, 12)
                bloctitle(doc, "Segon Apartat")

            # exercicis de l'apartat 2

            end(doc, 'questions')
        else:
            doc.append("Calia tirar-se tanta estona per no posar res? Potser no")
    else:
        doc.append("haha.. quina gràcia.. has fet un pdf sense res, que original...")

    doc.generate_pdf("deuresweb/static/pdfs/" + temallarg(tema))
    print("PDF generat.")

    return


def combinades(opcions, solucions=False):  # - - - - - - - - - - - - - - - - - - - - - COMBINADES
    tema = "comb"

    if opcions["solucions"] == "sí":
        solucions = True

    # getting opcions
    curs = opcions["curs"]
    print("Generant pdf: {} ({})".format(temallarg(tema), curs))

    if "sumes" in opcions:
        sumes = True
        qsumes = quantesson(opcions["qsumes"], "sumes")
        fpos = quantesvariant(opcions["fpos"])
        qpsumes = quantesson(opcions["qpsumes"], "psumes")
        noneg = quantesvariant(opcions["noneg"])
        print(f"A+B = {qsumes}, A+(+B) = {qpsumes}")
    else:
        sumes = False
        qsumes = 0
        qpsumes = 0

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
        nonegm = quantesvariant(opcions["nonegm"])
        print(f"A*B = {qmultis}, A*(-B) = {qsmultis}")
    else:
        multis = False
        qmultis = 0
        qsmultis = 0

    if "divisions" in opcions:
        divis = True
        qdivis = quantesson(opcions["qdivis"], "divis")
        qsdivis = quantesson(opcions["qsdivis"], "sdivis")
        dtaules = []
        if multis and opcions["copymult"] == "com":  # si estic copiant les multis, copio les taules i quantitats
            dtaules = taules
            qdivis = qmultis
            qsdivis = qsmultis
        else:
            for x in range(1, 13):
                if f"td{x}" in opcions:
                    dtaules.append(x)
            if len(dtaules) == 0:
                dtaules = list(range(1, 11))
        print("D.Taules: ", dtaules)
        nonegd = quantesvariant(opcions["nonegd"])
        print(f"A/B = {qdivis}, A/(-B) = {qsdivis}")
    else:
        divis = False
        qdivis = 0
        qsdivis = 0

    if "combinades" in opcions:
        combis = True
        qcombis = quantesson(opcions["qcombis"], "combis")
        ops = [1, 2, 3]
        if "op4" in opcions:
            ops += [4]
        if "op5" in opcions:
            ops += [5]
        print(f"combis = {qcombis}")
    else:
        print("eis")
        combis = False
        qcombis = 0

    # PyLaTeX code
    geometry = margins()
    doc = Document(documentclass="exam", geometry_options=geometry)
    doc.packages.append(Package('multicol'))
    doc.packages.append(Package('alphalph'))  # per permetre aa bb cc
    doc.packages.append(Package('needspace'))

    headfoot(doc, opcions, tema)
    myconfig(doc, solucions)

    # doc.append(NoEscape(r'\renewcommand{\partlabel}{\thepartno)}')) # canvia l'embolcall del número d'apartat
    doc.append(NoEscape(
        r'\renewcommand{\thepartno}{\alphalph{\value{partno}}}'))  # per permetre doble lletra, 26*26 = 676 apartats max

    # preguntes
    if any([sumes, multis, divis, combis]):
        if any([qsumes, qpsumes,
                qmultis, qsmultis,
                qdivis, qsdivis,
                qcombis]):
            begin(doc, 'questions')

            if sumes:
                needspace(doc, 12)
                bloctitle(doc, "Sumes i restes amb enters")

            if qsumes != 0:
                n = qsumes
                needspace(doc, 8)
                question(doc, f"{n // 4}")
                doc.append("Calcula les següents sumes i restes sense parèntesis.")
                var = (n * fpos) // 4  # quantitat de punts amb la variant
                begin(doc, 'parts')
                begin(doc, "multicols", "4")
                for x in range(n):
                    if x < var:
                        uncalcul(doc, [1, 1], "0.2cm")  # resultat positiu (proporció escollida)
                    elif x < (n + var) // 2:
                        uncalcul(doc, [1, 2], "0.2cm")  # a positiva (meitat de la resta
                    else:
                        uncalcul(doc, [1, 3], "0.2cm")  # normal
                end(doc, "multicols")
                end(doc, 'parts')

            if qpsumes:
                n = qpsumes
                needspace(doc, 8)
                question(doc, f"{n // 2}")
                doc.append("Calcula les següents sumes i restes amb parèntesis.")
                var = (n * noneg) // 4  # quantitat de punts amb la variant
                begin(doc, 'parts')
                begin(doc, "multicols", "3")
                for x in range(n):
                    if x < var:
                        uncalcul(doc, [2, 1], "0.2cm")  # sense doble neg
                    elif x < (n + var) // 2:
                        uncalcul(doc, [2, 2], "0.2cm")  # a positiva
                    else:
                        uncalcul(doc, [2, 3], "0.2cm")  # normal
                end(doc, "multicols")
                end(doc, 'parts')

            if multis or divis:
                needspace(doc, 12)
                if multis and divis:
                    bTitle = "Multiplicacions i divisions amb enters"
                elif multis:
                    bTitle = "Multiplicacions amb enters"
                else:
                    bTitle = "Divisions amb enters"
                bloctitle(doc, bTitle)

            if qmultis or qdivis:
                needspace(doc, 8)
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

            if qsmultis != 0 or qsdivis != 0:
                needspace(doc, 10)
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

                    if qsmultis:
                        n = qsmultis
                        var = (n * nonegm) // 4
                    else:
                        n = qsdivis
                        var = (n * nonegd) // 4

                    for x in range(n):
                        if x < var:
                            if qsmultis and not qsdivis:
                                uncalcul(doc, [3, 2], "0,2cm")  # mult
                            elif qsdivis and not qsmultis:
                                uncalcul(doc, [3, 5], "0,2cm")  # div
                            else:
                                uncalcul(doc, [3, random.choice([2, 5])], "0,2cm")  # mult i div
                        else:
                            if qsmultis and not qsdivis:
                                uncalcul(doc, [3, 3], "0,2cm")  # mult
                            elif qsdivis and not qsmultis:
                                uncalcul(doc, [3, 6], "0,2cm")  # div
                            else:
                                uncalcul(doc, [3, random.choice([3, 6])], "0,2cm")  # mult i div

                    end(doc, "multicols")
                    end(doc, 'parts')

            if combis:
                needspace(doc, 12)
                bloctitle(doc, "Operacions combinades")

            if qcombis:
                n = qcombis
                question(doc, f"{n}")
                doc.append("Calcula les següents operacions combinades.")
                begin(doc, 'parts')
                begin(doc, 'multicols', "2")
                solcombis = []
                for x in range((n * 2) // 3):
                    part(doc)
                    solcombis.append(random.randint(-10, 20))
                    if x < n // 3:
                        doc.append(NoEscape(r'$%s$' % gen.mixcomb(solcombis[-1], 2, doblesigne=False, ops=ops)))
                    else:
                        doc.append(NoEscape(r'$%s$' % gen.mixcomb(solcombis[-1], 2, doblesigne=True, ops=ops)))
                    space(doc, "1cm")
                end(doc, "multicols")
                space(doc, "0.5cm")
                for x in range(n - ((n * 2) // 3)):
                    part(doc)
                    solcombis.append(random.randint(-10, 20))
                    if x < n // 6:
                        doc.append(NoEscape(r'$%s$' % gen.mixcomb(solcombis[-1], 3, doblesigne=False, ops=ops)))
                    else:
                        doc.append(NoEscape(r'$%s$' % gen.mixcomb(solcombis[-1], 3, doblesigne=True, ops=ops)))
                    space(doc, "1cm")
                end(doc, 'parts')
                blocsolus(doc, solucions, solcombis)

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

    if "divisions" in opcions:
        divis = True
        qdivis = quantesson(opcions["qdivis"], "v_divis")
        qddivis = quantesson(opcions["qddivis"], "v_ddivis")

        # sense decimals
        ddalt = []
        for n in range(6, 1, -1):  # l'últim no el fa
            if f"ddalt{n}" in opcions:
                ddalt.append(n)
        if not ddalt:
            ddalt = [5, 4, 3, 2]  # si no hay arqueólogos me lo invento

        dbaix = []
        for n in range(4, 0, -1):  # l'últim no el fa
            if f"dbaix{n}" in opcions:
                dbaix.append(n)
        if not dbaix:
            dbaix = [2, 1]

        # amb decimals
        dddalt = []
        for n in range(6, 1, -1):  # l'últim no el fa
            if f"dddalt{n}" in opcions:
                dddalt.append(n)
        if not dddalt:
            dddalt = [4, 3, 2]

        ddecidalt = []
        for n in range(0, 3):  # l'últim no el fa
            if f"ddecidalt{n}" in opcions:
                ddecidalt.append(n)
        if not ddecidalt:
            ddecidalt = [1, 2]

        ddbaix = []
        for n in range(4, 0, -1):  # l'últim no el fa
            if f"ddbaix{n}" in opcions:
                ddbaix.append(n)
        if not ddbaix:
            ddbaix = [1]

        ddecibaix = []
        for n in range(0, 3):  # l'últim no el fa
            if f"ddecibaix{n}" in opcions:
                ddecibaix.append(n)
        if not ddecibaix:
            ddecibaix = [1]

        print(ddecidalt, ddecibaix)

    else:
        divis = False
        qdivis = 0
        qddivis = 0
    print(f"42/42 {qdivis} 4.2/4.2 {qddivis}")

    scale = 1.3  # per si me l'oblido

    # PyLaTeX code
    geometry = margins()
    doc = Document(documentclass="exam", geometry_options=geometry)
    doc.packages.append(Package('multicol'))
    doc.packages.append(Package('amsmath'))
    doc.packages.append(Package('alphalph'))
    doc.packages.append(Package('needspace'))
    doc.packages.append(Package('graphicx'))

    headfoot(doc, opcions, tema)
    myconfig(doc, solucions)

    doc.append(NoEscape(
        r'\renewcommand{\thepartno}{\alphalph{\value{partno}}}'))  # per permetre doble lletra, 26*26 = 676 apartats max

    # preguntes
    if sumes or restes or multis or divis:  # aquí van totes les grans
        if any([qsumes, qdsumes, qrestes, qdrestes, qmultis, qdmultis, qdivis, qddivis]):  # aquí van totes les petites
            begin(doc, 'questions')

            if sumes:
                needspace(doc, 12)
                bloctitle(doc, "Sumes")

            if qsumes:
                n = qsumes
                needspace(doc, 8)
                question(doc, f"{n}")
                doc.append("Resol les següents sumes apilades (sense decimals).")
                begin(doc, 'parts')
                begin(doc, "multicols", "4")
                scale = 1.3
                for x in range(0, n):
                    part(doc)
                    a = random.choice(sdalt)
                    b = random.choice(sbaix)
                    doc.append(NoEscape(r'\scalebox{%s}{$%s$}' % (scale, gen.apilades(1, 1, [a, b]))))
                    space(doc, "1cm")
                end(doc, "multicols")
                end(doc, 'parts')
                space(doc, "1cm")

            if qdsumes:
                n = qdsumes
                needspace(doc, 8)
                question(doc, f"{2 * n}")
                doc.append("Resol les següents sumes apilades (amb decimals).")
                begin(doc, 'parts')
                begin(doc, "multicols", "4")
                scale = 1.3
                for x in range(0, n):
                    part(doc)
                    a = random.choice(sddalt)
                    b = random.choice(sdbaix)
                    c = random.choice(sdecidalt)
                    d = random.choice(sdecibaix)
                    doc.append(NoEscape(r'\scalebox{%s}{$%s$}' % (scale, gen.apilades(1, 2, [a, b], [c, d]))))
                    space(doc, "1cm")
                end(doc, "multicols")
                end(doc, 'parts')
                space(doc, "1cm")

            if restes:
                needspace(doc, 12)
                bloctitle(doc, "Restes")

            if qrestes:
                n = qrestes
                needspace(doc, 8)
                question(doc, f"{n}")
                doc.append("Resol les següents restes apilades (sense decimals).")
                begin(doc, 'parts')
                begin(doc, "multicols", "4")
                scale = 1.3
                for x in range(0, n):
                    part(doc)
                    a = random.choice(rdalt)
                    b = random.choice(rbaix)
                    doc.append(NoEscape(r'\scalebox{%s}{$%s$}' % (scale, gen.apilades(2, x // n + 1, [a, b]))))
                    space(doc, "1cm")
                end(doc, "multicols")
                end(doc, 'parts')
                space(doc, "1cm")

            if qdrestes:
                n = qdrestes
                needspace(doc, 8)
                question(doc, f"{2 * n}")
                doc.append("Resol les següents restes apilades (amb decimals).")
                begin(doc, 'parts')
                begin(doc, "multicols", "4")
                scale = 1.3
                for x in range(0, n):
                    part(doc)
                    a = random.choice(rddalt)
                    b = random.choice(rdbaix)
                    c = random.choice(rdecidalt)
                    d = random.choice(rdecibaix)
                    doc.append(NoEscape(r'\scalebox{%s}{$%s$}' % (scale, gen.apilades(2, 3, [a, b], [c, d]))))
                    space(doc, "1cm")
                end(doc, "multicols")
                end(doc, 'parts')
                space(doc, "1cm")

            if multis:
                needspace(doc, 12)
                bloctitle(doc, "Multiplicacions")

            if qmultis:
                n = qmultis
                needspace(doc, 8)
                question(doc, f"{n}")
                doc.append("Resol les següents multiplicacions apilades (sense decimals).")
                begin(doc, 'parts')
                begin(doc, "multicols", "4")
                scale = 1.3
                for x in range(0, n):
                    part(doc)
                    a = random.choice(mdalt)
                    b = random.choice(mbaix)
                    doc.append(NoEscape(r'\scalebox{%s}{$%s$}' % (scale, gen.apilades(3, 1, [a, b]))))
                    space(doc, "1.6cm")
                end(doc, "multicols")
                end(doc, 'parts')
                space(doc, "1.6cm")

            if qdmultis:
                n = qdmultis
                needspace(doc, 8)
                question(doc, f"{2 * n}")
                doc.append("Resol les següents multiplicacions apilades (amb decimals).")
                begin(doc, 'parts')
                begin(doc, "multicols", "4")
                scale = 1.3
                for x in range(0, n):
                    part(doc)
                    a = random.choice(mddalt)
                    b = random.choice(mbaix)
                    c = random.choice(mdecidalt)
                    d = random.choice(mdecibaix)
                    doc.append(NoEscape(r'\scalebox{%s}{$%s$}' % (scale, gen.apilades(3, 2, [a, b], [c, d]))))
                    space(doc, "2.1cm")
                end(doc, "multicols")
                end(doc, 'parts')
                space(doc, "2.1cm")

            if divis:
                needspace(doc, 12)
                bloctitle(doc, "Divisions")

            if qdivis:
                n = qdivis
                needspace(doc, 8)
                question(doc, f"{n}")
                doc.append("Resol les següents divisions (sense decimals).")
                begin(doc, 'parts')
                begin(doc, "multicols", "3")
                scale = 1.3
                for x in range(0, n):
                    part(doc)
                    a = random.choice(ddalt)
                    b = random.choice(dbaix)
                    doc.append(NoEscape(r'\scalebox{%s}{$%s$}' % (scale, gen.apilades(4, 1, [a, b]))))
                    space(doc, "1.6cm")
                end(doc, "multicols")
                end(doc, 'parts')
                space(doc, "1.6cm")

            if qddivis:
                n = qddivis
                needspace(doc, 8)
                question(doc, f"{2 * n}")
                doc.append("Resol les següents divisions (amb decimals).")
                begin(doc, 'parts')
                begin(doc, "multicols", "3")
                scale = 1.3
                for x in range(0, n):
                    part(doc)
                    a = random.choice(dddalt)
                    b = random.choice(ddbaix)
                    c = random.choice(ddecidalt)
                    d = random.choice(ddecibaix)
                    doc.append(NoEscape(r'\scalebox{%s}{$%s$}' % (scale, gen.apilades(4, 2, [a, b], [c, d]))))
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
    doc.packages.append(Package('needspace'))

    headfoot(doc, opcions, tema)
    myconfig(doc, solucions)

    doc.append(NoEscape(
        r'\renewcommand{\thepartno}{\alphalph{\value{partno}}}'))  # per permetre doble lletra, 26*26 = 676 apartats max

    # preguntes
    if simple or composta:
        if any([qdirectes, qinverses, qbarrejades]):
            begin(doc, 'questions')

            if simple:
                needspace(doc, 12)
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
        metermes = []
        for x in range(2, 6):
            if f"metermes{x}" in opcions:
                metermes.append(x)
        if not metermes:
            metermes = [2, 3]
        if 2 not in metermes and 3 not in metermes:
            qmexp = quantesson(opcions["qmexp"], "p_mexp_45")
        else:
            qmexp = quantesson(opcions["qmexp"], "p_mexp")

        mbtermes = []
        for x in range(2, 6):
            if f"mbtermes{x}" in opcions:
                mbtermes.append(x)
        if not mbtermes:
            mbtermes = [2, 3]
        if 2 not in mbtermes and 3 not in mbtermes or 5 in mbtermes:
            qmbase = quantesson(opcions["qmbase"], "p_mbase_45")
        else:
            qmbase = quantesson(opcions["qmbase"], "p_mbase")

        qfrac = quantesson(opcions["qfrac"], "p_frac")
        fmbase = quantesvariant(opcions["fmbase"])
        qffrac = quantesson(opcions["qffrac"], "p_ffrac")
        fsexp = quantesvariant(opcions["fsexp"])
        qdfrac = quantesson(opcions["qdfrac"], "p_dfrac")
        print(f"Mateix exp {qmexp} ({metermes}), Mateixa base {qmbase} ({mbtermes})")
        print(f"Frac primers {qfrac}, Frac compost {qffrac}, Frac decimals {qdfrac}")
    else:
        pot = False
        qmexp = 0
        qmbase = 0
        qfrac = 0
        qffrac = 0
        qdfrac = 0

    if "sqrt" in opcions:
        sqrt = True
        asexp = quantesvariant(opcions["asexp"])
        atermes = []
        for x in range(2, 6):
            if f"atermes{x}" in opcions:
                atermes.append(x)
        if not atermes:
            atermes = [2, 3]
        if 2 not in atermes and 3 not in atermes:
            qarrels = quantesson(opcions["qarrels"], "arrels_45")
        else:
            qarrels = quantesson(opcions["qarrels"], "arrels")

        qcombradi = quantesson(opcions["qcombradi"], "combradi")
        einter = quantesvariant(opcions["einter"])

        qextreure = quantesson(opcions["qextreure"], "a_extreure")
        if "123" in opcions:
            if "abc" in opcions:
                lletres = 1
            else:
                lletres = 0
        else:
            if "abc" in opcions:
                lletres = 2
            else:
                lletres = 1
        fquad = quantesvariant(opcions["fquad"])

        qintrod = quantesson(opcions["qintrod"], "a_introd")
        if "i123" in opcions:
            if "iabc" in opcions:
                illetres = 1
            else:
                illetres = 0
        else:
            if "iabc" in opcions:
                illetres = 2
            else:
                illetres = 1
        iquad = quantesvariant(opcions["iquad"])

        qfextreure = quantesson(opcions["qfextreure"], "fextreure")
        ffquad = quantesvariant(opcions["ffquad"])

        qasum = quantesson(opcions["qasum"], "asum")
        scoef = quantesvariant(opcions["scoef"])

        qracions = quantesson(opcions["qracions"], "racions")
        if "ra" in opcions:
            ra = True
            if "rab" in opcions:
                rab = True
            else:
                rab = False
        elif "rab" in opcions:
            rab = True
            ra = False
        else:
            ra = True
            rab = True
        rquad = quantesvariant(opcions["rquad"])
        if rab:
            rdoble = quantesvariant(opcions["rdoble"])
        else:
            rdoble = 0
        print(f"Arrels s/ exp {qarrels} ({atermes})")
        print(f"Combinar {qcombradi} ({einter}), extreure {qextreure} ({fquad}), introduir {qintrod} ({iquad}), "
              f"fextreure {qfextreure} ({ffquad})")
        print(f"Sumes d'arrels {qasum} ({scoef}), racional {qracions} [{ra}, {rab}]({rquad}, {rdoble})")
    else:
        sqrt = False
        qarrels = 0
        qcombradi = 0
        qextreure = 0
        qintrod = 0
        qfextreure = 0
        qasum = 0
        qracions = 0


    # PyLaTeX code
    geometry = margins()
    doc = Document(documentclass="exam", geometry_options=geometry)
    doc.packages.append(Package('multicol'))
    doc.packages.append(Package('amsmath'))
    doc.packages.append(Package('alphalph'))
    doc.packages.append(Package('graphicx'))  # això és per scalebox (fer les mates més grans)
    doc.packages.append(Package('needspace'))

    headfoot(doc, opcions, tema)
    myconfig(doc, solucions)

    doc.append(NoEscape(
        r'\renewcommand{\thepartno}{\alphalph{\value{partno}}}'))  # per permetre doble lletra, 26*26 = 676 apartats max

    # preguntes
    if pot or sqrt:
        if any([qmexp, qmbase, qarrels, qfrac, qffrac, qdfrac, qcombradi, qextreure, qfextreure, qasum, qracions,
                qintrod]):
            begin(doc, 'questions')

            if pot:
                needspace(doc, 12)
                bloctitle(doc, "Potències")

            if qmexp:
                n = qmexp
                needspace(doc, 8)
                question(doc, f"{n}")
                doc.append("Expressa com un sol exponent.")
                begin(doc, 'parts')
                if 2 not in metermes and 3 not in metermes:
                    begin(doc, 'multicols', 2)
                else:
                    begin(doc, 'multicols', 3)
                for x in range(0, n):
                    part(doc)
                    doc.append(NoEscape(r'$%s$' % gen.powsqr(1, (2 * x) // n + 1, metermes[(len(metermes) * x) // n])))
                    space(doc, "0.7cm")
                end(doc, 'multicols')
                space(doc, "0.5cm")
                end(doc, 'parts')

            if qmbase:
                n = qmbase
                needspace(doc, 8)
                question(doc, f"{n}")
                doc.append("Expressa com un sol exponent.")
                begin(doc, 'parts')
                if 2 not in mbtermes and 3 not in mbtermes or 5 in mbtermes:
                    begin(doc, 'multicols', 2)
                else:
                    begin(doc, 'multicols', 3)
                for x in range(n):
                    part(doc)  # meitat multi (1) meitat muldiv (2) / macedònia de termes escollida
                    doc.append(NoEscape(r'$%s$' % gen.powsqr(2, (2 * x) // n + 1, mbtermes[(len(mbtermes) * x) // n])))
                    space(doc, "0.7cm")
                end(doc, 'multicols')
                space(doc, "0.5cm")
                end(doc, 'parts')

            if qfrac:
                n = qfrac
                needspace(doc, 8)
                question(doc, f"{n}")
                doc.append("Simplifica les fraccions següents")
                var = (n * fmbase) // 4
                begin(doc, 'parts')
                begin(doc, 'multicols', 3)
                scale = 1.3
                for x in range(n):
                    part(doc)
                    if x < var:
                        if x < var // 2 or x == 0:
                            doc.append(NoEscape(r'\scalebox{%s}{$%s$}' % (scale, gen.powsqr(10, 1, 5))))
                        else:
                            doc.append(NoEscape(r'\scalebox{%s}{$%s$}' % (scale, gen.powsqr(10, 2, 5))))
                    else:
                        if x < (n + var) // 2:
                            doc.append(NoEscape(r'\scalebox{%s}{$%s$}' % (scale, gen.powsqr(10, 3, 5))))
                        else:
                            doc.append(NoEscape(r'\scalebox{%s}{$%s$}' % (scale, gen.powsqr(10, 4, 5))))
                    space(doc, "0.7cm")
                end(doc, 'multicols')
                space(doc, "0.5cm")
                end(doc, 'parts')

            if qffrac:
                n = qffrac
                needspace(doc, 8)
                question(doc, f"{n}")
                doc.append("Factoritza i simplifica les fraccions següents")
                var = (n * fsexp) // 4
                begin(doc, 'parts')
                begin(doc, 'multicols', 3)
                scale = 1.3
                for x in range(n):
                    part(doc)
                    if x < var or (fsexp != 0 and x == 0):
                        doc.append(NoEscape(r'\scalebox{%s}{$%s$}' % (scale, gen.powsqr(10, 5, 3))))
                    else:
                        if x < (n + var) // 2:
                            doc.append(NoEscape(r'\scalebox{%s}{$%s$}' % (scale, gen.powsqr(10, 6, 3))))
                        else:
                            doc.append(NoEscape(r'\scalebox{%s}{$%s$}' % (scale, gen.powsqr(10, 7, 3))))
                    space(doc, "0.7cm")
                end(doc, 'multicols')
                space(doc, "0.5cm")
                end(doc, 'parts')

            if qdfrac:
                n = qdfrac
                needspace(doc, 8)
                question(doc, f"{n}")
                doc.append("Factoritza i simplifica les següents fraccions amb decimals")
                begin(doc, 'parts')
                begin(doc, 'multicols', 3)
                scale = 1.3
                for x in range(n):
                    part(doc)
                    doc.append(NoEscape(r'\scalebox{%s}{$%s$}' % (scale, gen.powsqr(10, 8, 3))))
                    space(doc, "0.7cm")
                end(doc, 'multicols')
                space(doc, "0.5cm")
                end(doc, 'parts')

            space(doc, "0.5cm")
            if sqrt:
                needspace(doc, 12)
                bloctitle(doc, "Arrels")

            if qarrels:
                n = qarrels
                needspace(doc, 8)
                question(doc, f"{n}")
                doc.append("Expressa com una sola arrel.")
                var = (n * asexp) // 4
                begin(doc, 'parts')
                if 2 not in atermes and 3 not in atermes or 5 in atermes:
                    begin(doc, 'multicols', 2)
                else:
                    begin(doc, 'multicols', 3)

                for x in range(n):
                    part(doc)
                    if x < var + 1:  # sense exponent vs amb exponent. Macedònia de termes
                        doc.append(NoEscape(r'$%s$' % gen.powsqr(103, 1, atermes[(len(atermes) * x) // n])))
                    else:
                        doc.append(NoEscape(r'$%s$' % gen.powsqr(103, 2, atermes[(len(atermes) * x) // n])))
                    space(doc, "0.7cm")
                end(doc, 'multicols')
                space(doc, "0.5cm")
                end(doc, 'parts')

            if qextreure:
                n = qextreure
                needspace(doc, 8)
                question(doc, f"{n}")
                doc.append("Extreu de l'arrel tants factors com puguis.")
                var = (n * fquad) // 4
                begin(doc, 'parts')
                begin(doc, 'multicols', 4)
                for x in range(n):
                    part(doc)
                    if x < var:  # només quadrada vs qualsevol
                        if x == 0 and lletres == 1:  # si hi ha 123 i abc, el primer nums
                            doc.append(NoEscape(r'$%s$' % gen.powsqr(105, 1, lletres=0)))
                        else:
                            doc.append(NoEscape(r'$%s$' % gen.powsqr(105, 1, lletres=lletres)))
                    else:
                        doc.append(NoEscape(r'$%s$' % gen.powsqr(105, 2, lletres=lletres)))
                    space(doc, "0.7cm")
                end(doc, 'multicols')
                space(doc, "0.5cm")
                end(doc, 'parts')

            if qintrod:
                n = qintrod
                needspace(doc, 8)
                question(doc, f"{n}")
                doc.append("Introdueix tots els factors dins l'arrel.")
                var = (n * iquad) // 4
                begin(doc, 'parts')
                begin(doc, 'multicols', 4)
                for x in range(n):
                    part(doc)
                    if x < var:  # només quadrada vs qualsevol
                        if x == 0 and illetres == 1:  # si hi ha 123 i abc, el primer nums
                            doc.append(NoEscape(r'$%s$' % gen.powsqr(106, 1, lletres=0)))
                        else:
                            doc.append(NoEscape(r'$%s$' % gen.powsqr(106, 1, lletres=illetres)))
                    else:
                        doc.append(NoEscape(r'$%s$' % gen.powsqr(106, 2, lletres=illetres)))
                    space(doc, "0.7cm")
                end(doc, 'multicols')
                space(doc, "0.5cm")
                end(doc, 'parts')

            if qcombradi:
                n = qcombradi
                needspace(doc, 8)
                question(doc, f"{n}")
                doc.append("Expressa com una sola arrel.")
                var = (n * einter) // 4
                begin(doc, 'parts')
                begin(doc, 'multicols', 4)
                for x in range(n):
                    part(doc)
                    if x < var:  # sense intercalats vs amb intercalats
                        doc.append(NoEscape(r'$%s$' % gen.powsqr(104, 1, 2)))
                    else:
                        if x < (n + var) // 2:  # meitat de la resta
                            doc.append(NoEscape(r'$%s$' % gen.powsqr(104, 2, 2)))
                        else:
                            doc.append(NoEscape(r'$%s$' % gen.powsqr(104, 2, 3)))
                    space(doc, "0.7cm")
                end(doc, 'multicols')
                space(doc, "0.5cm")
                end(doc, 'parts')

            if qfextreure:
                n = qfextreure
                needspace(doc, 8)
                question(doc, f"{n*2}")
                doc.append("Factoritza i extreu tants factors com puguis.")
                var = (n * ffquad) // 4
                begin(doc, 'parts')
                begin(doc, 'multicols', 3)
                for x in range(n):
                    part(doc)
                    if x < var:  # només quadrada vs qualsevol
                        doc.append(NoEscape(r'$%s$' % gen.powsqr(105, 11)))
                    else:
                        doc.append(NoEscape(r'$%s$' % gen.powsqr(105, 12)))
                    space(doc, "0.7cm")
                end(doc, 'multicols')
                space(doc, "0.5cm")
                end(doc, 'parts')

            if qasum:
                n = qasum
                needspace(doc, 8)
                question(doc, f"{2*n}")
                doc.append("Simplifica al màxim les sumes i restes següents.")
                var = (n * scoef) // 4
                begin(doc, 'parts')
                begin(doc, 'multicols', 2)
                for x in range(n):
                    part(doc)
                    if x < var:  # sense coeficient vs amb
                        if x < (var // 3) or x == 0:
                            doc.append(NoEscape(r'$%s$' % gen.powsqr(107, 1, 3)))
                        else:
                            doc.append(NoEscape(r'$%s$' % gen.powsqr(107, 11, 3)))
                    else:
                        if x < (n // 6) or x == 0:
                            doc.append(NoEscape(r'$%s$' % gen.powsqr(107, 2, 3)))
                        else:
                            doc.append(NoEscape(r'$%s$' % gen.powsqr(107, 12, 3)))
                    space(doc, "0.7cm")
                end(doc, 'multicols')
                space(doc, "0.5cm")
                end(doc, 'parts')

            if qracions:
                n = qracions
                needspace(doc, 8)
                question(doc, f"{n*2}")
                doc.append("Racionalitza les fraccions següents.")
                var1 = (n * rquad) // 4
                var2 = (n * rdoble) // 4
                begin(doc, 'parts')
                begin(doc, 'multicols', 3)
                scale = 1.3
                for x in range(n):
                    part(doc)
                    if not rab or x == 0 or random.choice([0, 1]):  # ra
                        if x < var1:  # només quadrada
                            doc.append(NoEscape(r'\scalebox{%s}{$%s$}' % (scale, gen.powsqr(108, 1))))
                        else:
                            if x < (n + var1) // 2:  # qualsevol, sense exp
                                doc.append(NoEscape(r'\scalebox{%s}{$%s$}' % (scale, gen.powsqr(108, 2))))
                            else:  # qualsevol, amb exp
                                doc.append(NoEscape(r'\scalebox{%s}{$%s$}' % (scale, gen.powsqr(108, 3))))
                    else:  # rab
                        if x < var2:  # sense arrel doble
                            if x < n // 2 or random.choice([0, 1, 1]):  # a la meitat barreja conjugats
                                doc.append(NoEscape(r'\scalebox{%s}{$%s$}' % (scale, gen.powsqr(108, 11))))
                            else:
                                doc.append(NoEscape(r'\scalebox{%s}{$%s$}' % (scale, gen.powsqr(108, 13))))
                        else:  # amb arrel doble
                            if x < n // 2 or random.choice([0, 1, 1]):
                                doc.append(NoEscape(r'\scalebox{%s}{$%s$}' % (scale, gen.powsqr(108, 12))))
                            else:  # a partir de la meitat barreja amb conjugats
                                doc.append(NoEscape(r'\scalebox{%s}{$%s$}' % (scale, gen.powsqr(108, 14))))
                    space(doc, "0.7cm")
                end(doc, 'multicols')
                space(doc, "0.5cm")
                end(doc, 'parts')

            end(doc, 'questions')
        else:
            doc.append("Calia tirar-se tanta estona per no posar res? Potser no...")
    else:
        doc.append("Amb la fitxa buida jo també trec un 10 si vols...")

    doc.generate_pdf("deuresweb/static/pdfs/" + temallarg(tema))
    print("PDF generat.")

    return


def fraccions(opcions, solucions=False):
    tema = "frac"

    # getting opcions
    curs = opcions["curs"]
    print("Generant pdf: {} ({})".format(temallarg(tema), curs))

    if opcions["solucions"] == "sí":
        solucions = True

    if "decimals" in opcions:
        decimals = True
        qfgen = quantesson(opcions["qfgen"], "fgen")
        fgdecims = []
        for x in range(1, 4):
            if f"decim{x}" in opcions:
                fgdecims.append(x)
        if not fgdecims:
            fgdecims = [4]
        notac = []
        if "barret" in opcions:
            notac.append(1)
        if "suspens" in opcions:
            notac.append(2)
        if not notac:
            notac = [1, 2]
    else:
        decimals = False
        qfgen = False

    if "simples" in opcions:
        simples = True
        qsumes = quantesson(opcions["qsumes"], "fr_sumes")
        qmultis = quantesson(opcions["qmultis"], "fr_multis")
        if "smul" in opcions:
            if "sdiv" in opcions:
                muldiv = 1
            else:
                muldiv = 0
        elif "sdiv" in opcions:
            muldiv = 2
        else:
            muldiv = 1
        print(f"Frac sumes {qsumes}, Frac multis {qmultis} (muldiv {muldiv})")
    else:
        simples = False
        qsumes = 0
        qmultis = 0

    if "combis" in opcions:
        combis = True
        qcombis = quantesson(opcions["qcombis"], "fr_combis")
        cops = [1, 2]  # sumrest i muldiv
        for x in [4, 5]:
            if f"op{x}" in opcions:
                cops.append(x)
        print(f"Frac combis {qcombis}")
    else:
        combis = False
        qcombis = 0

    # PyLaTeX code
    geometry = margins()
    doc = Document(documentclass="exam", geometry_options=geometry)
    doc.packages.append(Package('multicol'))
    doc.packages.append(Package('amsmath'))
    doc.packages.append(Package('alphalph'))
    doc.packages.append(Package('setspace'))  # això és per setstretch (interlineat de les solucions)
    doc.packages.append(Package('graphicx'))  # això és per scalebox (fer les mates més grans)
    doc.packages.append(Package('needspace'))

    headfoot(doc, opcions, tema)
    myconfig(doc, solucions)

    doc.append(NoEscape(
        r'\renewcommand{\thepartno}{\alphalph{\value{partno}}}'))  # per permetre doble lletra, 26*26 = 676 apartats max

    # preguntes
    if decimals or simples or combis:
        if any([qsumes, qmultis, qcombis, qfgen]):
            begin(doc, 'questions')

            if decimals:
                needspace(doc, 12)
                bloctitle(doc, "Nombres Decimals")

            if qfgen:
                n = qfgen
                needspace(doc, 8)
                question(doc, f"{n}")
                doc.append("Troba la fracció generatriu d'aquests nombres decimals.")
                begin(doc, 'parts')
                begin(doc, 'multicols', "4")
                for x in range(0, n):
                    part(doc)
                    if x < 3 and (x+1) in fgdecims:
                        doc.append(NoEscape(r'$%s$' % gen.decimals(x+1, random.choice(notac))))
                    else:
                        doc.append(NoEscape(r'$%s$' % gen.decimals(random.choice(fgdecims), random.choice(notac))))
                    space(doc, "1cm")
                end(doc, 'multicols')
                end(doc, 'parts')
                space(doc, "0.3cm")

            if simples:
                needspace(doc, 12)
                bloctitle(doc, "Operacions simples")

            if qsumes:
                n = qsumes
                needspace(doc, 8)
                question(doc, f"{n}")
                doc.append("Resol les següents sumes i restes de fraccions.")
                begin(doc, 'parts')
                begin(doc, 'multicols', 3)
                scale = 1.3
                for x in range(0, n):
                    part(doc)
                    doc.append(NoEscape(r'\scalebox{%s}{$%s$}' % (scale, gen.frac(1, 2, 2))))  # TODO var
                    space(doc, "1cm")
                end(doc, 'multicols')
                end(doc, 'parts')
                space(doc, "0.3cm")

            if qmultis:
                n = qmultis
                needspace(doc, 8)
                question(doc, f"{n}")
                if muldiv == 1:
                    doc.append("Resol les següents multiplicacions i divisions de fraccions.")
                elif muldiv == 0:
                    doc.append("Resol les següents multiplicacions de fraccions.")
                else:
                    doc.append("Resol les següents divisions de fraccions.")
                begin(doc, 'parts')
                begin(doc, 'multicols', 3)
                scale = 1.3
                for x in range(0, n):
                    part(doc)
                    if x == 0 and muldiv in [0, 1]:
                        doc.append(
                            NoEscape(r'\scalebox{%s}{$%s$}' % (scale, gen.frac(2, 3, 2, divis=0))))  # TODO var
                    else:
                        doc.append(NoEscape(r'\scalebox{%s}{$%s$}' % (scale, gen.frac(2, 3, 2, divis=muldiv))))  # TODO var
                    space(doc, "1cm")
                end(doc, 'multicols')
                end(doc, 'parts')

            if combis:
                needspace(doc, 12)
                bloctitle(doc, "Operacions combinades")

            if qcombis:
                n = qcombis
                needspace(doc, 8)
                question(doc, f"{n*4}")
                doc.append("Resol les següents operacions combinades amb fraccions.")
                begin(doc, 'parts')
                begin(doc, 'multicols', 2)
                scale = 1.3
                solus = []
                for x in range(0, n):
                    part(doc)
                    num = gen.randomfracnum(3)
                    den = gen.randomfracnum(3)
                    text = gen.fracmix(num, den, 2, ops=cops)
                    doc.append(NoEscape(r'\scalebox{%s}{$%s$}' % (scale, text)))
                    space(doc, "1cm")
                    num, den = gen.fracsimple(num, den)
                    if den == 1:
                        solu = num
                    else:
                        solu = "\\frac{" f"{num}" "}{" f"{den}" "}"
                    solus.append(solu)
                    print(solu, text)
                end(doc, 'multicols')
                end(doc, 'parts')
                blocsolus(doc, solucions, solus, mates=True, stretch="1.3")

            end(doc, 'questions')
        else:
            doc.append("Calia tirar-se tanta estona per no posar res? Potser no")
    else:
        doc.append("haha.. quina gràcia.. has fet un pdf sense res, que original...")

    doc.generate_pdf("deuresweb/static/pdfs/" + temallarg(tema))
    print("PDF generat.")

    return


def ncient(opcions, solucions=False):
    tema = "ncient"

    # getting opcions
    curs = opcions["curs"]
    print("Generant pdf: {} ({})".format(temallarg(tema), curs))

    if "ncient" in opcions:
        ncient = True
        qnumacient = quantesson(opcions["qnumacient"], "numacient")
        nc_unaxs = quantesvariant(opcions["nc_unaxs"])
        qcientanum = quantesson(opcions["qcientanum"], "cientanum")
        cn_unaxs = quantesvariant(opcions["cn_unaxs"])
        qmuldiv = quantesson(opcions["qmuldiv"], "nc_muldiv")
    else:
        ncient = False
        qnumacient = False
        qcientanum = False
        qmuldiv = False

    # PyLaTeX code
    geometry = margins()
    doc = Document(documentclass="exam", geometry_options=geometry)
    doc.packages.append(Package('multicol'))
    doc.packages.append(Package('amsmath'))
    doc.packages.append(Package('alphalph'))
    doc.packages.append(Package('graphicx'))  # això és per scalebox (fer les mates més grans)
    doc.packages.append(Package('needspace'))

    headfoot(doc, opcions, tema)
    myconfig(doc, solucions)

    doc.append(NoEscape(
        r'\renewcommand{\thepartno}{\alphalph{\value{partno}}}'))  # per permetre doble lletra, 26*26 = 676 apartats max

    # preguntes
    if ncient:
        if any([qnumacient, qcientanum, qmuldiv]):
            begin(doc, 'questions')

            if ncient:
                needspace(doc, 12)
                bloctitle(doc, "Notació Científica")

            if qnumacient:
                n = qnumacient
                needspace(doc, 8)
                var = (n * nc_unaxs) // 4
                question(doc, f"{n}")
                doc.append("Passa a notació científica els nombres següents.")
                begin(doc, 'parts')
                begin(doc, 'multicols', "4")
                for x in range(0, n):
                    part(doc)
                    if x < var or (var and x == 0):
                        if x == 0:
                            doc.append(NoEscape(r'$%s$' % gen.ncient(1, 1, direc=1)))
                        elif x == 1:
                            doc.append(NoEscape(r'$%s$' % gen.ncient(1, 2, direc=2)))
                        else:
                            doc.append(NoEscape(r'$%s$' % gen.ncient(1, 2)))
                    else:
                        if random.randint(0, 7):
                            doc.append(NoEscape(r'$%s$' % gen.ncient(1, 3)))
                        else:
                            doc.append(NoEscape(r'$%s$' % gen.ncient(1, 4)))
                    space(doc, "0.7cm")
                end(doc, 'multicols')
                end(doc, 'parts')
                space(doc, "0.3cm")

            if qcientanum:
                n = qcientanum
                needspace(doc, 8)
                var = (n * cn_unaxs) // 4
                question(doc, f"{n}")
                doc.append("Escriu amb totes les xifres els números següents.")
                begin(doc, 'parts')
                begin(doc, 'multicols', "4")
                for x in range(0, n):
                    part(doc)
                    if x < var or (var and x == 0):
                        if x == 0:
                            doc.append(NoEscape(r'$%s$' % gen.ncient(2, 1, direc=1)))
                        elif x == 1:
                            doc.append(NoEscape(r'$%s$' % gen.ncient(2, 2, direc=2)))
                        else:
                            doc.append(NoEscape(r'$%s$' % gen.ncient(2, 2)))
                    else:
                        doc.append(NoEscape(r'$%s$' % gen.ncient(2, 3)))
                    space(doc, "0.7cm")
                end(doc, 'multicols')
                end(doc, 'parts')
                space(doc, "0.3cm")

            if qmuldiv:
                n = qmuldiv
                needspace(doc, 8)
                question(doc, f"{n}")
                doc.append("Realitza les operacions següents.")
                begin(doc, 'parts')
                begin(doc, 'multicols', "2")
                for x in range(0, n):
                    part(doc)
                    doc.append(NoEscape(r'$%s$' % gen.ncient(3, 1)))
                    space(doc, "1cm")
                end(doc, 'multicols')
                end(doc, 'parts')
                space(doc, "0.3cm")

            end(doc, 'questions')
        else:
            doc.append("Calia tirar-se tanta estona per no posar res? Potser no")
    else:
        doc.append("haha.. quina gràcia.. has fet un pdf sense res, que original...")

    doc.generate_pdf("deuresweb/static/pdfs/" + temallarg(tema))
    print("PDF generat.")

    return


def crea_fitxa(opcions, solucions=False):
    opcions = parse_multi_form(opcions)  # converteix la patranya que m'arriba del post en un dict com cal

    if "temafitxa" in opcions:
        temafitxa = opcions["temafitxa"]
    else:
        temafitxa = "misteri"
    curs = opcions["curs"]

    print(f"Generant pdf {nom_tema(temafitxa, prep=True)} ({curs})")

    if "solucions" in opcions and opcions["solucions"] == "sí":
        solucions = True
    if "solulloc" in opcions:
        solulloc = opcions["solulloc"]
    else:
        solulloc = ""

    # ----- Setup PyLaTeX ----- #
    geometry = margins()
    doc = Document(documentclass="exam", geometry_options=geometry)
    doc.packages.append(Package('multicol'))  # TODO integrar a cada exercici quins necessita per triar-los automàtic
    doc.packages.append(Package('amsmath'))
    doc.packages.append(Package('alphalph'))
    doc.packages.append(Package('needspace'))
    # doc.packages.append(Package('hyperref'))  # això és per links (ha de ser l'últim paquet)

    headfoot(doc, opcions, temafitxa)
    myconfig(doc, solucions)

    doc.append(NoEscape(
        r'\renewcommand{\thepartno}{\alphalph{\value{partno}}}'))  # per permetre doble lletra, 26*26 = 676 apartats max

    # ----- Si et cal veure l'arbre d'opcions, activa això: ----- #
    """for t in opcions["temes"]:
        print(f"****** {t} *******".upper())
        for apartat in opcions["temes"][t]:
            print(f"{apartat}".upper())
            for exercici in opcions["temes"][t][apartat]:
                print(f"- {exercici} : {opcions['temes'][t][apartat][exercici]}")
    print("..::ROOT::..")
    for apartat in opcions:
        if apartat != "temes":
            print(f"- {apartat} : {opcions[apartat]}")"""

    # ------ PREPROCESSING ----- #

    tbuits = []  # temes per eliminar (perquè no tenen res dins)
    for tema in opcions["temes"]:
        apbuits = []  # apartats per eliminar (perquè no tenen res dins)
        for apartat in opcions["temes"][tema]:
            if "apartats" not in opcions or apartat not in opcions["apartats"][tema]:
                apbuits.append(apartat)
            else:
                exbuits = []  # exercicis per eliminar
                for exercici in opcions["temes"][tema][apartat]:
                    if opcions["temes"][tema][apartat][exercici]["quantes"] == "no":  # elimino exercicis buits
                        exbuits.append(exercici)
                    else:  # entro el nom de l'exercici i la tria de solus dins de sí mateix (per després)
                        opcions["temes"][tema][apartat][exercici]["exnom"] = exercici
                        opcions["temes"][tema][apartat][exercici]["solucions"] = solucions
                        opcions["temes"][tema][apartat][exercici]["solulloc"] = solulloc

                for exercici in exbuits:
                    opcions["temes"][tema][apartat].pop(exercici, None)
                if not len(opcions["temes"][tema][apartat]):
                    apbuits.append(apartat)
        for apartat in apbuits:
            opcions["temes"][tema].pop(apartat, None)
        if not len(opcions["temes"][tema]):
            tbuits.append(tema)
    for tema in tbuits:
        opcions["temes"].pop(tema, None)

    # ---------- FITXA EN SÍ --------- #

    if not len(opcions["temes"]):
        doc.append("Doncs res, tu, fem una fitxa buida. Si jo estic aquí per complir ordres, no passa res.")
        doc.append("...però vaja, jo potser hauria agafat un paper en blanc, no? No sé... sembla més pràctic.")
    else:
        qnum = 1  # num d'exercici
        sols_final = []
        begin(doc, "questions")
        for tema in opcions["temes"]:
            if len(opcions["temes"]) > 1:  # si hi ha més d'un tema, poso títols dels temes TODO hr potser
                needspace(doc, 16)
                bloctitle(doc, temallarg(tema).upper())
            for apartat in opcions["temes"][tema]:
                needspace(doc, 14)
                bloctitle(doc, nom_apartat(tema, apartat))
                for exercici in opcions["temes"][tema][apartat]:
                    g = mexs.constructor_de(exercici)
                    sols = g(doc, opcions["temes"][tema][apartat][exercici])
                    if sols and sols[1]:  # l'exercici ha retornat solució pel final (pq el formulari ho demanava)
                        sols_final.append([qnum, sols])
                    qnum += 1
        if sols_final:  # si no n'hi ha no les escric
            if opcions["solulloc"] == "final":
                breakpage = False
            else:
                breakpage = True
            metasolucions(doc, sols_final, breakpage=breakpage)
            pass
        end(doc, "questions")
        pre2pkg(doc)  # afegeix al doc els paquets especials que els exercicis hagin demanat

    doc.generate_pdf("deuresweb/static/pdfs/" + nom_tema(temafitxa, pdf=True))
    print("PDF generat.")

    return "/static/pdfs/" + nom_tema(temafitxa, pdf=True) + ".pdf"


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
    doc.packages.append(Package('needspace'))

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
                needspace(doc, 12)
                bloctitle(doc, "Successions aritmètiques")

            if qtermen:
                n = qtermen
                needspace(doc, 8)
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
                needspace(doc, 8)
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
                needspace(doc, 8)
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
                        t += " el terme $a_n$"
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
                    needspace(doc, 8)
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
                        needspace(doc, 8)
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
                        needspace(doc, 8)
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
                needspace(doc, 12)
                bloctitle(doc, "Successions geomètriques")

            if qgtermen:
                n = qgtermen
                needspace(doc, 8)
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
                needspace(doc, 8)
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
                needspace(doc, 8)
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
                    needspace(doc, 8)
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
                        needspace(doc, 8)
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
                        needspace(doc, 8)
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


def limits(opcions, solucions=False):
    tema = "lim"

    # getting opcions
    curs = opcions["curs"]
    print("Generant pdf: {} ({})".format(temallarg(tema), curs))

    if "calcul" in opcions:
        calcul = True
        qinf = quantesson(opcions["qinf"], "lim_inf")
        print(f"Infinit {qinf}")

        lims = []
        for x in range(5):  # 0-4
            if f"lim{x}" in opcions:
                lims.append(x)
        if not lims:
            lims = [1, 2, 3, 4]
    else:
        calcul = False
        qinf = 0

    # PyLaTeX code
    geometry = margins()
    doc = Document(documentclass="exam", geometry_options=geometry)
    doc.packages.append(Package('multicol'))
    doc.packages.append(Package('amsmath'))
    doc.packages.append(Package('alphalph'))
    doc.packages.append(Package('graphicx'))  # això és per scalebox (fer les mates més grans)
    doc.packages.append(Package('needspace'))
    # doc.packages.append(Package('hyperref'))  # això és per links (ha de ser l'últim paquet)

    headfoot(doc, opcions, tema)
    myconfig(doc, solucions)

    doc.append(NoEscape(
        r'\renewcommand{\thepartno}{\alphalph{\value{partno}}}'))  # per permetre doble lletra, 26*26 = 676 apartats max

    # preguntes
    if any([calcul]):  # aquí tots els botons grossos
        if any([qinf]):  # aquí tots els tipus d'exercici
            begin(doc, 'questions')

            if calcul:
                needspace(doc, 12)
                bloctitle(doc, "Càlcul de límits")

            if qinf:
                n = qinf
                needspace(doc, 8)
                question(doc, f"{n}")  # puntuació de l'exercici
                doc.append("Resol els límits següents.")
                begin(doc, 'parts')
                begin(doc, 'multicols', 2)  # columnes
                scale = 1.3
                text = ""
                for x in range(0, n):
                    part(doc)
                    tipus = random.choice(lims)
                    if tipus in [0, 1]:
                        text = gen.limits(tipus)
                    elif tipus == 2:
                        text = gen.limits(2, 2)
                    elif tipus == 3:
                        text = gen.limits(3, random.choice([1, 2]))  # √A-√B vs A-√B
                    elif tipus == 4:
                        text = gen.limits(4, random.choice([1, 2]))  # amb l'1 separat vs sense
                    if tipus in [1, 2, 4]:
                        scale = 1.2
                    else:
                        scale = 1
                    if solucions:
                        doc.append(NoEscape(r'\href{%s}{\scalebox{%s}{$%s$}}' % (w.urlfor(text, t="dx"), scale, text)))
                    else:
                        doc.append(NoEscape(r'\scalebox{%s}{$%s$}' % (scale, text)))
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


def derivades(opcions, solucions=False):
    tema = "dx"

    # getting opcions
    curs = opcions["curs"]
    print("Generant pdf: {} ({})".format(temallarg(tema), curs))

    if opcions["solucions"] == "sí":
        solucions = True

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
    doc.packages.append(Package('graphicx'))  # això és per scalebox (fer les mates més grans)
    doc.packages.append(Package('needspace'))
    doc.packages.append(Package('hyperref'))  # això és per links (ha de ser l'últim paquet)

    headfoot(doc, opcions, tema)
    myconfig(doc, solucions)

    doc.append(NoEscape(
        r'\renewcommand{\thepartno}{\alphalph{\value{partno}}}'))  # per permetre doble lletra, 26*26 = 676 apartats max

    # preguntes
    if rd:  # aquí tots els botons grossos
        if any([qsimples, qmuldiv, qcadena]):  # aquí tots els tipus d'exercici
            begin(doc, 'questions')

            if rd:
                needspace(doc, 12)
                bloctitle(doc, "Regles de Derivació")

            if qsimples:
                n = qsimples
                needspace(doc, 8)
                question(doc, f"{n}")
                doc.append("Resol les següents derivades sense regla de la cadena.")
                begin(doc, 'parts')
                begin(doc, 'multicols', 3)
                for x in range(0, n):
                    part(doc)
                    text = gen.dx(1, [1, 2, 3, 4, 5], simples=True)
                    if solucions:
                        doc.append(NoEscape(r'\href{%s}{$%s$}' % (w.urlfor(text, t="dx"), text)))
                    else:
                        doc.append(NoEscape(r'$%s$' % text))
                    space(doc, "1cm")
                end(doc, 'multicols')
                end(doc, 'parts')

            if qmuldiv != 0:
                n = qmuldiv
                needspace(doc, 8)
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
                        text = gen.dx(2, [1, 2, 3, 4, 5, 6, 7, 8], simples=True, inici=random.choice(propietats))
                    else:
                        text = gen.dx(3, [1, 2, 3, 4, 5, 6, 7, 8], simples=True, inici=random.choice(propietats))
                    scale = gen.fxscale(text)
                    if solucions:
                        doc.append(NoEscape(r'\href{%s}{\scalebox{%s}{$%s$}}' % (w.urlfor(text, t="dx"), scale, text)))
                    else:
                        doc.append(NoEscape(r'\scalebox{%s}{$%s$}' % (scale, text)))
                    space(doc, "1cm")
                end(doc, 'multicols')
                end(doc, 'parts')

            if qcadena != 0:
                n = qcadena
                needspace(doc, 8)
                question(doc, f"{3*n}")
                doc.append("Resol les següents derivades (amb regla de la cadena).")
                begin(doc, 'parts')
                begin(doc, 'multicols', 2)
                for x in range(0, n):
                    part(doc)
                    if x < (n // 2):
                        text = gen.dx(2, funcions)
                    else:
                        text = gen.dx(3, funcions)
                    scale = gen.fxscale(text)
                    if solucions:
                        doc.append(NoEscape(r'\href{%s}{\scalebox{%s}{$%s$}}' % (w.urlfor(text, t="dx"), scale, text)))
                    else:
                        doc.append(NoEscape(r'\scalebox{%s}{$%s$}' % (scale, text)))
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


# - - - - - - - - - - - - - - - - - - - - - - - - Química - - - - - - - - - - - - - - - - - - - - - - - - - #


def q_iso(opcions, solucions=False):
    tema = "q_iso"

    # getting opcions
    curs = opcions["curs"]
    print("Generant pdf: {} ({})".format(temallarg(tema), curs))

    if "iso" in opcions:
        iso = True
        qzapne = quantesson(opcions["qzapne"], "q_zapne")
        # ...
        print(f"Zapne {qzapne}")
    else:
        iso = False
        qzapne = 0
        # ...

    # PyLaTeX code
    geometry = margins()
    doc = Document(documentclass="exam", geometry_options=geometry)
    doc.packages.append(Package('multicol'))
    doc.packages.append(Package('amsmath'))
    doc.packages.append(Package('alphalph'))
    doc.packages.append(Package('needspace'))
    doc.packages.append(Package('isotope'))  # paquet per escriure isòtops
    doc.packages.append(Package('array'))
    doc.packages.append(Package('longtable'))
    doc.packages.append(NoEscape(r"\usepackage[catalan]{babel}"))  # ela geminada
    # doc.packages.append(Package('graphicx'))  # això és per scalebox (fer les mates més grans)
    # doc.packages.append(Package('hyperref'))  # això és per links (ha de ser l'últim paquet)

    headfoot(doc, opcions, tema, assig="Química")
    myconfig(doc, solucions)

    doc.append(NoEscape(
        r'\renewcommand{\thepartno}{\alphalph{\value{partno}}}'))  # per permetre doble lletra, 26*26 = 676 apartats max

    # preguntes
    if any([iso]):  # aquí tots els botons grossos
        if any([qzapne]):  # aquí tots els tipus d'exercici
            begin(doc, 'questions')

            if iso:
                needspace(doc, 12)
                bloctitle(doc, "Isòtops")

            if qzapne:
                n = qzapne
                needspace(doc, 8)
                question(doc, f"{n}")  # puntuació de l'exercici
                doc.append("Omple la taula següent.")
                header = [envt("Nom", 6), envt("Símbol"), envt("Z"), envt("A"), envt("p"), envt("n"), envt("e"),
                          envt("càrrega", 1)]
                obretaula(doc, taulaconfig(8, "c", [0, 2, 4, 7, -1]), header=header)
                # trio per avançat la selecció d'elements (z petits però no repetits)
                prezs = random.sample(qgen.els_ist[0:min(max(n + 10, 40), 117)], n)  # min 40, màx n+10 (no més de 117)
                for x in range(n):
                    filataula(doc, qgen.fisotops(1, 1 if x < n//4 else 2, prez=prezs[x % n]), py=10)
                tancataula(doc)

            end(doc, 'questions')
        else:
            doc.append("Calia tirar-se tanta estona per no posar res? Potser no")
    else:
        doc.append("haha.. quina gràcia.. has fet un pdf sense res, que original...")

    doc.generate_pdf("deuresweb/static/pdfs/" + temallarg(tema))
    print("PDF generat.")
    return


def q_formul(opcions, solucions=False):
    tema = "q_formul"

    # getting opcions
    curs = opcions["curs"]
    print("Generant pdf: {} ({})".format(temallarg(tema), curs))

    estil = opcions["estil"]
    if opcions["solucions"] == "sí":
        solucions = True

    if "inorg" in opcions:
        inorg = True
        descn = []  # TODO implementar tria de descartats negatius (almenys carbur i silicur)
        qsimples = quantesson(opcions["qsimples"], "q_simples")
        qhidrurs = quantesson(opcions["qhidrurs"], "q_hidrurs")
        qoxids = quantesson(opcions["qoxids"], "q_oxids")
        qsbin = quantesson(opcions["qsbin"], "q_sbin")
        qhidroxids = quantesson(opcions["qhidroxids"], "q_hidroxids")
        qbarreja = quantesson(opcions["qbarreja"], "q_f_barreja")
        opsbarreja = []
        for x in range(0, 5):  # 0-4
            if f"barr{x}" in opcions:
                opsbarreja.append(x)
        if not opsbarreja:  # si ha deixat buit, poso tot
            opsbarreja = [x for x in range(0, 5)]
        print(opsbarreja)
        # ...
        #print(f"Exercici 1 {qexercici1}, Exercici 2 {qexercici2} ...")
    else:
        inorg = False
        qsimples = 0
        qhidrurs = 0
        qoxids = 0
        qsbin = 0
        qhidroxids = 0
        qbarreja = 0
        # ...

    if "org" in opcions:
        org = True
        # ...
    else:
        org = False
        # ...

    # PyLaTeX code
    geometry = margins()
    doc = Document(documentclass="exam", geometry_options=geometry)
    doc.packages.append(Package('multicol'))
    doc.packages.append(Package('amsmath'))
    doc.packages.append(Package('alphalph'))
    doc.packages.append(Package('needspace'))
    doc.packages.append(Package('isotope'))  # paquet per escriure isòtops
    doc.packages.append(Package('array'))
    doc.packages.append(Package('longtable'))
    doc.packages.append(NoEscape(r"\usepackage[catalan]{babel}"))  # ela geminada
    # doc.packages.append(Package('graphicx'))  # això és per scalebox (fer les mates més grans)
    # doc.packages.append(Package('hyperref'))  # això és per links (ha de ser l'últim paquet)

    headfoot(doc, opcions, tema, assig="Química")
    myconfig(doc, solucions)

    doc.append(NoEscape(
        r'\renewcommand{\thepartno}{\alphalph{\value{partno}}}'))  # per permetre doble lletra, 26*26 = 676 apartats max

    # preguntes
    if any([inorg, org]):  # aquí tots els botons grossos
        if any([qsimples, qhidrurs, qoxids, qsbin, qhidroxids, qbarreja]):  # aquí tots els tipus d'exercici
            begin(doc, 'questions')
            qnum = 0  # i.e: en quina pregunta estic?

            if inorg:
                needspace(doc, 12)
                bloctitle(doc, "Formulació inorgànica")

            if qsimples:
                qnum += 1
                n = qsimples
                needspace(doc, 8)
                question(doc, f"{n}")  # puntuació de l'exercici
                doc.append(r"Omple aquesta taula de substàncies simples.")
                header = [envt("Símbol"), envt("Nomenclatura Stock"), "Nomenclatura Sistemàtica", envt("Nom comú")]
                obretaula(doc, taulaconfig(4, "c", [0, 1, -1]), header=header)
                ffiles = qgen.n_finorg(n, 1, descn=descn, estil=estil)
                solu_simples = []
                qnum_simples = qnum
                for x in range(n):
                    fila, fsolu = qgen.finorg(1, estil=estil, ffila=ffiles.pop(), solucions=True)
                    filataula(doc, fila, py=10)
                    solu_simples.append(fsolu)
                tancataula(doc)

            if qhidrurs:
                qnum += 1
                n = qhidrurs
                needspace(doc, 8)
                question(doc, f"{n}")
                doc.append(r"Omple aquesta taula de compostos binaris d'hidrogen.")
                header = [envt("Molècula"), envt("Nomenclatura Stock"), "Nomenclatura Sistemàtica", "Nom comú / Hidràcid"]
                obretaula(doc, taulaconfig(4, "c", [0, 1, -1]), header=header)
                ffiles = qgen.n_finorg(n, 10, 1, descn=descn, estil=estil)
                solu_hidrurs = []
                qnum_hidrurs = qnum
                for x in range(n):
                    fila, fsolu = qgen.finorg(10, 1, estil=estil, ffila=ffiles.pop(), solucions=True)
                    filataula(doc, fila, py=10)
                    solu_hidrurs.append(fsolu)
                tancataula(doc)

            if qoxids:
                qnum += 1
                n = qoxids
                needspace(doc, 8)
                question(doc, f"{n}")
                doc.append(r"Omple aquesta taula d'òxids.")
                header = [envt("Molècula"), envt("Nomenclatura Stock"), "Nomenclatura Sistemàtica", envt("Nom comú")]
                obretaula(doc, taulaconfig(4, "c", [0, 1, -1]), header=header)
                ffiles = qgen.n_finorg(n, 10, 2, descn=descn, estil=estil)
                solu_oxids = []
                qnum_oxids = qnum
                for x in range(n):
                    fila, fsolu = qgen.finorg(10, 2, estil=estil, ffila=ffiles.pop(), solucions=True)
                    filataula(doc, fila, py=10)
                    solu_oxids.append(fsolu)
                tancataula(doc)

            if qsbin:
                qnum += 1
                n = qsbin
                needspace(doc, 8)
                question(doc, f"{n}")
                doc.append(r"Omple aquesta taula de compostos binaris.")
                header = [envt("Molècula"), envt("Nomenclatura Stock"), "Nomenclatura Sistemàtica", envt("Nom comú")]
                obretaula(doc, taulaconfig(4, "c", [0, 1, -1]), header=header)
                solu_sbin = []
                qnum_sbin = qnum
                for x in range(n):
                    fila, fsolu = qgen.finorg(10, 3, estil=estil, solucions=True)
                    filataula(doc, fila, py=10)
                    solu_sbin.append(fsolu)
                tancataula(doc)

            if qhidroxids:
                qnum += 1
                n = qhidroxids
                needspace(doc, 8)
                question(doc, f"{n}")
                doc.append(r"Omple aquesta taula d'hidròxids.")
                header = [envt("Molècula"), envt("Nomenclatura Stock"), "Nomenclatura Sistemàtica", envt("Nom comú")]
                obretaula(doc, taulaconfig(4, "c", [0, 1, -1]), header=header)
                ffiles = qgen.n_finorg(n, 10, 4, descn=descn, estil=estil)
                solu_hidroxids = []
                qnum_hidroxids = qnum
                for x in range(n):
                    fila, fsolu = qgen.finorg(10, 4, estil=estil, ffila=ffiles.pop(), solucions=True)
                    filataula(doc, fila, py=10)
                    solu_hidroxids.append(fsolu)
                tancataula(doc)

            if qbarreja:
                qnum += 1
                n = qbarreja
                needspace(doc, 8)
                question(doc, f"{n}")
                doc.append(r"Omple aquesta taula de tot de coses barrejades.")
                header = [envt("Molècula"), envt("Nomenclatura Stock"), "Nomenclatura Sistemàtica", "Nom comú / Hidràcid"]
                obretaula(doc, taulaconfig(4, "c", [0, 1, -1]), header=header)
                # pregenero les quantitats
                ltipus = []  # llista d'on trauré el tipus de cada exercici
                ntipus = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}  # llista de qtats per tipus

                for t in opsbarreja:  # omplo a parts iguals (+1 per arrodonir la divisió entera amunt)
                    ntipus[t] = n // len(opsbarreja) + 1
                    ltipus += [t for _ in range(ntipus[t])]
                random.shuffle(ltipus)
                # pregenero les files (per evitar repeticions)
                ffsimples = qgen.n_finorg(ntipus[0], 1, descn=descn, estil=estil)
                ffhidro = qgen.n_finorg(ntipus[1], 10, 1, descn=descn, estil=estil)
                ffoxids = qgen.n_finorg(ntipus[2], 10, 2, descn=descn, estil=estil)
                ffhidroxids = qgen.n_finorg(ntipus[4], 10, 4, descn=descn, estil=estil)

                # solus
                solu_barreja = []
                qnum_barreja = qnum
                for x in range(n):
                    # trio tipus (l'agafo de la llista o l'invento si no quedés llista per motius estranys)
                    if not ltipus:
                        print("compte: opsbarreja")
                        tipus = random.choice(opsbarreja)
                    else:
                        tipus = ltipus.pop()
                    # genero la fila
                    if tipus == 0:  # simples
                        fila, fsolu = qgen.finorg(1, estil=estil, ffila=ffsimples.pop(), solucions=True)
                        filataula(doc, fila, py=10)
                    else:
                        ffila = []
                        if tipus == 1:  # hidrogen
                            ffila = ffhidro.pop()
                        elif tipus == 2:  # òxids
                            ffila = ffoxids.pop()
                        elif tipus == 4:  # hidròxids
                            ffila = ffhidroxids.pop()
                        fila, fsolu = qgen.finorg(10, tipus, estil=estil, ffila=ffila, solucions=True)
                        filataula(doc, fila, py=10)
                    solu_barreja.append(fsolu)
                tancataula(doc)

            if org:
                needspace(doc, 12)
                bloctitle(doc, "Formulació Orgànica")
            # exercicis d'orgànica'

            # ********* solucions al final ********* #
            if solucions:
                doc.append(NoEscape(r"\newpage"))
                bloctitle(doc, "Solucions dels exercicis")

                if qsimples:
                    doc.append(f"{qnum_simples}. Taula de substàncies simples.")
                    header = ["Símbol", "Nomenclatura Stock", "Nomenclatura Sistemàtica", "Nom comú"]
                    obretaula(doc, taulaconfig(4, "c", [0, 1, -1]), header=header)
                    for fila in solu_simples:
                        filataula(doc, fila, py=1)
                    tancataula(doc)

                if qhidrurs:
                    doc.append(f"{qnum_hidrurs}. Taula de compostos d'hidrogen.")
                    header = ["Símbol", "Nomenclatura Stock", "Nomenclatura Sistemàtica", "Nom comú / Hidràcid"]
                    obretaula(doc, taulaconfig(4, "c", [0, 1, -1]), header=header)
                    for fila in solu_hidrurs:
                        filataula(doc, fila, py=1)
                    tancataula(doc)

                if qoxids:
                    doc.append(f"{qnum_oxids}. Taula d'òxids.")
                    header = ["Símbol", "Nomenclatura Stock", "Nomenclatura Sistemàtica", "Nom comú"]
                    obretaula(doc, taulaconfig(4, "c", [0, 1, -1]), header=header)
                    for fila in solu_oxids:
                        filataula(doc, fila, py=1)
                    tancataula(doc)

                if qsbin:
                    doc.append(f"{qnum_sbin}. Taula de sals binàries.")
                    header = ["Símbol", "Nomenclatura Stock", "Nomenclatura Sistemàtica", "Nom comú"]
                    obretaula(doc, taulaconfig(4, "c", [0, 1, -1]), header=header)
                    for fila in solu_sbin:
                        filataula(doc, fila, py=1)
                    tancataula(doc)

                if qhidroxids:
                    doc.append(f"{qnum_hidroxids}. Taula d'hidròxids.")
                    header = ["Símbol", "Nomenclatura Stock", "Nomenclatura Sistemàtica", "Nom comú"]
                    obretaula(doc, taulaconfig(4, "c", [0, 1, -1]), header=header)
                    for fila in solu_hidroxids:
                        filataula(doc, fila, py=1)
                    tancataula(doc)

                if qbarreja:
                    doc.append(f"{qnum_barreja}. Taula de coses barrejades.")
                    header = ["Símbol", "Nomenclatura Stock", "Nomenclatura Sistemàtica", "Nom comú / Hidràcid"]
                    obretaula(doc, taulaconfig(4, "c", [0, 1, -1]), header=header)
                    for fila in solu_barreja:
                        filataula(doc, fila, py=1)
                    tancataula(doc)

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
    doc.packages.append(Package('isotope'))  # paquet per escriure isòtops
    doc.packages.append(Package('longtable'))
    doc.packages.append(Package('array'))
    doc.packages.append(Package('tikz'))  # dibuixos
    doc.packages.append(NoEscape(r"\usepackage[catalan]{babel}"))  # ela geminada

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
    doc.append(NoEscape(r'\renewcommand{\solutiontitle}{\noindent\textbf{Solució:}\noindent}'))  # \par si vols break
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

    # tikz
    question(doc, "42")
    doc.append("Bon dia, aquí tenim una pregunta d'intervals dibuixada amb tikz.")
    begin(doc, "multicols", 2)
    begin(doc, "parts")
    for _ in range(4):
        part(doc)
        a = random.randint(-5, 2)
        b = a + random.randint(2, 8)
        at, bt = (random.choice([True, False]) for _ in range(2))
        tikz = pic.recta_interval(a, b, at, bt)
        doc.append(NoEscape(tikz))
    # aquests de sota els he fet per una fitxa
    part(doc)
    doc.append("Aquí entren els personalitzats")
    part(doc)
    doc.append(NoEscape(pic.recta_interval(-1, 1, False, True)))
    part(doc)
    doc.append(NoEscape(pic.recta_interval(4, "inf", True, False)))
    part(doc)
    doc.append(NoEscape(pic.recta_interval("-inf", 3, False, True)))
    end(doc, "parts")
    end(doc, "multicols")

    # coses antigues
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

    end(doc, "multicols")
    end(doc, 'parts')

    question(doc, "42")
    doc.append(r"Taula formulació inorgànica ions, diatòmics i ozó")
    doc.append(NoEscape(R"\\"))
    obretaula(doc, taulaconfig(4, "c", [0, 1, -1]))
    filataula(doc, ["Símbol", "Nomenclatura Stock", "Nomenclatura Sistemàtica", "Nom comú"])
    for x in range(12):
        filataula(doc, qgen.finorg(1), py=10)
    tancataula(doc)

    question(doc, "42")
    doc.append(r"Taula de nomenclatura negativa")
    doc.append(NoEscape(R"\\"))
    obretaula(doc, "||c|c|c||c|c||c|c||")
    filataula(doc, ["Z", "Símbol", "Element", "Valències Positives", "València negativa", "Ió negatiu", "Nom negatiu"])
    for z in range(118):
        if "vn" in qgen.elements[z]:
            if "vp" in qgen.elements[z]:
                vp = ", ".join([f"{v}" for v in qgen.elements[z]["vp"]])
            else:
                vp = "-"
            filataula(doc, [f"{z}",
                       qgen.elements[z]["sym"],
                       qgen.elements[z]["nom"],
                       vp,
                       ", ".join([f"{v}" for v in qgen.elements[z]["vn"]]),
                       qgen.symio(z, qgen.elements[z]["vn"][0]),
                       qgen.nomio(z, qgen.elements[z]["vn"][0], True)
                       ])
    tancataula(doc)

    question(doc, "52")
    doc.append(r"Taula zapne d'isòtops")
    n = 30
    header = [envt("Nom", 6), envt("Símbol"), envt("Z"), envt("A"), envt("p"), envt("n"), envt("e"), envt("càrrega", 1)]
    obretaula(doc, taulaconfig(8, "c", [0, 2, 4, 7, -1]), header=header)
    # trio per avançat la selecció d'elements (z petits però no repetits)
    prezs = random.sample(qgen.els_ist[0:min(max(n + 10, 40), 117)], n)  # min 40, màx n+10, però no més de 117
    for x in range(n):
        filataula(doc, qgen.fisotops(1, 2, prez=prezs[x % n]), py=10)
    tancataula(doc)

    question(doc, "42")
    doc.append(r"Vaig a veure si faig una taula de molècules.")
    doc.append(NoEscape(R"\\"))
    space(doc, "1cm")
    # taula
    obretaula(doc, "||c||c|c|c||")
    filataula(doc, ["Molècula", "Nomenclatura Stock", "Nomenclatura Sistemàtica", "Nom comú"])
    for x in range(6):
        filataula(doc, qgen.finorg(10, 1), py=10)
    doc.append(NoEscape(r"\hline"))
    for x in range(6):
        filataula(doc, qgen.finorg(10, 2), py=10)
    doc.append(NoEscape(r"\hline"))
    for x in range(6):
        filataula(doc, qgen.finorg(10, 3), py=10)
    doc.append(NoEscape(r"\hline"))
    for x in range(6):
        filataula(doc, qgen.finorg(10, 4), py=10)
    tancataula(doc)

    question(doc, "30")
    doc.append(r"Vaig a veure si puc fer una taula d'isòtops")
    doc.append(NoEscape(R"\\"))
    space(doc, "1cm")
    # taula
    obretaula(doc, "||c|c|c||c|c||c|c||")
    filataula(doc, ["Z", "Símbol", "Element", "Valències Positives", "València negativa", "Ió més estable", "Nom ió"])
    for x in range(119):
        vp = "-"
        vn = "-"
        ime = "-"
        io = "-"
        if "vp" in qgen.elements[x]:
            vp = ", ".join([f"{v}" for v in qgen.elements[x]["vp"]])
            print(vp)
        if "vn" in qgen.elements[x]:
            vn = ", ".join([f"{v}" for v in qgen.elements[x]["vn"]])
        if "ime" in qgen.elements[x]:
            ime = qgen.elements[x]['ime']
            if ime == 1:
                exp = "+"
            elif ime == -1:
                exp = "-"
            elif ime > 0:
                exp = f"{ime}+"
            else:
                exp = f"{abs(ime)}-"
            ime = r"$\isotope{" + qgen.elements[x]["sym"] + "}^{" + exp + "}$"
        if "ime" in qgen.elements[x]:
            if qgen.elements[x]["ime"] > 0:
                io = "Ió " + qgen.elements[x]["nom"]
                if vp != "-":
                    if len(qgen.elements[x]["vp"]) > 1:
                        io += f" ({qgen.romans[qgen.elements[x]['ime']]})"
            else:
                if "nneg" in qgen.elements[x]:
                    io = "Ió " + qgen.elements[x]["nneg"]
                else:
                    io = "(Anió " + qgen.elements[x]["nom"] + ")"

        if not all([v == "-" for v in [vp, vn]]):
            filataula(doc, [f"{x}", qgen.elements[x]["sym"], qgen.elements[x]["nom"], vp, vn, ime, io])
    #filataula(doc, ["Símbol", "Nomenclatura Stock", "Nomenclatura Sistemàtica", "Nom Comú"])
    tancataula(doc)

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
    elif tema == "frac":
        return "fraccions"
    elif tema == "ncient":
        return "ncient"
    elif tema == "prop":
        return "proporcionalitat"
    elif tema == "px":
        return "polinomis"
    elif tema == "succ":
        return "successions"
    elif tema == "dx":
        return "derivades"
    elif tema == "lim":
        return "limits"
    # química
    elif tema == "q_formul":
        return "formulacio"
    elif tema == "q_iso":
        return "isotops"
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
    elif tema == "frac":
        return "de Fraccions"
    elif tema == "ncient":
        return "de Notació Científica i Errors"
    elif tema == "prop":
        return "de Proporcionalitat"
    elif tema == "px":
        return "de Polinomis"
    elif tema == "succ":
        return "de Successions"
    elif tema == "dx":
        return "de Derivades"
    # química
    elif tema == "q_formul":
        return "de Formulació"
    elif tema == "q_iso":
        return "d'Isòtops"
    # res
    elif tema == "no":
        return "de Qui sap què"
    else:
        return "de " + tema.title()


def quantesson(value, op):
    n = ["no", "poques", "normal", "moltes", "mitja", "plana", "doble"].index(value)
    return quantes_son(n, op)


def quantes_son(n, op):
    # enters
    if op == "sumes":
        quantitats = [0, 8, 20, 32, 48, 112, 200]
    elif op == "psumes":
        quantitats = [0, 9, 18, 27, 42, 87, 174]
    elif op in ["multis", "divis"]:
        quantitats = [0, 8, 20, 32, 48, 104, 200]
    elif op in ["smultis", "sdivis"]:
        quantitats = [0, 8, 15, 27, 42, 87, 174]
    elif op == "combis":
        quantitats = [0, 3, 6, 9, 9, 18, 39]
    # més xifres
    elif op == "v_sumes":
        quantitats = [0, 4, 8, 12, 16, 35, 76]
    elif op == "v_dsumes":
        quantitats = [0, 4, 8, 12, 16, 35, 76]
    elif op == "v_restes":
        quantitats = [0, 4, 8, 12, 16, 35, 76]
    elif op == "v_drestes":
        quantitats = [0, 4, 8, 12, 16, 35, 76]
    elif op == "v_multis":
        quantitats = [0, 3, 6, 9, 12, 28, 60]
    elif op == "v_dmultis":
        quantitats = [0, 3, 6, 9, 12, 24, 50]
    elif op == "v_divis":
        quantitats = [0, 3, 6, 9, 12, 28, 58]
    elif op == "v_ddivis":
        quantitats = [0, 3, 6, 9, 12, 24, 48]
    # potències i arrels
    elif op in ["p_mexp", "p_mbase", "arrels"]:
        quantitats = [0, 3, 6, 12, 21, 48, 101]
    elif op in ["p_mexp_45", "p_mbase_45", "arrels_45"]:
        quantitats = [0, 4, 6, 8, 14, 32, 68]
    elif op == "p_frac":
        quantitats = [0, 3, 6, 9, 17, 35, 71]
    elif op in ["p_ffrac", "p_dfrac"]:
        quantitats = [0, 2, 3, 6, 17, 35, 71]
    elif op in ["combradi"]:
        quantitats = [0, 4, 7, 11, 28, 59, 124]
    elif op in ["a_extreure", "a_introd"]:
        quantitats = [0, 4, 8, 12, 32, 66, 132]
    elif op in ["fextreure"]:
        quantitats = [0, 3, 6, 9, 21, 50, 104]
    elif op in ["asum"]:
        quantitats = [0, 2, 4, 8, 16, 34, 69]
    elif op in ["racions"]:
        quantitats = [0, 3, 6, 12, 18, 39, 86]
    # fraccions
    elif op in ["fr_sumes", "fr_multis"]:
        quantitats = [0, 3, 6, 12, 18, 37, 74]
    elif op == "fr_combis":
        quantitats = [0, 3, 6, 9, 11, 22, 50]
    elif op == "fgen":
        quantitats = [0, 4, 8, 12, 24, 52, 112]
    # notació científica
    elif op in ["cientanum", "numacient"]:
        quantitats = [0, 4, 12, 20, 30, 60, 120]
    elif op == "nc_muldiv":
        quantitats = [0, 2, 4, 8, 12, 26, 56]
    # equacions
    elif op == "idvseq":
        quantitats = [0, 2, 4, 8, 15, 33, 66]
    elif op == "simples":
        quantitats = [0, 4, 10, 12, 20, 50, 100]  # arrodonit avall (2) per evitar migpunts
    elif op == "dsimples":
        quantitats = [0, 3, 8, 9, 16, 32, 68]
    elif op == "incomps":
        quantitats = [0, 6, 9, 12, 15, 33, 66]
    elif op == "completes":
        quantitats = [0, 6, 9, 12, 15, 33, 66]
    elif op in ["polis", "1polis"]:
        quantitats = [0, 2, 4, 8, 10, 22, 44]
    elif op == "1racios":
        quantitats = [0, 2, 4, 8, 10, 20, 41]
    elif op in ["sistemes", "nsistemes"]:
        quantitats = [0, 3, 6, 9, 12, 29, 45]
    elif op == "gsistemes":
        quantitats = [0, 2, 3, 6, 12, 29, 45]
    elif op == "sistemes3":
        quantitats = [0, 3, 6, 9, 12, 27, 56]
    # proporcionalitat
    elif op == "directes":
        quantitats = [0, 3, 4, 5, 6, 12, 25]
    elif op == "inverses":
        quantitats = [0, 3, 4, 5, 6, 11, 22]
    elif op == "barrejades":
        quantitats = [0, 3, 4, 5, 6, 11, 23]
    # polinomis
    elif op == "px_monomi":
        quantitats = [0, 2, 4, 8, 24, 52, 108]
    elif op in ["px_invent", "px_aval", "px_residu"]:
        quantitats = [0, 1, 3, 5, 6, 12, 26]
    elif op == "px_fcomu":
        quantitats = [0, 2, 4, 6, 12, 26, 54]
    elif op == "px_cryp":
        quantitats = [0, 1, 2, 3, 4, 7, 14]
    elif op in ["px_idnot", "px_eidnot"]:
        quantitats = [0, 2, 4, 8, 20, 44, 88]
    elif op in ["px_sumes", "px_restes"]:
        quantitats = [0, 2, 3, 4, 5, 12, 24]
    elif op in ["px_multis", "px_rufis", "px_divis"]:
        quantitats = [0, 2, 3, 4, 5, 12, 24]
    elif op == "px_factor":
        quantitats = [0, 2, 3, 6, 12, 20, 46]
    elif op == "px_algeb":
        quantitats = [0, 1, 2, 4, 5, 10, 51]
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
    # ************* química ************* #
    # formulació inorgànica
    elif op in ["q_simples", "q_hidrurs", "q_oxids", "q_sbin", "q_hidroxids"]:
        quantitats = [0, 3, 5, 8, 11, 22, 52]
    elif op in ["q_f_barreja"]:
        quantitats = [0, 5, 8, 10, 11, 22, 52]
    elif op in ["q_zapne"]:
        quantitats = [0, 3, 5, 8, 11, 22, 52]
    else:
        quantitats = [0, 8, 20, 32, 48, 112, 200]
        print("no he trobat el codi " f"{op}")
    return quantitats[n]


def quantesvariant(valor):
    if valor == "poques":
        return 1
    elif valor == "meitat":
        return 2
    elif valor == "moltes":
        return 3
    elif valor == "totes":
        return 4
    else:
        return 0


# *************************** Common Blocks ******************************* #

def margins():
    return {"tmargin": "39mm", "lmargin": "15mm", "bmargin": "20mm", "rmargin": "15mm"}


def headfoot(doc, opcions, tema="no", assig="Matemàtiques"):
    tema = tematitol(tema)
    if 'curs' in opcions and opcions['curs'] != "Dificultat al Gust":
        curs = f" - {opcions['curs']}"
    else:
        curs = ""
    # header and footer
    doc.preamble.append(Command('pagestyle', "headandfoot"))
    doc.preamble.append(Command('runningheadrule'))
    doc.preamble.append(Command('footrule'))
    doc.preamble.append(Command('firstpageheadrule'))
    doc.preamble.append(NoEscape(r"\SolutionEmphasis{\raggedright}"))  # (esto me lo sugirió uno en TeX.StackExchange)
    doc.preamble.append(NoEscape(
        r"\firstpageheader{}{\hrulefill \\ \bfseries\LARGE Fitxa " + tema + r"\\ \vspace*{1mm} \large " + assig
        + f"{curs} " r"\scriptsize \\ \hrulefill \\  "
        + r"\small\mdseries Fitxa generada automàticament amb Dynamic Deures (http://bit.ly/DynamicDeures)}{}"))
    assig_mini = "Mates" if assig == "Matemàtiques" else assig
    doc.preamble.append(NoEscape(r"\runningheader{" + assig_mini
                                 + " de %s}{Fitxa %s}{Dynamic Deures}" % (opcions["curs"], tema)))
    doc.preamble.append(NoEscape(r"\footer{Total: \numpoints\ punts}{Pàgina \thepage /\numpages}{David Ruscalleda}"))

    return


def myconfig(doc, solucions=False):
    doc.append(NoEscape(r'\raggedcolumns'))  # permís per columnes desiguals (arregla una mica l'espaiat de l'última)
    doc.append(NoEscape(r'\pointpoints{punt}{punts}'))
    doc.append(NoEscape(r'\bracketedpoints'))
    doc.append(NoEscape(r'\addpoints'))
    doc.append(NoEscape(r'\renewcommand{\solutiontitle}{\noindent\textbf{Solucions: }\noindent}'))  # \par si vols break
    if solucions:
        doc.append(NoEscape(
            r'\printanswers'))  # Marca les respostes correctes dels multiopció i mostra les respostes definides
    return


# ********************* Aliases PyLaTeX **********************# TODO quitar de aquí y dejar sólo rpy.

# ésta en concreto no la he pasado a rpy, porque es como raruna
def uncalcul(doc, quin=[1, 1], sp="0.7cm"):  # op és llista d'opcions del generador
    part(doc)
    doc.append(NoEscape(r'$%s$' % gen.comb(*quin)))  # asterisc separa la llista i els envia individualment
    space(doc, sp)
    return


# *********************************** EXTERNAL FUNCTIONS *********************************** #


def parse_multi_form(form):
    """ Gets fake array (dict) from an html form and converts it to a proper dict (seems to work)

    Got it from Stack Overflow https://stackoverflow.com/a/49819417/5093220
    """
    data = {}
    for url_k in form:
        v = form[url_k]
        ks = []
        while url_k:
            if '[' in url_k:
                k, r = url_k.split('[', 1)
                ks.append(k)
                if r[0] == ']':
                    ks.append('')
                url_k = r.replace(']', '', 1)
            else:
                ks.append(url_k)
                break
        sub_data = data
        for i, k in enumerate(ks):
            if k.isdigit():
                k = int(k)
            if i+1 < len(ks):
                if not isinstance(sub_data, dict):
                    break
                if k in sub_data:
                    sub_data = sub_data[k]
                else:
                    sub_data[k] = {}
                    sub_data = sub_data[k]
            else:
                if isinstance(sub_data, dict):
                    sub_data[k] = v

    return data