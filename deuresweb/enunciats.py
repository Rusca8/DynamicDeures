import random

aes = [["a", "es"], ["", "s"]]
aen = ["a", "en"]
caquen = ["ca", "quen"]
noen = ["", "en"]
noa = ["a", ""]
lales = [["la", "les"], ["el", "els"]]
uuna = ["una", "ú"]
esessin = ["és", "essin"]
tdes = [["da", "des"], ["t", "ts"]]

poderf = ["podré", "podràs", "podrà", "podrem", "podreu", "podran"]
trigar = ["trigo", "trigues", "triga", "triguem", "trigueu", "triguen"]
trigarf = ["trigaré", "trigaràs", "trigarà", "trigarem", "trigareu", "trigaran"]
trigarc = ["trigaria", "trigaries", "trigaria", "trigaríem", "trigaríeu", "trigarien"]

haverc = ["hauria", "hauries", "hauria", "hauríem", "hauríeu", "haurien"]
sersubj = ["fos", "fossis", "fos", "fóssim", "fóssiu", "fossin"]

voler = ["vull", "vols", "vol", "volem", "voleu", "volen"]

possing = [["meva", "teva", "seva", "nostra", "vostra", "seva"], ["meu", "teu", "seu", "nostre", "vostre", "seu"]]


def propsimple(tipus, x, y, x2, y2):
    directa = [1, 2, 3]  # enunciats de directa
    inversa = [11]  # enunciats d'inversa
    enunciat = ""
    if tipus == 1:
        esquelet = random.choice(directa)
    elif tipus == 2:
        esquelet = random.choice(inversa)
    else:
        esquelet = random.choice(directa + inversa)

    if esquelet == 1:  # Per fer X coses calen Y materials
        verb, gc, cosa, gm, material = triacoses(esquelet)
        vaux1 = random.choice([f"em cal{noen[sp(y)]}", f"es necessit{aen[sp(y)]}"])
        vaux2 = random.choice(["em calen", "necessito"])
        if moneda():
            enunciat = f"Per {verb} {x} {cosa[sp(x)]} {vaux1} {y} {material[sp(y)]}. "
        else:
            vaux3 = random.choice([["Si tinc", "puc"], ["Necessito", "per"]])
            enunciat = f"{vaux3[0]} {y} {material[sp(y)]} {vaux3[1]} {verb} {x} {cosa[sp(x)]}. "
        if moneda():
            enunciat += f"Quant{aes[gc][1]} {cosa[1]} puc {verb} amb {y2} {material[sp(y2)]}?"
        else:
            enunciat += f"Quant{aes[gm][1]} {material[1]} {vaux2} per {verb} {x2} {cosa[sp(x2)]}?"

    elif esquelet == 2:  # En X bosses hi ha Y coses
        verb, gr, recipient, gc, cosa = triacoses(esquelet)
        enunciat = f"En {x} {recipient[sp(x)]} {verb[sp(y)]} {y} {cosa[sp(y)]}. "
        if moneda():
            enunciat += f"Quant{aes[gc][1]} {cosa[1]} {verb[1]} en {x2} {recipient[sp(x2)]}?"
        else:
            enunciat += f"Quant{aes[gr][1]} {recipient[1]} necessito per {verb[2]} {y2} {cosa[sp(y2)]}?"

    elif esquelet == 3:  # X es buida en Y minuts
        verbnum, verb, gc, cosa, gt, temp = triacoses(esquelet)
        p, subj = subjectes(esquelet, verbnum)
        f = febles(esquelet, verbnum)
        enunciat = f"{subj} {verb} {x} {cosa[sp(x)]} en {y} {temp[sp(y)]}. "
        if moneda():
            enunciat += f"Quant{aes[gc][1]} {cosa[1]} {poderf[p]} {verb}{f[p]} en {y2} {temp[sp(y2)]}?"
        else:
            enunciat += f"Quant {trigarf[p]} a {verb}{f[p]} {x2} {cosa[sp(x2)]}?"

    elif esquelet == 10:  # X treballadors triguen Y a fer una tasca
        tasca, ntreb, gtreb, treb, gt, temp = triacoses(esquelet, x)  # en aquest passo quants són per la tasca
        ntreb = ntreb + sp(x)*3
        if moneda():
            enunciat = f"{x} {treb[sp(x)]} {trigar[ntreb]} {y} {temp[sp(y)]} a {tasca}. "
        else:
            enunciat = f"Per {tasca} en {y} {temp[sp(y)]} cal{noen[sp(x)]} {x} {treb[sp(x)]}. "
            # TODO ajustar "en calen" vs "calen" en funció del subjecte?
        # TODO variants amb ahir vs avui, sabem que, etc
        if moneda():
            enunciat += f"Quant {trigarc[ntreb]} si {sersubj[ntreb%3+3*sp(x2)]} {x2}?"
        else:
            vaux1 = random.choice(["per", f"si {voler[ntreb%3+3]}"])
            enunciat += f"Quant{aes[gtreb][1]} {haverc[ntreb%3+3]} de ser {vaux1} trigar {y2} {temp[sp(y2)]}?"

    elif esquelet == 11:  # a X persones els toca Y d'un tresor
        tresornum, gt, tresor, gp, persona = triacoses(esquelet)
        if tresornum == 1:
            if x == 1:
                enunciat = (f"Si {x} {persona[0]} es queda {tresor[0]} per ell{noa[gp]} sol{noa[gp]}"
                            f" li to{caquen[sp(y)]} {y} {tresor[1][sp(y)]}. ")
            else:
                enunciat = (f"Si {x} {persona[1]} es reparteixen {tresor[0]},"
                            f" els to{caquen[sp(y)]} {y} {tresor[1][sp(y)]} per cada un{noa[gp]}. ")
            if moneda():
                enunciat += f"Quant{aes[gp][1]} haurien de ser per què els en toqu{esessin[sp(y2)]} {y2}?"
            else:
                enunciat += f"Quant{aes[gt][1]} n'hi hauria per cadasc{uuna[gp]} si fossin {x2}?"

        else:  # X persones s'han trobat un tresor amb Y coses dins
            if x == 1:
                enunciat = f"{x} {persona[0]} s'ha trobat {tresor[0]} on n'hi havia {y}. "
            else:
                if moneda():
                    enunciat = f"Un grup de {x} {persona[1]} s'ha trobat {tresor[0]}, "
                    if random.choice([0, 0, 1]):
                        enunciat += f"i n'han tocat {y} per cada un{noa[gp]}. "
                    elif moneda():
                        enunciat += f"i cadascun{noa[gp]} se n'ha quedat {y}. "
                    else:
                        enunciat += f"i n'han pogut repartir {y} per cap. "
                else:
                    enunciat = f"{x} {persona[1]} s'han trobat {tresor[0]}, "
                    if moneda():
                        enunciat += f"i se n'han quedat {y} cadascun{noa[gp]}. "
                    else:
                        enunciat += f"i n'han repartit {y} per cadascun{noa[gp]}. "
            if moneda():
                var1 = random.choice(["per quedar-se'n", "per tal que els en toquessin", "per aconseguir-ne"])
                if moneda():
                    enunciat += f"Quant{aes[gp][1]} haurien de ser {var1} {y2}?"
                else:
                    if moneda():
                        enunciat += f"A quanta gent li haurien de fer la pirula {var1} {y2}?"
                    else:
                        var2 = random.choice([f"{lales[gp][1]} altres en tinguessin", "a la resta els en toquin",
                                              f"{lales[gp][1]} altres en puguin aconseguir"])
                        enunciat += f"Quant{aes[gp][1]} haurien de marxar plorant per què {var2} {y2}?"
            else:
                var1 = random.choice(["en tocarien per cap", "se'n podrien quedar", "n'aconseguirien"])
                enunciat += f"Quant{aes[gt][1]} {var1} si fossin {x2}?"
    return enunciat


