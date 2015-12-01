#!/bin/env python

# send mailgun https://documentation.mailgun.com/user_manual.html#sending-via-api
# async ses - https://github.com/rsec/AsyncSES

import tornado.web
import tornado.gen
from tornado import httpclient, escape

import logger
from mandrill_handler import MandrillEmailHandler
from sendgrid_handler import SendgridEmailHandler
from ses_handler import SesEmailHandler

class MainEmailHandler(object):

	def __init__(self, main_logger = None):
		self.log = main_logger
		if not self.log:
			self.log = logger.init_logger("email")

		self.mandrill = MandrillEmailHandler(self.log)
		self.sendgrid = SendgridEmailHandler(self.log)
		self.ses 	  = SesEmailHandler(self.log)

	@tornado.gen.engine
	def send_email(self, text, callback):
		self.log.debug("Starting")

		result = yield tornado.gen.Task(
			# self.mandrill.send_email
			# self.sendgrid.send_email
			self.ses.send_email
		)

		self.log.debug("RETURNING %s" % result)
		callback(result)
		# self.finish()