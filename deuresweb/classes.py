"""
Definicions de les diferents classes que faré servir (ara que he vist que són útils) :)
"""
from dataclasses import dataclass, field, astuple, replace
from typing import List
from math import copysign
import random


class P:
    """Llista de quins percentatges ha d'ocupar cada variant de l'exercici (cada g).
    Té la següent forma: [[%1, {opcions1}], [%2, {opcions2}], [%3, {opcions3}], ...]

    Opcions:
        "max": quantitat d'apartats màxima que puc posar (independentment del percentatge)
    """
    def __init__(self, pesos, en_percentatge=False):
        """Construeix la llista de percentatges a partir dels pesos.

        :param pesos: pesos relatius de cada variant (p.ex. [1, 2, 2] == del 2n doble que del 1r, del 3r com del 2n)
        :param en_percentatge: True = he passat els percentatges ja fets en lloc dels pesos
        """
        self.p = []
        # els passo a la interna assegurant que hi ha màxim
        for q in pesos:
            try:
                self.p.append([q[0], q[1]])  # assegura llista [a, b]
                self.p[-1][1]["max"] = self.p[-1][1].get("max", 100000)  # és prou pq LaTeX limita a unes 700 (a-zz)
            except TypeError:
                self.p.append([q, {"max": 100000}])
        if not en_percentatge:
            # faig els pesos acumulats
            acc = 0
            for q in self.p:
                q[0] += acc
                acc = q[0]
            # converteixo en percentatges
            total = self.p[-1][0]
            self.p = [[round(q[0]*100/total, 3), q[1]] for q in self.p]  # divisió entera no conserva prou precisió

    def flex(self, nvar, pvar):  # TODO optimitzar amb map()
        """Estira i arronsa els percentatges de manera que l'índex escollit tingui el percentatge escollit

        :param nvar: índex escollit
        :param pvar: percentatge que ha de tenir l'índex escollit
        """
        print("vas canviar els paràmetres d'ordre, gamarús") if pvar < 10 else None
        # retallo per la frontera
        pre = self.p[:nvar + 1]
        post = self.p[nvar + 1:]
        frontera = pre[-1][0]
        # deformo cada tros
        pre = [[round(q[0]*pvar / frontera, 2), q[1]] for q in pre]  # sense round pot sortir tipus [1, 3, 3, 4, 6]
        post = [[pvar + round((q[0]-frontera)*(100-pvar) / (post[-1][0]-frontera), 2), q[1]] for q in post]
        # muntatge
        self.p = pre + post
        return self

    def get(self):
        return self.p


