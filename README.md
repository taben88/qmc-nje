# qmc-nje
Boolean function minimizer created as a homework project for Digital Technology I. [L-K-GINFBAL-DIGTECH1-1-KZ01] course of John von Neumann University.

# Usage
```
python3 ./main.py c 12 13 15 31 -dc 0 2 3 4 14 18 19 28 29 30
-----------MINTERMS-----------
12 13 15 31

----------DONT-CARES----------
0 2 3 4 14 18 19 28 29 30

-------PRIME IMPLICANTS-------
MINTERMS        MASK
0 2             000_0
0 4             00_00
4 12            0_100
2 3 18 19       _001_
12 13 14 15 28 29 30 31 _11__

--------COVERING SETS---------
BC
```
# Modes
- `g` for GUI mode (default)
- `c` subparser for console mode

# Console mode arguments
- positional arguments:
  - `MINTERMS`  The minterms of the function to minimize, seperated by white space.
- options:
  - `-dc`  List of don't-care terms, seperated by white space.
  - `-nv`  The number of variables of the boolean function, if different from least number of variables needed to express the highest term.
