import unittest

from src.models.novel_alerts_model import NovelAlertsModel

class TestCompileUpdatedURLS(unittest.TestCase):
    def setUp(self):
        self.model = NovelAlertsModel(print, "tests/unit/fixtures/testing_URL_log.csv", "tests/unit/fixtures/testing_email.txt")
        self.model.setEmail("")
        self.model._set_URL_data([])
        
        WLN_URL = "https://www.wlnupdates.com/series-id/42758/emperors-domination"
        novelupdates_URL = "https://www.novelupdates.com/series/genius-detective/"

        self._not_up_to_date_URLS = [{"URL": WLN_URL, "latestChapter": "ch. 3000.0"}, 
                                    {"URL": novelupdates_URL, "latestChapter": "c100"}]
        
        
        self._up_to_date_URLS = [{"URL": WLN_URL, "latestChapter": self.model._get_Latest_Chapter_URL_Filtered(WLN_URL)}, 
                                    {"URL": novelupdates_URL, "latestChapter": self.model._get_Latest_Chapter_URL_Filtered(novelupdates_URL)}]
        # No need to check for bad input
        # Not possible within the object/file unless manually set using _set_URL_data
        
    def test_not_up_to_date(self):
        self.model._set_URL_data(self._not_up_to_date_URLS)
        result = ["https://www.wlnupdates.com/series-id/42758/emperors-domination", 
                    "https://www.novelupdates.com/series/genius-detective/"]
        self.assertEqual(result, self.model._compile_updated_URLS())

    def test_up_to_date(self):
        self.model._set_URL_data(self._up_to_date_URLS)
        result = []
        self.assertEqual(result, self.model._compile_updated_URLS())
    
    

if __name__ == '__main__':
    unittest.main()