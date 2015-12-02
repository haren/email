#!/bin/env python
# -*- coding: utf-8 -*-
import redis
import config
import logger

class RedisDb(object):

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

	def save_user_sent_email(self, email):
		return True