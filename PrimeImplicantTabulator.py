from MintermCombination import MintermCombination

class PrimeImplicantTabulator:

    """Function relating to the first part of the Quine McCluskey Method."""

    @classmethod
    def getPrimeImplicants(cls, mintermTable: set[MintermCombination]) -> set[MintermCombination]:
         
        """Wrapper around __reduceToPrimeImplicants. Returns prime implicants as set of minterm combinations."""

        primeImplicants = set()
        cls.__reduceToPrimeImplicants(mintermTable=mintermTable, primeImplicantsOut=primeImplicants)
        return primeImplicants
         
    @classmethod
    def __reduceToPrimeImplicants(cls, mintermTable: set[MintermCombination], primeImplicantsOut: set[MintermCombination]) -> None:

        """Combine minterm combinations while any can be combined. Add non-combinables to primeImplicantsOut."""

        nextLevel: set[MintermCombination] = set()
        for this in mintermTable:
                isReducable: bool = False
                for other in mintermTable:
                    result: MintermCombination = this.combine(other)
                    if result:
                        isReducable = True
                        nextLevel.add(result)
                if not isReducable:
                    primeImplicantsOut.add(this)
        if nextLevel:
            cls.__reduceToPrimeImplicants(mintermTable=nextLevel, primeImplicantsOut=primeImplicantsOut)
