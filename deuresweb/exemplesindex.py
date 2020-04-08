import generator as g

def genera(aleatoris=False):
    ex = {}
    ex["en"] = {}
    ex["omx"] = {}
    ex["eq"] = {}
    ex["pp"] = {}
    if aleatoris:
        ex["en"]["suma1"] = g.comb(1, 3)
        ex["en"]["suma2"] = g.comb(2, 1)
        ex["en"]["suma3"] = g.comb(2, 3)
        ex["en"]["multi1"] = g.comb(3, 1)
        ex["en"]["multi2"] = g.comb(3, 2)
        ex["en"]["multi3"] = g.comb(3, 3)
        ex["en"]["divi1"] = g.comb(3, 4)
        ex["en"]["divi2"] = g.comb(3, 5)
        ex["en"]["divi3"] = g.comb(3, 6)
        ex["eq"]["simple"] = g.eq(2, 3)
        ex["eq"]["sis2d"] = g.sisteq(1, 2)
        ex["eq"]["sis3d"] = g.sisteq(101, 3)
        ex["omx"]["suma"] = g.apilades(1, 1, [3, 2])
        ex["omx"]["sumad"] = g.apilades(1, 2, [3, 2], [2, 2])
        ex["omx"]["resta"] = g.apilades(2, 1, [2, 2])
        ex["omx"]["restad"] = g.apilades(2, 3, [3, 2], [2, 2])
        ex["omx"]["multi"] = g.apilades(3, 1, [3, 2])
        ex["omx"]["multid"] = g.apilades(3, 2, [2, 2], [2, 1])
        ex["pp"]["directa"] = g.prop(1, 1)
        ex["pp"]["inversa"] = g.prop(1, 2)
    else:
        ex["en"]["suma1"] = "3+7="
        ex["en"]["suma2"] = "6-8"
        ex["en"]["suma3"] = "9-(+5)="
        ex["en"]["multi1"] = r"3\times 5"
        ex["en"]["multi2"] = r"2\times (-4)"
        ex["en"]["multi3"] = r"-6\times (-7)"
        ex["en"]["divi1"] = r"20\div 4"
        ex["en"]["divi2"] = r"-36\div 9="
        ex["en"]["divi3"] = r"-42\div (-7)="
        ex["eq"]["simple"] = "2x+5=7"
        ex["eq"]["sis2d"] = r"\begin{cases} x+3y=-14 \\ 5x-3y=-16 \end{cases}"
        ex["eq"]["sis3d"] = r"\begin{cases} x+5y-3z=39 \\ -2x+3y+5z=13 \\ 3x+16y+2z=124 \end{cases}"
        ex["omx"]["suma"] = r"\begin{array}{c}\phantom{+}565\\ \underline{+\phantom{9}64}\\ \end{array}"
        ex["omx"]["sumad"] = r"\begin{array}{c}\phantom{+}115.19\phantom{9}\\ \underline{+\phantom{9}43.658\phantom{}}\\ \end{array}"
        ex["omx"]["resta"] = r"\begin{array}{c}\phantom{-}93\\ \underline{-\phantom{}11}\\ \end{array}"
        ex["omx"]["restad"] = r"\begin{array}{c}\phantom{-}210.16\phantom{9}\\ \underline{-\phantom{9}83.42\phantom{}}\\ \end{array}"
        ex["omx"]["multi"] = r"\begin{array}{c}\phantom{\times99}391\\ \underline{\times\phantom{999}58}\\ \end{array}"
        ex["omx"]["multid"] = r"\begin{array}{c}\phantom{\times999}73.71\\ \underline{\times\phantom{9999}1.61}\\ \end{array}"
        ex["pp"]["directa"] = "Aquell senyor que passa per allà pot fer 70 dibuixos en 5 minuts. Quants dibuixos podrà fer en 6 minuts?"
        ex["pp"]["inversa"] = "22 equilibristes s'han trobat un ramat de spaghetti, i n'han repartit 14 per cada una. Quants se'n podrien quedar si fossin 77?"

    return ex