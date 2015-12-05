#!/bin/env python

##############################################################################
# TO USE MAKE SURE YOUR aws_access_key_id and aws_secret_access_key
# ARE STORED IN ~/.aws/credentials
##############################################################################

from tornado_botocore import Botocore
import tornado.web
import tornado.gen

import config
import logger

class SesEmailHandler(object):
	"""
	Handler class for Amazon SES external email service provider.

	Source: https://aws.amazon.com/ses/
    """

	def __init__(self, main_logger = None):
		"""Initalizes the logger for the object.
		Creates an async boto client to communicate with the aws service.
		API keys are derived from the environment (e.g. ~/.aws/credentials).

	    Args:
	    	main_logger: logger to which the logs should be sent, optional
	    """
		self.log = main_logger or logger.init_logger("ses")

		self.ses_client = Botocore(
			service='ses', operation='SendEmail', region_name='eu-west-1'
		)

	@tornado.gen.engine
	def send_email(self, to_addr, cc_addr, bcc_addr, topic, text, callback):
		"""Sends an email using mailgun service.

		If call succeedes, returns QUEUED status. An SNS topic has been created
		and webhook with a subscription to the topic has been setup for
		delivery confirmations (server.DeliverySesHandler).

	    Args:
	    	to_addr: Email address of the main recipient.
	        cc_addr: A list of email addresses of all cc'd recipients.
	        bcc_addr: A list of email addresses of all bcc'd recipients.
	        topic: Email subject.
	        text: Email body.
	    Returns:
	    	(SendStatus, ExternalId)
	    	SendStatus: FAILED/QUEUED
	    	ExternalId: External id that the service assigned to the email. None if FAIELD.
	    """
		message     = self._prepare_message(topic, text)
		destination = self._prepare_destination(to_addr, cc_addr, bcc_addr)

		response = yield tornado.gen.Task(self.ses_client.call,
			Source=config.FROM_ADDRESS, Message=message, Destination=destination
		)
		if (int(response['ResponseMetadata']['HTTPStatusCode'])
				== config.RESPONSE_OK):
			# SES always queues.
			callback(config.SEND_STATUS.QUEUED, response['MessageId'])
			return

		# failed
		callback(config.SEND_STATUS.FAILED, None)
		return

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