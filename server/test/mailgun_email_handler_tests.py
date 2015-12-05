import tornado
from tornado import testing
from tornado.httpclient import AsyncHTTPClient

import sys
sys.path.append('..')

from email_handlers.mailgun_handler import MailgunEmailHandler
import config

class SendMailgunEmailCorrectTestCase(testing.AsyncTestCase):

	def __init__(self, *args, **kwargs):
		super(SendMailgunEmailCorrectTestCase, self).__init__(*args, **kwargs)

		self.mailgun_handler = MailgunEmailHandler()
		self.expected_result = config.SEND_STATUS.QUEUED

	def setUp(self):
		super(SendMailgunEmailCorrectTestCase, self).setUp()
		# force mailgun client use the same io_loop as the test case,
		# otherwise nothing will be yielded in the test method
		self.mailgun_handler.http_client = AsyncHTTPClient(io_loop = self.io_loop)

	@testing.gen_test
	def test_send_correct_email(self):
		cb_result = yield tornado.gen.Task(
			self.mailgun_handler.send_email,
			'lukasz.harezlak@gmail.com', None, None, 'test3', 'text3'
		)
		result, external_id = cb_result[0][0], cb_result[0][1]
		self.assertEqual(result, self.expected_result)
		self.assertIsNotNone(external_id)