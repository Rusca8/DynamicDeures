# Dynamic Deures

> Online math worksheet generator.

Dynamic Deures is a Flask (python) web app that generates personalized math worksheets (with different numbers each time).
The worksheets are generated via PyLaTeX (LaTeX running in python), and the result is a pdf that is shown to the user so that she/he can print it on the go.

_Read this in other languages: [Catalán (CA)](README.md), [Castellano (ES)](README.es.md), [English (EN)](README.en.md)_
## Index
- [Implemented subjects](#implemented-subjects)
- [Notes for developers](#notes-for-developers)
- [Try it!](#try-it)

## Implemented subjects
- Equations
  - Simple lineal
  - Lineal systems
    - Two unknowns
    - Three unknowns
- Proportionality
  - Simple
    - Direct proportionality problems
    - Inverse proportionality problems
- Operations with integers
  - Additions and substractions
  - Products
  - Divisions
- Operacions with more digits (columnar)
  - Additions
  - Substractions
  - Multiplicacions

## Notes for developers
For PyLaTeX to run in your local machine you'll need MacTeX or something along the way (I got it to work with MacTeX, which is 6Gb, and couldn't make it work with anything smaller than that).
Otherwise, it's quite easy to make it run (for free) in pythonAnywhere.com, since they already have LaTeX installed by default (which is exactly how I made this before version control).

## Try it!
You can access the website to generate your own personalized math worksheets here: [Dynamic Deures](http://bit.ly/DynamicDeures)
