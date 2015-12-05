import tornado
from tornado import testing
from tornado.httpclient import AsyncHTTPClient

import sys
sys.path.append('..')

from email_handlers.mandrill_handler import MandrillEmailHandler
import config

class SendMandrillEmailCorrectTestCase(testing.AsyncTestCase):

	def __init__(self, *args, **kwargs):
		super(SendMandrillEmailCorrectTestCase, self).__init__(*args, **kwargs)

		self.mandrill_handler = MandrillEmailHandler()
		self.expected_result  = config.SEND_STATUS.SENT

	def setUp(self):
		super(SendMandrillEmailCorrectTestCase, self).setUp()
		# force mandrill client use the same io_loop as the test case,
		# otherwise nothing will be yielded in the test method
		self.mandrill_handler.http_client = AsyncHTTPClient(io_loop = self.io_loop)

	@testing.gen_test
	def test_send_correct_email(self):
		cb_result = yield tornado.gen.Task(
			self.mandrill_handler.send_email,
			config.FROM_ADDRESS, None, None, 'test2', 'text2'
		)
		result, external_id = cb_result[0][0], cb_result[0][1]
		self.assertEqual(result, self.expected_result)
		self.assertIsNotNone(external_id)


class SendMandrillEmailInorrectTestCase(testing.AsyncTestCase):

	def __init__(self, *args, **kwargs):
		super(SendMandrillEmailInorrectTestCase, self).__init__(*args, **kwargs)

		self.mandrill_handler = MandrillEmailHandler()
		self.expected_result  = config.SEND_STATUS.FAILED

	def setUp(self):
		super(SendMandrillEmailInorrectTestCase, self).setUp()
		# force mandrill client use the same io_loop as the test case,
		# otherwise nothing will be yielded in the test method
		self.mandrill_handler.http_client = AsyncHTTPClient(io_loop = self.io_loop)
		# replace the key to make sure the call fails
		self.mandrill_handler.key         = "WRONG_KEY"

	@testing.gen_test
	def test_send_correct_email(self):
		cb_result = yield tornado.gen.Task(
			self.mandrill_handler.send_email,
			config.FROM_ADDRESS, None, None, 'test2', 'text2'
		)
		result, external_id = cb_result[0][0], cb_result[0][1]
		self.assertEqual(result, self.expected_result)
		self.assertIsNone(external_id)