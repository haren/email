#!/bin/env python

##############################################################################
# TO USE MAKE SURE YOUR aws_access_key_id and aws_secret_access_key
# ARE STORED IN ~/.aws/credentials
##############################################################################

from tornado.httpclient import AsyncHTTPClient
from tornado_botocore import Botocore
import tornado.web
import tornado.gen

import config

class SesEmailHandler(object):

	def __init__(self, logger):
		self.log = logger
		if not self.log:
			self.log = logger.init_logger("mandrill")

		self.http_client = AsyncHTTPClient()

	@tornado.gen.engine
	def send_email(self, callback):
		ses_send_email = Botocore(
			service='ses', operation='SendEmail',
			region_name='eu-west-1'
		)
		source = 'lukasz.harezlak@gmail.com'
		message = {
			'Subject': {
				'Data': 'Example subject'.decode('utf-8'),
			},
			'Body': {
				'Html': {
					'Data': '<html>Example content</html>'.decode('utf-8'),
				},
			'Text': {
				'Data': 'Example content'.decode('utf-8'),
				}
			}
		}
		destination = {
			'ToAddresses': ['lukasz.harezlak@gmail.com'],
		}

		response = yield tornado.gen.Task(ses_send_email.call,
			Source=source, Message=message, Destination=destination
		)

		self.log.info(response)
		callback(response)