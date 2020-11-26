#!/usr/bin/env python

# Filename: novel_Alerts_App.pyw

"""
    Novel alerts is a simple GUI that allows the user to enter in data so that the application can web scrape novelupdates.com and send email alerts when updates are detected.
"""

#Import sys for clean closing of application memory
import sys

# Import QApplication and the required widgets from PyQt5.QtWidgets
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
                             QMainWindow, QMessageBox, QPushButton,
                             QVBoxLayout, QWidget)

from controller import NovelAlertsCtrl
# Import NovelAlertsModel class to connect view and model through controller class
from model import NovelAlertsModel


# Note subclass of Qmainwindow in docstring in classs
# Create a subclass of QMainWindow to setup novel alerts GUI
class NovelAlertsApp(QMainWindow):
    """NovelAlertsApp View (GUI)"""
    def __init__(self):
        """View Initializer"""
        super().__init__()
        # Gets the title to the app window.
        self.setWindowTitle("Novel-Alerts | PyQt5 Desktop Application | Webscraper")
        # Set the size of the window
        self.setFixedSize(1120, 640)
        # Set general layout
        self.generalVLayout = QVBoxLayout()
        # Creates a QWidget object as the central widget to be the "parent" for the other GUI components
        # Object is stored in a class variable -> "_centralWidget"
        self._centralWidget = QWidget(self)
        # Set the central widget
        self.setCentralWidget(self._centralWidget)
        # Set the layout onto the central widget
        self._centralWidget.setLayout(self.generalVLayout)
        # Moves the window to cords on screen.
        self.move(400, 200)
        # Create and add QLabel widget to generalVLayout
        self._createPasswordMsg()
        # Create and add QlineEdit Widget to generalVLayout
        self._createTextField()
        # Create and add Create/delet buttons
        self._createButton()
        # Set layout properties for vertical layout
        self.generalVLayout.setContentsMargins(300, 200, 300, 225)

    def _createPasswordMsg(self):
        """Creates a QLabel msg if password is not entered in"""
        # Create Qlabel
        self.msgList = []
        self.msgList.append(QLabel("<h2>Email must be entered to enable web scraping!</h2>"))
        self.msgList.append(QLabel("<h2>Password must be entered to enable web scraping!</h2>"))

        for msg in self.msgList:
            msg.setAlignment(Qt.AlignCenter)
            msg.setWordWrap(True)
            # Add to general layout
            self.generalVLayout.addWidget(msg)

    def _createTextField(self):
        """Create display for input field"""
        self.textF = {}
        dataInput = ["Email", "Password", "URL"]

        # Create the textfield widget
        for dataLabel in dataInput:
            self.textF[dataLabel] = QLineEdit()

        def _setTextFieldProperties(lineEditObj, placeHolder):
            """Set textfield properties and adds QLineEdit to generalVLayout"""
            lineEditObj.setFixedHeight(35)
            lineEditObj.setFixedWidth(500)
            lineEditObj.setAlignment(Qt.AlignLeft)
            lineEditObj.setPlaceholderText(placeHolder)
            lineEditObj.setClearButtonEnabled(True)
            # Add the textfield to the general vertical layout
            self.generalVLayout.addWidget(lineEditObj)
    
        # Call _setTextFieldProperties to keep code DRY
        for dataLabel in dataInput:
            _setTextFieldProperties(self.textF[dataLabel], dataLabel)

    def _createButton(self):
        """Create display for enter/delete buttons"""
        # horizontal layout to make buttons look better
        horizontalLayout = QHBoxLayout()

        # Create button for entering data
        self.enterBtn = QPushButton("Enter")
        self.deleteBtn = QPushButton("Delete")
        def _setButtonProperties(buttonObj):
            """Set button properties and add QPushButton to horizontal layout"""
            buttonObj.setFixedSize(60, 35)
            # Add the enter/delete buttons to the horizontal layout
            horizontalLayout.addWidget(buttonObj)

        # Call _setButtonProperties to keep code DRY
        _setButtonProperties(self.enterBtn)
        _setButtonProperties(self.deleteBtn)
        # Set horizontal layout properties
        horizontalLayout.setContentsMargins(200, 0, 200, 0)
        # Adds horizontal button layout to generalVLayout
        self.generalVLayout.addLayout(horizontalLayout)

    def getDisplayText(self, textF):
        """Get the specific text fields text"""
        return textF.text()
    
    def clearTextField(self, textF):
        """Clears the text field when enter/delete btns are clicked"""
        textF.clear()
        textF.setFocus()

    def msgBox(self, msg):
        """Alert box for if user tries to delete email instead of enter new one"""
        alert = QMessageBox()
        alert.setText(msg)
        alert.exec_()



# Client code
def main():
    """Main function"""
    # Creates an instance/object of QApplication
    # Use sys.argv as parameter if you will have cmd-line args
    app = QApplication([])
    # Create the applications GUI.
    # Window is a instance/object of QWidget.
    window = NovelAlertsApp()
    # Shows GUI through a paint event. Think of it like a stack. 
    window.show()
    # Create an instance of model
    model = NovelAlertsModel(window.msgBox)
    # Create instance of the controller
    NovelAlertsCtrl(model=model, view=window)
    # Run app's event loop or main loop.
    # Allows for clean exit and release of memory resources.
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
