"""
INSERTE LICENCIA
"""
import logging


class LogWrapper:
    """Logging wrapper class"""

    def __init__(self, name, config):

        if config[1] == "ALL":
            self.info = self.rstatus = self.exc = self.debug = True
        else:
            self.info = config[1]
            self.rstatus = config[2]
            self.exc = config[3]
            self.debug = config[4]

        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter('[%(levelname)s] %(message)s')

        # File Handler.
        if config[0]: # pylint=invalid-name
            self.fh = logging.FileHandler('app.log')
            self.fh.setLevel(logging.DEBUG)
            self.fh.setFormatter(formatter)
            self.logger.addHandler(self.fh)

        # Console Handler.
        self.ch = logging.StreamHandler()
        self.ch.setLevel(logging.DEBUG)
        self.ch.setFormatter(formatter)
        self.logger.addHandler(self.ch)


    def lsuccess(self, text):
        """Log success (200) messages."""
        self.logger.info('SUCCESS::%s', text)


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
            if not is_error:
                self.logger.warning('EXCEPTION(%s)::%s', exception, url)
            else:
                self.logger.error(exception)


    def lstatus(self, status_code, url):
        """Log other connection status codes (different from 200)"""
        if self.rstatus:
            if status_code[0] == "3":
                self.logger.info('REDIRECT(%s)::%s', status_code, url)
            elif status_code[0] in ("4", "5"):
                self.logger.info('FAIL(%s)::%s', status_code, url)
