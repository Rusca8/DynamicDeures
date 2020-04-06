# Dynamic Deures

> Generador de fitxes de matemàtiques online.

Dynamic Deures és una web app fet amb Flask (python) que genera fitxes personalitzades de deures de matemàtiques (amb números diferents cada vegada).
Les fitxes es generen mitjançant PyLaTeX (LaTeX sobre python), i el resultat és un pdf que es mostra a l'usuari per què el pugui imprimir al moment.

_Llegeix això en altres idiomes: [Catalán (CA)](README.md), [Castellano (ES)](README.es.md), [English (EN)](README.en.md)_
## Índex
- [Temes implementats](#temes-implementats)
- [Notes per desenvolupadors](#notes-per-desenvolupadors)
- [Prova-ho!](#prova-ho)

## Temes implementats
- Equacions
  - Senzilles de primer grau
  - Sistemes lineals
    - Dues incògnites
    - Tres incògnites
- Proporcionalitat
  - Simple
    - Problemes de directa
    - Problemes d'inversa
- Operacions amb enters
  - Sumes i restes
  - Multiplicacions
  - Divisions
- Operacions amb més xifres
  - Sumes
  - Restes
  - Multiplicacions

## Notes per desenvolupadors
Per fer córrer PyLaTeX en local a l'ordinador necessitareu MacTeX o alguna cosa per l'estil (jo he aconseguit que funcioni amb MacTeX, que ocupa 6Gb, i no he sabut trobar res més petit que funcionés).

Si no, és bastant fàcil fer-lo anar (gratis) a pythonAnywhere.com, ja que ells tenen ja LaTeX instal·lat per defecte (aquest és el camí que vaig seguir jo per fer això abans d'implementar-ne el control de versions).

## Prova-ho!
Pots accedir a la web per generar les teves fitxes personalitzades aquí: [Dynamic Deures](http://bit.ly/DynamicDeures)

