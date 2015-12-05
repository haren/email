#!/bin/env python

from tornado.httpclient import AsyncHTTPClient
import tornado.web
import tornado.gen

import config
import logger

class SendgridEmailHandler(object):

	def __init__(self, main_logger = None):
		self.log = main_logger or logger.init_logger("sendgrind")

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

		request = HTTPRequest(
			url=config.SENDGRID_URL + "/mail.send.json",
			connect_timeout=config.TIMEOUT, request_timeout=config.TIMEOUT,
			body=body, method='POST')

		response = yield tornado.gen.Task(
			self.http_client.fetch, request)

		callback(response)
		return