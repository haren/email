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
	"""
	Class exposing email sending functionality. Concrete handlers are hidden from the clients.
	Failover supported.
    """

	def __init__(self, db, main_logger = None):
		"""Initalizes the database and the logger for the object.

		Creates objects for all available email handlers.

	    Args:
	    	main_logger: logger to which the logs should be sent, optional
	    	db: database connection object.
	    """
		self.log = main_logger or logger.init_logger("email")
		self.db  = db

		self.handlers = {
			config.EMAIL_HANDLERS.MANDRILL.value: 	MandrillEmailHandler(self.log),
			config.EMAIL_HANDLERS.MAILGUN.value: 	MailgunEmailHandler(self.log),
			config.EMAIL_HANDLERS.SES.value: 		SesEmailHandler(self.log)
		}
		self.db.init_email_handlers(config.EMAIL_HANDLERS)

	@tornado.gen.engine
	def send_email(self, to_addr, cc_addr, bcc_addr, topic, text, sender_id, callback):
		"""Sends an email using one of the registered email services.

		Supports failover (tries all available services before failing).

		Uses a simple round robin selection for email handlers.

		Saves the email data and send result in redis.

	    Args:
	    	to_addr: Email address of the main recipient.
	        cc_addr: A list of email addresses of all cc'd recipients.
	        bcc_addr: A list of email addresses of all bcc'd recipients.
	        topic: Email subject.
	        text: Email body.
	        sender_id: User id of the user requesting the email to be sent.
	    Returns:
	    	SendStatus: FAILED/QUEUED/SENT
	    """

		# try all handlers until once sends / queues message
		for i in range(0, len(config.EMAIL_HANDLERS.__members__)): # no nice way to get enum members length
			# obtain current handler, round-robin'ed
			handler_id      = self.db.get_email_handler_and_rotate()
			current_handler = self.handlers.get(handler_id, None)
			if not current_handler:
				self.log.warning("Couldn't obtain handler.")
				callback(config.SEND_STATUS.FAILED)
				return # failed to find a working handler

			# attempt to send email using the current handler
			cb_result = yield tornado.gen.Task(
				current_handler.send_email,
				to_addr, cc_addr, bcc_addr, topic, text
			)
			# cb_result[0] - args, cb_result[1] - kwargs
			# http://www.tornadoweb.org/en/stable/gen.html#tornado.gen.Arguments
			result, external_id = cb_result[0][0], cb_result[0][1]

			self.log.info(
				"Email %s sending result through handler %s: %s, external_id: %s."
				% (topic, current_handler, result, external_id)
				)

			if result != config.SEND_STATUS.FAILED:
				# save sent email
				self.db.save_email(
					to_addr, cc_addr, bcc_addr, topic, text,
					sender_id, handler_id, external_id, result)

				# only continue with the iterations if failed to send.
				# reaching this close suggests sent / queued, function can exit
				callback(result)
				return

		else: # no success / queued email has been returned, sending failed.
			self.log.warning(
				"No handler managed to send an email %s to %s successfully."
				% (topic, to_addr	)
			)

			self.db.save_email(
				to_addr, cc_addr, bcc_addr, topic,
				text, sender_id, handler_id,
				None, config.SEND_STATUS.FAILED)

			callback(config.SEND_STATUS.FAILED)
			return
