"""
INSERTE LICENCIA
"""
import logging
from colorama import Fore, Back


# New logging level (SUCCESS) #
SUCCESS_LEVEL_NUM = 15
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

        if config[2] == "ALL":
            self.info = self.rstatus = self.exc = self.debug = True
        else:
            self.info = config[2]
            self.rstatus = config[3]
            self.exc = config[4]
            self.debug = config[5]

        # Get new logger.
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter('[%(levelname)s] %(message)s')

        # File Handler.
        if config[0]:
            self.fh = logging.FileHandler('app.log')
            self.fh.setLevel(logging.DEBUG)
            self.fh.setFormatter(formatter)
            self.logger.addHandler(self.fh)

        # Console Handler.
        if config[1]:
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
            self.logger.debug('DEBUG::%s', debug_text)


    def linfo(self, info_text):
        """Log fuzzer execution information."""
        if self.info:
            self.logger.info(info_text)


    def lexc(self, exception, is_error, url=""):
        """Log exceptions."""
        if self.exc:
            if is_error == 0:
                self.logger.warning('EXCEPTION(%s)::%s', exception, url)
            elif is_error == 1:
                self.logger.error(exception)
            elif is_error == 2:
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

