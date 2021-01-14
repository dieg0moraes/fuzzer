"""
Copyright (c) 2020 Diego Moraes. MIT license, see LICENSE file.
"""
import logging
from sys import exit as sysexit
from colorama import Fore, Back
from .settings import SUCCESS_LEVEL_NUM, LOG_FILE_NAME, LOG_DEFAULTS, EXIT_ON_CRITICAL


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
    # pylint: disable=too-many-instance-attributes

    def __init__(self, name, config={}, enabled=True):  # FIXME: ¿No es seguro config={}?

        self.info = config.get("info", LOG_DEFAULTS["info"])
        self.rstatus = config.get("status", LOG_DEFAULTS["status"])
        self.exc = config.get("exceptions", LOG_DEFAULTS["exceptions"])
        self.debug = config.get("debug", LOG_DEFAULTS["debug"])
        self.file = config.get("file", LOG_DEFAULTS["file"])
        self.colors = config.get("colors", LOG_DEFAULTS["colors"])
        self.enabled = enabled

        # Get new logger.
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter('[%(module)s][%(levelname)s] %(message)s')

        if self.enabled:
            # File Handler.
            if self.file:
                fh = logging.FileHandler(LOG_FILE_NAME)
                fh.setLevel(logging.DEBUG)
                fh.setFormatter(formatter)
                self.logger.addHandler(fh)

            # Console Handler.
            if self.colors:
                formatter = _CustomFormatter()

            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)
            ch.setFormatter(formatter)
            self.logger.addHandler(ch)

        else:
            self.logger.disabled = True


    def ldebug(self, debug_text):
        """Log debug messages"""
        if self.debug:
            self.logger.debug(debug_text)


    def linfo(self, info_text):
        """Log fuzzer execution information."""
        if self.info:
            self.logger.info(info_text)


    def lwarn(self, warning):
        """Log warnings."""
        self.logger.warning(warning)


    def lexc(self, exception, url=""):
        """Unhandled exceptions"""
        if self.exc:
            self.logger.error('EXCEPTION(%s)::%s', exception, url)


    def lerr(self, message):
        """Log other errors."""
        if self.exc:
            self.logger.error(message)


    def lcritical(self, message):
        """Log critical errors."""
        self.logger.critical(message)
        if EXIT_ON_CRITICAL:
            sysexit(1)


    def lstatus(self, status_code, url):
        """Log connection status code with url"""
        if status_code[0] == "2":
            self.logger.success('(%s) %s', status_code, url)
        elif self.rstatus:
            if status_code[0] == "3":
                self.logger.info('REDIRECT(%s)::%s', status_code, url)
            elif status_code[0] in ("4", "5"):
                self.logger.info('FAIL(%s)::%s', status_code, url)
            elif status_code[0] == "1":
                self.logger.info('INFO(%s)::%s', status_code, url)


class _CustomFormatter(logging.Formatter):
    """Logging Formatter to add colors"""

    yellow = Fore.LIGHTYELLOW_EX
    green = Fore.LIGHTGREEN_EX
    red = Fore.LIGHTRED_EX
    bold_red = Back.RED
    reset = Fore.RESET + Back.RESET
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
