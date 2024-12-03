# qmc-nje
Boolean function minimizer created as a homework project for Digital Technology I. [L-K-GINFBAL-DIGTECH1-1-KZ01] course of John von Neumann University.

# Modes
- `g` for GUI mode (default)
- `c` subparser for console mode

# Console mode arguments
- positional arguments:
  - `MINTERMS`  The minterms of the function to minimize, seperated by white space.
- options:
  - `dc`  List of don't-care terms, seperated by white space.
  - `nv`  The number of variables of the boolean function, if different from least number of variables needed to express the highest term.
