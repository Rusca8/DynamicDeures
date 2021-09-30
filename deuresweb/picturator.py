"""
PICTURATOR
Crea les imatges Tikz dels exercicis que en tenen
"""


def recta_interval(a, b, at=False, bt=False, trepitja=False, w=4, h=2):
    """Dibuixa una recta real i hi marca l'interval en vermell
    :param a: primer número de l'interval (pot ser "-inf")
    :param b: segon número de l'interval (pot ser "inf")
    :param at: l'inici és tancat?
    :param bt: el final és tancat?
    :param trepitja: posa la línia vermella a sobre de l'altra
    :param w: amplada del dibuix
    :param h: alçada del dibuix
    """
    # alias per fer-ho més compacte
    def r(x):
        return round(x, 2)

    # mides de referència dl dibuix
    hb = 0.5  # alçada barra
    rc = r(hb/3)  # radi cercle
    div = 7  # divisions que faig servir per posicionar els números marcats (7: xa=w/7, xb=6w/7 )
    xa, xb = r(w/div), r(w*(div-1)/div)  # posició dels números marcats

    # gestiono els infinits
    linf = "inf" in f"{a}"  # left infinity
    rinf = "inf" in f"{b}"  # right infinity
    if all([linf, rinf]):
        a = 0
        b = div
    elif linf:
        a = b - div
    elif rinf:
        b = a + div

    # canvas i línia
    dibuix = [fr"\draw[white] (0, 0) rectangle ({w}, {h});",  # canvas size
              fr"\draw[thick] (0, {r(h/2)}) -- ({w}, {r(h/2)});"]  # recta real

    # barretes extra
    d = b-a
    if 1 < d < 2.5*w:  # entre número i número, les que hi vagin
        for i in range(1, d):
            x = r(xa+i*(xb-xa)/d)
            dibuix.append(fr"\draw ({x}, {r(h/2+hb/2)}) -- ({x}, {r(h/2-hb/2)});")
        if d > div-2:  # si hi caben, dues més a esquerra i dreta
            for i in [-1, d+1]:
                x = r(xa+i*(xb-xa)/d)
                dibuix.append(fr"\draw ({x}, {r(h / 2 + hb / 2)}) -- ({x}, {r(h / 2 - hb / 2)});")

    # barres i cercles dels números de l'exercici
    for x, n, nt, inf in [[xa, a, at, linf], [xb, b, bt, rinf]]:
        dibuix.append(fr"\draw ({x}, {r(h/2+hb/2)}) -- ({x}, {r(h/2-hb/2)}) node[below]" "{%s};" % (" " if inf else n))
        yc = r(h/2 if trepitja else h/2+hb)
        color = "red" if nt else "white"
        if not inf:
            dibuix.append(fr"\filldraw[very thick,fill={color}, draw=red] ({x}, {yc}) circle[radius={rc}];")

    # línia vermella que uneix els cercles
    dibuix.append(fr"\draw[very thick, red] ({xa+rc}, {yc}) -- ({r(xb-rc)}, {yc});")
    if linf:
        dibuix.append(fr"\draw[->, very thick, red] ({xa+rc}, {yc}) -- (0, {yc});")
    if rinf:
        dibuix.append(fr"\draw[->, very thick, red] ({r(xb-rc)}, {yc}) -- ({w}, {yc});")

    return tikzpicture("\n".join(dibuix), scale=0.5)


def tikzpicture(drawing, pb=0.15, scale=1):
    """Entorn per una imatge tikz (inclou eines per centrar-la amb la lletra de l'apartat)

    :param drawing: el dibuix de tikz, que l'haurà fet una altra funció
    :param pb: padding a sota el dibuix
    :param scale: ampliació de la mida del dibuix
    :return:
    """
    # l'últim rectangle és per aixecar el dibuix una mica (centrar-lo amb la part)
    tikz = r"""
    \raisebox{-0.5\height}{
        \begin{tikzpicture}%s
            %s
            \draw[white] (0, 0) rectangle (1, -%s);
        \end{tikzpicture}
    }
    """ % ((f"[scale={scale}]" if scale != 1 else ""), drawing, round(pb/scale, 2))
    return tikz
