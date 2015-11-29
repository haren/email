#!/bin/env python


# async sendgrid - https://github.com/Greplin/greplin-tornado-sendgrid
# async mandrill - http://stackoverflow.com/a/12159106/1731005
# async ses - https://github.com/rsec/AsyncSES


import time

class EmailHandler(object):

	def __init__(self, logger):
		self.log = logger

	def send_email(self, text, callback):
		self.log.debug("Starting")
		result = 1
		self.log.debug("RETURNING")
		callback(result)