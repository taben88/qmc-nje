from GUIView import GUIView
from Controller import Controller
from io import StringIO

class GUIController(Controller):

    """Controller for the GUI view."""

    def __init__(self, view: GUIView) -> None:
        super().__init__(view=view)
        self._view: GUIView
        self._view._submitButton.bind(sequence="<Button-1>", func=lambda _: self.__onSubmit())
        self._view._primeImplicantsTree.bind(sequence="<Control-c>", func=lambda _:self.__primeImplicantstoClipboard())

    def __primeImplicantstoClipboard(self) -> None:

        """Copy selected prime implicants to the clipboard."""

        with StringIO() as buffer:
            for i in self._view.getTreeSelectionContent():
                print("\t".join(i), file=buffer)
            out: str = buffer.getvalue()
        self._view.toClipboard(out)

    def __onSubmit(self) -> None:

        """Callback of submit button. Run calculation and output results or errors stemming from user input."""

        if error := self.initQMC():
            self._view.outputError(error)
            return
        self._view.outputResult(result=self.calculate())
        self._view.showOutput()
        self._view.centerWindow()

    def run(self) -> None:

        """Start GUI."""

        self._view.centerWindow()
        self._view.mainloop()