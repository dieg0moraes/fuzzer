"""
Copyright (c) 2020 Diego Moraes. MIT license, see LICENSE file.
"""
import logging
from colorama import Fore, Back
from .settings import SUCCESS_LEVEL_NUM, EXCEPTION_CODE, ERROR_CODE, CRITICAL_CODE


# New logging level (SUCCESS) #
logging.addLevelName(SUCCESS_LEVEL_NUM, "SUCCESS")

def success_def(self, message, *args, **kws):
    if self.isEnabledFor(SUCCESS_LEVEL_NUM):
        self._log(SUCCESS_LEVEL_NUM, message, args, **kws)

logging.Logger.success = success_def
logging.SUCCESS = SUCCESS_LEVEL_NUM
logging.__all__ += ['SUCCESS']


class LogWrapper:
    """Logging wrapper class"""

    def __init__(self, name, config):

        self.info = config["info"]
        self.rstatus = config["status"]
        self.exc = config["exceptions"]
        self.debug = config["debug"]

        # Get new logger.
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter('[%(levelname)s] %(message)s')

        # File Handler.
        if config["file"]:
            self.fh = logging.FileHandler('app.log')
            self.fh.setLevel(logging.DEBUG)
            self.fh.setFormatter(formatter)
            self.logger.addHandler(self.fh)

        # Console Handler.
        if config["colors"]:
            formatter = CustomFormatter()

        self.ch = logging.StreamHandler()
        self.ch.setLevel(logging.DEBUG)
        self.ch.setFormatter(formatter)
        self.logger.addHandler(self.ch)


    def lsuccess(self, text):
        """Log success (200) messages."""
        self.logger.success(text)


    def ldebug(self, debug_text):
        """Log debug messages"""
        if self.debug:
            self.logger.debug(debug_text)


    def linfo(self, info_text):
        """Log fuzzer execution information."""
        if self.info:
            self.logger.info(info_text)


    def lexc(self, exception, code_num, url=""):
        """Log exceptions."""
        if self.exc:
            if code_num == EXCEPTION_CODE:
                self.logger.warning('EXCEPTION(%s)::%s', exception, url)
            elif code_num == ERROR_CODE:
                self.logger.error(exception)
            elif code_num == CRITICAL_CODE:
                self.logger.critical(exception)


    def lstatus(self, status_code, url):
        """Log other connection status codes (different from 200)"""
        if self.rstatus:
            if status_code[0] == "3":
                self.logger.info('REDIRECT(%s)::%s', status_code, url)
            elif status_code[0] in ("4", "5"):
                self.logger.info('FAIL(%s)::%s', status_code, url)


class CustomFormatter(logging.Formatter):
    """Logging Formatter to add colors"""

    yellow = Fore.LIGHTYELLOW_EX
    green = Fore.LIGHTGREEN_EX
    red = Fore.LIGHTRED_EX
    bold_red = Back.RED
    reset = Fore.RESET
    format = "[%(levelname)s] %(message)s"

    FORMATS = {
        logging.DEBUG: format,
        logging.INFO: format,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset,
        logging.SUCCESS: green + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
