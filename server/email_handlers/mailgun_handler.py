from tornado.httpclient import AsyncHTTPClient
import tornado.web
import tornado.gen

import requests
from trequests import setup_session
from tornalet import tornalet

import config

class MailgunEmailHandler(object):

	def __init__(self, logger):
		self.log = logger
		if not self.log:
			self.log = logger.init_logger("mandrill")

		self.http_client = AsyncHTTPClient()

	@tornado.gen.engine
	def send_email(self, callback):
		"""This is handled slightly differently because of mailgun responds internally."""
		request_url = config.MAILGUN_URL + '/messages'
		response = requests.post(
			request_url, auth=('api', config.MAILGUN_KEY),
			data= {
			    'from': "lukasz.harezlak@gmail.com",
			    'to': 'lukasz.harezlak@gmail.com',
			    'subject': 'Hello',
			    'text': 'Hello from Mailgun'
			}
		)

		# # self.log.info('Status: {0}'.format(response.status_code))
		# # self.log.info('Body:   {0}'.format(response.text))
		# mail_data = {
		# 	'from': "lukasz.harezlak@gmail.com",
		#     'to': 'lukasz.harezlak@gmail.com',
		#     'subject': 'Hello',
		#     'text': 'Hello from Mailgun'
		# 	# "auth": {
		# 	# 	"api": config.MAILGUN_KEY
		# 	# },
		# 	# "data": {
		# 		# # "html": "html email from tornado sample app <b>bold</b>",
		# 		# "text": "plain text email from tornado sample app",
		# 		# "subject": "from tornado sample app",
		# 		# "from": "lukasz.harezlak@gmail.com",
		# 		# # "from_name": "Hello Team",
		# 		# "to": "lukasz.harezlak@gmail.com",
		# 		# "user": "api:%s" % config.MAILGUN_KEY
		# 	# }
		# }
		# body = tornado.escape.json_encode(mail_data)

		# self.log.info(body)

		# response = yield tornado.gen.Task(
		# 	self.http_client.fetch, config.MAILGUN_URL + "/messages",
		# 	method='POST', body=body, auth_username='api', auth_password=config.MAILGUN_KEY
		# )

		request_url = config.MAILGUN_URL + '/events'
		response = requests.get(request_url, auth=('api', config.MAILGUN_KEY), params={'limit': 5})

		self.log.info(response.text)
		self.log.info(response.status_code)

		callback(response)
		# self.finish(response)