import unittest
import sys
from tornado import testing
from tornado_botocore import Botocore
from tornado.httpclient import AsyncHTTPClient

sys.path.append('..')
from email_handlers.ses_handler import SesEmailHandler
import config

class SendSesEmailCorrectTestCase(testing.AsyncTestCase):

	def __init__(self, *args, **kwargs):
		super(SendSesEmailCorrectTestCase, self).__init__(*args, **kwargs)

		self.ses_handler     = SesEmailHandler()
		self.expected_result = config.SEND_STATUS.QUEUED

	def setUp(self):
		super(SendSesEmailCorrectTestCase, self).setUp()
		# force ses.botocore client use the same io_loop as the test case,
		# otherwise nothing will be yielded in the test method
		self.ses_handler.ses_client.http_client = AsyncHTTPClient(io_loop = self.io_loop)

	@testing.gen_test(timeout=config.TIMEOUT * 5)
	def test_send_correct_email(self):
		cb_result = yield testing.gen.Task(
			self.ses_handler.send_email, 'lukasz.harezlak@gmail.com', None, None, 'test2', 'text2')
		result, external_id = cb_result[0][0], cb_result[0][1]
		self.assertEqual(result, self.expected_result)
		self.assertIsNotNone(external_id)


class SendSesEmailIncorrectTestCase(testing.AsyncTestCase):

	def __init__(self, *args, **kwargs):
		super(SendSesEmailIncorrectTestCase, self).__init__(*args, **kwargs)

		self.ses_handler     = SesEmailHandler()
		self.expected_result = config.SEND_STATUS.FAILED

	def setUp(self):
		super(SendSesEmailIncorrectTestCase, self).setUp()
		# initialize with the wrong region (no SES subscription)
		self.ses_handler.ses_client = Botocore(
			service='ses', operation='SendEmail', region_name='us-east-1'
		)
		# force ses.botocore client use the same io_loop as the test case,
		# otherwise nothing will be yielded in the test method
		self.ses_handler.ses_client.http_client = AsyncHTTPClient(io_loop = self.io_loop)

	@testing.gen_test(timeout=config.TIMEOUT * 5)
	def test_send_correct_email(self):
		cb_result = yield testing.gen.Task(
			self.ses_handler.send_email, 'lukasz.harezlak@gmail.com', None, None, 'test2', 'text2')
		result, external_id = cb_result[0][0], cb_result[0][1]
		self.assertEqual(result, self.expected_result)
		self.assertIsNone(external_id)