def subjectes(esquelet, verb=1):
    p = 0  # jo
    subj = "NINGÚ ENCARA"
    if esquelet == 3:
        if verb in [1, 2]:  # menjar i beure
            if moneda():
                if moneda():
                    subj = "El meu os de peluix es pot"
                    p = 2  # ell
                else:
                    subj = "Tu si t'esforces et pots"
                    p = 1
            elif moneda():
                subj = "El meu camell preferit es pot"
                p = 2
            else:
                subj = "Em puc"
        elif verb in [3, 4]:  # caminar i fer
            if moneda():
                if moneda():
                    subj = "Puc"
                else:
                    subj = "Si vull puc"
            elif moneda():
                if moneda():
                    subj = "Un pangolí experimentat pot"
                    p = 2
                else:
                    subj = "Crec que l'ornitorrinc del meu veí pot"
                    p = 2
            else:
                if moneda():
                    subj = "Aquell senyor que passa per allà pot"
                    p = 2
                else:
                    subj = "Aquella senyora que passa per allà pot"
                    p = 2
        else:
            subj = "NO HAURÍEM DE SER AQUÍ"
    return [p, subj]


def tresors(esquelet, tresornum):
    gt = 0  # f
    if esquelet == 11:
        if tresornum == 1:  # coses que "es volen repartir"
            v = random.randint(1, 6)
            if v == 1:
                tresor = ["les galetes que han robat", ["galeta", "galetes"]]
            elif v == 3:
                tresor = ["les formigues d'un formiguer", ["formiga", "formigues"]]
            elif v == 4:
                tresor = ["les gotes de l'oceà", ["gota", "gotes"]]
            elif v == 5:
                tresor = ["els mocs del president", ["moc", "mocs"]]
                gt = 1
            else:
                tresor = ["les diapositives del treball en grup", ["diapositiva", "diapositives"]]
        if tresornum == 2:  # coses "s'han trobat i n'han pogut repartir"
            v = random.randint(1, 5)
            if v == 1:
                tresor = ["un sac de moniatos", ["moniato", "moniatos"]]
                gt = 1
            elif v == 2:
                tresor = ["un bagul ple de camells", ["camell", "camells"]]
                gt = 1
            elif v == 3:
                tresor = ["un ramat de spaghetti", ["spaghetto", "spaghetti"]]
                gt = 1
            elif v == 4:
                tresor = ["un eixam de polvorons", ["polvoró", "polvorons"]]
                gt = 1
            else:
                tresor = ["un hipopòtam ple de drames", ["drama", "drames"]]
                gt = 1
    else:
        tresor = ["TRESOR NOM 42", "PEÇA NOM 42"]
    return gt, tresor


