#!/bin/env python

# async sendgrid - https://github.com/Greplin/greplin-tornado-sendgrid
# async mandrill - http://stackoverflow.com/a/12159106/1731005
# async ses - https://github.com/rsec/AsyncSES

import tornado.web
import tornado.gen
from tornado import httpclient, escape
import time

import logger

class EmailHandler(object):

	def __init__(self, logger = None):
	    self.log = logger
	    if not self.log:
			self.log = logger.init_logger("email")

	@tornado.gen.engine
	def send_email(self, text, callback):
		self.log.debug("Starting")
		result = yield tornado.gen.Task(tornado.ioloop.IOLoop.instance().add_timeout, time.time() + 4)
		self.log.debug("RETURNING")
		callback(result)
		# self.finish()