# Dynamic Deures

> Generador de fichas de matemáticas online.

Dynamic Deures es una web app que he hecho con Flask (python) que genera fichas personalizadas de deberes de matemáticas (con números distintos cada vez).
Las fichas se generan a través de PyLaTeX (LaTeX sobre python), y el resultado es un pdf que se muestra al usuario para que lo pueda imprimir al momento.

_Lee esto en otros idiomas: [Catalán (CA)](README.md), [Castellano (ES)](README.es.md), [English (EN)](README.en.md)_ 
## Índice
- [Temas implementados](#temas-implementados)
- [Notas para desarrolladores](#notas-para-desarrolladores)
- [Pruébalo!](#pruébalo)

## Temas implementados
- Ecuaciones
  - Sencillas de primer grado
  - Sistemas lineales
    - Dos incógnitas
    - Tres incógnitas
- Proporcionalidad
  - Simple
    - Problemas de directa
    - Problemas de inversa
- Operaciones con enteros
  - Sumas y restas
  - Multiplicaciones
  - Divisiones
- Operaciones con más cifras
  - Sumas
  - Restas
  - Multiplicaciones

## Notas para desarrolladores
La puesta a punto de PyLaTeX en local en el ordenador no es especialmente trivial (aparentemente necesita instalar MacTeX o similar, que por otro lado ocupa más de 6Gb). Pero la buena notícia es que es fácil hacerlo funcionar (de modo gratuito) en pythonAnywhere.com, ya que éste lleva LaTeX por defecto.

Yo para evitar dolores de cabeza arranqué toda la parte de PyLaTeX directamente online de este modo (y justo he vuelto ahora para pelearme con la instalación local, a ver si puedo aprovechar este nuevo control de versiones para no tener que parar la web cuando pruebo cosas nuevas).

_Seguiremos informando..._

## Pruébalo!
Puedes acceder a la web para hacer tus fichas personalizadas aquí: [Dynamic Deures](http://bit.ly/DynamicDeures)

