#!/bin/env python

from tornado.httpclient import AsyncHTTPClient
import tornado.web
import tornado.gen

import config
import logger

class MandrillEmailHandler(object):

	def __init__(self, main_logger = None):
		self.log = main_logger or logger.init_logger("mandrill")

		self.http_client = AsyncHTTPClient()

	@tornado.gen.engine
	def send_email(self, to_addr, cc_addr, bcc_addr, topic, text, callback):
		"""No need for a web hook handling here.
		async=false so when the call returns we will know if it is sent / rejected"""

		mail_data = {
			"key": config.MANDRILL_KEY,
			"message": self._prepare_message(to_addr, cc_addr, bcc_addr, topic, text)
		}
		body = tornado.escape.json_encode(mail_data)

		response = yield tornado.gen.Task(
			self.http_client.fetch, config.MANDRILL_URL + "/messages/send.json",
			method='POST', body=body
		)

		self.log.info(response.body)

		if int(response.code) == config.RESPONSE_OK:
			callback(config.SEND_STATUS.SENT)
			return
		else:
			callback(config.SEND_STATUS.FAILED)
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
