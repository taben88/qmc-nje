from collections.abc import Iterable

class Utils:
    @staticmethod
    def absorb(this: int, other: int) -> int:

        """Return this, if this is equal to bitwise intersection of this and other, else return other."""

        intersection: int = this & other
        if this == intersection:
            return this
        else:
            return other

    @classmethod
    def absorbAll(cls, this: int, others: Iterable[int]) -> list[int]:

        """Return a list gained by filtering others with this using the boolean law of absorption."""

        result: set[int] = set()
        for other in others:
            result.add(
                cls.absorb(this, other)
                )
        return list(result)

    @classmethod
    def reduceByAbsorption(cls, terms: Iterable[int]) -> list[int]:

        """Return a list from terms filtered using the boolean law of absorption."""

        reduced: list[int] = sorted(terms, key=lambda i: i.bit_count())
        for term in terms:
            reduced = cls.absorbAll(term, reduced)
        return reduced

    @classmethod
    def distribute(cls, terms: list[tuple[int]], out: list[int]) -> list[int]:

        """Implementation of boolean distribution. Tuples of bitfields represent the groups of variables. If input was DNF output is CNF and vica-versa."""

        prefix: tuple[int] = terms.pop()
        newOut: list[int] = []
        for i in prefix:
            for j in out:
                newOut.append(i|j)
        if terms:
            return cls.distribute(terms=terms, out=newOut)
        else:
            return newOut

    @staticmethod
    def decomposeBitField(bitField: int) -> tuple[int]:

        """Return a tuple populated by breaking up a bit field into of powers of two."""

        out: list[int] = []
        exponent: int = 0
        while bitField:
            if bitField & 1:
                out.append(1 << exponent)
            bitField >>= 1
            exponent += 1
        return tuple(out)