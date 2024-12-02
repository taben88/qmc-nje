from ConsoleView import ConsoleView
from QMC import QMC
from Controller import Controller

class ConsoleController(Controller):

    """Controller for the console view."""

    def __init__(self, view: ConsoleView):
        self._view: ConsoleView = view
        self._model: QMC = None
   
    def run(self) -> None:

        """Runs calculation and output results or errors stemming from user input to console."""

        if error := self.initQMC():
            self._view.outputError(error)
            return
        self._view.outputResult(result=self.calculate())