tipus_tresors = 2


def persones(esquelet, tresornum):
    gp = 0  # f
    pers = ["p42", "p42"]
    if esquelet == 11:
        if tresornum in [1, 2]:  # es reparteixen  ||  s'han trobat
            v = random.randint(1, 6)
            if v == 1:
                if moneda():
                    pers = ["paio", "paios"]
                    gp = 1
                else:
                    pers = ["xica", "xiques"]
            elif v == 2:
                pers = ["equilibrista", "equilibristes"]
                if moneda():
                    gp = 1
            elif v == 3:
                if moneda():
                    pers = ["ventríloc", "ventrílocs"]
                    gp = 1
                else:
                    pers = ["ventríloqua", "ventríloqües"]
            elif v == 4:
                pers = ["macarró solitari", "macarrons solitaris"]
                gp = 1
            elif v == 5:
                if tresornum == 1:
                    pers = ["estàtua (però que es mou)", "estàtues (però que es mouen)"]
                elif tresornum == 2:
                    pers = ["estàtua (però que es movia)", "estàtues (però que es movien)"]
            elif v == 6:
                pers = ["cacauet divertit", "cacauets divertits"]
                gp = 1
            elif v == 7:
                if moneda():
                    pers = ["sabata abandonada", "sabates abandonades"]
                else:
                    pers = ["incomodíssima sabata de tacó", "incomodíssimes sabates de tacó"]
            elif v == 8:
                pers = ["panellet", "panellets"]
                gp = 1
            elif v == 9:
                pers = ["cabra boja", "cabres boges"]
            elif v == 10:
                if moneda():
                    pers = ["dutxa burocràtica", "dutxes burocràtiques"]
                else:
                    pers = ["banyera exòtica", "banyeres exòtiques"]
            # TODO corregir nums v
    return [gp, pers]


def tasques(esquelet, tascanum, nre=2):
    tasca = "NI IDEA"
    if esquelet == 10:
        if tascanum == 1:  # tema antàrtida
            v = random.randint(1, 5)
            if v == 1:
                tasca = "fer un iglú molt bonic"
            elif v == 2:
                tasca = "fer un ninot de neu"
            elif v == 3:
                tasca = f"cruspir{febles(esquelet, 1)[nre]} tots els investigadors de l'antàrtida"
            elif v == 4:
                tasca = "matxacar-nos en una guerra de boles de neu"
            elif v == 5:
                tasca = f"pescar el {possing[1][nre]} sopar"
        elif tascanum == 2:  # tema robatoris i malifetes
            v = random.randint(1, 5)
            if v == 1:
                tasca = "preparar una festa sorpresa que no és per mi"
            elif v == 2:
                tasca = f"menjar{febles(esquelet, 1)[nre]} totes les galetes que havia fet a l'exercici anterior"
            elif v == 3:
                tasca = f"emportar{febles(esquelet, 1)[nre]} totes les joies que tinc"
            elif v == 4:
                tasca = f"pintar la {possing[0][random.choice([1, 3])]} cara en un graffiti"
            elif v == 5:
                if moneda():
                    tasca = f"maquinar un pla malèfic que sort que no el saps, perquè t'espantaries"
                else:
                    tasca = f"maquinar un pla malèfic"
    return tasca


tasques_inv = 2  # tasques de proporcionalitat simple inversa.


def treballadors(esquelet, tascanum):
    nt = 2  # 3a pers
    gt = 0  # f
    if esquelet == 10:
        if tascanum == 1:  # iglú
            v = random.randint(1, 5)
            if v == 1:
                treb = ["pingüí eixerit", "pingüins eixerits"]
                gt = 1
            elif v == 2:
                treb = ["tauró amb ganes de caminar", "taurons amb ganes de caminar"]
                gt = 1
            elif v == 3:
                treb = ["foca menjacrancs", "foques menjacrancs"]
            elif v == 4:
                if moneda():
                    treb = ["esquimal ben abrigat", "esquimals ben abrigats"]
                    gt = 1
                else:
                    treb = ["esquimal ben abrigades", "esquimals ben abrigades"]
            else:
                treb = ["ós polar (dels amables)", "óssos polars (dels amables)"]
                gt = 1
        elif tascanum == 2:  # robatoris i malifetes
            v = random.randint(1, 4)
            if v == 1:
                if moneda():
                    treb = ["amic meu", "dels meus amics"]
                    gt = 1
                else:
                    treb = ["amiga meva", "de les meves amigues"]
            elif v == 2:
                if moneda():
                    treb = ["lladregot", "lladregots"]
                    gt = 1
                else:
                    treb = ["lladregota", "lladregotes"]
                if moneda():
                    treb = [s + " que he contractat" for s in treb]
                else:
                    treb = [s + " que no hauria d'haver contractat" for s in treb]
            elif v == 3:
                treb = ["ós rentador sospitós", "óssos rentadors sospitosos"]
                gt = 1
            elif v == 4:
                if moneda():
                    treb = ["com tu, que ets un xungo,", "com tu, que ets un xungo,"]
                    gt = 1
                    nt = 1 # tu/vosaltres
                else:
                    treb = ["com tu, que ets una xunga,", "com tu, que ets una xunga"]
                    nt = 1
            else:
                treb = ["ERROR DE LLADREGOT", "ERRORS DE LLADREGOT"]
    return [nt, gt, treb]


