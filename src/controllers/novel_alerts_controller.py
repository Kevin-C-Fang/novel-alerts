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

    TYPES = ["Email", "Password", "URL"]
    
    def __init__(self, model_Obj: object, view_Obj: object) -> None:
        """Controller Initializer"""

        self.view = view_Obj
        self.model = model_Obj
        self._connect_signals()

        # Check if email is already loaded and if so, clear email msg
        if self.model.getEmail():
            self.view.messages[0].setText("")

    def _check_Enter(self) -> None:
        """Checks text field input and enters data into NovelAlertsModel object."""

        # Checks if the textFields have input and gets rid of QLabel messages once email and password are entered
        if self.view.textFields[self.TYPES[0]].text():
            self.model.setEmail(self.view.textFields[self.TYPES[0]].text())
            self.view.messages[0].setText("")
            self.view.clearLineEdit(self.view.textFields[self.TYPES[0]])
        if self.view.textFields[self.TYPES[1]].text():
            self.model.setPassword(self.view.textFields[self.TYPES[1]].text())
            self.view.messages[1].setText("")
            self.view.clearLineEdit(self.view.textFields[self.TYPES[1]])
        if self.view.textFields[self.TYPES[2]].text():
            self.model.addURLData(self.view.textFields[self.TYPES[2]].text())
            self.view.clearLineEdit(self.view.textFields[self.TYPES[2]])

    def _check_Delete(self) -> None:
        """Checks input from textFields and only deletes URL data, otherwise an error message is displayed."""

        # Checks if textFields have input and clears text fields if there is input
        if self.view.textFields[self.TYPES[0]].text():
            self.view.msgBox("ERROR: Cannot delete email, only enter in new one!")
            self.view.clearLineEdit(self.view.textFields[self.TYPES[0]])
        if self.view.textFields[self.TYPES[1]].text():
            self.view.msgBox("ERROR: Cannot delete password, only enter in new one!")
            self.view.clearLineEdit(self.view.textFields[self.TYPES[1]])
        if self.view.textFields[self.TYPES[2]].text():
            self.model.deleteURLData(self.view.textFields[self.TYPES[2]].text())
            self.view.clearLineEdit(self.view.textFields[self.TYPES[2]])

    def _connect_signals(self) -> None:
        """Connects the button signals to the _checkEnter and _checkDelete slots/methods."""

        self.view.buttons[0].clicked.connect(lambda: self._check_Enter())
        self.view.buttons[1].clicked.connect(lambda: self._check_Delete())