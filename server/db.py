#!/bin/env python
# -*- coding: utf-8 -*-
import redis

import config
import logger
from helpers import epoch_millis

class RedisDb(object):
	"""
	Class connecting and operating with a redis database.

	For the project scope working only with a local database,
	thus using async drivers is unnecessary.
    """

	#############################################################################
	# CONNECTION INITIALIZATION
	#############################################################################

	def __init__(self, main_logger=None):
		"""Initializes the database connection and logging for the object.

	    Args:
	        main_logger: logger to which the logs should be sent, optional
		Raises:
	        RuntimeError: if redis is not connected properly.
	    """
		self.log = main_logger or logger.init_logger("db")

		self.db_r = redis.StrictRedis(
			host	= config.REDIS_HOST,
			port 	= config.REDIS_PORT,
			db 		= config.REDIS_DB
		)

		if not self.db_r or not self.test_redis_connection():
			# critical
			raise RuntimeError("Redis not connected properly.")

		self.log.debug("Redis initialization complete.")

	def test_redis_connection(self):
		"""Tests redis connection.

	    Returns:
	        True if connected properly, False otherwise.
	    """
		try:
			self.db_r.ping()
		except Exception, e:
			self.log.error("Exception connecting to redis: " + str(e))
			return False
		return True

	#############################################################################
	# EMAIL FUNCTIONALITY
	#############################################################################

	def get_email_data(self, handler_id, external_id):
		"""Retrieves all data stored in redis for a given email.

	    Args:
	        handler_id: Which handler was used to send the email.
	        external_id: External id that the service assigned to the email.
	    Returns:
	    	A dictionary with all values stored for a given email.
	    """
		return self.db_r.hgetall(
			"email:%s:%s" % (handler_id, external_id))

	def get_user_sent_emails(self, user_id):
		"""Retrieves a detailed list of all emails sent by a given user.

	    Args:
	        user_id: User id for whom the emails are to be retrieved.
	    Returns:
	    	A list of dictionaries with all values stored for all emails user sent.
	    """
		if not user_id:
			return []

		emails = []

		# each one in format <HANDLER_ID>:<EXTERNAL_ID>
		user_email_ids = self.db_r.smembers("emails:%s" % user_id)
		for e_id in user_email_ids:
			handler_id, external_id = e_id.split(':')
			emails.append(self.get_email_data(handler_id, external_id))
		return emails

	def save_email(self, to_addr, cc_addr, bcc_addr, topic,
					text, sender_id, handler_id, external_id, result):
		"""Saves email data in redis.

		The hash to which email is saved in redis can be accessed with key:
		email:<HANDLER_ID>:<EXTERNAL_ID>

		The method also adds "<HANDLER_ID>:<EXTERNAL_ID>" to the user's emails
		set of emails identified by key emails:<SENDER_ID>.

	    Args:
	        to_addr: Email address of the main recipient.
	        cc_addr: A list of email addresses of all cc'd recipients.
	        bcc_addr: A list of email addresses of all bcc'd recipients.
	        topic: Email subject.
	        text: Email body.
	        sender_id: user_id of the sender.
	        handler_id: Id of the email handler that was used to send the email.
	        external_id: External id that the service assigned to the email.
	        result: Send result (failed / sent / queued), enum value.
	    """

		now = epoch_millis()
		cc_addr  = cc_addr or []
		bcc_addr = bcc_addr or []
		email_data = {
			'to': to_addr,
			'cc': ','.join(cc_addr),
			'bcc': ','.join(bcc_addr),
			'subject': topic,
			'text': text,
			'sender_id': sender_id,
			'id': "%s:%s" % (handler_id, external_id)
		}
		if result == config.SEND_STATUS.SENT:
			email_data['sent_at'] = now
		elif result == config.SEND_STATUS.QUEUED:
			email_data['queued_at'] = now
		else:
			email_data['failed_at'] = now

		self.db_r.hmset("email:%s:%s" % (handler_id, external_id), email_data)
		self.db_r.sadd('emails:%s' % sender_id, '%s:%s' % (handler_id, external_id))
		return

	def set_email_sent(self, handler_id, external_id):
		"""Marks email identified by <HANDLER_ID>:<EXTERNAL_ID> as sent.

	    Args:
	    	handler_id: Id of the email handler that was used to send the email.
	        external_id: External id that the service assigned to the email.
	    Returns:
	    	The result of redis operation.
	    """
		now = epoch_millis()
		return self.db_r.hset(
			"email:%s:%s" % (handler_id, external_id), 'sent_at', now)


	def set_email_rejected(self, handler_id, external_id):
		"""Marks email identified by <HANDLER_ID>:<EXTERNAL_ID> as rejected.

	    Args:
	    	handler_id: Id of the email handler that was used to send the email.
	        external_id: External id that the service assigned to the email.
	    Returns:
	    	The result of redis operation.
	    """
		now = epoch_millis()
		return self.db_r.hset(
			"email:%s:%s" % (handler_id, external_id), 'rejected_at', now)


	#############################################################################
	# EMAIL HANDLERS FUNCTIONALITY
	#############################################################################

	def init_email_handlers(self, email_handlers):
		"""Dynamically initializes all email handlers
		(saves them in redis to facilitate round robin in the main email handler).

		Called on main email handler creation.

	    Args:
	    	email_handlers: an Enum object with all email handlers.
	    """
		registered_handlers = self.db_r.lrange('handlers', 0, -1)
		for handler in email_handlers:
			if str(handler.value) not in registered_handlers:
				self.db_r.lpush('handlers', handler.value)
		return

	def get_email_handler_and_rotate(self):
		"""Retrieves the least recently used handler and rotates
		the list used to round-robin handlers.

	    Returns:
	    	handler_value: An integer representing the enum value of the selected handler.
	    """
		handler_value = self.db_r.rpoplpush('handlers', 'handlers')

		if not handler_value or not len(handler_value):
			self.log.warning("Handlers not initalized in redis.")
			return None
		return int(handler_value)
