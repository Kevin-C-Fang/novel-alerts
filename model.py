#!/usr/bin/env python

# Filename: model.py

"""Model that runs operations on data that is fed in through the controller."""

# Import csv for reading, appending, and writing csv files
import csv
# Import smtplib and ssl for sending emails
import smtplib
import ssl
# Import time for sleep function to webscrape every X minutes
import time
# Import requests and BeautifulSoup libraries to web scrape URL's
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup


class NovelAlertsModel:
    """
    A class that represents the model for the Model-View-Controller(MVC) design pattern.

    :param fieldnames: List of dict string key headings
    :type fieldnames: List[]
    :param file_: Location of URL data
    :type file_: String
    :param email: Location of email data
    :type email: String
    :param usrEmail: Users email
    :type usrEmail: String
    :param list_of_dict: List of dictionaries in the format: {"URL": "url_Link, "latestChapter": "chapter"}
    :type list_of_dict: list[dict]
    :param password: users email password
    :type password: String
    :param errorFunc: GUI error msg method that brings up a message box
    :type errorFunc: NovelAlertsApp method
    """

    fieldnames = ["URL", "latestChapter"]
    file_ = "data/urlLog.csv"
    email = "data/email.txt"

    def __init__(self, msgBox):
        """Model initializer/constructor
        
        :param msgBox: GUI msgBox method that brings up a message box
        :type msgBox: NovelAlertsApp method       
        """

        self.usrEmail = self._loadEmail()
        self.list_of_dict = self._loadURLData()
        self.password = ""
        self.msgBox = msgBox
        # Initializes the csv file with column headers regardless of there being previous data
        self._writeURLData(self.list_of_dict)
        #self._webScrape()

    def _getLatestChapter(self, URL):
        """Web scrapes the latest chapter from the URL link and must be from domain novelupdates.com
        
        :param URL: URL link
        :type URL: String
        :returns: Text of the latest chapter
        :rtype: String
        """

        try:
            # Title: How to Web Scrape using Beautiful Soup in Python without running into HTTP error 403
            # Author: Raiyan Quaium
            # Availability: https://medium.com/@raiyanquaium/how-to-web-scrape-using-beautiful-soup-in-python-without-running-into-http-error-403-554875e5abed

            # Requests the URL data with disguised headers 
            req = Request(URL, headers={"User-Agent": "Mozilla/5.0"})
            # Opens the url and reads the html as a string
            webpage = urlopen(req).read()
            # Creates a BeautifulSoup object
            # Arguments consist of html to be parsed and which parser to use.
            page_soup = soup(webpage, "html.parser")
            # Uses the soup object to find all 'a' tags with the class 'chp-release'
            # Uses the bracket to access the first result which is the latest chp
            # .text is used to grab the text within the tag and nothing else.
            # Ex. <a class="chp-release" href="someLink.com"> text </a>
            latestChapter = page_soup.findAll("a", "chp-release")[0].text
            return latestChapter
        except Exception:
            # Sends error msg through GUI when URL cannot be accessed or URL is not valid
            self.msgBox("ERROR: URL is not valid!")

    def _sendEmail(self, urlList):
        """Sends a email to user with a list of URL's that have new updates
        
        :param urlList: List of URL's that have new updates
        :type urlList: list
        """

        # Title: Sending Emails with Python
        # Author: Joska de Langen
        # Availability: https://realpython.com/python-send-email/

        # For SSL
        port = 465 
        message = """
        New updates: 
        """

        # Iterates through list of urls and adds them to the message with newline/tab formatting
        for url in urlList:
            message += f"\t{url}\n"
        # default context validates host name, certificates, and optimizes security of connection
        context = ssl.create_default_context()

        # Try to set up server connection and login.
        # It it fails then call msgBox for GUI to show messagebox
        try:
            # Initiates a TLS-encrypted connection
            with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
                try:
                    server.login(self.usrEmail, self.password)
                    server.sendmail(self.usrEmail, self.usrEmail, message)
                except Exception:
                    self.msgBox("ERROR: Email or password is incorrect!")
        except Exception:
            self.msgBox("ERROR: Server connection could not be established!")

    def _webScrape(self):
        """Web scrapes the URL data while making a new list of URL's that have updates and sending it to the users email"""

        while True:
            while len(self.list_of_dict) != 0:
                try:
                    newUpdateList = []
                    # Iterates through list of dictionaries
                    for dict_ in self.list_of_dict:
                        # Gets the latestchapter and compares it to the current one in object/file
                        # If it is less than the latest chapter then append to list of updated URL's and enter new chp into object
                        latestChapter = self._getLatestChapter(dict_[self.fieldnames[0]])
                        if dict_[self.fieldnames[1]] < latestChapter:
                            newUpdateList.append(dict_[self.fieldnames[0]])
                            dict_[self.fieldnames[1]] = latestChapter

                    # After all URL's have been processed then write the new URL data into the csv file.
                    self._writeURLData(self.list_of_dict)
                    # Sends updated URL list to _sendEmail
                    self._sendEmail(newUpdateList)
                except Exception:
                    print("Error: Webscraper did not work")                  
            #Pauses the function for X minutes, so that it can restart later
            time.sleep(30)
            #time.sleep(60 * 10)

    def setEmail(self, email):
        """Set the new email
        
        :param email: Email of the user
        :type email: String
        """

        # Assigns the parameter email to object variable
        self.usrEmail = email
        # Opens the email file to write in the new email
        with open(self.email, "w") as email_File:
            email_File.write(self.usrEmail)

    def _loadEmail(self):
        """Loads the email from email.txt into object variable
        
        :return email: Email of the user or empty string if there was no previous email
        :rtype email: String
        """

        # Opens the email file to read in the email
        with open(self.email, "r") as email_File:
            email = email_File.read()
        # Checks if there was a previous email and if so, return that, otherwise return empty string
        if email != "":
            return email
        else:
            return ""
    
    def setPassword(self, password):
        """Set the password
        
        :param password: Password of the user
        :type password: String
        """

        self.password = password

    def _loadURLData(self):
        """Opens a csv file to be read into a list of dictionarys and checks if empty
        
        :return list_of_dict: List of dictionaries read in from csv file into object
        :rtype list_of_dict: list[dict]
        """

        with open(self.file_, mode='r') as csv_file:
            reader = csv.DictReader(csv_file)
            list_of_dict = list(map(dict, reader))

        if len(list_of_dict) == 0:
            return []
        else:
            return list_of_dict

    def _addURLData(self, URL):
        """Adds the new URL to the dictionary and csv file while
        
        :param URL: URL to be deleted from object and file
        :type URL: String
        """

        # Gets the latest chapter and if return type is None, then function call did not get latest chapter
        latestChapter = self._getLatestChapter(URL)
        if latestChapter == None:
            return
        
        # Function call did get latest chapter, so create dictionary with that data and URL
        # Append it to both the object variable and the csv file
        dictRow = {self.fieldnames[0]: URL, self.fieldnames[1]: latestChapter}
        self.list_of_dict.append(dictRow)
        with open(self.file_, mode='a') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.fieldnames)
            writer.writerow(dictRow)

    def _writeURLData(self, listOfDict):
        """Writes the data inside of listOfDict into the csv file
        
        :param listOfDict: List of dictionaries to be written into csv file
        :type listOfDict: list[dict]
        """

        # Opens the csv file to write the list of the dictionary data to the csv file.
        with open(self.file_, mode='w') as csv_file:
            # DictWriter object that allows for file output with dictionary keys as fieldnames/columns
            writer = csv.DictWriter(csv_file, fieldnames=self.fieldnames)

            # Write column/key headings into csv
            writer.writeheader()
            # For each dictionary in list, write the dictionary data
            for dict_ in listOfDict:
                writer.writerow(dict_)

    def deleteURLData(self, URL):
        """Delete the URL from the object and rewrite that data into the csv file
        
        :param URL: URL to be deleted from object and file
        :type URL: String
        """

        # Iterates through list of dictionaries and if URL value is equal to the parameter then remove that dictionary
        # After removal from object then write that data into csv file.
        for dict_ in self.list_of_dict:
            if dict_[self.fieldnames[0]] == URL:
                self.list_of_dict.remove(dict_)
                self.msgBox("Success")
                self._writeURLData(self.list_of_dict)
                return
        # Calls msgBox because URL data has been iterated through and match was not found
        # So URL parameter is either not within object or not correct
        self.msgBox("Error: URL is not within existing data or not correct!")