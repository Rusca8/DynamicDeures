import random
import generator as g


def genera(aleatoris=False):
    ex = {}
    ex["en"] = {}
    ex["omx"] = {}
    ex["pow"] = {}
    ex["frac"] = {}
    ex["eq"] = {}
    ex["px"] = {}
    ex["pp"] = {}
    ex["succ"] = {}
    ex["dx"] = {}
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
        ex["en"]["combi1"] = g.mixcomb(random.randint(-10, 20), 3, doblesigne=True)
        ex["en"]["combi2"] = g.mixcomb(random.randint(-10, 20), 3, doblesigne=True, ops=[1, 2, 3, 4, 5])
        # pow
        ex["pow"]["mexp1"] = g.powsqr(1, 1, 2)
        ex["pow"]["mexp2"] = g.powsqr(1, 2, 3)
        ex["pow"]["mbase1"] = g.powsqr(2, 1, 2)
        ex["pow"]["mbase2"] = g.powsqr(2, 2, 3)
        ex["pow"]["frac1"] = g.powsqr(10, 1, 5)
        ex["pow"]["frac2"] = g.powsqr(10, 4, 5)
        ex["pow"]["ffrac1"] = g.powsqr(10, 5, 3)
        ex["pow"]["ffrac2"] = g.powsqr(10, 7, 3)
        ex["pow"]["dfrac1"] = g.powsqr(10, 8, 3)
        ex["pow"]["dfrac2"] = g.powsqr(10, 8, 3)
        ex["pow"]["sq1"] = g.powsqr(103, 1, 2)
        ex["pow"]["sq2"] = g.powsqr(103, 1, 3)
        ex["pow"]["sqp1"] = g.powsqr(103, 2, 2)
        ex["pow"]["sqp2"] = g.powsqr(103, 2, 3)
        ex["pow"]["comb1"] = g.powsqr(104, 1, 2)
        ex["pow"]["comb2"] = g.powsqr(104, 2, 3)
        ex["pow"]["extr1"] = g.powsqr(105, 1, lletres=0)
        ex["pow"]["extr2"] = g.powsqr(105, 2, lletres=1)
        ex["pow"]["intro1"] = g.powsqr(106, 1, lletres=0)
        ex["pow"]["intro2"] = g.powsqr(106, 2, lletres=1)
        ex["pow"]["fext1"] = g.powsqr(105, 11)
        ex["pow"]["fext2"] = g.powsqr(105, 12)
        ex["pow"]["asum"] = g.powsqr(107, 12, 3)
        ex["pow"]["racio1"] = g.powsqr(108, random.choice([1, 2, 3]))
        ex["pow"]["racio2"] = g.powsqr(108, random.choice([12, 14]))
        # frac
        ex["frac"]["fgen1"] = g.decimals(4, notac=random.choice([1, 2]))
        ex["frac"]["fgen2"] = g.decimals(4, notac=1)
        ex["frac"]["fgen3"] = g.decimals(4, notac=2)
        ex["frac"]["suma1"] = g.frac(1, 1)
        ex["frac"]["suma2"] = g.frac(1, 3)
        ex["frac"]["multi"] = g.frac(2, 3, divis=0)
        ex["frac"]["divi"] = g.frac(2, 3, divis=2)
        ex["frac"]["combi"] = g.fracmix(random.choice([-1, 1]) * g.randomfracnum(3), g.randomfracnum(3), 3)
        ex["frac"]["combi2"] = g.fracmix(random.choice([-1, 1]) * g.randomfracnum(3), g.randomfracnum(3), 3, ops=[1, 2, 4, 5])
        # px
        ex["px"]["monom1"] = g.rand_multimon(2)
        ex["px"]["monom2"] = g.rand_multimon(3)
        ex["px"]["inv"] = g.en.px_invent()
        ex["px"]["aval"] = g.px(6, 1)
        ex["px"]["fcom1"] = g.px(0, 1, termes=2)
        ex["px"]["fcom2"] = g.px(0, 2)
        ex["px"]["cryp"] = " ".join([fr" $\ \ \ \ {x}$ " for x in g.crypt.fc_frase(g.en.factorcomu())])
        ex["px"]["idnot1"] = g.idnotable(1, random.choice([1, 2]), random.choice([random.choice([1, 3]), 2]))
        ex["px"]["idnot2"] = g.idnotable(1, random.choice([4, 5, 6]), random.choice([random.choice([1, 2]), 3]))
        ex["px"]["eidnot1"] = g.idnotable(2, random.choice([1, 2]), random.choice([random.choice([1, 2]), 3]))
        ex["px"]["eidnot2"] = g.idnotable(2, random.choice([4, 5, 6]), random.choice([random.choice([1, 3]), 2]))
        ex["px"]["sumrest"] = g.px(random.choice([1, 2]), random.choice([1, 2, 3]))
        ex["px"]["multi"] = g.px(3, random.randint(1, 4))
        ex["px"]["rufi"] = g.px(4, random.randint(1, 2))
        ex["px"]["divi"] = g.px(5, random.randint(1, 2))
        ex["px"]["tres"] = g.px(6, 2)
        ex["px"]["fact"] = g.px(7, 3)
        ex["px"]["alg"] = g.px(8)
        # eq
        ex["eq"]["simple"] = g.eq(2, 3)
        ex["eq"]["1poli"] = random.choice([g.eq(3, 1), g.eq(4, random.choice([1, 2]))])
        ex["eq"]["racio"] = g.eq(5, 2)
        ex["eq"]["segoni1"] = g.eq(101, 1)
        ex["eq"]["segoni2"] = g.eq(102, 3)
        ex["eq"]["segonc1"] = g.eq(103, 2)
        ex["eq"]["segonc2"] = g.eq(103, 3)
        ex["eq"]["poli"] = g.eq(104)
        ex["eq"]["sis2d"] = g.sisteq(1, 2)
        ex["eq"]["sisnl1"] = g.sisteq(11, random.choice([1, 2, 3]))
        ex["eq"]["sisnl2"] = g.sisteq(12, random.choice([1, 2, 3]))
        ex["eq"]["sis3d"] = g.sisteq(101, 3)
        # omx
        ex["omx"]["suma"] = g.apilades(1, 1, [3, 2])
        ex["omx"]["sumad"] = g.apilades(1, 2, [3, 2], [2, 2])
        ex["omx"]["resta"] = g.apilades(2, 1, [2, 2])
        ex["omx"]["restad"] = g.apilades(2, 3, [3, 2], [2, 2])
        ex["omx"]["multi"] = g.apilades(3, 1, [3, 2])
        ex["omx"]["multid"] = g.apilades(3, 2, [2, 2], [2, 1])
        # pp
        ex["pp"]["directa"] = g.prop(1, 1)
        ex["pp"]["inversa"] = g.prop(1, 2)
        ex["succ"]["termen"] = g.success(random.choice([1, 2]), 2)
        # ex["succ"]["gtermen"] = g.success(2, 2)
        ex["succ"]["dades"] = g.success(random.choice([1, 2]), 3)
        # ex["succ"]["gdades"] = g.success(2, 3)
        ex["succ"]["extreure"] = g.success(1, 101, random.choice([1, 2, 3, 4]))
        ex["succ"]["gextreure"] = g.success(2, 101, random.choice([1, 2, 3, 4]))
        ex["dx"]["simple1"] = g.dx(1, [1, 2, 3, 4, 5], simples=True)
        ex["dx"]["simple2"] = g.dx(1, [1, 2, 3, 4, 5], simples=True)
        ex["dx"]["cadena"] = g.dx(3, [1, 2, 3, 4, 5])
    else:
        # en
        ex["en"]["suma1"] = "3+7="
        ex["en"]["suma2"] = "6-8"
        ex["en"]["suma3"] = "9-(+5)="
        ex["en"]["multi1"] = r"3\times 5"
        ex["en"]["multi2"] = r"2\times (-4)"
        ex["en"]["multi3"] = r"-6\times (-7)"
        ex["en"]["divi1"] = r"20\div 4"
        ex["en"]["divi2"] = r"-36\div 9="
        ex["en"]["divi3"] = r"-42\div (-7)="
        ex["en"]["combi1"] = r"(6+32):\lbrack-6-(-8)\rbrack-\lbrack-(1+(-64)):(-6+3)\rbrack"
        ex["en"]["combi2"] = r"\sqrt{36}:3-35:\sqrt{25}+\lbrack -4-(-{3}^2)\rbrack \cdot {(-9:3)}^2"
        # pow
        ex["pow"]["mexp1"] = r"7^{8}\cdot 5^{8}"
        ex["pow"]["mexp2"] = r"35^{7}\div 7^{7}\cdot (-8)^{7}"
        ex["pow"]["mbase1"] = r"13^{-8}\cdot 13^{7}"
        ex["pow"]["mbase2"] = r"5^{7}\cdot 5^{-6}\cdot 5^{5}"
        ex["pow"]["frac1"] = r"\frac{5^{7}\cdot5^{5}}{5^{2}\cdot5^{-2}\cdot5^{3}}"
        ex["pow"]["frac2"] = r"\frac{(3^{2}\cdot3^{-4})^{-2}}{(3^{-6}\cdot3\cdot7)^{4}}"
        ex["pow"]["ffrac1"] = r"\frac{275\cdot 55}{135}"
        ex["pow"]["ffrac2"] = r"\frac{39^{3}\cdot 99^{-4}}{84^{-3}}"
        ex["pow"]["dfrac1"] = r"\frac{0.0012}{0.003\cdot 0.07}"
        ex["pow"]["dfrac2"] = r"\frac{0.008}{0.0015\cdot 0.0049}"
        ex["pow"]["sq1"] = r"\sqrt[3]{5}\cdot \sqrt[2]{2}"
        ex["pow"]["sq2"] = r"\sqrt[2]{7}\cdot \sqrt[6]{4}\cdot \sqrt[3]{5}"
        ex["pow"]["sqp1"] = r"\sqrt[3]{5^{5}}\cdot \sqrt[2]{6^{7}}"
        ex["pow"]["sqp2"] = r"\sqrt[5]{4^{3}}\cdot \sqrt[2]{2^{4}}\cdot \sqrt[5]{3^{3}}"
        ex["pow"]["comb1"] = r"\sqrt[3]{\sqrt{2}}"
        ex["pow"]["comb2"] = r"\sqrt[4]{2\sqrt{\sqrt[5]{7}}}"
        ex["pow"]["extr1"] = r"\sqrt{7^{5}}"
        ex["pow"]["extr2"] = r"\sqrt[4]{5^{6}d^{2}a^{5}}"
        ex["pow"]["intro1"] = r"3\sqrt{3^{5}}"
        ex["pow"]["intro2"] = r"2^{3}\cdot 7^{3}\cdot c^{2}\sqrt[5]{7^{8}}"
        ex["pow"]["fext1"] = r"\sqrt{52}"
        ex["pow"]["fext2"] = r"\sqrt[4]{480}"
        ex["pow"]["asum"] = r"8\sqrt{27}-2\sqrt{3}-\sqrt{75}"
        ex["pow"]["racio1"] = r"\frac{5}{\sqrt{2}}"
        ex["pow"]["racio2"] = r"\frac{1}{5+\sqrt{6}}"
        # frac
        ex["frac"]["fgen1"] = r"8.65"
        ex["frac"]["fgen2"] = r"6.7\overline{42}"
        ex["frac"]["fgen3"] = r"3.40555..."
        ex["frac"]["suma1"] = r"\frac{2}{3}+\frac{5}{4}"
        ex["frac"]["suma2"] = r"\frac{7}{6}-\frac{9}{2}"
        ex["frac"]["multi"] = r"\frac{3}{5}\cdot \frac{4}{6}"
        ex["frac"]["divi"] = r"\frac{3}{5}\div \frac{-1}{-2}"
        ex["frac"]["combi"] = r"(\frac{3}{2}\cdot \frac{1}{3}-\frac{1}{3}\cdot \frac{3}{2}+\frac{1}{2}): (\frac{2}{4}\cdot \frac{-14}{3}+\frac{7}{5}: \frac{9}{7})"
        ex["frac"]["combi2"] = r"\lbrack \sqrt{\frac{17}{2}-\frac{1}{2}+1}: (\frac{10}{3}-\frac{43}{21})\rbrack ^2"
        # px
        ex["px"]["monom1"] = r"7ya^{3}"
        ex["px"]["monom2"] = r"-53z^{10}a^{32}y^{4}"
        ex["px"]["inv"] = r"De grau 34, incomplet, desordenat i que el terme independent sigui 6."
        ex["px"]["aval"] = "Troba el valor numèric del polinomi $P(x)=x^{5}+x^{4}+5x^{2}-7$ per a $x=1$."
        ex["px"]["fcom1"] = r"8x^{5}-2x^{2}"
        ex["px"]["fcom2"] = r"10bax+10ba^{4}x+20bat"
        ex["px"]["cryp"] = r"$\ \ \ \ me^{2}lus-es^{2}l$   $\ \ \ \ camsi-nmaoi$   $\ \ \ \ ensab+qasub+beas$   $\ \ \ \ tleva-a^{2}l$   $\ \ \ \ mgaer-nreg-gaer$   $\ \ \ \ jmean-m^{2}oecn-mesn$   $\ \ \ \ grdea-enotd-dea$   $\ \ \ \ nqua-uahiq$   $\ \ \ \ hal+lhaun-a^{2}h$   $\ \ \ \ nple+lepa$"
        ex["px"]["idnot1"] = r"(x+3)^2"
        ex["px"]["idnot2"] = r"(2ba^{3}+a)(2ba^{3}-a)"
        ex["px"]["eidnot1"] = r"x^{2}+10x+25"
        ex["px"]["eidnot2"] = r"9c^{2}a^{2}-4"
        ex["px"]["sumrest"] = r"(15x^{3}+14x^{2}+15x-12)+(x^{2}+x-11)"
        ex["px"]["multi"] = r"(-5x^{2}-6x-4)\times (x+2)"
        ex["px"]["rufi"] = "(7x^{2}-13x-2)\div (x-2)"
        ex["px"]["divi"] = "(-6x^{5}-6x^{4}-5x^{3}-5x^{2})\div (x^{2}+x)"
        ex["px"]["tres"] = r"Sense fer la divisió, digues quin és el residu de $(-x^{4}+4x^{2}-7x+1)\div(x+2)$."
        ex["px"]["fact"] = r"x^{5}-3x^{4}-10x^{3}"
        ex["px"]["alg"] = r"\frac{x^{3}+2x^{2}-8x}{x^{4}-12x^{2}+16x}"
        # eq
        ex["eq"]["simple"] = "2x+5=7"
        ex["eq"]["1poli"] = "-2x-10-3x-39=1+5x"
        ex["eq"]["racio"] = r"\frac{x}{2}-\frac{x+4}{6}=3x+2"
        ex["eq"]["segoni1"] = "x^2-9=0"
        ex["eq"]["segoni2"] = "x^2-7x=0"
        ex["eq"]["segonc1"] = "x^2-3x+2=0"
        ex["eq"]["segonc2"] = "-2x^2+12x-10=0"
        ex["eq"]["poli"] = "-16-3x^2=10x-8x-24-2x^2"
        ex["eq"]["sis2d"] = r"\begin{cases} x+3y=-14 \\ 5x-3y=-16 \end{cases}"
        ex["eq"]["sisnl1"] = r"\begin{cases} 2x+y=20 \\ xy=18 \end{cases}"
        ex["eq"]["sisnl2"] = r"\begin{cases} x^{2}+y^{2}=10 \\ x+y=-4 \end{cases}"
        ex["eq"]["sis3d"] = r"\begin{cases} x+5y-3z=39 \\ -2x+3y+5z=13 \\ 3x+16y+2z=124 \end{cases}"
        # omx
        ex["omx"]["suma"] = r"\begin{array}{c}\phantom{+}565\\ \underline{+\phantom{9}64}\\ \end{array}"
        ex["omx"]["sumad"] = r"\begin{array}{c}\phantom{+}115.19\phantom{9}\\ \underline{+\phantom{9}43.658\phantom{}}\\ \end{array}"
        ex["omx"]["resta"] = r"\begin{array}{c}\phantom{-}93\\ \underline{-\phantom{}11}\\ \end{array}"
        ex["omx"]["restad"] = r"\begin{array}{c}\phantom{-}210.16\phantom{9}\\ \underline{-\phantom{9}83.42\phantom{}}\\ \end{array}"
        ex["omx"]["multi"] = r"\begin{array}{c}\phantom{\times99}391\\ \underline{\times\phantom{999}58}\\ \end{array}"
        ex["omx"]["multid"] = r"\begin{array}{c}\phantom{\times999}73.71\\ \underline{\times\phantom{9999}1.61}\\ \end{array}"
        ex["pp"]["directa"] = "Aquell senyor que passa per allà pot fer 70 dibuixos en 5 minuts. Quants dibuixos podrà fer en 6 minuts?"
        ex["pp"]["inversa"] = "22 equilibristes s'han trobat un ramat de spaghetti, i n'han repartit 14 per cada una. Quants se'n podrien quedar si fossin 77?"
        ex["succ"]["termen"] = "D'una successió aritmètica sabem que $a_1 = 7$ i que $d = 3$. Calcula el terme $a_{2}$."
        # ex["succ"]["gtermen"] = "Sabem que el primer terme d'una successió geomètrica és $4$ i que $r = 2$. Quin serà el $2n$ terme?"
        ex["succ"]["dades"] = "En una successió aritmètica, $a_{23} = 90$, $d = 4$. Troba el terme $a_1$ de la successió."
        # ex["succ"]["gdades"] = "En una successió geomètrica, $a_1 = -3$, $a_{4} = -375$. Troba la raó $r$ de la successió."
        ex["succ"]["extreure"] = r"6, 12, 18, 24, 30, ...\  (a_{46}?)"
        ex["succ"]["gextreure"] = r"5, -25, 125, -625, 3125, ...\  (S_{8}?)"
        ex["dx"]["simple1"] = "sin(x+12)"
        ex["dx"]["simple2"] = r"2\cdot 7^{x}"
        ex["dx"]["cadena"] = r"-3\, \sqrt{log_2(arcsin(x))}"

    return ex