from MintermCombination import MintermCombination
from Utils import Utils

class PrimeImplicantFilter:

    """Function relating to the second part of the Quine McCluskey Method."""
    
    @staticmethod
    def __groupPrimeImplicantsByMinterms(minterms: set[int], primeImplicants: dict[int, MintermCombination]) -> set[int]:

        """Return a set of bitfields each signifying the prime implicants associated with a minterm."""

        primeImplicantsGroupedByMinterms: set[int] = set()
        for mt in minterms:
            out: int = 0
            for value, pi in primeImplicants.items():
                if mt in pi:
                    out += value
            primeImplicantsGroupedByMinterms.add(out)
        return  primeImplicantsGroupedByMinterms

    @staticmethod
    def __extractEssential(primeImplicantsGroupedByMinterms: set[int]) -> tuple[tuple[int], tuple[int]]:

        """Return a tuple of all essential prime implicants and one with all remaining bifields of prime implicants associated with uncovered minterms."""

        reduced: list[int] = Utils.reduceByAbsorption(primeImplicantsGroupedByMinterms) # Absorb any terms, which are supersets of other terms
        
        esssential: set[int] = {term for term in reduced if term.bit_count() == 1}
        
        remaining: list[int] = list(set(reduced).difference(esssential))
        
        if len(remaining) > 1: # If there are more than one complex terms in suffix, try to find (and take) a simplex term shared by all complex terms in suffix
            commonComponent: int = remaining[0]
            for i in remaining:
                commonComponent &= i
            if commonComponent: # If there is a common component, it can be used to cover all remaining minterms.
                esssential.add(commonComponent)
                remaining = tuple()

        return tuple(esssential), tuple(remaining)

    @staticmethod
    def __petriksMethod(suffix: tuple[int]) -> set[frozenset[int]]:

        """Implementation of Petrik's method. Returns a set of possible covering sets."""

        terms: list[tuple[int]] = [Utils.decomposeBitField(i) for i in suffix]
        out = Utils.distribute(terms=terms, out=[0])
        out: list[int] = Utils.reduceByAbsorption(out)
        out.sort(key=lambda i: i.bit_count())
        return {frozenset(Utils.decomposeBitField(i)) for i in out}
    
    @classmethod
    def getCoveringPrimeImplicantCombinations(cls, minterms: set[int], primeImplicants: set[MintermCombination]) -> list[set[MintermCombination]]:

        """Return all possible optimal covering sets of prime implicants."""

        primeImplicantsTemp: dict[int, MintermCombination] = dict()
        for i, pi in enumerate(tuple(primeImplicants)):
            primeImplicantsTemp[2**i] = pi

        essential: tuple[int]
        remaining: tuple[int]
        essential, remaining = cls.__extractEssential(cls.__groupPrimeImplicantsByMinterms(minterms=minterms, primeImplicants=primeImplicantsTemp))
        
        possibleCoveringCombinations: list[set[int]] = []

        if remaining:
            extractedCombinations: list[frozenset[int]] = sorted(cls.__petriksMethod(remaining), key=lambda i: len(i))
            minLength: int = len(extractedCombinations[0])
            for i in extractedCombinations:
                if len(i) == minLength:
                    possibleCoveringCombinations.append(i.union(essential))
        else:
            possibleCoveringCombinations.append(set(essential))
            
        out: list[set[MintermCombination]] = []
        for combination in possibleCoveringCombinations:
            out.append({primeImplicantsTemp[i] for i in combination})
        return out