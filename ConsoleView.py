import argparse
from View import View
from io import StringIO

class ConsoleView(View):
    def __init__(self) -> None:
        self.rootParser: argparse.ArgumentParser = argparse.ArgumentParser(prog="Boolean function minimizer")
        parsers: argparse._SubParsersAction[argparse.ArgumentParser] = self.rootParser.add_subparsers()
        self.GUISubparser: argparse.ArgumentParser = parsers.add_parser("g", help="Start minimizer in GUI mode (default).")
        self.consoleSubparser: argparse.ArgumentParser= parsers.add_parser("c", help="Start minimizer in console mode.")
        self.consoleSubparser.add_argument("MINTERMS", nargs="+", type=int, help="The minterms of the function to minimize, seperated by white space.")
        self.consoleSubparser.add_argument("-dc", nargs="*", dest="DONT_CARES", type=int, default=[], help="List of don't-care terms, seperated by white space.")
        self.consoleSubparser.add_argument("-nv", nargs="?", dest="NVARS", type=int, default=0, help="The number of variables of the boolean function, if different from least number of variables needed to express the highest term.")
        self.args: dict[str, int|list[int]] = vars(self.rootParser.parse_args())

    def getMinterms(self) -> list[int]:

        """Get list of minterms from input."""

        return self.args.get("MINTERMS", [])
    
    def getDontCares(self) -> list[int]:

        """Get list of don't-cares from input."""

        return self.args["DONT_CARES"]
    
    def getNVars(self) -> int:

        """Get number of variables from input or 0, if not specified."""

        return self.args["NVARS"]
    
    @staticmethod
    def __assemblePrimeImplicantsTable(primeImplicants: list[tuple[str, str]]) -> str:

        """Helper function that returns a string table of the prime implicants."""

        headers: tuple[str, str] = "MINTERMS", "MASK"
        longestRow: int = len(max(primeImplicants, key=lambda i: len(i[0])))
        longestRow = longestRow if longestRow >= len(headers[0]) else len(headers[0])

        with StringIO() as buffer:
            print(headers[0].ljust(longestRow), headers[1], sep="\t", file=buffer)
            for i in primeImplicants:
                minterms: str = i[0]
                print(minterms.ljust(longestRow), i[1], sep="\t", file=buffer)
            table: str = buffer.getvalue()
        return table
    
    @staticmethod
    def __assembleCoveringSetsTable(coveringSets: list[str]) -> str:

        """Helper function that returns a string table of the covering sets."""

        with StringIO() as buffer:
            for i in coveringSets:
                print(i, file=buffer)
            table: str = buffer.getvalue()
        return table

    def outputResult(self, result: dict[str, str|list[str]|list[tuple[str, str]]]) -> None:

        """Render output to console."""

        minterms: str = result["minterms"]
        dontCares: str = result["dontCares"]
        primeImplicants: list[tuple[str, str]] = result["primeImplicants"]
        coveringSets: list[str] = result["coveringSets"]
        
        paddedLength: int = 30
        print(f"{'MINTERMS':-^{paddedLength}}")
        print(minterms)
        print()
        
        if dontCares:
            print(f"{'DONT-CARES':-^{paddedLength}}")
            print(dontCares)
            print()

        print(f"{'PRIME IMPLICANTS':-^{paddedLength}}")
        print(self.__assemblePrimeImplicantsTable(primeImplicants=primeImplicants))
        
        print(f"{'COVERING SETS':-^{paddedLength}}")
        print(self.__assembleCoveringSetsTable(coveringSets=coveringSets))
    
    def outputError(self, error: Exception) -> None:

        """Re-raise error passed."""

        raise error

