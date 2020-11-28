#!/usr/bin/env python

# Filename: novel_Alerts_App.pyw

"""
    Novel alerts is a simple GUI that allows the user to enter in data so that the application can web scrape novelupdates.com and send email alerts when updates are detected.
"""

#Import sys for clean closing of application memory
import sys
# Import threading to run webscraper along with GUI
import threading

# Import QApplication and the required widgets from PyQt5.QtWidgets
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
                             QMainWindow, QMessageBox, QPushButton,
                             QVBoxLayout, QWidget)

# Import NovelAlertsCtrl class to connect view and model through controller class within client code
from controller import NovelAlertsCtrl
# Import NovelAlertsModel class to pass object to controller within client code
from model import NovelAlertsModel

class NovelAlertsApp(QMainWindow):
    """NovelAlertsApp View (GUI)
    
    :param generalVLayout: Main layout for the central widget
    :type : QVBoxLayout
    :param : msgList 
    :type : List[QLabel]

    :param textF: Dictionarys that are in this format: {["Email", "Password", "URL"]: QLineEdit()}
    :type textF: Dict[]
    :param enterBtn: Push button for enter within a horizontal layout
    :type enterBtn: QPushButton
    :param deleteBtn: Push button for delete within a horizontal layout
    :type deleteBtn: QPushButton

    Subclass of QMainWindow
    """

    def __init__(self):
        """View Initializer/constructor"""

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
        self._createQLabelMsg()
        # Create and add QlineEdit Widget to generalVLayout
        self._createTextField()
        # Create and add Create/delet buttons
        self._createButton()
        # Set layout properties for vertical layout
        self.generalVLayout.setContentsMargins(300, 200, 300, 225)

    def _createQLabelMsg(self):
        """Creates a QLabel msg if email or password is not entered in"""

        # Make a list of QLabel's
        self.msgList = []
        self.msgList.append(QLabel("<h2>Email must be entered to enable web scraping!</h2>"))
        self.msgList.append(QLabel("<h2>Password must be entered to enable web scraping!</h2>"))

        # Sets QLabel properties and add to vertical layout
        for msg in self.msgList:
            msg.setAlignment(Qt.AlignCenter)
            msg.setWordWrap(True)
            # Add to general layout
            self.generalVLayout.addWidget(msg)

    def _createTextField(self):
        """Create input fields and adds to the vertical layout"""

        self.textF = {}
        # List that represents the type of data to be inputted for text fields
        dataInput = ["Email", "Password", "URL"]

        # Create the textfield widget using dictionary: {dataInput[0-n]: QLineEdit()}
        for dataLabel in dataInput:
            self.textF[dataLabel] = QLineEdit()

        def _setTextFieldProperties(lineEditObj, placeHolder):
            """Set textfield properties and adds QLineEdit to generalVLayout
            
            :param placeHolder: placeholder text to tell the user what type of data to enter
            :type placeHolder: String
            """

            lineEditObj.setFixedHeight(35)
            lineEditObj.setFixedWidth(500)
            lineEditObj.setAlignment(Qt.AlignLeft)
            lineEditObj.setPlaceholderText(placeHolder)
            lineEditObj.setClearButtonEnabled(True)
            # Add the textfield to the general vertical layout
            self.generalVLayout.addWidget(lineEditObj)
    
        # Iterate through dictionary and set QLineEdit properties
        for dataLabel in dataInput:
            _setTextFieldProperties(self.textF[dataLabel], dataLabel)

    def _createButton(self):
        """Create enter/delete buttons and add to general layout"""

        # Horizontal layout to make buttons look align horizontally
        horizontalLayout = QHBoxLayout()

        # Create button for entering data
        self.enterBtn = QPushButton("Enter")
        self.deleteBtn = QPushButton("Delete")

        def _setButtonProperties(buttonObj):
            """Set button properties and add QPushButton to horizontal layout"""

            buttonObj.setFixedSize(60, 35)
            # Add the enter/delete buttons to the horizontal layout
            horizontalLayout.addWidget(buttonObj)

        # Call _setButtonProperties to set properties and make horizontal
        _setButtonProperties(self.enterBtn)
        _setButtonProperties(self.deleteBtn)
        # Set horizontal layout properties
        horizontalLayout.setContentsMargins(200, 0, 200, 0)
        # Adds horizontal button layout to generalVLayout
        self.generalVLayout.addLayout(horizontalLayout)

    def getDisplayText(self, textF):
        """Get the specific text fields text
        
        :param textF: QLineEdit widget passed in to retrieve contents
        :type textF: QLineEdit
        :return text: Text or contents of the QLineEdit
        :rtype text: String
        """

        return textF.text()
    
    def clearTextField(self, textF):
        """Clears the text field of QLineEdit widgets
        
        :param textF: QLineEdit widget that is passed in to clear contents
        :type textF: QLineEdit
        """
        
        textF.clear()
        textF.setFocus()

    def msgBox(self, msg):
        """GUI QMessageBox to output any message such as errors or success/failure messages
        
        :param msg: Message to be shown on GUI through QMessageBox
        :type msg: String
        """

        alert = QMessageBox()
        alert.setText(msg)
        alert.exec_()

class NovelAlertsThread(QThread):
    """ Novel Alerts Thread Class

    :param model: Object of class NovelAlertsModel
    :type model: NovelAlertsModel
    """

    def __init__(self, model):
        """Thread Initializer/constructor"""

        QThread.__init__(self)
        self.model = model

    def __del__(self):
        """Thread destructor"""

        self.wait()

    def run(self):
        """Automaticly web scrapes for updated chapters every 10 minutes
        
        This function is called when NovelAlertsThread object.start() is called.
        """

        while True:
            # Calls Web scraper
            self.model._webScrape()
            # Pauses the loop for 10 minutes
            self.sleep(60 * 10)


def main():
    """Main function"""
    # Creates an instance/object of QApplication
    # Use sys.argv as parameter if you will have cmd-line args
    app = QApplication([])
    # Create the applications GUI.
    # Window is a instance/object of GUI/QMainWindow.
    window = NovelAlertsApp()
    # Shows GUI through a paint event. Think of it like a stack. 
    window.show()
    # Create an instance of model
    model = NovelAlertsModel(window.msgBox)
    # Create instance of the controller
    NovelAlertsCtrl(model=model, view=window)
    # Create instance of threading class and start the thread
    thread = NovelAlertsThread(model)
    thread.start()
    # Run app's event loop or main loop.
    # Allows for clean exit and release of memory resources.
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
