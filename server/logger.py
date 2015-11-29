import logging
from logging.handlers import TimedRotatingFileHandler
import os

def init_logger(name):
    """Initialize the logging system for a given module/process."""
    log_file_name = name + '.log'
    formatter     = logging.Formatter('%(asctime)s %(levelname)-8s - %(module)s - %(message)s')

    # prepare file name
    current_directory = os.path.abspath(os.path.dirname(__file__))
    log_directory = os.path.join(current_directory, 'logs', log_file_name)
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    file_name = os.path.join(log_directory, log_file_name)

    # create and configure a rotating file handler
    file_handler = TimedRotatingFileHandler(filename=file_name, when='H', interval=8, backupCount=6)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    # create logger and add handlers
    logger = logging.getLogger(name)
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)
    return logger