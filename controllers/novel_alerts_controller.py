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
    
    def __init__(self, model: object, view: object):
        """Controller Initializer"""

        self._view = view
        self._model = model
        self._connect_signals()

        # Check if email is already loaded and if so, clear email msg
        if self._model.getEmail():
            self._view.messages[0].setText("")

    def _check_enter(self):
        """Checks text field input and enters data into NovelAlertsModel object."""

        for key, value in self._view.textFields.items():
            # Checks if the textFields have input and gets rid of QLabel messages once email and password are entered
            if self._view.getDisplayText(self._view.textFields[key]) and key == "Email":
                self._model.setEmail(value.text())
                self._view.messages[0].setText("")
            if self._view.getDisplayText(self._view.textFields[key]) and key == "Password":
                self._model.setPassword(value.text())
                self._view.messages[1].setText("")
            if self._view.getDisplayText(self._view.textFields[key]) and key == "URL":
                self._model.addURLData(value.text())

            self._view.clearLineEdit(self._view.textFields[key])

    def _check_delete(self) -> None:
        """Checks input from textFields and only deletes URL data, otherwise an error message is displayed."""

        for key, value in self._view.textFields.items():
            # Checks if textFields have input
            if self._view.getDisplayText(self._view.textFields[key]) and key == "Email":
                self._view.msgBox("ERROR: Cannot delete email, only enter in new one!")
            if self._view.getDisplayText(self._view.textFields[key]) and key == "Password":
                self._view.msgBox("ERROR: Cannot delete password, only enter in new one!")
            if self._view.getDisplayText(self._view.textFields[key]) and key == "URL":
                self._model.deleteURLData(value.text())

            self._view.clearLineEdit(self._view.textFields[key])  

    def _connect_signals(self):
        """Connects the button signals to the _checkEnter and _checkDelete slots/methods."""

        self._view.enterButton.clicked.connect(lambda: self._check_enter())
        self._view.deleteButton.clicked.connect(lambda: self._check_delete())