from MintermCombination import MintermCombination
from PrimeImplicantTabulator import PrimeImplicantTabulator
from PrimeImplicantSelector import PrimeImplicantFilter

class QMC:
    def __init__(self, minterms: list[int], dontCares: list[int], nVars: int=0) -> None:
        if not minterms:
            raise ValueError("At least one minterm has to be provided!")
        
        minterms: set[int] = set(minterms)
        dontCares: set[int] = set(dontCares)
        
        if minterms.intersection(dontCares):
            raise AssertionError("No overlap between minterms and don't-cares allowed!")

        allTerms = minterms.union(dontCares)
        for i in allTerms:
            if i < 0:
                raise ValueError("Terms can only be represented by positive integers and 0!")
            
        maxBitLength: int = max(minterms.union(dontCares)).bit_length()
        maxBitLength = maxBitLength if maxBitLength else 1
        nVars = maxBitLength if not nVars else nVars

        if nVars < maxBitLength:
                raise AssertionError("Number of variables cannot be lower than bit length of highest value minterm!")

        self.__minterms: set[int] = set(minterms)
        self.__dontCares: set[int] = set(dontCares)
        self.__nVars = nVars
        self.__primeImplicants = None
        self.__coveringSets = None

    def calculate(self) -> None:

        """Calculate prime implicants and covering sets of associated function."""

        termsUnion = self.__minterms.union(self.__dontCares)
        mintermTable: set[MintermCombination] = {MintermCombination(i, nVars=self.__nVars) for i in termsUnion}
        self.__primeImplicants = PrimeImplicantTabulator.getPrimeImplicants(mintermTable=mintermTable)
        self.__coveringSets = PrimeImplicantFilter.getCoveringPrimeImplicantCombinations(minterms=self.__minterms, primeImplicants=self.__primeImplicants)

    def getMinterms(self) -> tuple[int]:

        """Return sorted tuple of minterms associated with function."""

        return tuple(sorted(self.__minterms))
    
    def getDontCares(self) -> tuple[int]:
        
        """Return sorted tuple of don't-care terms associated with function."""

        return tuple(sorted(self.__dontCares))
    
    def getNVars(self) -> int:

        """Return the number of variables of function."""

        return self.__nVars

    def getPrimeImplicants(self) -> tuple[MintermCombination]:

        """Return prime implicants associated with function."""

        return tuple(
            sorted(
                self.__primeImplicants,
                key=lambda x: (len(x), x.getMinterms())
                )
            )
    
    def getAllCoveringSets(self) -> tuple[tuple[MintermCombination]]:

        """Return all optimal prime implicant combinations, which cover all minterms associated with function."""

        return tuple(tuple(sorted(i, key=lambda x: str(x))) for i in self.__coveringSets)