import unittest

from src.models.novel_alerts_model import NovelAlertsModel

class TestSetPassword(unittest.TestCase):
    def setUp(self):
        self.model = NovelAlertsModel(print, "tests/unit/fixtures/testing_URL_log.csv", "tests/unit/fixtures/testing_email.txt")
        self.model.setEmail("")
        self.model._set_URL_data([])
        
    def test_set_password(self):
        # Note: no need to check for bad values because it won't break program
        # User can just enter in new password value
        password = "iamhungry12345"
        self.model.setPassword(password)
        self.assertEqual(password, self.model.getPassword())
        
if __name__ == '__main__':
    unittest.main()