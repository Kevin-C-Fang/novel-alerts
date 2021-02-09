import unittest

from src.models.novel_alerts_model import NovelAlertsModel

class TestIntegrateUpdatedURLS(unittest.TestCase):
    def setUp(self):
        self.model = NovelAlertsModel(print, "tests/unit/fixtures/testing_URL_log.csv", "tests/unit/fixtures/testing_email.txt")
        self.model.setEmail("")
        self.model._set_URL_data([])        

    def test_input_of_updated_URLS(self):
        updated_URLS = ["https://www.wlnupdates.com/series-id/2697/chaotic-sword-god", "https://www.novelupdates.com/series/yu-ren/"]

        advanced_result = """"""
        for url in updated_URLS:
            advanced_result += f"""{url}\n"""

        self.assertEqual(advanced_result, self.model._integrate_Updated_URLS(updated_URLS))

    def test_empty_list_input(self):
        empty = []

        basic_result = """"""

        self.assertEqual(basic_result, self.model._integrate_Updated_URLS(empty))

if __name__ == '__main__':
    unittest.main()