from View import View
from QMC import QMC
from string import ascii_uppercase
from abc import ABC, abstractmethod

class Controller(ABC):

    """Abstract base class for console and GUI controllers."""

    def __init__(self, view: View):
        self._view: View = view
        self._model: QMC = None

    def initQMC(self) -> ValueError | AssertionError | None:

        """Initialize model object. Return None or any error stemming from user input."""

        minterms: list[int] = self._view.getMinterms()
        dontCares: list[int] = self._view.getDontCares()
        nVars: int = self._view.getNVars()
        try:  
            self._model = QMC(minterms=minterms, dontCares=dontCares, nVars=nVars)    
        except (ValueError, AssertionError) as e:
            return e
        
        return None
    
    def calculate(self) -> dict[str, str|list[str]|list[tuple[str, str]]]:

        """Calculate prime implicants and covering sets of associated function. Return a dictionary with minterms, don't-cares, prime implicants and covering sets."""

        self._model.calculate()
        minterms: str = " ".join(str(i) for i in self._model.getMinterms())
        dontCares: str = " ".join(str(i) for i in self._model.getDontCares())

        primeImplicants: list[tuple[str, str]] = []
        for i in self._model.getPrimeImplicants():
            associatedMinterms: str = " ".join(str(j) for j in i.getMinterms())
            mask: str = str(i)
            primeImplicants.append(
                (associatedMinterms, mask)
            )
        coveringSets: list[str] = []
        for coveringSet in self._model.getAllCoveringSets():
            if self._model.getNVars() <= len(ascii_uppercase):
                coveringSets.append("+".join(i.toAlpha() for i in coveringSet))
            else:
                coveringSets.append("+".join(str(i) for i in coveringSet))
        result = {
            "minterms": minterms,
            "dontCares": dontCares,
            "primeImplicants": primeImplicants,
            "coveringSets": coveringSets
            }
        return result
    
    @abstractmethod
    def run(self) -> None:
        ...