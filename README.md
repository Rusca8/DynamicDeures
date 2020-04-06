# Dynamic Deures

> Generador de fitxes de matemàtiques online.

Dynamic Deures és una web app fet amb Flask (python) que genera fitxes personalitzades de deures de matemàtiques (amb números diferents cada vegada).
Les fitxes es generen mitjançant PyLaTeX (LaTeX sobre python), i el resultat és un pdf que es mostra a l'usuari per què el pugui imprimir al moment.

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
La posada a punt de PyLaTeX en local a l'ordinador no és especialment trivial (aparentment necessita instal·lar MacTeX o similar, que d'altra banda ocupen més de 6Gb). La bona notícia, però, és que és fàcil fer-lo córrer (de manera gratuïta) a pythonAnywhere.com, ja que aquest porta instal·lat LaTeX per defecte.

Jo per evitar maldecaps tota la part de PyLaTeX la vaig arrancar online d'aquesta manera (i tot just he tornat ara a encarar-me amb la instal·lació local, per veure si puc aprofitar el control de versions per no haver d'aturar el web quan provo coses noves).

_Seguirem informant..._

## Prova-ho!
Pots accedir a la web per generar les teves fitxes personalitzades aquí: [Dynamic Deures](http://bit.ly/DynamicDeures)