@dataclass()
class Fr:
    """Fracció (num, den)"""
    sort_index: float = field(init=False, repr=False)
    num: int
    den: int
    signe: int = field(default=1)  # signe global (±1)

    def __post_init__(self):  # per si ha entrat un signe que no tocava (i per copiar signes)
        self.signe = signe_de(self.signe)
        self.new_sort_index()

    def __format__(self, fkey):
        if "i" in fkey:
            return format(self.simple(), fkey.replace("i", ""))
        if self.signe < 0:
            s = "-"
        elif 's' in fkey:
            s = "+"
        else:
            s = ""

        if abs(self.den) == 1:
            return f"{self.signe * signe_de(self.den) * self.num}"

        if 'r' in fkey:
            if not (isinstance(self.num, int) and isinstance(self.den, int)):
                try:
                    num = f"({self.num:r})"
                except:
                    num = self.num
                try:
                    den = f"({self.den:r})"
                except:
                    den = self.den
                return f"{s}{num}/{den}"
            else:
                return f"{s}{to_sup(self.num)}/{to_sub(self.den)}"
        else:
            return fr"{s}\frac" + "{" + f"{self.num}" + "}{" + f"{self.den}" + "}"

    def __abs__(self):
        return Fr(abs(self.num), abs(self.den))

    def __neg__(self):
        return replace(self, signe=-self.signe)

    def __add__(self, other):
        if other == 0:
            return self
        if other.__class__ is self.__class__:
            a = self.simple()
            b = other.simple()
            return Fr(a.signe * a.num * b.den + b.signe * b.num * a.den, a.den * b.den).simple()
        elif isinstance(other, int):
            return self.__add__(Fr(other, 1))
        else:
            return NotImplemented

    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)

    def __sub__(self, other):
        if other == 0:
            return self
        else:
            if self.__class__ is other.__class__:
                return self.__add__(replace(other, signe=-self.signe))
            elif isinstance(other, int):
                return self.__add__(-other)

    def __rsub__(self, other):
        if other == 0:
            return self
        else:
            return replace(self, signe=-self.signe).__add__(other)

    def __mul__(self, other):
        if other == 0:
            return Fr(0, 1)
        elif other == 1:
            return self
        else:
            if self.__class__ is other.__class__:
                return Fr(self.num * other.num, self.den * other.den, self.signe * other.signe).simple()
            elif isinstance(other, int):
                return replace(self, num=other*self.num).simple()
            else:
                return NotImplemented

    def __rmul__(self, other):
        if other == 0:
            return Fr(0, 1)
        elif other == 1:
            return self
        else:
            return self.__mul__(other)

    def __truediv__(self, other):
        if other == 0:
            raise ZeroDivisionError("Què cardes dividint per zero, criminal.")
        elif other == 1:
            return self
        else:
            if self.__class__ is other.__class__:
                return self.__mul__(other.inversa())
            elif isinstance(other, int):
                return self.__mul__(Fr(1, other))
            else:
                return NotImplemented

    def __rtruediv__(self, other):
        if other == 0:
            return Fr(0, 1)
        elif other == 1:
            return self
        else:
            if isinstance(other, int):
                return Fr(other, 1).__mul__(self.inversa())
            else:
                return NotImplemented

    def __floordiv__(self, other):
        if not self.__class__ == other.__class__:
            return self.__truediv__(other)
        a = other.num
        b = other.den
        signe = other.signe
        return Fr(num=self.num//a, den=self.den//b, signe=self.signe*signe)

    def __rfloordiv__(self, other):
        return self.__rtruediv__(other)

    def __pow__(self, power, modulo=None):
        if modulo:
            return NotImplemented
        if power == 0:
            return Fr(1, 1)
        elif power == 1:
            return self
        else:
            if isinstance(power, int):
                a = self.simple()
                return replace(a, num=a.num**power, den=a.den**power, signe=(a.signe if power % 2 else 1))
            else:
                return NotImplemented

    def __rpow__(self, other):
        raise NotImplementedError("No sé fer potències fracció. Espero no fer-te anar malament.")

    def simple(self):
        # agrupo signes
        signe = self.signe * signe_de(self.num) * signe_de(self.den)
        num = abs(self.num)
        den = abs(self.den)
        # arreglo possibles entrepans de fraccions
        if any(isinstance(x, Fr) for x in [num, den]):
            fr: Fr = num / den
            num, den = fr.num, fr.den
        # faig irreductible
        try:
            d = mcd(num, den)
            return Fr(num//d, den//d, signe)
        except Exception as ex:
            print(f"{ex}: has simplificat una fracció estranya (no he simplificat).")
            return replace(self)

    def simplifica(self):
        simple = self.simple()
        self.num, self.den, self.signe = simple.num, simple.den, simple.signe
        self.new_sort_index()
        return

    def inversa(self):
        return Fr(self.den, self.num, self.signe)

    def new_sort_index(self):
        """Actualitza el sort index (per quan faig canvis que no generen una instància nova)"""
        try:
            self.sort_index = self.num/self.den * self.signe
        except Exception as ex:
            # doble poli
            if isinstance(self.num, Px) and isinstance(self.den, Px):
                self.sort_index = sum(t.coef for t in self.num.termes)
            # altres ex
            else:
                # print(f"{ex}: Sort index impossible (Fr)")
                self.sort_index = 0


@dataclass(order=True)
class Mx:
    """Monomi (coef, {var:exp, var:exp})

       Exemples:
         Mx(3, {"x": 2, "y": 4}) = 3·x²y⁴
         Mx(2, 4) = 2·x⁴
    """
    sort_index: List = field(init=False, repr=False)
    coef: int
    lit: dict = field(default_factory=lambda: {"x": 0})  # part literal
    ordenat: bool = True
    amagat: bool = False  # per facilitar exercicis que amaguen trossos (inclou signe, si no el vols fes abs())

    def __post_init__(self):
        if isinstance(self.lit, int):  # si no està especificat, serà 'x'
            self.lit = {"x": self.lit}
        try:
            self.lit = dict(sorted(self.lit.items()))
        except Exception as ex:
            print(f"{ex}: L'has liada, pavo (no puc ordenar els exponents del monomi)")
        self.new_sort_index()

    def __format__(self, fkey):
        """
        Opcions pel format (caràcters dins fkey):
            s: incloure signe
            r: raw (non-latex)
        """
        if self.amagat:
            s = "+" if 's' in fkey and not es_negatiu(self, False) else "-" if es_negatiu(self, False) else ""
            return f"{s}" + r"\_" * 4

        if self.coef == 0:
            return "0"

        lit = []
        for v, e in self.lit.items():
            if not e:
                lit.append("")
            elif e == 1:
                lit.append(v)
            else:
                if 'r' in fkey:
                    lit.append(v + to_sup(e))
                else:
                    lit.append(v + "^{" f"{e}" "}")

        s = "+" if 's' in fkey and not es_negatiu(self, False) else ""

        punt = True
        if f"{abs(self.coef)}" == "1" and any(v for v in lit):  # si quedarà ±1 i tinc variables, amago l'1
            c = "-" if es_negatiu(self, False) else ""
            punt = False  # amago el punt per evitar -·x
        else:
            if 'r' in fkey:
                if not isinstance(self.coef, int):
                    try:
                        c = f"{self.coef:r}"
                    except:
                        c = self.coef
                else:
                    c = self.coef
            else:
                c = self.coef
        dot = "·" if 'r' in fkey and c and punt and any(e for e in self.lit.values()) else ""
        if not self.ordenat:
            random.shuffle(lit)
        return f"{s}{c}{dot}" + "".join(lit)

    def __abs__(self):
        return replace(self, coef=abs(self.coef))

    def __neg__(self):
        return replace(self, coef=-self.coef)

    def __add__(self, other):
        if other == 0:
            return self
        else:
            if self.__class__ is other.__class__:
                return Px([self]) + Px([other])
            else:
                return NotImplemented

    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)

    def __sub__(self, other):
        if other == 0:
            return self
        else:
            if self.__class__ is other.__class__:
                return Px([self]) - Px([other])
            else:
                return NotImplemented

    def __rsub__(self, other):
        if other == 0:
            return -self
        else:
            return replace(self, coef=-self.coef).__add__(other)

    def __mul__(self, other):
        if other == 0:
            return Mx(0)
        elif other == 1:
            return self
        else:
            if self.__class__ is other.__class__:
                coef = self.coef * other.coef
                lit = self.lit.copy()
                for v, e in other.lit.items():
                    lit[v] = lit.get(v, 0) + e
                return Mx(coef, lit)
            elif isinstance(other, Fr) or isinstance(other, int):
                return replace(self, coef=self.coef*other)
            else:
                return NotImplemented

    def __rmul__(self, other):
        if other == 0:
            return Mx(0)
        elif other == 1:
            return self
        else:
            return self.__mul__(other)

    def __truediv__(self, other):
        if other == 0:
            raise ZeroDivisionError("Què cardes dividint per zero, criminal.")
        elif other == 1:
            return self
        else:
            if self.__class__ is other.__class__:
                if abs(self) == abs(other):
                    return signe_de(self) * signe_de(other)
                else:
                    coef = Fr(self.coef, other.coef).simple()
                    lit = self.lit.copy()
                    for v, e in other.lit.items():
                        lit[v] = lit.get(v, 0) - e
                    return Mx(coef, lit)
            elif isinstance(other, Fr) or isinstance(other, int):
                return replace(self, coef=self.coef / other)
            else:
                return NotImplemented

    def __rtruediv__(self, other):
        if other == 0:
            return Mx(0)
        else:
            if isinstance(other, int):
                return Mx(other).__truediv__(self)
            else:
                return NotImplemented

    def __floordiv__(self, other):
        if other == 0:
            raise ZeroDivisionError("Què cardes dividint per zero, criminal.")
        elif other == 1:
            return self
        else:
            if self.__class__ is other.__class__:
                if abs(self) == abs(other):
                    return signe_de(self) * signe_de(other)
                else:
                    coef = self.coef // other.coef
                    lit = self.lit.copy()
                    for v, e in other.lit.items():
                        lit[v] = lit.get(v, 0) - e
                    return Mx(coef, lit)
            elif isinstance(other, Fr) or isinstance(other, int):
                return replace(self, coef=self.coef // other)
            else:
                return NotImplemented

    def __rfloordiv__(self, other):
        if other == 0:
            return Mx(0)
        else:
            if isinstance(other, int):
                return Mx(other).__floordiv__(self)
            else:
                return NotImplemented

    def __pow__(self, power, modulo=None):
        if power == 2:
            return self.__mul__(self)
        else:
            raise NotImplementedError

    def new_sort_index(self):
        try:
            self.sort_index = [list(self.lit.keys()), [-e for e in self.lit.values()], -self.coef]
        except Exception as ex:
            print(f"{ex} || Sort index impossible for (Mx)")
            print(self)


@dataclass()
class Px:
    """Polinomi de múltiples variables [Mx, Mx, Mx, ...]

       Exemples:
         Px([Mx(...), Mx(...), Mx(...)])
         npx([coefs estil numpy]) == Px([coefs estil numpy], np=True)
    """
    termes: List = field(default_factory=lambda: [])
    np: bool = False  # coefs donats estil numpy: [1, 2, 3, 4, 5, 6] grau ascendent >
    np_var: str = "x"  # variable que hi posaré quan converteixi el polinomi de np

    def __post_init__(self):
        if self.np:
            self.termes = [Mx(coef, {self.np_var: exp}) for exp, coef in enumerate(self.termes) if coef != 0]
            self.termes = self.termes or [Mx(0)]   # per coherència, el polinomi 0 tindrà un monomi 0 a dins
            self.sort()
        else:
            for i, x in enumerate(self.termes):  # converteixo per si de cas he passat algun num sol
                if not isinstance(x, Mx):
                    self.termes[i] = Mx(x)

    def __format__(self, fkey):
        """
        Opcions pel format (caràcters dins fkey):
            r: raw (non-latex)
            d: desordenat
        """
        if "r" in fkey:
            r = "r"
        else:
            r = ""

        ordre = list(range(len(self.termes)))
        if "d" in fkey:
            random.shuffle(ordre)

        text = []
        for i, t in enumerate(ordre):
            t = self.termes[t]
            if i > 0:
                if r:
                    text.append(" ")
                text.append(f"{t:{r}s}")
            else:
                text.append(f"{t:{r}}")
        return "".join(text) or "0"

    def __iter__(self):
        return iter(self.termes)

    def __abs__(self):
        return Px([replace(t, coef=abs(t.coef)) for t in self.termes])

    def __neg__(self):
        return Px([replace(t, coef=-t.coef) for t in self.termes])

    def __add__(self, other):
        if other == 0:
            return self
        # ajusto Mx a Px
        if other.__class__ is Mx:
            other = Px([other])
        # Px + Px
        if other.__class__ is self.__class__:
            return Px(self.termes + other.termes).simplificat()

    def __radd__(self, other):
        if other == 0:
            return self
        return self.__add__(other)

    def __sub__(self, other):
        if other == 0:
            return self
        # prèvia: ajusto Mx a Px
        if other.__class__ is Mx:
            other = Px([other])
        # Px - Px
        if other.__class__ is self.__class__:
            return Px(self.termes + (-other).termes).simplificat()

    def __rsub__(self, other):
        if other == 0:
            return -self
        return (-self).__add__(other)

    def __mul__(self, other):
        if other == 0:
            return 0
        elif other == 1:
            return self
        elif other == -1:
            return -self
        else:
            # Px * num
            if isinstance(other, int) or isinstance(other, float):
                return replace(self, termes=[replace(t, coef=t.coef*other) for t in self.termes])
            # previ: Mx -> Px
            if isinstance(other, Mx):
                other = Px([other])
            # Px * Px
            if self.__class__ == other.__class__:
                return Px([x*y for x in self.termes for y in other.termes]).simplificat()

    def __rmul__(self, other):
        if other == 0:
            return 0
        elif other == 1:
            return self
        elif other == -1:
            return -self
        else:
            return self.__mul__(other)

    def __pow__(self, power, modulo=None):
        if power == 2:
            return self.__mul__(self)
        else:
            raise NotImplementedError

    def sorted(self):
        return Px(sorted(self.termes))

    def sort(self):
        self.termes = self.sorted().termes

    def simplificat(self):
        for mx in self.termes:
            mx.lit = {v: exp for v, exp in mx.lit.items() if exp}

        termes = []
        for mx in self.termes:
            for i, t in enumerate(termes):
                if t.lit == mx.lit:
                    termes[i].coef += mx.coef
                    break
            else:
                termes.append(replace(mx))
        return Px([t for t in termes if t.coef]).sorted()

    def simplifica(self):
        self.termes = self.simplificat().termes

    def append(self, monomi):
        if isinstance(monomi, Mx):
            self.termes.append(monomi)
        else:
            self.termes.append(Mx(monomi))

    @property
    def variables(self):
        vs = set()
        for t in self.termes:
            for v, grau in t.lit.items():
                if grau != 0:
                    vs.add(v)
        return sorted(vs)

    def avalua(self, punt):
        # si entra només un número, el faig llista per gestionar-lo després
        if isinstance(punt, int) or isinstance(punt, float):
            punt = [punt]

        # si entra llista de valors, els assigno a les variables que tinc (alfabèticament)
        if isinstance(punt, list):
            punt = {v: n for v, n in zip(self.variables, punt)}  # és el meu primer zip oficial, crec :)

        # avaluem
        px = Px()
        for t in self.termes:
            coef = t.coef
            lit = {}
            for v, exp in t.lit.items():
                if v in punt:
                    coef *= punt[v] ** exp
                else:
                    lit[v] = exp
            px.append(Mx(coef, lit or {"x": 0}))

        return px.simplificat()


def npx(termes, var="x"):
    return Px(termes, np=True, np_var=var)


@dataclass()
class Mul:
    """Multiplicació (indicada, pendent de fer) de dues coses"""
    factors: List = field(default_factory=lambda: [])

    def __format__(self, fkey):
        if "r" in fkey:
            cdot = "·"
        else:
            cdot = r"\cdot "

        totsdots = "·" in fkey

        ordre = list(range(len(self.factors)))
        if "d" in fkey:
            random.shuffle(ordre)

        text = []
        for i, f in enumerate(ordre):
            f = self.factors[f]
            try:
                tf = f"{f:{fkey}}"
            except Exception:
                tf = f"{f}"
            if i:
                if es_bloc(f) or es_negatiu(f):
                    if totsdots:
                        text.append(cdot + f"({tf})")
                    else:
                        text.append(f"({tf})")
                else:
                    text.append(cdot + tf)
            else:
                if es_bloc(f):
                    text.append(f"({tf})")
                else:
                    text.append(tf)

        return "".join(text)

    def __abs__(self):
        print("Abs de multi?")
        return 42

    def append(self, factor):
        self.factors.append(factor)

    def simplificat(self):
        resultat = 1
        for factor in self.factors:
            resultat *= factor
        return resultat


@dataclass()
class Div:
    """Divisió (indicada, pendent de fer) de dues coses"""
    divisors: List = field(default_factory=lambda: [])

    def __format__(self, fkey):
        if "r" in fkey:
            div = " / "
        else:
            div = r"\div "

        ordre = list(range(len(self.divisors)))
        if "d" in fkey:
            random.shuffle(ordre)

        text = []
        for i, f in enumerate(ordre):
            f = self.divisors[f]
            try:
                tf = f"{f:{fkey}}"
            except Exception:
                tf = f"{f}"
            if i:
                if es_bloc(f) or es_negatiu(f):
                    text.append(div + f"({tf})")
                else:
                    text.append(div + tf)
            else:
                if es_bloc(f):
                    text.append(f"({tf})")
                else:
                    text.append(tf)

        return "".join(text)

    def __abs__(self):
        print("Abs de divi?")
        return 42

    def append(self, divisor):
        self.divisors.append(divisor)

    def simplificat(self):
        resultat = 1
        for divisor in self.divisors:
            resultat /= divisor
        return resultat


# //////////////////////////// AUXILIARS ////////////////////////////// #
_superscript = str.maketrans("0123456789+-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻")
_subscript = str.maketrans("0123456789+-", "₀₁₂₃₄₅₆₇₈₉₊₋")


def to_sup(nums):
    return f"{nums}".translate(_superscript)


def to_sub(nums):
    return f"{nums}".translate(_subscript)


def signe_de(cosa, collapse=True):
    """Retorna el signe d'un objecte donat

    :param cosa: objecte
    :param collapse: True = unificar signes, False = només signe d'escriptura
    """
    if isinstance(cosa, Mx):
        return signe_de(cosa.coef, collapse)
    elif isinstance(cosa, Fr):
        if collapse:
            return cosa.simple().signe
        else:
            return cosa.signe
    elif isinstance(cosa, Px):
        if len(cosa.termes) == 1:
            return copysign(1, cosa.termes[0].coef)
        else:
            return 1  # considero el polinomi "positiu" per defecte (per compatibilitat)
    else:
        try:
            return int(copysign(1, cosa))
        except Exception as ex:
            print(f"{ex}: no sé trobar el signe d'un {type(cosa)}.")


def es_negatiu(cosa, collapse=True):
    return signe_de(cosa, collapse) < 0


def es_bloc(cosa):
    """Et diu si la cosa és un bloc de coses que han d'anar juntes."""
    if isinstance(cosa, Px) and len(cosa.termes) > 1:
        return True
    return False


def mcd(a, b):
    """Retorna el mcd dels dos números (o objectes) donats"""
    # si són altres trastos
    if any(isinstance(x, Mx) for x in [a, b]):
        return mcd_mx(a, b)
    elif any(isinstance(x, Fr) for x in [a, b]):
        return mcd_fr(a, b)
    # si són enters normals (Euler Recursiu)
    if b == 0:
        return a
    return mcd(b, a % b)


def mcd_mx(a, b):
    # conversions, just in case
    if not isinstance(a, Mx):
        a = Mx(a)
    if not isinstance(b, Mx):
        b = Mx(b)

    # càlculs
    coef = mcd(a.coef, b.coef)
    lit = {}
    for v, e in a.lit.items():
        if v in b.lit:
            lit[v] = min(e, b.lit[v])
    return Mx(coef, lit)


def mcd_fr(a, b):
    # conversions
    if not isinstance(a, Fr):
        a = Fr(abs(a), 1, signe_de(a))
    if not isinstance(b, Fr):
        b = Fr(abs(b), 1, signe_de(b))
    # càlculs
    return Fr(mcd(a.num, b.num), mcd(a.den, b.den), -1 if es_negatiu(a) and es_negatiu(b) else 1)


# TODO mirar si pots fer __le__ per evitar els sort_index intensius quan només vols dibuixar

# ////////////////////////////////// Debugging ////////////////////////////////// #
if __name__ == "__main__":
    """
    a = Mx(Fr(-3, 4), {'a': 2, 'b': 3, 'x': 15})
    b = Mx(Fr(1, 3), {"x": -3, "a": 3, "q": 3})

    c = Mx(Fr(2, 5, -1), {"x": 3, "y": 5})
    d = Mx(Fr(-1, 3), {"z": 2, "y": -1})

    e = Mx(Fr(15, 30), {"x": 4, "y": 3, "z": 6})
    f = Mx(Fr(10, 70), {"x": 3, "z": 2})
    g = mcd(a, b)

    poli = Px([b, a, d, c, e, f, g]).sorted()
    print(f"{poli:r}")

    noupoli = npx([1, 2, 3, 4, 5, 6], var="y")
    print(f"{noupoli:r}")

    print(f"{Fr(npx([1, 2]),npx([3, 4]))}")

    p = npx([1, 2, 1, 4, 1, 0, 7])
    q = Px([Mx(1, {"y": 3}), Mx(1, 2)])
    print(f"({q:r}) * ({p:r}) = ({q*p:r})")"""
    m = Mul([-1, npx([2, 1, 1]), npx([0, 3]), npx([3, 1])])
    print(f"{m:r}")

    p = npx([1, 2, 3, 4, 5, 6, 7])
    print(f"{p:rd}")

