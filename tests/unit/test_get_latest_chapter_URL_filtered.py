import unittest

from src.models.novel_alerts_model import NovelAlertsModel

class TestGetLatestChapterURLFiltered(unittest.TestCase):
    def setUp(self):
        self.model = NovelAlertsModel(print, "tests/unit/fixtures/testing_URL_log.csv", "tests/unit/fixtures/testing_email.txt")
        self.model.setEmail("")
        self.model._set_URL_data([])

    def test_WLN_URL_without_series_id(self):
        URL = "https://www.wlnupdates.com/"
        self.assertEqual(None, self.model._get_Latest_Chapter_URL_Filtered(URL))

    def test_novelupdates_URL_without_series(self):
        URL = "https://www.novelupdates.com/"
        self.assertEqual(None, self.model._get_Latest_Chapter_URL_Filtered(URL))

    def test_correct_WLN_URL(self):
        URL = "https://www.wlnupdates.com/series-id/91919/treeincarnation"
        self.assertEqual("ch. 3.0", self.model._get_Latest_Chapter_URL_Filtered(URL))

    def test_correct_novelupdates_URL(self):
        URL = "https://www.novelupdates.com/series/smiling-proud-wanderer/"
        self.assertEqual("c1-40", self.model._get_Latest_Chapter_URL_Filtered(URL))

    def test_different_integer_input(self):
        for i in range(5):
            with self.assertRaises(TypeError):
                self.assertEqual(None, self.model._get_Latest_Chapter_URL_Filtered(i))

    def test_wrong_string_input(self):
        test_input = "awdanodanwdiondwaindo"
        self.assertEqual(None, self.model._get_Latest_Chapter_URL_Filtered(test_input))

if __name__ == '__main__':
    unittest.main()