#!/usr/bin/env python

# Filename: novel_Alerts_App.pyw

"""
    Novel alerts is a simple GUI that allows the user to enter in data so that the application can web scrape novelupdates.com and send email alerts when updates are detected.
"""

import sys

# Import QApplication and the required widgets from PyQt5.QtWidgets
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout

from functools import partial 

from model import NovelAlertsModel


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
        # Create and add QlineEdit Widget to generalVLayout
        self._createTextField()
        # Create and add Create/delet buttons
        self._createButton()
        # Set layout properties for vertical layout
        self.generalVLayout.setContentsMargins(300, 200, 300, 250)

    def _createTextField(self):
        """Create display for input field"""
        self.textF = {}
        dataInput = ["Email", "URL"]

        # Create the textfield widget
        self.textF[dataInput[0]] = QLineEdit()
        self.textF[dataInput[1]] = QLineEdit()

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
        _setTextFieldProperties(self.textF[dataInput[0]], dataInput[0])
        _setTextFieldProperties(self.textF[dataInput[1]], dataInput[1])

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

    def clearTextField(textF):
        """Clears the text field when enter/delete btns are clicked"""
        textF.clear()
        textF.setFocus()

# Constroller class to connect the view (GUI) and the model
class NovelAlertsCtrl:
    """Novel Alerts Controller class"""
    def __init__(self, model, view):
        """Controller initializer"""
        self._view = view
        self._model = model
        # Connect btn signals to slots
        self._connectSignals()

    def _connectSignals(self):
        """Connect signals and slots"""
        pass

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
    # Create instances of the model and controller
    NovelAlertsCtrl(model=NovelAlertsModel, view=window)
    # Run app's event loop or main loop.
    # Allows for clean exit and release of memory resources.
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()