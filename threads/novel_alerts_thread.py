# Filename: novel_alerts_thread.py

"""Thread class that allows for concurrently operations."""

# Import callable to type annotate functions
from typing import Callable

# Import QThread to run webscraper along with GUI
from PyQt5.QtCore import QThread


class NovelAlertsThread(QThread):
    """ 
    Novel Alerts Thread Class

    :param model: Object of class NovelAlertsModel
    :type model: NovelAlertsModel
    :param message_box: NovelAlertsView method that brings up a QMessageBox box
    :type message_box: NovelAlertsView method

    Subclass of QThread
    """

    def __init__(self, model: object, message_box: Callable) -> None:
        """Thread Initializer"""

        QThread.__init__(self)
        self.model = model
        self._message_box = message_box

    def __del__(self) -> None:
        """Thread destructor"""

        self.wait()

    def run(self) -> None:
        """Automaticly web scrapes for updated chapters every 10 minutes"""

        while True:
            self.model.webScrape()
            self.sleep(60 * 10)