def verbs(esquelet, verb):
    if esquelet == 1:
        if verb == 1:
            if random.choice([0, 1, 1]):
                return "fabricar"
            elif moneda():
                return "construir"
            else:
                return "fer"
        elif verb == 2:
            if moneda():
                return "cuinar"
            else:
                return "preparar"
    elif esquelet == 2:
        if verb == 1:
            if moneda():
                return ["hi cap", "hi caben", "guardar"]
            else:
                return ["puc amagar", "puc amagar", "amagar"]
        elif verb == 2:
            if random.choice([0,0,1]):
                return ["hi ve", "hi venen", "tenir"]
            elif moneda():
                return ["hi ha", "hi ha", "aconseguir"]
            else:
                return ["em trobo", "em trobo", "trobar-me"]
        elif verb == 3:
            return ["et posen", "et posen", "què em posin"]
        else:
            return ["VERB INEXISTENT", "VERB INEXISTENT", "VERB INEXISTENT"]
    elif esquelet == 3:
        if verb == 1:
            return "menjar"
        elif verb == 2:
            return "beure"
        elif verb == 3:
            if moneda():
                return "recórrer"
            else:
                return "caminar"
        elif verb == 4:
            return "fer"


verbs_cabre = 3
verbs_trigar = 4


def febles(esquelet, verbnum=1):
    f = ["", "", "", "", "", ""]
    if esquelet == 3:
        if verbnum == 1:  # menjar
            f = ["-me", "-te", "-se", "-nos", "-vos", "-se"]
        elif verbnum == 2: # beure
            f = ["'m", "'t", "'s", "'ns", "-us", "'s"]
    elif esquelet == 10:
        if verbnum == 2:
            return febles(3, 2)
        else:
            return febles(3, 1)
    return f


def coses(esquelet, verb, cosa):
    gc = 0
    if esquelet == 1:
        if verb == 1:  # fabricar
            if cosa == 1:
                c = ["vaca", "vaques"]
            elif cosa == 2:
                c = ["girafa", "girafes"]
            elif cosa == 3:
                c = ["edifici tot fashion", "edificis tot fashions"]
                gc = 1
            elif cosa == 4:
                c = ["pela-pipes automàtic", "pela-pipes automàtics"]
                gc = 1
            elif cosa == 5:
                c = ["avió", "avions"]
                gc = 1
            elif cosa == 6:
                c = ["iglú", "iglús"]
                gc = 1
            else:
                c = ["WUT THIS DOESN'T EXIST 4", "WUT THIS DOESN'T EXIST 4"]
        elif verb == 2:  # cuinar
            if cosa == 1:
                v = random.randint(1, 3)
                if v == 1:
                    c = ["galeta", "galetes"]
                elif v == 2:
                    c = ["pastís", "pastissos"]
                    gc = 1
                elif v == 3:
                    c = ["brownie", "brownies"]
                    gc = 1
            elif cosa == 2:
                c = ["ració de sopa", "racions de sopa"]
            else:
                c = ["WUT THIS DOESN'T EXIST 3", "WUT THIS DOESN'T EXIST 3"]
        else:
            c = ["WUT THIS DOESN'T EXIST 2", "WUT THIS DOESN'T EXIST 2"]
    elif esquelet == 2:
        if verb == 1:  # caben
            var = random.choice([1, 2, 3, 4])
            if var == 1:
                c = ["pinya", "pinyes"]
            elif var == 2:
                c = ["rinoceront", "rinoceronts"]
                gc = 1
            elif var == 3:
                c = ["llauna de suc de càctus", "llaunes de suc de càctus"]
            elif var == 4:
                c = ["gra d'arròs", "grans d'arròs"]
        elif verb == 2:  # venen
            if cosa == 1:
                if random.choice([0, 0, 1]):
                    c = ["ml d'aire", "ml d'aire"]
                    gc = 1
                elif moneda():
                    c = ["patata gegant", "patates gegants"]
                else:
                    c = ["kg de sal", "kg de sal"]
                    gc = 1
            else:
                if moneda():
                    c = ["llàgrima de xocolata", "llàgrimes de xocolata"]
                else:
                    var = random.choice(["del cuiner", "de la cuinera"])
                    c = [f"pèl {var}", f"pèls {var}"]
        elif verb == 3:  # et posen
            if random.choice([0, 0, 1]):
                c = ["pàgina de deures", "pàgines de deures"]
            elif moneda():
                c = ["examen", "exàmens"]
                gc = 1
            else:
                c = ["exercici complicadot", "exercicis complicadots"]
                gc = 1
        else:
            c = ["NI IDEA TU", "NI IDEES TU"]
    elif esquelet == 3:
        if verb == 1:  # menjar
            v = random.randint(1, 7)
            if v == 1:
                c = ["plat de nuggets cruixent", "plats de nuggets cruixents"]
                gc = 1
            elif v == 2:
                c = ["dotzena de bikinis", "dotzenes de bikinis"]
            elif v == 3:
                c = ["pot d'ungles de mosca", "pots d'ungles de mosca"]
                gc = 1
            elif v == 4:
                c = ["caixa de gomes d'esborrar", "caixes de gomes d'esborrar"]
            elif v == 5:
                c = ["bol de cues de pansa", "bols de cues de pansa"]
                gc = 1
            elif v == 6:
                c = ["muntanya de peles de cigró", "muntanyes de peles de cigró"]
            else:
                c = ["magdalena que hi ha aquí a terra", "magdalenes que hi ha aquí a terra"]

        elif verb == 2:  # beure
            v = random.randint(1, 6)
            if v == 1:
                c = ["got de suc de cactus", "gots de suc de cactus"]
                gc = 1
            elif v == 2:
                c = ["banyera sencera", "banyeres senceres"]
            elif v == 3:
                c = ["marmita de sopa", "marmites de sopa"]
            elif v == 4:
                c = ["flascó de pintaungles", "flascons de pintaungles"]
                gc = 1
            elif v == 4:
                c = ["pot de llàgrimes d'unicorn", "pots de llàgrimes d'unicorn"]
                gc = 1
            else:
                c = ["pot de mocs", "pots de mocs"]
                gc = 1
        elif verb == 3:  # caminar
            c = ["km", "km"]
            gc = 1
        elif verb == 4:  # fer
            v = random.randint(1, 4)
            if v == 1:
                c = ["dibuix", "dibuixos"]
                gc = 1
            elif v == 2:
                c = ["rotonda grossa i lletja", "rotondes grosses i lletges"]
            elif v == 3:
                c = ["exercici d'aquests que m'han posat de deures", "exercicis d'aquests que m'han posat de deures"]
            else:
                c = ["mica de pena", "miques de pena"]
        else:
            c = ["NO SE PAS", "NO SE PASOS"]
    else:
        c = ["WUT THIS DOESN'T EXIST 1", "WUT THIS DOESN'T EXIST 1"]
    return [gc, c]


