import unittest

from src.models.novel_alerts_model import NovelAlertsModel

class TestDeleteURLData(unittest.TestCase):
    def setUp(self):
        self.model = NovelAlertsModel(print, "tests/unit/fixtures/testing_URL_log.csv", "tests/unit/fixtures/testing_email.txt")
        self.model.setEmail("")

        # No need to check if in object/file because _set_URL_data saves to both
        self.model._set_URL_data([{"URL": "https://www.wlnupdates.com/series-id/42758/emperors-domination", "latestChapter": "ch. 3463.0"}, 
                                    {"URL": "https://www.novelupdates.com/series/genius-detective/", "latestChapter": "c572"}])
          
    def test_delete_WLN_URL(self):
        URL = "https://www.wlnupdates.com/series-id/42758/emperors-domination"
        dict_row = {"URL": URL, "latestChapter": self.model._get_Latest_Chapter_URL_Filtered(URL)}

        # Delete from object/file
        self.model.deleteURLData(URL)

        # Check not in object
        self.assertNotIn(dict_row, self.model._get_URL_data())
        # Check not in file
        self.model._load_URL_Data()
        self.assertNotIn(dict_row, self.model._get_URL_data())

    def test_delete_novelupdates_URL(self):
        URL = "https://www.novelupdates.com/series/genius-detective/"
        dict_row = {"URL": URL, "latestChapter": self.model._get_Latest_Chapter_URL_Filtered(URL)}

        # Delete from object/file
        self.model.deleteURLData(URL)

        # Check not in object
        self.assertNotIn(dict_row, self.model._get_URL_data())
        # Check not in file
        self.model._load_URL_Data()
        self.assertNotIn(dict_row, self.model._get_URL_data())
    

if __name__ == '__main__':
    unittest.main()