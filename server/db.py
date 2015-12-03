#!/bin/env python
# -*- coding: utf-8 -*-
import redis
import config
import logger
from helpers import epoch_millis

class RedisDb(object):
	"""Local redis db. Using async drivers would be an overkill."""

	#############################################################################
	# CONNECTION INITIALIZATION
	#############################################################################

	def __init__(self, main_logger=None):
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
		try:
			self.db_r.ping()
		except Exception, e:
			self.log.error("Exception connecting to redis: " + str(e))
			return False
		return True

	#############################################################################
	# EMAIL FUNCTIONALITY
	#############################################################################

	def get_user_sent_emails(self, user_id):
		return []

	def save_email(self, to_addr, cc_addr, bcc_addr, topic,
					text, sender_id, handler_id, external_id, result):
		"""
		Uses hash email:<HANDLER_ID>:<EXTERNAL_ID>.
		Also adds <HANDLER_ID>:<EXTERNAL_ID> to the user's emails
		set of emails identified by key emails:<SENDER_ID>.
		"""
		now = epoch_millis()
		email_data = {
			'to_addr': to_addr,
			'cc_addr': ','.join(cc_addr),
			'bcc_addr': ','.join(bcc_addr),
			'topic': topic,
			'text': text,
			'sender_id': sender_id,
			'to_addr': to_addr

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


	#############################################################################
	# EMAIL HANDLERS FUNCTIONALITY
	#############################################################################

	def init_email_handlers(self, email_handlers):
		registered_handlers = self.db_r.lrange('handlers', 0, -1)
		for handler in email_handlers:
			if str(handler.value) not in registered_handlers:
				self.db_r.lpush('handlers', handler.value)
		return

	def get_email_handler_and_rotate(self):
		handler_value = self.db_r.rpoplpush('handlers', 'handlers')

		if not handler_value or not len(handler_value):
			self.log.warning("Handlers not initalized in redis.")
			return None
		return int(handler_value)
