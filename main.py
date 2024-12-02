from Controller import Controller
from ConsoleController import ConsoleController
from GUIController import GUIController
from View import View
from ConsoleView import ConsoleView
from GUIView import GUIView

def main():
    view: View = ConsoleView()
    controller: Controller
    if not view.getMinterms():
        view = GUIView()
        controller = GUIController(view=view)
    else:
        controller = ConsoleController(view=view)
    controller.run()

if __name__ == "__main__":
    main()
