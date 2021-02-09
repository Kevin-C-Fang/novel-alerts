import unittest

from src.models.novel_alerts_model import NovelAlertsModel

class TestAddURLData(unittest.TestCase):
    def setUp(self):
        self.model = NovelAlertsModel(print, "tests/unit/fixtures/testing_URL_log.csv", "tests/unit/fixtures/testing_email.txt")
        self.model.setEmail("")

        # No need to check if in file or object since _set_URL_data saves new data to both
        self.model._set_URL_data([])

    def test_add_correct_WLN_URL(self):
        URL = "https://www.wlnupdates.com/series-id/91919/treeincarnation"
        dict_row = {"URL": URL, "latestChapter": self.model._get_Latest_Chapter_URL_Filtered(URL)}

        # Adds data to object and file
        self.model.addURLData(URL)

        # Check if in object
        self.assertIn(dict_row, self.model._get_URL_data())
        # Check if in file
        self.model._load_URL_Data()
        self.assertIn(dict_row, self.model._get_URL_data())

    def test_add_correct_novelupdates_URL(self):
        URL = "https://www.novelupdates.com/series/smiling-proud-wanderer/"
        dict_row = {"URL": URL, "latestChapter": self.model._get_Latest_Chapter_URL_Filtered(URL)}

        # Adds data to object and file
        self.model.addURLData(URL)

        # Check if in object
        self.assertIn(dict_row, self.model._get_URL_data())
        # Check if in file
        self.model._load_URL_Data()
        self.assertIn(dict_row, self.model._get_URL_data())

    def test_add_integer_input(self):
        for i in range(5):
            with self.assertRaises(TypeError):
                self.model.addURLData(i)
                self.assertNotIn(i, self.model._get_URL_data())

    def test_add_wrong_string_input(self):
        test_input = "awdanodanwdiondwaindo"
        self.model.addURLData(test_input)
        self.assertNotIn(test_input, self.model._get_URL_data())
    

if __name__ == '__main__':
    unittest.main()