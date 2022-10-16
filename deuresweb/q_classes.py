"""
Definicions de classes pels exercicis de química (de moment molècules d'orgànica)
"""

from dataclasses import dataclass, field, astuple, replace
from typing import List


abbr = ["Met", "Et", "Prop", "But", "Pent", "Hex", "Hept"]
err = r"^{\color{red}X}"

@dataclass()
class Node:
    """Node d'una molècula orgànica

    link: enllaç al següent node de la cadena
    at: àtom central del node (C, O, N)
    rads: llista de coses extra que pengen (excepte H)
    n: quantitat d'enllaços que pot fer (especificar només si no és típic)
    clink: de quin àtom del bloc ha de sortir l'enllaç (per HxC-, HOC-, HOOC-, etc.)
    """
    at: str = field(default="C")
    link: int = field(default=0)
    rads: List = field(default_factory=lambda: [])
    angle: int = field(default=0)
    n: int = field(default=4)
    hc: bool = field(default=False)
    clink: int = field(default=1, init=False, repr=False)

    def __post_init__(self):
        # check enllaços indicats
        if any(x in self.at for x in ["=", "~"]):
            if "~" in self.at:
                self.link = 3
            elif "=" in self.at:
                self.link = 2
            self.at = self.at.replace("=", "").replace("~", "") or "C"

        # check electrons covalents
        if self.at in "C":
            self.n = 4
        elif self.at == "N":
            self.n = 3
        elif self.at == "O":
            self.n = 2
        else:
            self.n = 1
        # check radicals
        self.check_rads()

    def check_rads(self):
        """Converteixo en Morg els radicals que no ho siguin"""
        for i, x in enumerate(self.rads):
            try:
                x.prelink = x.prelink or 1
            except AttributeError:
                if x in abbr:
                    self.rads[i] = Morg([Node() for i in range(abbr.index(x)+1)])
                else:
                    self.rads[i] = Morg([x])
                self.rads[i].prelink = 1

    def new_rad(self, rad):
        self.rads.append(rad)
        self.check_rads()

    def set_angle(self, angle):
        self.angle = angle % 360

    def get_bondfig(self):
        """bond configuration (angle i altres paràmetres de l'enllaç)"""
        angle = f"::{self.angle}"
        length = ""
        """if 45 < self.angle < 135 or 225 < self.angle < 315:  # faria falta saber l'angle absolut :_)
            length = "0.8"
        else:
            length = """""
        departure = f"{self.clink}" if self.clink > 1 else ""
        arrival = ""
        config = [angle, length, departure, arrival]
        while not config[-1]:
            config = config[:-1]

        return f"[{','.join(config)}]"

    def get_at(self, fhc=False):
        """Retorna l'àtom escrit de la manera adequada (i.e. invertit si hc o si es força des de fora amb fhc)"""
        if self.hc or fhc:
            at = []
            part = []
            for c in self.at:
                if c.isupper():
                    at += part
                    part = [c]
                else:
                    part.append(c)
            return "".join(at + part)
        else:
            return self.at

    def __format__(self, fkey):
        return f"{self.at}({','.join(self.rads)})"


links = ["", "-", "=", "~"]


@dataclass()
class Morg:
    """Molècula orgànica

    nodes: blocs que vull separats per enllaços dins la molècula
    prelink: Enllaç que ajunta una molècula radical amb una principal
    angle: Inclinació general de tota la molècula
    """
    nodes: List = field(default_factory=lambda: [])
    prelink: int = field(default=0)
    angle: int = field(default=0)

    def __post_init__(self):
        for i, n in enumerate(self.nodes):  # entro en Nodes si només era la lletra
            try:  # he passat un node?
                n.link
            except AttributeError:
                if isinstance(n, str):  # he passat un text
                    if n == "Ald":
                        self.nodes[i] = Node("C", rads=[Morg(["O"], prelink=2), "H"])
                    elif n == "Cet":
                        self.nodes[i] = Node("C", rads=[Morg(["O"], prelink=2)])
                    elif n == "Acid":
                        self.nodes[i] = Node(rads=[Morg(["O"], prelink=2), "O"])
                    elif n in ["Amid", "Amida"]:
                        self.nodes[i] = Node(rads=[Morg(["O"], prelink=2), "N"])
                    else:
                        self.nodes[i] = Node(n)
                else:  # he passat una llista
                    try:
                        self.nodes[i] = Node(n[0], rads=[Morg([r]) for r in n[1:]])
                    except IndexError:
                        self.nodes[i] = Node("?")
        for n in self.nodes[:-1]:
            if not n.link:
                n.link = 1

    def append(self, node):
        """Afegeix un node a la cadena"""
        self.nodes += [node]

    def set_angle(self, angle):
        """Assigna un angle a la molècula sencera (e.g. a un radical etil)"""
        self.nodes[0].set_angle(angle)

    def get_angle(self):
        return self.nodes[0].angle

    def set_clink(self, clink):
        for r in self.nodes[0].rads:
            r.clink = clink

    def bend(self):
        if self.nodes[-1].link:  # cíclica
            print("cycle.bend() not implemented")
            return
        for i, n in enumerate(self.nodes):
            radlinks = [[r.prelink, j] for j, r in enumerate(n.rads)]
            radlinks.sort(reverse=True)
            if radlinks and radlinks[0][0] > 1:
                if len(radlinks) == 1:
                    n.rads[radlinks[0][1]].set_angle(90)
                elif len(radlinks) == 2:
                    n.rads[radlinks[0][1]].set_angle(45)
                    n.rads[radlinks[1][1]].set_angle(-45)
                    if i == 0:  # si són a l'esquerra
                        for r in n.rads:
                            r.set_angle(r.get_angle() + 180)
                            r.nodes[0].hc = True
                else:
                    print("estranya molècula, amic")
            else:
                radlen = [[len(r.nodes), j] for j, r in enumerate(n.rads)]  # llista amb les longituds dels radicals
                radlen.sort(reverse=True)
                for j, x in enumerate(radlen):  # radlen és [longitud, índex]
                    n.rads[x[1]].set_angle([-90, 90, 180 if i == 0 else 0][j])

    def __format__(self, fkey=""):
        h3c = True
        text = []
        self.bend()  # TODO opció per respectar els angles triats manualment
        if self.nodes[-1].link:  # cíclica
            return "CICLE format not implemented"
        else:
            for i, n in enumerate(self.nodes):
                rads = (f'({links[x.prelink or 1]}{x})' for j, x in enumerate(n.rads))
                hidros = self.nodes[i].n - sum(x.prelink or 1 for x in self.nodes[i].rads) - self.nodes[i].link
                if i > 0:
                    hidros -= self.nodes[i-1].link
                elif self.prelink:
                    hidros -= self.prelink
                h = (f"H" + ("_{" + f"{hidros}" + "}" if hidros != 1 else "")) if hidros > 0 else err if hidros else ""
                if i != 0 or self.prelink:
                    text.append(f"{n.get_bondfig()}")
                if h3c and h and (n.hc or (i == 0 and len(self.nodes) > 1 and not self.prelink)):
                    for r in n.rads:
                        r.nodes[0].clink = 2
                    text.append(f"{h}{self.nodes[i].get_at(True)}")
                else:
                    text.append(f"{self.nodes[i].get_at()}{h}")
                text.append(''.join(rads) + f"{links[self.nodes[i].link]}")
        return "".join(text)
