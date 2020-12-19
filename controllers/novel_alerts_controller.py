# Filename: novel_alerts_controller.py

"""Controller that connects data flow from the view(GUI) to the model."""

class NovelAlertsController:
    """
    A class that represents the controller for the Model-View-Controller(MVC) design pattern. 
    
    Controller receives events/requests and input from the view that puts the model to work.
    
    :param model: Object of the NovelAlertsModel class (Model)
    :type model: NovelAlertsModel
    :param view: Object of the NovelAlertsView class (View)
    :type view: NovelAlertsView
    """
    
    def __init__(self, model: object, view: object) -> None:
        """Controller Initializer"""

        self._view = view
        self._model = model
        self._connect_signals()

        # Check if email is already loaded and if so, clear email msg
        if self._model.getEmail():
            self._view.messages[0].setText("")

    def _check_enter(self) -> None:
        """Checks text field input and enters data into NovelAlertsModel object."""

        # Checks if the textFields have input and gets rid of QLabel messages once email and password are entered
        if self._view.textFields["Email"].text():
            self._model.setEmail(self._view.textFields["Email"].text())
            self._view.messages[0].setText("")
            self._view.clearLineEdit(self._view.textFields["Email"])
        if self._view.textFields["Password"].text():
            self._model.setPassword(self._view.textFields["Password"].text())
            self._view.messages[1].setText("")
            self._view.clearLineEdit(self._view.textFields["Password"])
        if self._view.textFields["URL"].text():
            self._model.addURLData(self._view.textFields["URL"].text())
            self._view.clearLineEdit(self._view.textFields["URL"])

    def _check_delete(self) -> None:
        """Checks input from textFields and only deletes URL data, otherwise an error message is displayed."""

        # Checks if textFields have input and clears text fields if there is input
        if self._view.textFields["Email"].text():
            self._view.msgBox("ERROR: Cannot delete email, only enter in new one!")
            self._view.clearLineEdit(self._view.textFields["Email"])
        if self._view.textFields["Password"].text():
            self._view.msgBox("ERROR: Cannot delete password, only enter in new one!")
            self._view.clearLineEdit(self._view.textFields["Password"])
        if self._view.textFields["URL"].text():
            self._model.deleteURLData(self._view.textFields["URL"].text())
            self._view.clearLineEdit(self._view.textFields["URL"])

    def _connect_signals(self) -> None:
        """Connects the button signals to the _checkEnter and _checkDelete slots/methods."""

        self._view.enterButton.clicked.connect(lambda: self._check_enter())
        self._view.deleteButton.clicked.connect(lambda: self._check_delete())