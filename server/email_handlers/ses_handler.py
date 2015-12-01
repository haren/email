#!/bin/env python

##############################################################################
# TO USE MAKE SURE YOUR aws_access_key_id and aws_secret_access_key
# ARE STORED IN ~/.aws/credentials
##############################################################################

from tornado_botocore import Botocore
import tornado.web
import tornado.gen

import config

class SesEmailHandler(object):

	def __init__(self, logger):
		self.log = logger
		if not self.log:
			self.log = logger.init_logger("ses")

		self.ses_client = Botocore(
			service='ses', operation='SendEmail', region_name='eu-west-1'
		)

	@tornado.gen.engine
	def send_email(self, to_addr, cc_addr, bcc_addr, topic, text, callback):
		message     = self._prepare_message(topic, text)
		destination = self._prepare_destination(to_addr, cc_addr, bcc_addr)

		response = yield tornado.gen.Task(self.ses_client.call,
			Source="lukasz.harezlak@gmail.com", Message=message, Destination=destination
		)

		self.log.info(response)
		callback(response)

	def _prepare_message(self, topic, text):
		return {
			'Subject': {
				'Data': topic.decode('utf-8'),
			},
			'Body': {
				'Text': {
					'Data': text.decode('utf-8'),
				}
			}
		}

	def _prepare_destination(self, to_addr, cc_addr, bcc_addr):
		destination = {
			'ToAddresses': [to_addr]
		}
		if cc_addr:
			destination['CcAddresses'] = cc_addr
		if bcc_addr:
			destination['BccAddresses'] = bcc_addr
		return destination