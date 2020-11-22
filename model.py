#!/usr/bin/env python

# Filename: model.py

"""
    Model for the Novel Alerts Application. This application will take in the data from the controller class and run operations with that data.
"""

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup

import smtplib, ssl
import time

class NovelAlertsModel:
    """Main function"""
    def __init__(self):
        """Main function"""
        # Dictonary will be in the format: key(URL): value(latestChapter) <- string because of different chapter text
        self.urlDict = {}
        self.usrEmail = ""
        self.password = ""

    def _getLatestChapter(self, URL):
        """Web scrapes the latest chapter on novelupdates.com"""
        req = Request(URL, headers={"User-Agent": "Mozilla/5.0"})
        webpage = urlopen(req).read()
        page_soup = soup(webpage, "html.parser")
        latestChapter = page_soup.findAll("a", "chp-release")[0].text
        return latestChapter

    def _sendEmail(self, urlUpdateDict):
        """Sends a email with url and chapter to notify the user about a new chapter"""
        # For SSL
        port = 465 
        smtp_server = "smtp.gmail.com"
        message = """
        New updates: 
        """

        for url in urlUpdateDict.keys():
            message += f"\t{url}\n"

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(self.usrEmail, self.password)
            server.sendmail(self.usrEmail, self.usrEmail, message)

    def _webScrape(self):
        """Web scrapes the added URL's and sends email to user using a new dictionary of updated URLs"""
        try:
            newUpdateDict = {}
            for url, chp in self.urlDict.items():
                latestChapter = self._getLatestChapter(url)
                if chp < latestChapter:
                    newUpdateDict[url] = chp
                    self.urlDict[url] = latestChapter
            self._sendEmail(newUpdateDict)
                
            time.sleep(5)
            #time.sleep(60 * 10)
        except Exception:
            print("Error: Email or Password is not correct. Enter email or password again!")

    def _setEmail(self, email):
        """Set the new email"""
        self.usrEmail = email
    
    def _setPassword(self, password):
        """Set the password"""
        self.password = password

    def _addURL(self, URL):
        """Adds the new URL to the dictionary while webscraping the latest chapter"""
        try:
            latestChapter = self._getLatestChapter(URL)
            self.urlDict[URL] = latestChapter
        except Exception:
            return "Error: URL is not valid!"

    def _deleteURL(self, URL, errorFunc):
        """Delete the URL from the dictionary"""
        try:
            self.urlDict.pop(URL)
        except Exception:
            errorFunc("ERROR: URL not found within existing data!")
