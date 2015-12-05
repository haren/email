from tornado.httpclient import AsyncHTTPClient
import tornado.web
import tornado.gen

import requests
import json

import config
import logger

class MailgunEmailHandler(object):
	"""
	Handler class for Mailgun external email service provider.

	Source: https://www.mailgun.com/
    """

	def __init__(self, main_logger = None):
		"""Initalizes the logger for the object.
		Creates an async http client to communicate with the service.
		Initalizes the api key from the config.

	    Args:
	    	main_logger: logger to which the logs should be sent, optional
	    """
		self.log = main_logger or logger.init_logger("mailgun")

		self.http_client = AsyncHTTPClient()
		self.key         = config.MAILGUN_KEY

	@tornado.gen.engine
	def send_email(self, to_addr, cc_addr, bcc_addr, topic, text, callback):
		"""Sends an email using mailgun service.

		If call succeedes, returns QUEUED status. A webhook has been setup for
		delivery confirmations (server.DeliveryMailgunHandler).

	    Args:
	    	to_addr: Email address of the main recipient.
	        cc_addr: A list of email addresses of all cc'd recipients.
	        bcc_addr: A list of email addresses of all bcc'd recipients.
	        topic: Email subject.
	        text: Email body.
	    Returns:
	    	(SendStatus, ExternalId)
	    	SendStatus: FAILED/QUEUED
	    	ExternalId: External id that the service assigned to the email. None if FAIELD.
	    """

		email_id = self._register_send_email(
			to_addr, cc_addr, bcc_addr, topic, text)
		if not email_id:
			# sending email failed, check logs for details
			callback(config.SEND_STATUS.FAILED, None)
			return
		callback(config.SEND_STATUS.QUEUED, email_id)

	def _register_send_email(self, to_addr, cc_addr, bcc_addr, topic, text):
		try:
			# IMPORTANT: this is a blocking request so set the timeout on 1s.
			request_url = config.MAILGUN_URL + '/messages'
			message     = self._prepare_message(to_addr, cc_addr, bcc_addr, topic, text)

			response = requests.post(
				request_url,
				auth = ('api', self.key),
				data = message,
				timeout = config.BLOCKING_TIMEOUT
			)

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

	def _prepare_message(self, to_addr, cc_addr, bcc_addr, topic, text):
		return {
		    'from': config.FROM_ADDRESS,
		    'to': to_addr,
		    'cc': cc_addr,
		    'bcc': bcc_addr,
		    'subject': topic,
		    'text': text
		}
