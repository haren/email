#!/bin/env python

from tornado.httpclient import AsyncHTTPClient
import tornado.web
import tornado.gen

import config

class MandrilEmailHandler(object):

	def __init__(self, logger):
		self.log = logger
		if not self.log:
			self.log = logger.init_logger("mandrill")

		self.http_client = AsyncHTTPClient()

	@tornado.gen.engine
	def send_email(self, callback):
		mail_data = {
			"key": config.MANDRILL_KEY,
			"message": {
				"html": "html email from tornado sample app <b>bold</b>",
				"text": "plain text email from tornado sample app",
				"subject": "from tornado sample app",
				"from_email": "hello@example.com",
				"from_name": "Hello Team",
				"to":[{"email": "lukasz.harezlak@gmail.com"}]
			}
		}
		body = tornado.escape.json_encode(mail_data)

		response = yield tornado.gen.Task(
			self.http_client.fetch, config.MANDRILL_URL + "/messages/send.json",
			method='POST', body=body
		)
		self.log.info(response)
		self.log.info(response.body)

		callback(response)