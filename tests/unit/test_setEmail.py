import unittest

from src.models.novel_alerts_model import NovelAlertsModel

class TestSetEmail(unittest.TestCase):
    def setUp(self):
        self.model = NovelAlertsModel(print, "tests/unit/fixtures/testing_URL_log.csv", "tests/unit/fixtures/testing_email.txt")
        self.model.setEmail("")
        self.model._set_URL_data([])
        
    def test_set_correct_email(self):
        # Note: no need to check for bad values because it won't break program
        # User can just enter in new email value
        email = "testingemail123@yahoo.com"
        self.model.setEmail(email)

        self.assertEqual(email, self.model.getEmail())
        self.model._load_email()
        self.assertEqual(email, self.model.getEmail())

if __name__ == '__main__':
    unittest.main()