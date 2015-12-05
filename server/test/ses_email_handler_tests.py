import unittest
import sys
from tornado_botocore import Botocore

sys.path.append('..')
from email_handlers.ses_handler import SesEmailHandler
import config

class SendSesEmailCorrectTestCase(unittest.TestCase):

	def __init__(self, *args, **kwargs):
		super(SendSesEmailCorrectTestCase, self).__init__(*args, **kwargs)

		self.ses_handler     = SesEmailHandler()
		self.expected_result = config.SEND_STATUS.QUEUED

	def assert_send_result(self, result, external_message_id):
		self.assertEqual(result, self.expected_result)
		self.assertIsNotNone(external_message_id)

	def test_send_correct_email(self):
		self.ses_handler.send_email(
    		'lukasz.harezlak@gmail.com', None, None, 'test', 'text', self.assert_send_result
    	)


class SendSesEmailInorrectTestCase(unittest.TestCase):

	def __init__(self, *args, **kwargs):
		super(SendSesEmailInorrectTestCase, self).__init__(*args, **kwargs)

		self.ses_handler     = SesEmailHandler()
		# replace the default client with badly initialized one
		self.ses_handler.ses_client = Botocore(
			service='ses', operation='SendEmail', region_name='us-east-1'
		)
		self.expected_result = config.SEND_STATUS.FAILED

	def assert_send_result(self, result, external_message_id):
		self.assertEqual(result, self.expected_result)
		self.assertIsNone(external_message_id)

	def test_send_incorrect_email(self):
		self.ses_handler.send_email(
    		'lukasz.harezlak@gmail.com', None, None, 'test', 'text', self.assert_send_result
    	)