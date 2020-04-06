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
Para que funcione PyLaTeX en local en el ordenador os hará falta MacTeX o alguna cosa por el estilo (yo he conseguido que funcione con MacTeX, que ocupa 6Gb, y no he sabido encontrar nada más pequeño que funcionara).
Si no, es bastante fácil usarlo (gratis) en pythonAnywhere.com, ya que ellos tienen ya el LaTeX instalado por defecto (así es como hice yo esto antes de implementar el control de versiones).

## Pruébalo!
Puedes acceder a la web para hacer tus fichas personalizadas aquí: [Dynamic Deures](http://bit.ly/DynamicDeures)

