#!/bin/env python

from tornado.httpclient import AsyncHTTPClient, HTTPRequest
import tornado.web
import tornado.gen
import json

import config
import logger

class MandrillEmailHandler(object):
	"""
	Handler class for Mandrill external email service provider.

	Source: https://www.mandrill.com/
    """

	def __init__(self, main_logger = None):
		"""Initalizes the logger for the object.
		Creates an async http client to communicate with the service.
		Initalizes the api key from the config.

	    Args:
	    	main_logger: logger to which the logs should be sent, optional
	    """
		self.log = main_logger or logger.init_logger("mandrill")

		self.http_client = AsyncHTTPClient()
		self.key         = config.MANDRILL_KEY

	@tornado.gen.engine
	def send_email(self, to_addr, cc_addr, bcc_addr, topic, text, callback):
		"""Sends an email using Mandrill service.

		No need for a web hook handling here.
		Async parameter of mandrill api call defaults to false,
		so when the call returns it always does with a sent / rejected status.

	    Args:
	    	to_addr: Email address of the main recipient.
	        cc_addr: A list of email addresses of all cc'd recipients.
	        bcc_addr: A list of email addresses of all bcc'd recipients.
	        topic: Email subject.
	        text: Email body.
	    Returns:
	    	(SendStatus, ExternalId)
	    	SendStatus: SENT/FAILED
	    	ExternalId: External id that the service assigned to the email. None if FAIELD.
	    """

		mail_data = {
			"key": self.key,
			"message": self._prepare_message(to_addr, cc_addr, bcc_addr, topic, text)
		}
		body = tornado.escape.json_encode(mail_data)

		request = HTTPRequest(
			url=config.MANDRILL_URL + "/messages/send.json",
			connect_timeout=config.TIMEOUT, request_timeout=config.TIMEOUT,
			body=body, method='POST', validate_cert = False)

		response = yield tornado.gen.Task(
			self.http_client.fetch, request)

		if int(response.code) == config.RESPONSE_OK:
			body = json.loads(response.body)
			# Each sent email gets assigned a different id. First (To address) used.
			email_id = body[0]['_id']
			callback(config.SEND_STATUS.SENT, email_id)
			return
		else:
			callback(config.SEND_STATUS.FAILED, None)
			return


	def _prepare_message(self, to_addr, cc_addr, bcc_addr, topic, text):
		return {
			# "html": "html email from tornado sample app <b>bold</b>",
			"text": text,
			"subject": topic,
			"from_email": config.FROM_ADDRESS,
			"from_name": config.FROM_NAME,
			"to": self._prepare_destination(to_addr, cc_addr, bcc_addr)
		}

	def _prepare_destination(self, to_addr, cc_addr, bcc_addr):
		recipients_list = [
			{"email": to_addr, "type": "to"},
		]
		if cc_addr:
			recipients_list += [
				{"email": e, "type": 'cc'} for e in cc_addr
			]
		if bcc_addr:
			recipients_list += [
				{"email": e, "type": 'bcc'} for e in bcc_addr
			]
		return recipients_list