coses_fab = 5  # esquelet 1
coses_cui = 2
coses_menjar = 1  # esquelet 2
coses_beure = 1
coses_caminar = 1
coses_fer = 1


def recipients(esquelet, verb, cosa):
    grec = 0
    if esquelet == 2:
        if verb == 1:  # caben
            v = random.randint(1, 5)
            if v == 1:
                rec = ["nevera de les bones", "neveres de les bones"]
            elif v == 2:
                rec = ["bagul", "baguls"]
                grec = 1
            elif v == 3:
                rec = ["carmanyola", "carmanyoles"]
            elif v == 4:
                rec = ["carretó", "carretons"]
                grec = 1
            elif v == 5:
                rec = ["armari bonic", "armaris bonics"]
                grec = 1
        elif verb == 2:  # venen
            if cosa == 1:
                rec = ["bossa de patates", "bosses de patates"]
            else:
                rec = ["galeta cookie", "galetes cookies"]
        elif verb == 3:  # et posen
            rec = ["dia de classe", "dies de classe"]
            grec = 1
        else:
            rec = ["QUI SAP, NO M'HO ESPERAVA", "QUI SAP, NO M'HO ESPERAVA"]
    return [grec, rec]


recipients_caben = 1
recipients_venen = 2
recipients_etposen = 1


def materials(verb, cosa):
    gmat = 0  # f
    if verb == 1:  # fabricar
        if cosa == 1:  # vaca
            if random.choice([0, 0, 1]):
                mat = ["banya de recanvi", "banyes de recanvi"]
            elif moneda():
                mat = ["vaquipeça", "vaquipeces"]
            else:
                mat = ["taca grossa", "taques grosses"]
        elif cosa == 2:  # girafa
            if moneda():
                mat = ["escala molt alta", "escales molt altes"]
            else:
                mat = ["pot de xarop allargacolls", "pots de xarop allargacolls"]
                gmat = 1
        elif cosa == 3:  # edifici tot fashion
            if random.randint(1, 20) == 3:
                mat = ["arquitecte o sea superguai", "arquitectes o sea superguais"]
                gmat = 1
            elif moneda():
                mat = ["arquitecte", "arquitectes"]
                if moneda():
                    gmat = 1
            else:
                mat = ["maó de colorins", "maons de colorins"]
                gmat = 1
        elif cosa == 4:  # pelapipes
            if random.randint(1, 20) == 3:
                mat = ["rodeta que no sé molt bé què fa", "rodetes que no sé molt bé què fan"]
            else:
                mat = ["cargol", "cargols"]
                gmat = 1
        elif cosa == 5:  # avió
            if moneda():
                mat = ["seient incòmode", "seients incòmodes"]
                gmat = 1
            else:
                mat = ["revista irrellevant", "revistes irrellevants"]
        else:
            mat = ["alguna cosa que en David no m'ha dit", "alguna cosa que en David no m'ha dit"]
    elif verb == 2:  # cuinar
        if cosa == 1:  # galeta
            if moneda():
                mat = ["kg d'espinacs frescos", "kg d'espinacs frescos"]
                gmat = 1
            else:
                mat = ["ml de moc de granota", "ml de moc de granota"]
                gmat = 1
        elif cosa == 2:  # sopa
            if moneda():
                mat = ["grill salvatge", "grills salvatges"]
                gmat = 1
            else:
                mat = ["llimac ben saborós", "llimacs ben saborosos"]
                gmat = 1
        else:
            mat = ["alguna cosa que en David no m'ha dit", "alguna cosa que en David no m'ha dit"]
    else:
        mat = ["WUT THIS DOESN'T EXIST", "WUT THIS DOESN'T EXIST"]
    return [gmat, mat]


