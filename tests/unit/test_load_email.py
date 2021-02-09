import unittest

from src.models.novel_alerts_model import NovelAlertsModel

class TestLoadEmail(unittest.TestCase):
    def setUp(self):
        self.model = NovelAlertsModel(print, "tests/unit/fixtures/testing_URL_log.csv", "tests/unit/fixtures/testing_email.txt")
        self.model.setEmail("")
        self.model._set_URL_data([])
        
    def test_load_email(self):
        # set the string to obj/file
        self.model.setEmail("testingemail123@yahoo.com")
        # Reload email info and check that it's the same
        self.model._load_email()
        self.assertEqual("testingemail123@yahoo.com", self.model.getEmail())

    def test_load_wrong_input_string(self):
        # set the string to obj/file
        self.model.setEmail("wadafgagwafgafwafa")
        # Reload email info and check that it's the same
        self.model._load_email()
        self.assertEqual("wadafgagwafgafwafa", self.model.getEmail())

if __name__ == '__main__':
    unittest.main()