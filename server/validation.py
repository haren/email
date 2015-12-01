#!/bin/env python

from validate_email import validate_email

class Validator(object):

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