def temps(esquelet, verbnum):
    if esquelet == 3:
        gt = 0
        if verbnum in [1, 2]:  # menjar o beure
            t = random.choice([1, 2, 3])
        elif verbnum == 3:  # caminar
            t = random.choice([3, 4])
        else:  # fer
            t = random.choice([2, 3, 4])

        if t == 1:
            temp = ["segon", "segons"]
            gt = 1
        elif t == 2:
            gt = 1
            temp = ["minut", "minuts"]
        elif t == 3:
            temp = ["hora", "hores"]
        else:
            temp = ["dia", "dies"]

    elif esquelet == 10:
        gt, temp = temps(3, random.choice([1, 2, 3, 4]))
    return [gt, temp]


def triacoses(esquelet, x=1):
    if esquelet == 1:  # fabricar coses
        if random.randint(1, coses_fab + coses_cui) <= coses_fab:
            verbnum = 1
        else:
            verbnum = 2
        verb = verbs(esquelet, verbnum)
        if verbnum == 1:  # fab
            cosanum = random.randint(1, coses_fab)  # coses que pots fabricar
        elif verbnum == 2:  # cui
            cosanum = random.randint(1, coses_cui)  # coses que pots cuinar
        gc, cosa = coses(esquelet, verbnum, cosanum)
        gm, material = materials(verbnum, cosanum)
        return [verb, gc, cosa, gm, material]

    elif esquelet == 2:
        verbnum = random.randint(1, verbs_cabre)
        verb = verbs(esquelet, verbnum)
        if verbnum == 1:  # caben
            cosanum = random.randint(1, recipients_caben)  # recipients on caben coses
        elif verbnum == 2:  # vewnen
            cosanum = random.randint(1, recipients_venen)  # recipients on venen coses
        elif verbnum == 3:
            cosanum = random.randint(1, recipients_etposen)  # recipients on et posen coses
        else:
            cosanum = 42
        gr, recipient = recipients(esquelet, verbnum, cosanum)
        gc, cosa = coses(esquelet, verbnum, cosanum)
        return [verb, gr, recipient, gc, cosa]

    elif esquelet == 3:
        verbnum = random.randint(1, verbs_trigar)
        verb = verbs(esquelet, verbnum)
        if verbnum == 1:  # menjar
            cosanum = random.randint(1, coses_menjar)
        elif verbnum == 2:  # beure
            cosanum = random.randint(1, coses_beure)
        elif verbnum == 3:  # caminar
            cosanum = random.randint(1, coses_caminar)
        elif verbnum == 4:  # fer
            cosanum = random.randint(1, coses_fer)
        else:
            cosanum = 42
        gc, cosa = coses(esquelet, verbnum, cosanum)
        gt, temp = temps(esquelet, verbnum)
        return [verbnum, verb, gc, cosa, gt, temp]

    elif esquelet == 10:
        tascanum = random.randint(1, tasques_inv)
        np, gp, persona = treballadors(esquelet, tascanum)
        if random.randint(1, 4) == 1:
            altres = [*range(1, tasques_inv+1)]
            altres.remove(tascanum)
            tascanum = random.choice(altres)  # de tant en tant coses rares, que també fa gràcia
        tasca = tasques(esquelet, tascanum, np + sp(x)*3)  # la última és nombre del verb i febles (jo-ells = 0-5)
        gt, temp = temps(esquelet, tascanum)
        return [tasca, np, gp, persona, gt, temp]

    elif esquelet == 11:
        tresornum = random.randint(1, tipus_tresors)
        gt, tresor = tresors(esquelet, tresornum)
        gp, persona = persones(esquelet, tresornum)
        return [tresornum, gt, tresor, gp, persona]

# *************************** Polinomis ***************************** #


def px_residu(nivell, px, dx, x):
    if nivell == 1:
        if random.randint(0, 3):
            text1 = random.choice([f"Avalua el polinomi $P(x)={px}$", f"Troba el valor numèric del polinomi $P(x)={px}$",
                                   f"Calcula el resultat d'avaluar el polinomi $P(x)={px}$"])
            text2 = random.choice([f" quan $x={x}$.", f" si sabem que la $x$ val ${x}$.", f" per a $x={x}$.",
                                   f" quan la $x$ és ${x}$"])
        else:
            text1 = random.choice([f"Donat el polinomi $P(x)={px}$,", f"Si sabem que $P(x)={px}$,"])
            text2 = random.choice([f" calcula $P({x})$.", f" troba el valor de $P(x)$ quan $x={x}$.",
                                   f" avalua $P(x)$ per $x={x}$."])
        return text1 + text2

    elif nivell == 2:
        text1 = random.choice(["", "Sense fer la divisió,", random.choice(["Fent servir el teorema del residu,",
                               "Aplicant el teorema del residu,", "Mitjançant el teorema del residu,"]),
                               "Utilitzant el mètode que prefereixis,"])
        text2 = (random.choice([" digues quin és", " troba", " calcula"])
                 + random.choice([f" el residu de dividir ${px}$ entre ${dx}$.",
                                 f" el residu de $({px})\\div({dx})$."]))
        if not text1:
            text2 = text2[1:].capitalize()
        return text1 + text2
    else:
        return "No hi ha tants nivells a px_residu"


