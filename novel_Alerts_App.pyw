#!/usr/bin/env python

# Filename: novel_Alerts_App.pyw

"""
    Novel alerts is a simple GUI that allows the user to enter in data so that the application can web scrape novelupdates.com and send email alerts when updates occur.
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

# from functools import partial 
# If i want extra parameters for slots


# Create a subclass of QMainWindow to setup novel alerts GUI
class NovelAlertsApp(QMainWindow):
    """NovelAlertsApp View (GUI)"""
    def __init__(self):
        """View Initializer"""
        super().__init__()
        # Gets the title to the app window.
        self.setWindowTitle("Novel-Alerts | PyQt5 Desktop Application | Webscraper")
        # Set the size of the window and where to place it on the screen.
        # First two parameters are x and y cords on where window will be on screen.
        # Last two parameters are width and height of the window.
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
        self.move(350, 230)
        # Creates central display
        self._createCentralDisplay()
        # Set layout properties for vertical layout
        self.generalVLayout.setContentsMargins(25, 225, 0, 325)

    def _createCentralDisplay(self):
        """Creates the central display"""
        btnList = ["Email", "URL"]
        for i in range(2):
            # Define horizontal layout
            horizontalLayout = QHBoxLayout()
            # Create and add QlineEdit Widget
            self._createTextField(horizontalLayout, btnList[i])
            # Create and add Create/delet buttons
            self._createButton(horizontalLayout)
            # Set layout properties for horizontal layout
            horizontalLayout.setContentsMargins(300, 0, 300, 0)
            # Add to generalVLayout
            self.generalVLayout.addLayout(horizontalLayout)

    def _createTextField(self, horizontalLayout, placeHolder):
        """Create display for input field"""
        # Create the textfield widget
        self.textField = QLineEdit()
        # Set textfield properties
        self.textField.setFixedHeight(30)
        self.textField.setFixedWidth(300)
        self.textField.setAlignment(Qt.AlignRight)
        self.textField.setPlaceholderText(placeHolder)
        self.textField.setClearButtonEnabled(True)
        # Add the textfield to the horizontal layout
        horizontalLayout.addWidget(self.textField)

    def _createButton(self, horizontalLayout):
        """Create display for enter/delete buttons"""
        # Create button for entering data
        self.enterBtn = QPushButton("Enter")
        self.deleteBtn = QPushButton("Delete")
        # Settin button properties
        self.enterBtn.setFixedSize(60, 35)
        self.deleteBtn.setFixedSize(60, 35)
        # Add the enter/delete buttons to the horizontal layout
        horizontalLayout.addWidget(self.enterBtn)
        horizontalLayout.addWidget(self.deleteBtn)

    def clearTextField(self):
        """Clears the text field when enter/delete btns are clicked"""
        self.textField.clear()
        self.textField.setFocus()

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
    # Run app's event loop or main loop.
    # Allows for clean exit and release of memory resources.
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
