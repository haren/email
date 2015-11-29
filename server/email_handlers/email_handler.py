#!/bin/env python

# async sendgrid - https://github.com/Greplin/greplin-tornado-sendgrid
# async ses - https://github.com/rsec/AsyncSES

import tornado.web
import tornado.gen
from tornado import httpclient, escape
import time

import logger
from mandrill_handler import MandrilEmailHandler

class EmailHandler(object):

	def __init__(self, main_logger = None):
		self.log = main_logger
		if not self.log:
			self.log = logger.init_logger("email")

		self.mandrill = MandrilEmailHandler(self.log)

	@tornado.gen.engine
	def send_email(self, text, callback):
		self.log.debug("Starting")
		result = yield tornado.gen.Task(
			self.mandrill.send_email
		)
		self.log.debug("RETURNING %s" % result)
		callback(result)
		# self.finish()