def px_invent():
    grau = random.randint(2, random.choice([5, 42]))
    text0 = f"de grau {grau}"

    if grau > 4 or moneda():
        text1 = "incomplet"
    else:
        text1 = "complet"

    text2 = random.choice(["ordenat", "desordenat"])

    coef = random.randint(3, random.choice([10, random.choice([42, 1583])])) * random.choice([1, -1])
    if moneda():
        text3 = random.choice([f"amb el terme independent igual a {coef}", f"que el terme independent sigui {coef}",
                               f"amb un {coef} com a terme independent"])
    else:
        grauc = random.randint(1, grau)
        text3 = random.choice([f"que el coeficient del terme de grau {grauc} sigui {coef}",
                               f"amb un {coef} al coeficient del terme de grau {grauc}"])

    if not random.randint(0, 5):
        var = random.choice(["y", "n", "q", "ç", "j", "t", "w"])
        text4 = random.choice(["que la variable no sigui la x", f"que la variable sigui la {var}",
                               f"fent servir la variable {var}", f"amb la {var} en el lloc de la x"])
    else:
        text4 = ""

    text = []
    forats = 0
    for x in [text0, text1, text2, text3, text4]:
        if x and (random.randint(0, 8) or forats > 1):  # màxim esborro 2 condicions (no nul·les)
            text.append(x)
        else:
            forats += 1
    if len(text) > 2:
        intercoma = ", "
    else:
        intercoma = ""
    return text[0].capitalize() + intercoma + ", ".join(text[1:-1]) + " i " + text[-1] + "."

# *************************** Successions *************************** #

def success(tipus, nivell, variant, d, a1, n, an):
    text = "El terme 42 és 42, quin és el terme 42?"
    if tipus == 1:  # successions aritmètiques
        if nivell in [1, 2]: # trobar el terme n
            if moneda():
                text = random.choice([f"El primer terme d'una successió aritmètica és ${a1}$",
                                      f"En una successió aritmètica el primer terme és ${a1}$",
                                      f"En una successió aritmètica, $a_1 = {a1}$"])
                text += random.choice([f", i la diferència entre els termes és ${d}$. ", f" i $d = {d}$. ",
                                       f" i la diferència $d$ és de ${d}$. "])
            else:
                text = random.choice([f"Sabem que el primer terme d'una successió aritmètica és ${a1}$",
                                 f"D'una successió aritmètica sabem que $a_1 = {a1}$"])
                text += random.choice([f", i que la diferència és ${d}$. ",
                                       f", i que els elements estan separats ${d}$ unitats. ",
                                       f" i que $d = {d}$. "])
            text += random.choice(["Quin serà el terme " + f"${n}$?",
                                   f"Quin terme ocuparà la posició ${n}$?",
                                   "Calcula el terme $a_{"+f"{n}"+"}$.", f"Quin serà el ${ordinal(n)}$ terme?"])
        elif nivell == 3 or nivell == 4:
            text = "En una successió aritmètica, "
            ordre = [0, 1, 2, 3]
            random.shuffle(ordre)
            for x in range(3):
                if ordre[x] == 0:
                    text += f"$a_1 = {a1}$"
                elif ordre[x] == 1:
                    text += f"$d = {d}$"
                elif ordre[x] == 2:
                    if ordre[3] == 3:  # em cal (pregunta an)
                        text += f"$n = {n}$"
                elif ordre[x] == 3:
                    if ordre[3] == 2:  # em pregunta n
                        text += f"$a_n = {an}$"
                    else:
                        text += "$a_{" + f"{n}" + "} = " + f"{an}$"
                if x == 2:
                    text += ". "
                else:
                    text += ", "
            if ordre[3] == 0:
                text += "Troba el terme $a_1$ de la successió."
            elif ordre[3] == 1:
                text += "Troba la diferència entre termes."
            elif ordre[3] == 2:
                text += "Quina posició ocupa aquest terme $a_n$?"
            elif ordre[3] == 3:
                text += "Calcula el terme $a_n$."
        elif nivell == 101:  # bulk troba la diferència, el terme general i el terme an
            text = ""
            for x in range(5):
                text += f"{a1 + x * d}, "
            text += r"...\ "
            if variant == 2:  # trobar diferència, terme general i an indicat
                text += " (a_{" + f"{n}" + "}?)"
            elif variant == 3:  # trobar suma dels primers n termes
                text += " (S_{" + f"{n%4+6}" + "}?)"
            elif variant == 4:
                text += " (a_{" + f"{n}" + r"}?\ S_{" + f"{random.randint(5, 15)}" + "}?)"

    if tipus == 2:  # successions geomètriques
        if nivell in [1, 2]: # trobar el terme n
            if moneda():
                text = random.choice([f"El primer terme d'una successió geomètrica és ${a1}$",
                                      f"En una successió geomètrica el primer terme és ${a1}$",
                                      f"En una successió geomètrica, $a_1 = {a1}$"])
                text += random.choice([f", i la raó entre els termes és ${d}$. ", f" i $r = {d}$. ",
                                       f" i la raó $r$ és de ${d}$. "])
            else:
                text = random.choice([f"Sabem que el primer terme d'una successió geomètrica és ${a1}$",
                                      f"D'una successió geomètrica sabem que $a_1 = {a1}$"])
                text += random.choice([f", i que la raó és ${d}$. ",
                                       f" i que $r = {d}$. "])
            text += random.choice(["Quin serà el terme " + f"${n}$?",
                                   f"Quin terme ocuparà la posició ${n}$?",
                                   "Calcula el terme $a_{" + f"{n}" + "}$.", f"Quin serà el ${ordinal(n)}$ terme?"])

        elif nivell == 3 or nivell == 4:
            text = "En una successió geomètrica, "
            ordre = [0, 1, 2, 3]
            random.shuffle(ordre)
            for x in range(3):
                if ordre[x] == 0:
                    text += f"$a_1 = {a1}$"
                elif ordre[x] == 1:
                    text += f"$r = {d}$"
                elif ordre[x] == 2:
                    if ordre[3] == 3:  # em cal (pregunta an)
                        text += f"$n = {n}$"
                elif ordre[x] == 3:
                    if ordre[3] == 2:  # em pregunta n
                        text += f"$a_n = {an}$"
                    else:
                        text += "$a_{"+f"{n}"+"} = " + f"{an}$"
                if x == 2:
                    text += ". "
                else:
                    text += ", "
            if ordre[3] == 0:
                text += "Troba el terme $a_1$ de la successió."
            elif ordre[3] == 1:
                text += "Troba la raó $r$ de la successió."
            elif ordre[3] == 2:
                text += "Quina posició ocupa terme $a_n$?"
            elif ordre[3] == 3:
                text += "Calcula el terme $a_n$."

        elif nivell == 101:  # bulk geomètriques (var 1 = només la successió)
            text = ""
            for x in range(5):
                text += f"{a1 * pow(d, x)}, "
            text += r"...\ "
            if variant == 2:  # trobar diferència, terme general i an indicat
                text += " (a_{" + f"{n}" + "}?)"
            elif variant == 3:  # trobar suma dels primers n termes
                text += " (S_{" + f"{n%4+6}" + "}?)"
            elif variant == 4:
                text += " (a_{" + f"{n}" + r"}?\ S_{" + f"{random.randint(5, 10)}" + "}?)"

    return text


