# Dynamic Deures

> Generador de fichas de matemáticas online.

Dynamic Deures es una web app que he hecho con Flask (python) que genera fichas personalizadas de deberes de matemáticas (con números distintos cada vez).
Las fichas se generan a través de PyLaTeX (LaTeX sobre python), y el resultado es un pdf que se muestra al usuario para que lo pueda imprimir al momento.

_Lee esto en otros idiomas: [Catalán (CA)](README.md), [Castellano (ES)](README.es.md), [English (EN)](README.en.md)_
## Índice
- [Temas implementados](#temas-implementados)
- [Notas para desarrolladores](#notas-para-desarrolladores)
  - [Clonando el repositorio](#clonando-el-repositorio)
- [Pruébalo!](#pruébalo)

## Temas implementados
- Ecuaciones
  - Sencillas de primer grado
  - Segundo grado
    - Sencillas
    - Polinómicas
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
- Potencias y raíces
  - Potències con la misma base o exponente
  - Raíces con distinto índice (MCM)
- Succesiones
  - Succesiones aritméticas
  - Succesiones geométricas
- Derivadas
  - Reglas de derivación (con y sin cadena)

## Notas para desarrolladores
Para que funcione PyLaTeX en local en el ordenador os hará falta MacTeX o alguna cosa por el estilo (yo he conseguido que funcione con MacTeX, que ocupa 6Gb, y no he sabido encontrar nada más pequeño que funcionara).

Si no, es bastante fácil usarlo (gratis) en pythonAnywhere.com, ya que ellos tienen ya el LaTeX instalado por defecto (así es como hice yo esto antes de implementar el control de versiones).

### Clonando el repositorio
Debido al sistema de feedback por Telegram que tengo montado en la web (el bot me avisa cuando se generan documentos, diciéndome de qué tipo), si clonáis el repositorio (para curiosear o contribuir) tendréis que hacer un pequeño ajuste: el archivo que dice `teletoken.examply` se tiene que duplicar bajo el nombre `teletoken.py`, tal como se explica en el propio archivo.

En caso de no hacer esto la web dará un error en el momento de generar el pdf (porque no podrá importar la clave secreta del bot, que no he incluído por motivos evidentes).

_Por otro lado, a mí PyCharm me marca un error importando mis propios módulos, pero luego a la hora de la verdad funciona bien._
## Pruébalo!
Puedes acceder a la web para hacer tus fichas personalizadas aquí: [Dynamic Deures](http://bit.ly/DynamicDeures)

