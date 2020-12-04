# Filename: novel_alerts_model.py

"""Model that runs operations on data that is fed in through the controller."""

# Import csv for reading, appending, and writing csv files
import csv
# Import smtplib and ssl for sending emails
import smtplib
import ssl
# Import callable to type annotate functions
from typing import Callable, Union
# Import requests and BeautifulSoup libraries to web scrape URL's
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup


class NovelAlertsModel:
    """
    A class that represents the model for the Model-View-Controller(MVC) design pattern.

    :param FIELD_NAMES: List of dict string key headings
    :type FIELD_NAMES: List[str]
    :param URL_FILE_PATH: File path of URL data
    :type URL_FILE_PATH: str
    :param EMAIL_FILE_PATH: File path of email data
    :type EMAIL_FILE_PATH: str
    :param _user_email: Users email
    :type _user_email: str
    :param _url_data: List of dictionaries in the format: {"URL": "url_Link, "latestChapter": "chapter"}
    :type _url_data: list[dict[str, str]]
    :param _password: users email password
    :type _password: str
    :param _message_box: GUI error msg method that brings up a message box
    :type _message_box: NovelAlertsView method
    """

    FIELD_NAMES = ["URL", "latestChapter"]
    URL_FILE_PATH = "data/urlLog.csv"
    EMAIL_FILE_PATH = "data/email.txt"

    def __init__(self, message_box: Callable) -> None:
        """Model Initializer"""

        self._user_email = self._load_email()
        self._url_data = self._load_URL_data()
        self._password = ""
        self._message_box = message_box 
        
        # Initializes the csv file with column headers if there was no previous data.
        if not self._url_data:
            self._write_URL_data()

    def _get_Latest_Chapter(self, URL: str) -> Union[str, None]:
        """Web scrapes the latest chapter from the URL link and must be from domain novelupdates.com"""
        
        if "novelupdates" not in URL or "series" not in URL:
            self._message_box("ERROR: URL is not from novelupdates or it is not a correct novelupdates URL")
            return

        try:
            # Title: How to Web Scrape using Beautiful Soup in Python without running into HTTP error 403
            # Author: Raiyan Quaium
            # Availability: https://medium.com/@raiyanquaium/how-to-web-scrape-using-beautiful-soup-in-python-without-running-into-http-error-403-554875e5abed

            # Requests the URL data with disguised headers 
            req = Request(URL, headers={"User-Agent": "Mozilla/5.0"})
            # Opens the url and reads the html as a string
            webpage = urlopen(req).read()
            # Creates Bs4 object with arguments consisting of html to be parsed and which parser to use.
            page_soup = soup(webpage, "html.parser")
            # Uses the soup object to find all 'a' tags with the class 'chp-release'
            # Uses the bracket to access the first result which is the latest chp
            # .text is used to grab the text within the tag and nothing else.
            # Ex. <a class="chp-release" href="someLink.com"> text </a>
            latest_chapter = page_soup.findAll("a", "chp-release")[0].text
            return latest_chapter
        except Exception:
            self._message_box("ERROR: Could not find latest chapter")

    def _send_email(self, updated_URLS: list[str]) -> None:
        """Sends a email to user with a list of URL's that have new updates"""

        # Title: Sending Emails with Python
        # Author: Joska de Langen
        # Availability: https://realpython.com/python-send-email/

        # For SSL
        port = 465 
        message = """
        New updates: 
        """

        for url in updated_URLS:
            message += f"\t{url}\n"

        # default context validates host name, certificates, and optimizes security of connection
        context = ssl.create_default_context()

        try:
            # Initiates a TLS-encrypted connection
            with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
                try:
                    server.login(self._user_email, self._password)
                    server.sendmail(self._user_email, self._user_email, message)
                except Exception:
                    self._message_box("ERROR: Email or password is incorrect!")
        except Exception:
            self._message_box("ERROR: Server connection could not be established!")

    def webScrape(self) -> None:
        """Web scrapes the URL data while making a new list of URL's that have updates and sending it to the users email"""

        if self._url_data:
            try:
                updated_URLS = []
                for dict_ in self._url_data:
                    # Gets the latestchapter and compare it to the current one in object
                    # If it is less than the latest chapter then append URL to list of updated URL's and set new chapter into object
                    latest_chapter = self._get_Latest_Chapter(dict_[self.FIELD_NAMES[0]])
                    if dict_[self.FIELD_NAMES[1]] < latest_chapter:
                        updated_URLS.append(dict_[self.FIELD_NAMES[0]])
                        dict_[self.FIELD_NAMES[1]] = latest_chapter
        
                # After all URL's have been processed, write the new URL data into the csv file.
                self._write_URL_data()

                if updated_URLS:
                    self._send_email(updated_URLS)
            except Exception:
                self._message_box("Error: Webscraper did not work")                  

    def setEmail(self, email: str) -> None:
        """Set the new email and saves it to email file"""

        self._user_email = email

        with open(self.EMAIL_FILE_PATH, "w") as email_file:
            email_file.write(self._user_email)

    def _load_email(self) -> str:
        """Loads the email from email file into class property"""

        with open(self.EMAIL_FILE_PATH, "r") as email_file:
            return email_file.read()

    def getEmail(self) -> str:
        """Returns email of the user"""
        return self._user_email
    
    def setPassword(self, password: str) -> None:
        """Set the password"""

        self.password = password

    def _load_URL_data(self) -> list[dict[str, str]]:
        """Opens csv file to be read into a list of dictionarys"""

        with open(self.URL_FILE_PATH, mode='r') as csv_file:
            reader = csv.DictReader(csv_file)
            return list(map(dict, reader))

    def addURLData(self, URL: str) -> None:
        """Add the new URL to the dictionary and csv file"""

        # Gets the latest chapter and if return type is None, then function call did not get latest chapter
        latest_chapter = self._get_Latest_Chapter(URL)
        if latest_chapter == None:
            return
        
        dict_row = {self.FIELD_NAMES[0]: URL, self.FIELD_NAMES[1]: latest_chapter}
        self._url_data.append(dict_row)

        with open(self.URL_FILE_PATH, mode='a') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.FIELD_NAMES)
            writer.writerow(dict_row)

    def _write_URL_data(self) -> None:
        """Writes current object _url_data into the csv file"""

        with open(self.URL_FILE_PATH, mode='w') as csv_file:
            # DictWriter object that allows for file output with dictionary keys as fieldnames/columns/headers
            writer = csv.DictWriter(csv_file, fieldnames=self.FIELD_NAMES)

            writer.writeheader()
            for dict_ in self._url_data:
                writer.writerow(dict_)

    def deleteURLData(self, URL: str) -> None:
        """Delete the URL from the class object and rewrite data into the csv file """

        for dict_ in self._url_data:
            if dict_[self.FIELD_NAMES[0]] == URL:
                self._url_data.remove(dict_)
                self._message_box("Success")
                self._write_URL_data()
                return
        
        # Calls msgBox because URL data has been iterated through and match was not found
        self._message_box("Error: URL is not within existing data or not correct!")
