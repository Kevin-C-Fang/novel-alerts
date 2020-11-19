#!/usr/bin/env python

# Filename: model.py

"""
    Model for the Novel Alerts Application. This application will take in the data from the controller class and run operations with that data.
"""

class NovelAlertsModel:
    """Main function"""
    def __init__(self):
        """Main function"""
        self.urlSet = set()
        self.usrEmail = ""

    def webScrape(self):
        """"""
        pass

    def sendEmail(self):
        """"""
        pass

    def _setEmail(self, email):
        """Set the new email"""
        self.usrEmail = email
        
    def _addURL(self, URL):
        """Add the new URL to the set"""
        self.urlSet.add(URL)

    def _deleteURL(self, URL):
        """Delete the URL from the set"""
        self.urlSet.remove(URL)