"""
Copyright (c) 2020 Diego Moraes. MIT license, see LICENSE file.
"""
import asyncio
from math import ceil
from sys import platform
from typing import Dict, Union
from .client import Client
from .log import LogWrapper
from .stats import Stats
from .builder import UrlBuilder
from .exceptions import ConfigError
from .settings import TIMEOUT, TOR_TIMEOUT, WORKERS, END_DEFAULT


class Fuzzer:
    """
    Fuzzer class

    Attributes
    ----------
    timeout: int
        timeout seconds for each request.
    workers: int
        workers to use.
    tor: bool
        Perform requests over the Tor Network.
    proxy: str
        proxy url to use.

    Parameters
    ----------
    save: bool
        Save results to a csv file.
    show_logs: bool
        Set to False to disable logs.
    log_config: Dict[str, bool]
        Logger configuration.
        Example:
        log_config = {
            'option': bool,
            'option2': bool,
            ...
        }
        Options:
        Option (Default value) Description
        file (False) Set true if you want to log to settings.LOG_FILE_NAME.
        colors (True) Use colors on console handler.
        debug (False) Log debug messages.
        info (True) Log information messages.
        status (True) Log status code of each request.
        exceptions (True) Log exceptions and errors.
    """
    # pylint: disable=too-many-instance-attributes

    def __init__(self, save: bool = False, log_config: Dict[str, bool] = {}, show_logs: bool = True):
        # Logging attributes.
        self.logger = LogWrapper("fuzzer_logger", log_config, enabled=show_logs)
        self.stats = Stats(self.logger, save)

        # Performance attributes.
        self.timeout = TIMEOUT
        self.workers = WORKERS
        self._interval = None

        # Target attributes
        self._dictionary = None
        self._url = None
        self._range = [0, 0]  # [start, end]

        # Connection attributes.
        self.tor = False
        self.proxy = None
        self.urls = []
        self.ssl_check = None


    async def _fuzz(self, start, end):
        data = await self._get_results(start, end)
        return data


    async def _get_results(self, start, end):
        client = Client(self.logger, self.stats, self.ssl_check)
        data = await client.get_data(self.urls[start:end], self.workers, self.timeout, self.tor, self.proxy)
        return data


    def _checkrun(self):
        """Check arguments before execution"""
        if self.tor:
            if self.proxy:
                raise ConfigError("Cannot use Tor and a custom proxy at the same time.")

            # If the default timeout has not been changed and
            # tor is in use, set timeout to TOR_TIMEOUT.
            if self.timeout == TIMEOUT:
                self.timeout = TOR_TIMEOUT
                self.logger.lwarn(f"No timeout provided, using default: {TOR_TIMEOUT}")

        if self.timeout < 1:
            raise ConfigError("Timeout must be greater than 0.")
        if self.workers < 1:
            raise ConfigError("Use at least 1 worker.")
        if self._range[1] - self._range[0] < self._interval:
            raise ConfigError("Interval too large")

        return True


    def run(self, interval_count: int = 0, ssl_check: Union[None, bool] = None):
        """
        Start execution

        Parameters
        ----------
        interval_count: int
            Set custom execution intervals to avoid
            performance issues. This parameter indicates
            the number of requests per interval.
            Defaults to the total number of requests, creating
            only 1 execution interval.
        ssl_check: None, bool
            Set True or False to force Client to check
            ssl. Leave None for default option.
        """
        self.stats.reset_stats()

        if ssl_check is None:
            # Solution to issue #5
            if platform == "darwin":
                # False: No ssl check.
                self.ssl_check = False
            else:
                # None: Default ssl check.
                self.ssl_check = None
        elif ssl_check:
            self.ssl_check = None
        elif not ssl_check:
            self.ssl_check = False

        if interval_count == 0:
            self._interval = self._range[1] - self._range[0]
        else:
            self._interval = interval_count

        self._checkrun()

        loop_start = 0
        loop_end = self._interval

        total_loop_count = int(ceil((self._range[1] - self._range[0]) / self._interval))
        loop_count = 0

        loop = asyncio.get_event_loop()

        self.stats.get_start_time()

        try:
            while self.urls:
                loop_count += 1
                self.logger.linfo(f"@-------------{loop_count}/{total_loop_count}-------------@")
                future = asyncio.ensure_future(self._fuzz(loop_start, loop_end+1))
                loop.run_until_complete(future)

                del self.urls[loop_start:loop_end+1]
        except KeyboardInterrupt:
            self.logger.lerr("I've been interrupted :(")
        finally:
            self.logger.linfo(f"@-----------------------------@")
            # Always wipe tasks and urls.
            future.cancel()
            del self.urls[:]
            self.stats.get_end_time()
            self.stats.export_results()


    def build_urls(self, ask: bool = False, inject: bool = True):
        """
        Build urls to test

        Use set_target before this.

        Parameters
        ----------
        ask: bool
            ask before using an injection "[*]".
            Set True only when using CLI.
        inject: bool
            if ask = False, set this to False to
            avoid using injections by default.
        """
        if not self._url or not self._dictionary:
            raise ConfigError("Missing settings, try using set_target before this.")
        url_build = UrlBuilder(self._url, self._dictionary, self._range, ask, inject)
        self.urls = url_build.urls


    def set_target(self, dictionary: str, url: str, start: int = 0, end: int = END_DEFAULT):
        """
        Set execution intervals.

        Use this before build_urls or
        use reset_urls after building urls
        to be able to use this.

        Parameters
        ----------
        dictionary_path: str
            Path to the file with the words to test.
            Dictionary must have one word per line.
        url: str
            You may add "[*]" to set a custom injection point,
            for example:

                "https://[*].example.com/" will be:
                "https://word.example.com/"

            by default, it will go at the end of the url:

                "https://www.example.com/[*]"
        start: int
            Index of the first word in the dictionary to use.
            Defaults to 0.
        end: int
            Index of the last word to use.
            Defaults to the last word in the dictionary.
        """
        # Checking parameters.
        params = [start, end]
        for param in params:
            if not isinstance(param, int):
                raise ConfigError(f"{param} parameter must be int type.")
        del params

        if end == END_DEFAULT:
            end = 0
            for _ in open(dictionary, 'r'):
                end += 1

        if start < 0 or end < 0:
            raise ConfigError("Parameters must be positive numbers.")
        if start >= end:
            raise ConfigError("start parameter must be smaller than end.")

        # Setter.
        self._range[0] = start
        self._range[1] = end
        self._url = url
        self._dictionary = dictionary


    def print_stats(self):
        """Print result statistics"""
        self.logger.linfo("Results:")
        for key, value in self.stats.req_stats.items():
            self.logger.linfo(f"{key}: {value}")
        self.logger.linfo(f"Start at {self.stats.start_time}")
        self.logger.linfo(f"End at {self.stats.end_time}")
