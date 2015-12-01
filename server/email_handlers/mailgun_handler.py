from tornado.httpclient import AsyncHTTPClient
import tornado.web
import tornado.gen

import requests
import json

import config

class MailgunEmailHandler(object):

	def __init__(self, logger):
		self.log = logger
		if not self.log:
			self.log = logger.init_logger("mandrill")

		self.http_client = AsyncHTTPClient()

	@tornado.gen.engine
	def send_email(self, to_addr, cc_addr, bcc_addr, topic, text, callback):
		"""This is handled slightly differently than other mailing libraries
		because of how mailgun responds internally."""

		email_id = self._register_send_email(
			to_addr, cc_addr, bcc_addr, topic, text)
		if not email_id:
			# sending email failed, check logs for details
			callback(config.SEND_STATUS.FAILED)
			return
		callback(config.SEND_STATUS.QUEUED)

	def _register_send_email(self, to_addr, cc_addr, bcc_addr, topic, text):
		try:
			# IMPORTANT: this is a blocking request so set the timeout on 1s.
			request_url = config.MAILGUN_URL + '/messages'
			response = requests.post(
				request_url, auth = ('api', config.MAILGUN_KEY),
				data = {
				    'from': config.FROM_ADDRESS,
				    'to': to_addr,
				    'cc': cc_addr,
				    'bcc': bcc_addr,
				    'subject': topic,
				    'text': text
				},
				timeout = config.BLOCKING_TIMEOUT
			)

			self.log.info(response.content)

			if int(response.status_code) == config.RESPONSE_OK:
				response = json.loads(response.text)
				return response['id'].replace('<', '').replace('>', '')
			return None

		except (requests.ConnectionError, requests.Timeout), e:
			self.log.error(
				"Failed to send email %s using mailgun. Connection Error/Timeout: %s"
				% (text, e)
			)
			return None
		except Exception, e:
			self.log.error(
				"Failed to send email %s using mailgun. Mal-formatted Data/Unknown Exception: %s"
				% (text, e)
			)
			return None

	# def _get_email_send_status(self, email_id):
	# 	# http://nullege.com/codes/search/tornado.gen.with_timeout
		# request_url = config.MAILGUN_URL + '/events'
		# response = requests.get(request_url, auth=('api', config.MAILGUN_KEY), params={'limit': 5})

		# sent_success = self._get_email_send_status(email_id)

		# self.log.info(response.text)
		# self.log.info(response.status_code)