import unittest
import requests
import sys

sys.path.append('..')
import config

class UrlTestCase(unittest.TestCase):

    def test_incorrect_url(self):
        response = requests.get('http://%s:%s/WRONG_URL' % (config.HOST, config.PORT))

        self.assertEqual({"status": 404, "msg": "Incorrect request url."}, response.json())
        self.assertEqual(200, response.status_code)