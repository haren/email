#!/bin/env python

import tornado.web
import tornado.gen
from tornado import httpclient, escape

import logger
import config

from mandrill_handler 	import MandrillEmailHandler
from sendgrid_handler 	import SendgridEmailHandler
from ses_handler 		import SesEmailHandler
from mailgun_handler 	import MailgunEmailHandler

class MainEmailHandler(object):

	def __init__(self, db, main_logger = None):
		self.log = main_logger or logger.init_logger("email")
		self.db  = db

		self.handlers = {
			config.EMAIL_HANDLERS.MANDRILL.value: MandrillEmailHandler(self.log),
			config.EMAIL_HANDLERS.MAILGUN.value: MailgunEmailHandler(self.log),
			config.EMAIL_HANDLERS.SES.value: SesEmailHandler(self.log),
			# config.EMAIL_HANDLERS.SENDGRID.value: SendgridEmailHandler(self.log)
		}
		self.db.init_email_handlers(config.EMAIL_HANDLERS)

	@tornado.gen.engine
	def send_email(self, to_addr, cc_addr, bcc_addr, topic, text, callback):
		"""Uses simple round robin to pick a handler."""
		self.log.debug("Starting")

		# while status failed and not all tried
		current_handler = self.handlers.get(
			self.db.get_email_handler_and_rotate(), None)
		if not current_handler:
			self.log.warning("Couldn't obtain handler.")
			callback(config.SEND_STATUS.FAILED)
			return

		result = yield tornado.gen.Task(
			current_handler.send_email, to_addr, cc_addr, bcc_addr, topic, text
		)
		# if success / queued return
		callback(result)
		return