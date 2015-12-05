#!/bin/env python
import logger
from validate_email import validate_email

class Validator(object):
	"""
	Class bucketing all validation needed by the server.
    """

	def __init__(self, main_logger=None):
		"""Initializes the logging for the object.

	    Args:
	        main_logger: logger to which the logs should be sent, optional
	    """
		self.log = main_logger or logger.init_logger("validator")

	def is_valid_email_address(self, addr):
		"""Checks  if the host has SMTP Server and the email really exists.

		Source: https://pypi.python.org/pypi/validate_email

	    Args:
	        addr: a string containing the email address to be validated
		Returns:
	        True if email address is valid, False otherwise
	    """
		# the call is blocking, so only syntactic analysis performed
		# To check if the SMTP server exists change check_mx to True
		# to check if email address exists change verify to true
		return addr is not None and validate_email(addr, verify=False, check_mx=False)

	def are_valid_email_addresses(self, addr_list):
		"""Performs basic syntactic email validation on a list of emails
		passed as a comma separated string.

	    Args:
	        addr: a list of strings containing the email addresses to be validated
		Returns:
	        True if all email addresses are valid, False otherwise
	    """
		addr_list = str(addr_list).split(',')
		for addr in addr_list:
			if not self.is_valid_email_address(addr):
				return False
		return True

	def is_email_request_valid(self, to_addr, cc_addr, bcc_addr, topic, text):
		"""Performs validation for the /api/emails send email post request.

	    Args:
	        to_addr: Email address of the main recipient.
	        cc_addr: A list of email addresses of all cc'd recipients.
	        bcc_addr: A list of email addresses of all bcc'd recipients.
	        topic: Email subject.
	        text: Email body.
		Returns:
	        (Success, ErrorMessage)
	        Success: a boolean indicating if validation was successful
	        ErrorMessage: which indicates the reason why validation failed and
	        can be safely passed on to the client (None if validation passed).
	    """
		if not self.is_valid_email_address(to_addr):
			self.log.debug(
                'Incorrect to_addr %s.' % (to_addr))
			return False, 'Invalid main recipient.'

		if cc_addr and len(cc_addr) and not self.are_valid_email_addresses(cc_addr):
			self.log.debug(
                'Incorrect cc_addr list %s submitted.' % (cc_addr))
			return False, 'At least one of cc recipients invalid.'

		if bcc_addr and len(bcc_addr) and not self.are_valid_email_addresses(bcc_addr):
			self.log.debug(
                'Incorrect bcc_addr list %s.' % (bcc_addr))
			return False, 'At least one of bcc recipients invalid.'

		if not topic or not len(topic):
			self.log.debug(
                'Empty topic submitted.')
			return False, 'Topic cannot be empty.'

		if not text or not len(text):
			self.log.debug(
                'Empty text submitted.')
			return False, 'Text cannot be empty.'
		# valid!
		return True, None
