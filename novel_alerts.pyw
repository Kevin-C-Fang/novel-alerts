#!/usr/bin/env python

# Filename: novel_alerts.pyw

"""Novel alerts is a simple GUI that allows the user to enter in data so that the application can web scrape novelupdates.com and send email alerts when updates are detected."""

#Import sys for clean closing of application memory
import sys

# Import QApplication to create instance of application GUI
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication

# Import MVC and thread file to run GUI
from src.models.novel_alerts_model import NovelAlertsModel
from src.views.novel_alerts_view import NovelAlertsView
from src.controllers.novel_alerts_controller import NovelAlertsController
from src.threads.novel_alerts_thread import NovelAlertsThread


def main():
    """Main function"""

    app = QApplication([])

    window = NovelAlertsView()
    window.show()

    model = NovelAlertsModel(window.msgBox)
    NovelAlertsController(model_Obj=model, view_Obj=window)

    thread = NovelAlertsThread(model, window.msgBox)
    thread.start()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
