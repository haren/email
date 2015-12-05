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
			'lukasz.harezlak@gmail.com', None, None, 'test2', 'text2'
		)
		result, external_id = cb_result[0][0], cb_result[0][1]
		self.assertEqual(result, self.expected_result)
		self.assertIsNotNone(external_id)


# class SendMandrillEmailInorrectTestCase(unittest.TestCase):

# 	def __init__(self, *args, **kwargs):
# 		super(SendMandrillEmailInorrectTestCase, self).__init__(*args, **kwargs)

# 		self.mandrill_handler     = MandrillEmailHandler()
# 		# replace the default client with badly initialized one
# 		self.mandrill_handler.ses_client = Botocore(
# 			service='ses', operation='SendEmail', region_name='us-east-1'
# 		)
# 		self.expected_result = config.SEND_STATUS.FAILED

# 	def assert_send_result(self, result, external_message_id):
# 		self.assertEqual(result, self.expected_result)
# 		self.assertIsNone(external_message_id)

# 	def test_send_incorrect_email(self):
# 		self.mandrill_handler.send_email(
#     		'lukasz.harezlak@gmail.com', None, None, 'test', 'text', self.assert_send_result
#     	)