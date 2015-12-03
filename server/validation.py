#!/bin/env python
import logger
from validate_email import validate_email

class Validator(object):

	def __init__(self, main_logger=None):
		self.log = main_logger or logger.init_logger("validator")

	def is_valid_email_address(self, addr):
		"""Checks  if the host has SMTP Server and the email really exists
		Source: https://pypi.python.org/pypi/validate_email

		Expects a single string, returns boolean."""
		# the call is blocking, so only syntactic analysis performed
		# To check if the SMTP server exists change check_mx to True
		# to check if email address exists change verify to true
		return addr is not None and validate_email(addr, verify=False, check_mx=False)

	def are_valid_email_addresses(self, addr_list):
		"""Performs basic syntactic email validation on a list of emails
		passed as a comma separated string.
		Expects a list, returns boolean."""
		addr_list = str(addr_list).split(',')
		for addr in addr_list:
			if not self.is_valid_email_address(addr):
				return False
		return True

	def is_email_request_valid(self, to_addr, cc_addr, bcc_addr, topic, text):
		if not self.is_valid_email_address(to_addr):
			self.log.debug(
                'Incorrect to_addr %s submitted by user %s'
                % (to_addr, user_id))
			return False, 'Invalid main recipient.'

		if cc_addr and len(cc_addr) and not self.are_valid_email_addresses(cc_addr):
			self.log.debug(
                'Incorrect cc_addr list %s submitted by user %s'
                % (cc_addr, user_id))
			return False, 'At least one of cc recipients invalid.'

		if bcc_addr and len(bcc_addr) and not self.are_valid_email_addresses(bcc_addr):
			self.log.debug(
                'Incorrect bcc_addr list %s submitted by user %s'
                % (bcc_addr, user_id))
			return False, 'At least one of bcc recipients invalid.'

		if not topic or not len(topic):
			self.log.debug(
                'Empty topic submitted by user %s'
                % (user_id))
			return False, 'Topic cannot be empty.'

		if not text or not len(text):
			self.log.debug(
                'Empty text submitted by user %s'
                % (user_id))
			return False, 'Text cannot be empty.'
		# valid!
		return True, None
