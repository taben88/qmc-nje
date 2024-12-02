from typing import Literal
from string import ascii_uppercase

class MintermCombination:

    """Class representing the combination of minterms used in the Quine-McCluskey method."""

    def __init__(self, *minterms: int, mask: int = 0, nVars: int) -> None:
        self.__minterms: tuple[int] = tuple(sorted(list(set(minterms)))) # Minterms covered by combination
        self.__mask: int = mask # The mask representing the indifferent bits that make combining terms possible
        self.__nVars: int = nVars # The number of variables of the function associated with the combination

    def __hash__(self) -> int:
        return hash(self.getMinterms())
    
    def __eq__(self, other: "MintermCombination") -> bool:
        sameClass: bool = isinstance(other, self.__class__)
        if not sameClass:
            return False

        thisRepr: str = str(self)
        otherRepr: str = str(self)     
        return thisRepr == otherRepr
    
    def __contains__(self, item: int) -> bool:
        return item in self.getMinterms()

    def __repr__(self) -> str:
        repr: str = ""
        onBits: int = self.getMinterms()[0]
        for mt in self.getMinterms()[1:]:
            onBits &= mt
        onBits = bin(onBits)[2:].zfill(self.getNVars())
        mask: str = bin(self.getMask())[2:].zfill(self.getNVars())
        for i, j in zip(onBits, mask):
            if j == "1":
                repr += "_"
            elif i == "1":
                repr += "1"
            else:
                repr += "0"
        return repr
    
    def __len__(self) -> int:
        return len(self.getMinterms())

    def toAlpha(self) -> str:

        """Return alphabetic ASCII representation of minterm."""

        if len(ascii_uppercase) < self.getNVars():
            raise AssertionError(f"Too many variables, cannot be represented using alphabetic ASCII characters.")

        alphaRepr: str = ""
        for i, char in enumerate(str(self)):
            match char:
                case "0":
                    alphaRepr += f"{ascii_uppercase[i]}'"
                case "1":
                    alphaRepr += ascii_uppercase[i]
                case "_":
                    pass
        return alphaRepr

    def getNVars(self) -> int:

        """Return the number of variables in associated function."""

        return self.__nVars

    def getMinterms(self) -> tuple[int]:

        """Return all minterms covered by this minterm combination."""

        return self.__minterms

    def getMask(self) -> int:

        """Return the mask associated with the minterm combination."""

        return self.__mask

    def combine(self, other: "MintermCombination") -> Literal[None] | "MintermCombination":

        """Return a new minterm, if self and other can be combined, otherwise return None."""

        differentNVars = self.getNVars() != other.getNVars()
        if differentNVars:  # Check if same number of variables
            raise AssertionError("Cannot combine minterms of functions of different size.")
        
        thisMask: int = self.getMask()
        otherMask: int = other.getMask()
        if thisMask != otherMask: # Check if same mask
            return None
        
        thisMinterms: tuple[int] = self.getMinterms()
        otherMinterms: tuple[int] = other.getMinterms()
        
        thisValue: int = thisMinterms[0]
        otherValue: int = otherMinterms[0]
        thisMasked: int = thisMask | thisValue
        otherMasked: int = otherMask | otherValue

        difference: int = thisMasked ^ otherMasked
        if difference.bit_count() == 1: # Check if differ by single bit
            newMask: int = thisMask | difference
            newMinterms = set()
            newMinterms.update(thisMinterms)
            newMinterms.update(otherMinterms)
            return MintermCombination(*newMinterms, mask=newMask, nVars=self.getNVars())
        else:
            return None
    