import unittest
import requests
import sys

sys.path.append('..')
import config

class UrlTestCase(unittest.TestCase):

    def test_incorrect_get(self):
        response = requests.get('http://%s:%s/WRONG_URL' % (config.HOST, config.PORT))

        self.assertEqual({"status": 404, "msg": "Incorrect request url."}, response.json())
        self.assertEqual(200, response.status_code)

    def test_correct_main_page_get(self):
        response = requests.get('http://%s:%s/' % (config.HOST, config.PORT))

        # see if page content send over
        self.assertIn("<!DOCTYPE html>", response.text)
        self.assertEqual(200, response.status_code)

    def test_correct_emails_get(self):
        response = requests.get('http://%s:%s/emails' % (config.HOST, config.PORT))

        self.assertIn("emails", response.text)
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json()['status'])

    def test_send_correct_email_post(self):
        email_data = {'to': 'lukasz.harezlak@gmail.com', 'subject': 'test', 'text': 'test'}
        response = requests.post(
            'http://%s:%s/emails' % (config.HOST, config.PORT), data=email_data)

        self.assertIn("send_status", response.text)
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json()['status'])
        self.assertIn(response.json()["send_status"], [s.name for s in config.SEND_STATUS])

    def test_incorrect_to_address_email_post(self):
        email_data = {'to': 'xxxx@@@@not', 'subject': 'test', 'text': 'test'}
        response = requests.post(
            'http://%s:%s/emails' % (config.HOST, config.PORT), data=email_data)

        self.assertEqual(200, response.status_code)
        self.assertEqual(500, response.json()['status'])
        self.assertIn("msg", response.text)
        self.assertIn("Invalid main recipient.", response.text)

    def test_empty_subject_email_post(self):
        email_data = {'to': config.FROM_ADDRESS, 'subject': '', 'text': 'test'}
        response = requests.post(
            'http://%s:%s/emails' % (config.HOST, config.PORT), data=email_data)

        self.assertEqual(200, response.status_code)
        self.assertEqual(500, response.json()['status'])
        self.assertIn("msg", response.text)
        self.assertIn("Topic cannot be empty.", response.text)

    def test_empty_body_email_post(self):
        email_data = {'to': config.FROM_ADDRESS, 'subject': 'subject', 'text': ''}
        response = requests.post(
            'http://%s:%s/emails' % (config.HOST, config.PORT), data=email_data)

        self.assertEqual(200, response.status_code)
        self.assertEqual(500, response.json()['status'])
        self.assertIn("msg", response.text)
        self.assertIn("Text cannot be empty.", response.text)