def factorcomu():
    text = "No ha funcionat la cosa em temo"
    var1 = random.choice([1, 1, 2, 2, 2])
    if var1 == 1:  # vull menjar
        t1 = random.choice(["Amb la gana que tinc podria menjar-me",
                            "Voldria menjar-me",
                            "Voldria poder menjar",
                            "Tinc un gran desig de crospir-me"])
        t2, g, p = random.choice([[" el cel blau", 1, 0],
                                  [" el paraigües de la veïna", 1, 0],
                                  random.choice([[" les potes de la millor taula de l'ikea", 0, 1],
                                                 [" el moble de sota el microones", 1, 0]]),
                                  [" un escarabat d'aquells egipcis", 1, 0],
                                  [" els nebots de la gent del poble", 1, 1]])
        t3 = random.choice([" cadascun dels dies" + random.choice([" de la meva vida",
                                                                   " del mes de juliol",
                                                                   " de la setmana"]),
                            f" barreja{tdes[g][p]} amb" + random.choice([" carquinyolis de colors",
                                                                         " suc de cactus",
                                                                         " pèls de ximpanzé"]),
                            f" posa{tdes[g][p]} en forma de sopa de lletres",
                            f" banya{tdes[g][p]} en" + random.choice([" grumolls de colacao",
                                                                      " suor de cocodril",
                                                                      " llàgrimes de cuc de terra"])])
        text = t1 + t2 + t3
    elif var1 == 2:  #
        t1 = random.choice(["El secret més ben guardat d'amèrica és que",
                            "Els meus amics no saben que",
                            "Tots sabem que d'amagat",
                            "Per molt que dissimuli es nota bastant que",
                            "És ben sabut per tots que"])
        t2 = random.choice([" el president",
                            " vostè",
                            random.choice([" la teva germana", " el teu germà"]),
                            ])
        t3 = random.choice([" menja mocs de granota",
                            " s'alimenta d'ulls de sargantana",
                            " baixa al riu a xuclar llimacs",
                            " llepa la bústia del veí de dalt",
                            " parla amb les mosques de casa",
                            " se'n va a viure sota la pica",
                            " posa pinya a la pizza",
                            " barreja nocilla i nutella",
                            " entona cants gregorians"])
        t4 = random.choice([" cada cop que en té la oportunitat",
                            random.choice([" quan hi ha lluna plena", "els dies de lluna plena"]),
                            " un dia sí i altre també",
                            random.choice([" quan no mira ningú", " quan estem tots despistats"]),
                            " perquè li agrada que no vegis"])
        text = t1 + t2 + t3 + t4
    return text


# ****************************** General **************************** #


def sp(num):  # hauràs d'afegir un d'allò per incontable, pero bueno
    if num == 1:
        return 0
    else:
        return 1

def ordinal(num):
    if num in [1, 3]:
        return f"{num}r"
    elif num == 2:
        return f"{num}n"
    elif num == 4:
        return f"{num}t"
    else:
        return f"{num}è"


def moneda():
    return bool(random.getrandbits(1))
