import unittest

from src.models.novel_alerts_model import NovelAlertsModel

class TestLoadURLData(unittest.TestCase):
    def setUp(self):
        self.model = NovelAlertsModel(print, "tests/unit/fixtures/testing_URL_log.csv", "tests/unit/fixtures/testing_email.txt")
        self.model.setEmail("")
        self.model._set_URL_data([])
        
    def test_loading_of_URL_data(self):
        URL_data = [{"URL": "https://www.wlnupdates.com/series-id/42758/emperors-domination", "latestChapter": "ch. 3463.0"}, 
                                    {"URL": "https://www.novelupdates.com/series/genius-detective/", "latestChapter": "c572"}]

        # Set new URL data to obj/file and reload to check that value is the same
        self.model._set_URL_data(URL_data)
        self.model._load_URL_Data()
        self.assertEqual(URL_data, self.model._get_URL_data())

if __name__ == '__main__':
    unittest.main()