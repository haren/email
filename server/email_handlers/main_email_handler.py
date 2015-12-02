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
			config.EMAIL_HANDLERS.MANDRILL.value: 	MandrillEmailHandler(self.log),
			config.EMAIL_HANDLERS.MAILGUN.value: 	MailgunEmailHandler(self.log),
			config.EMAIL_HANDLERS.SES.value: 		SesEmailHandler(self.log),
			# config.EMAIL_HANDLERS.SENDGRID.value: SendgridEmailHandler(self.log)
		}
		self.db.init_email_handlers(config.EMAIL_HANDLERS)

	@tornado.gen.engine
	def send_email(self, to_addr, cc_addr, bcc_addr, topic, text, callback):
		"""Uses simple round robin to pick a handler."""
		self.log.debug("Starting")

		# try all handlers until once sends / queues message
		for i in range(0, 3):
			# obtain current handler, round-robin'ed
			current_handler = self.handlers.get(
				self.db.get_email_handler_and_rotate(), None)
			if not current_handler:
				self.log.warning("Couldn't obtain handler.")
				callback(config.SEND_STATUS.FAILED)
				return # failed to find a working handler

			# attempt to send email using the current handler
			result = yield tornado.gen.Task(
				current_handler.send_email,
				to_addr, cc_addr, bcc_addr, topic, text
			)

			self.log.info("===========>Attempting using %s" % current_handler)

			if result != config.SEND_STATUS.FAILED:
				# only continue with the iterations if failed to send.
				# reaching this close suggests sent / queued, function can exit
				callback(result)
				return

		else: # no success / queued email has been returned, sending failed.
			self.log.warning(
				"No handler managed to send an email %s to %s successfully."
				% (topic, to_addr	)
			)
			callback(config.SEND_STATUS.FAILED)
			return
