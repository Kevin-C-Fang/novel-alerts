# Filename: novel_alerts_view.py

"""View that is solely focused on the GUI aspect of the application."""

# Import PyQt5 and the required widgets from PyQt5.QtWidgets
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QHBoxLayout, QLabel, QLineEdit,
                             QMainWindow, QMessageBox, QPushButton,
                             QVBoxLayout, QWidget)

class NovelAlertsView(QMainWindow):
    """
    A class that represents the view for the Model-View-Controller(MVC) design pattern. 
    
    :param _general_vertical_layout: Main layout for the central widget
    :type : QVBoxLayout
    :param : messages 
    :type : List[QLabel]

    :param textFields: Dictionarys that are in this format: {["Email", "Password", "URL"]: QLineEdit()}
    :type textFields: Dict[str, QLineEdit]
    :param enterButton: Push button for enter within a horizontal layout
    :type enterButton: QPushButton
    :param deleteButton: Push button for delete within a horizontal layout
    :type deleteButton: QPushButton

    Subclass of QMainWindow
    """

    def __init__(self) -> None:
        """View Initializer"""

        super().__init__()

        self.setWindowTitle("Novel-Alerts | PyQt5 Desktop Application | Webscraper")
        self.setFixedSize(1120, 640)
        self._general_vertical_layout = QVBoxLayout()

        self._central_widget = QWidget(self)
        self.setCentralWidget(self._central_widget)
        self._central_widget.setLayout(self._general_vertical_layout)

        self.move(400, 200)

        self._create_Qlabel_msg()
        self._create_text_fields()
        self._create_button()

        self._general_vertical_layout.setContentsMargins(300, 200, 300, 225)

    def _create_Qlabel_msg(self) -> None:
        """Creates a QLabel messages that tells if the email and password have been entered"""

        self.messages = [QLabel("<h2>Email must be entered to enable web scraping!</h2>"), 
                        QLabel("<h2>Password must be entered to enable web scraping!</h2>")]

        def _set_label_message_properties(label_object: QLabel) -> None:
            """Set QLabel properties and add to vertical layout"""

            label_object.setAlignment(Qt.AlignCenter)
            label_object.setWordWrap(True)

            self._general_vertical_layout.addWidget(label_object)

        for message in self.messages:
            _set_label_message_properties(message)

    def _create_text_fields(self) -> None:
        """Create text fields and adds to the vertical layout"""

        self.textFields = {}
        # Type of data to be inputted for text fields and Key for dict
        types = ["Email", "Password", "URL"]

        # Create dictionary holding {"type": QLineEdit}
        for type_ in types:
            self.textFields[type_] = QLineEdit()

        def _set_text_field_properties(lineEditObj: QLineEdit, placeHolder: str) -> None:
            """Set lineEditield properties and adds QLineEdit to _general_vertical_layout"""

            lineEditObj.setFixedHeight(35)
            lineEditObj.setFixedWidth(500)
            lineEditObj.setAlignment(Qt.AlignLeft)
            lineEditObj.setPlaceholderText(placeHolder)
            lineEditObj.setClearButtonEnabled(True)

            self._general_vertical_layout.addWidget(lineEditObj)
    
        for type_ in types:
            _set_text_field_properties(self.textFields[type_], type_)

    def _create_button(self) -> None:
        """Create enter/delete buttons and add to general layout"""

        horizontal_layout = QHBoxLayout()

        self.buttons = [QPushButton("Enter"), QPushButton("Delete")]

        def _set_button_properties(button: QPushButton) -> None:
            """Set button properties and add QPushButton to horizontal layout"""

            button.setFixedSize(60, 35)
            horizontal_layout.addWidget(button)

        for button in self.buttons:
            _set_button_properties(button)

        horizontal_layout.setContentsMargins(200, 0, 200, 0)
        self._general_vertical_layout.addLayout(horizontal_layout)

    def clearLineEdit(self, line_edit: QLineEdit) -> None:
        """Clears the Text Fields/QLineEdit widgets"""
        
        line_edit.clear()
        line_edit.setFocus()

    def msgBox(self, message: str) -> None:
        """GUI QMessageBox to pop up any messages such as errors or success/failure messages"""

        alert = QMessageBox()
        alert.setText(message)
        alert.exec_()