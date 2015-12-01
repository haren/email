#!/bin/env python

##############################################################################
# REST SERVER
##############################################################################

COOKIE_NAME 	= 'user'
COOKIE_SECRET 	= '8f961186-ab96-4c2a-b043-f623b153b3c2b1f3b9f1-01ea-41ea-be93-6a0deee62ca7'

# Response codes
RESPONSE_ERROR         = 500
RESPONSE_NOTFOUND      = 404
RESPONSE_OK            = 200

# Api listening port
PORT = 8888

##############################################################################
# REDIS
##############################################################################

REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DB   = 0

##############################################################################
# EMAIL CONFIG
##############################################################################
FROM_ADDRESS = "lukasz.harezlak@gmail.com"

MANDRILL_URL = "https://mandrillapp.com/api/1.0/"
MANDRILL_KEY = "FILL_IN_THE_KEY"

SENDGRID_URL      = "https://api.sendgrid.com/api"
SENDGRID_USERNAME = "FILL_IN_USERNAME"
SENDGRID_KEY      = "FILL_IN_THE_KEY"

MAILGUN_USERNAME 	= "FILL_IN_USERNAME"
MAILGUN_URL 		= "https://api.mailgun.net/v3/%s.mailgun.org" % MAILGUN_USERNAME
MAILGUN_KEY 		= "FILL_IN_THE_KEY"

##############################################################################
# EMAIL TIMEOUTS
##############################################################################
 # how long clients are allowed to wait for
 # a send confirmation before aborting / canceling (in seconds)
TIMEOUT = 3

# how long blocking clients are allowed to wait for
# a send confirmation before aborting / canceling (in seconds)
BLOCKING_TIMEOUT = 1

##############################################################################
# EMAIL SEND STATUS
##############################################################################
enum = lambda **enums: type('Enum', (), enums) # simulate enums
SEND_STATUS = enum(
	SENT=2,
	FAILED=1,
	QUEUED=0
)

# when running in docker container this needs to be changed to the
# docker VM IP, e.g. on Mac can be looked up (depeneding on the used tool) using:
# docker-machine ip dev
# or
# boot2docker ip
HOST = "192.168.59.103" # localhost - "127.0.0.1", boot2docker on mac: "192.168.59.103"