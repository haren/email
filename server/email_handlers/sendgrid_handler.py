#!/bin/env python

from tornado.httpclient import AsyncHTTPClient
import tornado.web
import tornado.gen

import config

class SendgridEmailHandler(object):

	def __init__(self, logger):
		self.log = logger
		if not self.log:
			self.log = logger.init_logger("sendgrind")

		self.http_client = AsyncHTTPClient()

	@tornado.gen.engine
	def send_email(self, callback):
		mail_data = {
			"api_user": config.SENDGRID_USERNAME,
			"api_key": config.SENDGRID_KEY,
			"to":"lukasz.harezlak@gmail.com",
			"toname": "Lukasz",
			"subject": "Example_Subject",
			"text": "testingtextbody",
			"from": "lukasz.harezlak@gmail.com"
		}
		body = tornado.escape.json_encode(mail_data)

		response = yield tornado.gen.Task(
			self.http_client.fetch, config.SENDGRID_URL + "/mail.send.json",
			method='POST', body=body
		)
		self.log.info(response)
		self.log.info(response.body)

		callback(response)