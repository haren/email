#!/bin/env python
import re

class Validator(object):

	def __init__(self):
		self.email_regex = re.compile('[^@]+@[^@]+\.[^@]+')

	def is_valid_email_address(self, addr):
		"""Performs basic syntactic email validation.
		Expects a single string, returns boolean."""
		return addr is not None and self.email_regex.match(addr)

	def are_valid_email_addresses(self, addr_list):
		"""Performs basic syntactic email validation on a list of emails.
		Expects a list, returns boolean."""
		for addr in addr_list:
			if not self.is_valid_email_address(addr):
				return False
		return True
