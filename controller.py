# Filename: controller.py

"""Controller that connects data flow from the view(GUI) to the model."""

class NovelAlertsCtrl:
    """
    A class that represents the controller for the Model-View-Controller(MVC) design pattern. Controller receives events/requests and input from the view that puts the model to work.
    
    :param model: Object of the NovelAlertsModel class (Model)
    :type model: NovelAlertsModel
    :param view: Object of the NovelAlertsApp class (View)
    :type view: NovelAlertsApp
    """
    
    def __init__(self, model, view):
        """Controller initializer/constructor
        
        :param model: NovelAlertsModel class Object
        :type model: NovelAlertsModel
        :param view: NovelAlertsApp class object
        :type view: NovelAlertsApp
        """

        self._view = view
        self._model = model
        self._connectSignals()

        # Check if email is already logged and if so, clear email msg
        if self._model.usrEmail:
            self._view.msgList[0].setText("")

    def _checkEnter(self):
        """Checks text field input and enters data into NovelAlertsModel object."""

        # Iterates through text fields: textF - > {"Type of data": QLineEdit}
        for key, value in self._view.textF.items():
            # Checks if the textfields have input and that the type of data is correct
            # Then it uses methods from the class NovelAlertsModel to enter data
            # Also, sets the text of the msgs to empty strings once Email and Password are entered
            if self._view.getDisplayText(self._view.textF[key]) != "" and key == "Email":
                self._model.setEmail(value.text())
                self._view.msgList[0].setText("")
            if self._view.getDisplayText(self._view.textF[key]) != "" and key == "Password":
                self._model.setPassword(value.text())
                self._view.msgList[1].setText("")
            if self._view.getDisplayText(self._view.textF[key]) != "" and key == "URL":
                # Enters URL data into object, but raises exception using function parameter if URL is not valid
                self._model._addURLData(value.text())
            # Clears text field
            self._view.clearTextField(self._view.textF[key])

    def _checkDelete(self):
        """Checks input from textfields and only deletes URL data, otherwise an error message is displayed."""

        # Iterates through text fields: textF - > {"Type of Data": QLineEdit}
        for key, value in self._view.textF.items():
            # Checks if textfields have input and that type of data is correct
            # Calls msgBox method if user tries to delete email or password
            if self._view.getDisplayText(self._view.textF[key]) != "" and key == "Email":
                self._view.msgBox("ERROR: Cannot delete email, only enter in new one!")
            if self._view.getDisplayText(self._view.textF[key]) != "" and key == "Password":
                self._view.msgBox("ERROR: Cannot delete password, only enter in new one!")
            if self._view.getDisplayText(self._view.textF[key]) != "" and key == "URL":
                # Deletes URL data from object and CSV file
                # Calls errogmsg method if URL is not within data
                self._model.deleteURLData(value.text())
            # Clears text field
            self._view.clearTextField(self._view.textF[key])  

    def _connectSignals(self):
        """Connects the button signals to the _checkEnter and _checkDelete slots/methods."""

        self._view.enterBtn.clicked.connect(lambda: self._checkEnter())
        self._view.deleteBtn.clicked.connect(lambda: self._checkDelete())