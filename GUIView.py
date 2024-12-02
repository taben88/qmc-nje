from View import View
import tkinter as tk
from tkinter.messagebox import showerror
from tkinter import ttk
import re

class GUIView(View):

    @staticmethod
    def __isSpaceSeperatedPosInt(text: str) -> bool:

        """Return true if text is a mix of numerics and white space."""

        # Helper for input validation

        pattern: str = r"^[\ \d]+$"
        match: re.Match = re.match(pattern=pattern, string=text)
        return bool(match) or text == ""

    @staticmethod
    def __isPosInt(text: str) -> bool:

        """Return true if text is an unsigned integer."""

        # Helper for input validation

        pattern: str = r"^\d*$"
        match: re.Match = re.match(pattern=pattern, string=text)
        return bool(match)

    def __init__(self) -> None:
        self.__root: tk.Tk = tk.Tk()

        # Main frame
        self.__mainFrame: tk.Frame = tk.Frame(master=self.__root)
        self.__mainFrame.pack(fill=tk.BOTH)

        # Containers and widgets for accepting input
        self.__inputFrame: tk.Frame = tk.Frame(master=self.__mainFrame)
        self.__inputFrame.pack(fill=tk.X)

        self.__mintermsFrame: tk.LabelFrame = tk.LabelFrame(master=self.__inputFrame, text="Minterms")
        self.__minterms: tk.StringVar = tk.StringVar(master=self.__mintermsFrame)
        self.__mintermsEntry: tk.Entry = tk.Entry(master=self.__mintermsFrame, textvariable=self.__minterms, validatecommand=(self.__root.register(self.__isSpaceSeperatedPosInt),'%P'), validate="all")
        self.__mintermsFrame.pack(fill=tk.X)
        self.__mintermsEntry.pack(fill=tk.X)

        self.__dontCaresFrame: tk.LabelFrame = tk.LabelFrame(master=self.__inputFrame, text="Don't-cares")
        self.__dontCares: tk.StringVar = tk.StringVar(master=self.__dontCaresFrame)
        self.__donCaresEntry: tk.Entry = tk.Entry(master=self.__dontCaresFrame, textvariable=self.__dontCares, validatecommand=(self.__root.register(self.__isSpaceSeperatedPosInt),'%P'), validate="all")
        self.__dontCaresFrame.pack(fill=tk.X)
        self.__donCaresEntry.pack(fill=tk.X)

        self.__nVarsFrame: tk.LabelFrame = tk.LabelFrame(master=self.__inputFrame, text="Number of variables (0 to auto calculate)")
        self.__nVars: tk.IntVar = tk.IntVar(master=self.__nVarsFrame, value=0)
        self.__nVarsEntry: tk.Entry = tk.Entry(master=self.__nVarsFrame, textvariable=self.__nVars, validatecommand=(self.__root.register(self.__isPosInt),'%P'), validate="all", justify=tk.RIGHT)
        self.__nVarsFrame.pack(fill=tk.X)
        self.__nVarsEntry.pack(fill=tk.X)

        # Submit button
        self.__buttonFrame: tk.Frame = tk.Frame(master=self.__mainFrame) 
        self._submitButton: tk.Button = tk.Button(master=self.__buttonFrame, text="Submit")
        self._submitButton.pack()
        self.__buttonFrame.pack(fill=tk.X)

        # Containers and widgets for rendering output, starts not visible
        self.__outputFrame: tk.Frame = tk.Frame(master=self.__mainFrame)

        self.__mintermsOutFrame: tk.LabelFrame = tk.LabelFrame(master=self.__outputFrame, text="Minterms")
        self.__mintermsOutFrame.pack(fill=tk.X)
        self.__outMinterms: tk.Entry = tk.Entry(master=self.__mintermsOutFrame)
        self.__outMinterms.pack(fill=tk.X)

        self.__dontCaresOutFrame: tk.LabelFrame = tk.LabelFrame(master=self.__outputFrame, text="Don't-cares")
        self.__dontCaresOutFrame.pack(fill=tk.X)
        self.__outDontCares: tk.Entry = tk.Entry(master=self.__dontCaresOutFrame)
        self.__outDontCares.pack(fill=tk.X)

        self.__primeImplicantsFrame: tk.LabelFrame = tk.LabelFrame(master=self.__outputFrame, text="Prime Implicants")
        self._primeImplicantsTree: ttk.Treeview = ttk.Treeview(master=self.__primeImplicantsFrame, columns=["minterms", "mask"], show="headings")
        self._primeImplicantsTree.heading("minterms", text="Minterms")
        self._primeImplicantsTree.heading("mask", text="Mask")
        self.__primeImplicantsFrame.pack(fill=tk.X)
        self._primeImplicantsTree.pack(fill=tk.X)

        self.__coveringSetsFrame: tk.LabelFrame = tk.LabelFrame(master=self.__outputFrame, text="Covering Sets")
        self.__coveringSetsListbox: tk.Listbox = tk.Listbox(master=self.__coveringSetsFrame)        
        self.__coveringSetsFrame.pack(fill=tk.X)
        self.__coveringSetsListbox.pack(fill=tk.X)

    def showOutput(self) -> None:

        """Makes frame with output visible."""

        self.__outputFrame.pack(fill=tk.X, after=self.__buttonFrame)

    def getMinterms(self) -> list[int]:

        """Get the value of minterms entry field as list of integers."""

        minterms = [int(i) for i in self.__minterms.get().split()]
        return minterms
    
    def getDontCares(self) -> list[int]:

        """Get the value of don't-cares entry field as list of integers."""

        dontCares = [int(i) for i in self.__dontCares.get().split()]
        return dontCares

    def getNVars(self) -> int:
        
        """Get the value of number of variables entry field."""

        return self.__nVars.get()
    
    def getTreeSelectionContent(self) -> list[tuple[str, str]]:

        """Return a list of tuples with the values of the selected rows."""

        selectionContent: list[tuple[str, str]] = []
        for i in self._primeImplicantsTree.selection():
            rowContent: tuple[str, str] = self._primeImplicantsTree.item(item=i, option="values")
            selectionContent.append(rowContent)
        return selectionContent
    
    def toClipboard(self, text: str) -> None:

        """Clear clipboard and append the value of text to it."""

        self.__root.clipboard_clear()
        self.__root.clipboard_append(string=text)
    
    def centerWindow(self) -> None:

        """Centers window."""

        self.__root.update_idletasks()
        windowCenter: tuple[int, int] = self.__root.winfo_screenwidth() // 2, self.__root.winfo_screenheight() // 2
        windowSize: tuple[int, int] = self.__root.winfo_width(), self.__root.winfo_height()
        topLeft: tuple[int, int] = windowCenter[0] - windowSize[0] // 2, windowCenter[1] - windowSize[1] // 2
        newGeometry: str = f"+{topLeft[0]}+{topLeft[1]}"
        self.__root.geometry(newGeometry=newGeometry)

    @staticmethod
    def __setReadOnlyEntry(entry: tk.Entry, value: str) -> None:

        """Clear and set value of read-only Entry widget."""

        entry.configure(state="normal")
        entry.delete(first=0, last=tk.END)
        entry.insert(index=0, string=value)
        entry.configure(state="readonly")

    def __populatePrimeImplicantsTree(self, primeImplicants: list[tuple[str, str]]) -> None:

        """Clear and populate TreeView widget holding prime implicants."""

        for i in self._primeImplicantsTree.get_children():
            self._primeImplicantsTree.delete(i)
        for i in primeImplicants:
            self._primeImplicantsTree.insert(parent="", index=tk.END, values=[i[0], i[1]])

    def __populateCoveringSetsListBox(self, coveringSets: list[str]) -> None:

        """Clear and populate ListBox widget holding covering sets."""

        self.__coveringSetsListbox.delete(first=0, last=tk.END)
        for i in coveringSets:
            self.__coveringSetsListbox.insert(tk.END, i)

    def outputResult(self, result: dict[str, str|list[str]|list[tuple[str, str]]]) -> None:

        """Public wrapper around methods responsible for rendering output."""

        self.__setReadOnlyEntry(entry=self.__outMinterms, value=result["minterms"])
        self.__setReadOnlyEntry(entry=self.__outDontCares, value=result["dontCares"])
        self.__populatePrimeImplicantsTree(primeImplicants=result["primeImplicants"])
        self.__populateCoveringSetsListBox(coveringSets=result["coveringSets"])
    
    def outputError(self, error: Exception) -> None:

        """Show error dialog box with message of error passed."""

        showerror(title="Invalid input", message=str(error))

    def mainloop(self) -> None:

        """Wrapper around root Tk object's mainloop method."""

        self.__root.mainloop()