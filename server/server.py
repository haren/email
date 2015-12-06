#!/bin/env python

import os
import tornado.ioloop
import tornado.httpserver
import tornado.escape
import tornado.web
import tornado.gen
import uuid
import json

import config
import logger
import db
import email_handlers.main_email_handler as eh
import validation

##############################################################################
# MAIN APPLICATION CLASS
##############################################################################

class Application(tornado.web.Application):
    """
    Main application class.
    """

    def __init__(self):
        """Initalizes the tornado server.

        Defines the routing and server settings.
        """
        handlers = [
            # static files handler
            (r"/www/(.*)", tornado.web.StaticFileHandler, {
                "path": os.path.join(os.path.dirname(__file__), '../www/')}),

            # end user email functionality
            (r"/emails/*",  EmailsHandler),

            # Email handlers confirmation webhooks
            (r"/delivered/mailgun/*",   DeliveryMailgunHandler),
            (r"/delivered/ses/*",       DeliverySesHandler),

            # Main handlers - serving static content & handling url errors.
            (r"/*",         MainHandler),
            (r".*",         DefaultHandler)
        ]
        settings = dict(
            cookie_secret   = config.COOKIE_SECRET,
            template_path   = os.path.join(
                                os.path.dirname(__file__), '../www/'),
            xsrf_cookies    = True,
            debug           = True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

##############################################################################
# BASE RESPONSE CLASS
##############################################################################

class AjaxResponse(object):
    """Base class for forming responses.
    """

    def __init__(self, status=0):
        self.response           = {}
        self.response['status'] = status

    def get(self):
        return self.response

    def add_code(self, code):
    	return self.add_field('status', code)

    def add_msg(self, msg):
        return self.add_field('msg', msg)

    def add_field(self, name, value):
        self.response[name] = value

##############################################################################
# HANDLERS
##############################################################################

class BaseHandler(tornado.web.RequestHandler):
    """
    Base Handler class.

    Sets supported http methods and response types.

    Aggregates methods shared by all handlers.
    """

    def check_xsrf_cookie(self):
        # TODO REMOVE AFTER TESTING
        pass

    SUPPORTED_METHODS = ("GET", "POST")

    def write(self, *args, **kwargs):
        main_logger.debug("Writing %s." % args)
        # set correct header type
        self.set_header("Content-Type", "application/json")
        super(BaseHandler, self).write(*args, **kwargs)

    def get_current_user(self):
        user_id = self.get_secure_cookie(config.COOKIE_NAME)
        if not user_id:
            return None
        else:
            return user_id

    def set_current_user(self, expires_days=7):
        new_user_id = str(uuid.uuid4())
        self.set_secure_cookie(
                config.COOKIE_NAME,
                tornado.escape.url_escape(str(new_user_id)),
                expires_days=expires_days
        )
        main_logger.debug("New user %s registered." % new_user_id)
        return new_user_id


class MainHandler(BaseHandler):
    """
    Main Handler class.

    Serves the index page.
    """

    def write(self, *args, **kwargs):
        # Do not set json type for this handler.
        super(BaseHandler, self).write(*args, **kwargs)

    def get(self):
        """Sets the cookie if not set and renders the page."""
        user_id = self.get_current_user() or self.set_current_user()

        main_logger.debug("Page loaded for user: %s" % user_id)
        return self.render('index.html')


class EmailsHandler(BaseHandler):
    """
    Email Handler class.

    Servers the email sending and email data retrieval functionalities
    through its post and get methods respectively.
    """

    # @tornado.web.removeslash
    def get(self):
        """Retrieves a list of all emails sent by a given user.

        If call succeedes, returns QUEUED status. A webhook has been setup for
        delivery confirmations (server.DeliveryMailgunHandler).

        Returns:
            {
                'status': Response status.
                'emails': A list of email objects. Included only if status == 200.
                'msg': Error message. Included only if status != 200.
            }
        """
        try:
            response = AjaxResponse()
            user_id  = self.get_current_user()
            main_logger.debug("Requested emails list for user %s." % user_id)

            emails = main_db.get_user_sent_emails(user_id)

            response.add_code(config.RESPONSE_OK)
            response.add_field('emails', emails)

        except Exception, e:
            main_logger.exception("Rest server exception: %s" % e)
            response.add_code(config.RESPONSE_ERROR)
            response.add_msg('Internal Error')

        finally:
            response = tornado.escape.json_encode(
            	response.get())
            self.write(response)
            self.finish()

    # @tornado.web.removeslash
    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        """Sends an email if the request is valid. Performs the validation.

        If call succeedes, returns QUEUED status. A webhook has been setup for
        delivery confirmations (server.DeliveryMailgunHandler).

        Args:
            to: A string containing a valid email address of the main recipient.
            cc: A string containing a comma-separated list of cc addresses.
            bcc: A string containing a comma-separated list of bcc addresses.
            subject: A string containing email subject. Cannot be empty.
            text: A string containing email body. Cannot be empty.

        Returns:
            {
                'status': Response status.
                'send_status': 'SENT' / 'QUEUED' / 'FAILED'. Included only if status == 200.
                'msg': Error message. Included only if status != 200.
            }
        """
        global main_email_handler
        global validator
        try:
            response  = AjaxResponse()
            user_id   = self.get_current_user()
            to_addr   = self.get_argument('to', None)
            cc_addr   = self.get_argument('cc', None)
            bcc_addr  = self.get_argument('bcc', None)
            topic     = self.get_argument('subject', None)
            text      = self.get_argument('text', None)

            valid, message = validator.is_email_request_valid(
                to_addr, cc_addr, bcc_addr, topic, text)

            if not valid:
                response.add_code(config.RESPONSE_ERROR)
                response.add_msg(message)
                return
                yield

            # valid, convertion safe
            if cc_addr and len(cc_addr):
                cc_addr = str(cc_addr).split(',')
            if bcc_addr and len(bcc_addr):
                bcc_addr = str(bcc_addr).split(',')

            status = yield tornado.gen.Task(
                main_email_handler.send_email,
                to_addr, cc_addr, bcc_addr,
                topic, text, user_id
            )

            main_logger.debug(
                "Email %s to %s by user %s sent with status %s."
                % (topic, to_addr, user_id, status))
            response.add_code(config.RESPONSE_OK)
            response.add_field('send_status', status.name)

        except Exception, e:
            main_logger.exception(e)
            response.add_code(config.RESPONSE_ERROR)
        finally:
            json_ = tornado.escape.json_encode(response.get())
            self.write(json_)
            self.finish()


class DeliveryMailgunHandler(BaseHandler):
    """
    Handler prepared for the Mailgun delivery confirmation webhook.
    """

    def post(self):
        """Marks the email sent by a mailgun handler as sent in the database.
        """
        try:
            response    = AjaxResponse()
            external_id = self.get_argument("Message-Id", None)

            if external_id:
                external_id = external_id.replace('<', '').replace('>', '')


            main_db.set_email_sent(
                config.EMAIL_HANDLERS.MAILGUN.value, external_id)

            main_logger.debug(
                "Mailgun email %s sent confirmation received." % external_id)

        except Exception, e:
            main_logger.exception(e)
            response.add_code(config.RESPONSE_ERROR)
        finally:
            json_ = tornado.escape.json_encode(response.get())
            self.write(json_)
            self.finish()


class DeliverySesHandler(BaseHandler):
    """
    Handler prepared for the Ses delivery confirmation webhook.
    """

    def post(self):
        """Marks the email sent by a SES handler as sent in the database.
        """
        try:
            response    = AjaxResponse()

            message     = json.loads(self.request.body)["Message"]
            external_id = json.loads(message)["mail"]["messageId"]

            main_db.set_email_sent(
                config.EMAIL_HANDLERS.SES.value, external_id)

            main_logger.debug(
                "SES email %s sent confirmation received." % external_id)

        except Exception, e:
            main_logger.exception(e)
            response.add_code(config.RESPONSE_ERROR)
        finally:
            json_ = tornado.escape.json_encode(response.get())
            self.write(json_)
            self.finish()


class DefaultHandler(BaseHandler):
    """
    Default handler.

    Handles all requests attempting to reach non-existing API endpoints.
    """

    def get(self):
        try:
            response = AjaxResponse()
            if 'favicon' not in self.request.uri:
                # favicon requests often come down from browsers
                main_logger.warning("Incorrect url requested.")
                response.add_msg("Incorrect request url %s." % self.request.uri)

            response.add_code(config.RESPONSE_NOTFOUND)

        except Exception, e:
        	main_logger.exception("Rest server exception: %s" % e)
        	response.add_code(config.RESPONSE_ERROR)
        	response.add_msg('Internal Error')

        finally:
            if 'favicon' not in self.request.uri:
                response = tornado.escape.json_encode(
                	response.get())
                self.write(response)
                self.finish()

##############################################################################
# MAIN APPLICATION
##############################################################################

if __name__ == '__main__':
    global main_logger
    main_logger = logger.init_logger('main')

    global main_db
    main_db = db.RedisDb(main_logger)

    global email_handler
    main_email_handler = eh.MainEmailHandler(main_db, main_logger)

    global validator
    validator = validation.Validator()

    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(config.PORT)
    main_logger.debug("Application initialized.")
    tornado.ioloop.IOLoop.instance().start()
