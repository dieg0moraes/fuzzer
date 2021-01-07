"""
Copyright (c) 2020 Diego Moraes. MIT license, see LICENSE file.
"""
import asyncio
from math import ceil
from typing import Dict, Union
from .client import Client
from .log import LogWrapper
from .stats import Stats
from .builder import UrlBuilder
from .exceptions import ConfigError
from .settings import TIMEOUT, WORKERS


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
        # Preguntarle a Diego si lo quiere así o con funciones.
        # Modificando el atributo o con un setter.
        # Logging attributes.
        self.logger = LogWrapper("fuzzer_logger", log_config, enabled=show_logs)
        self.stats = Stats(self.logger, save)

        # Performance attributes.
        self.timeout = TIMEOUT
        self.workers = WORKERS
        self.start = 0
        self.end = None
        self.interval = None

        # Connection attributes.
        self.tor = False
        self.proxy = None
        self.urls = []


    async def _fuzz(self, start, end):
        data = await self._get_results(start, end)
        return data


    async def _get_results(self, start, end):
        client = Client(self.logger, self.stats)
        data = await client.get_data(self.urls[start:end], self.workers, self.timeout, self.tor, self.proxy)
        return data


    def _checkrun(self):
        """Check arguments before execution"""
        if self.tor and self.proxy:
            raise ConfigError("Cannot use Tor and a custom proxy at the same time.")
        if self.timeout < 1:
            raise ConfigError("Timeout must be grater than 0.")

        return True


    def run(self, no_stop: bool = False):  # TODO: Ver si hay mucho 200 y preguntar si seguir.
        """
        Start execution

        Parameters
        ----------
        no_stop: bool
            Disable query_yes_no.        
        """
        self._checkrun()

        loop_start = 0
        loop_end = self.interval
        hard_end = len(self.urls) - 1

        total_loop_count = int(ceil((self.end - self.start) / self.interval))
        loop_count = 0

        loop = asyncio.get_event_loop()

        self.stats.get_start_time()
        while True:
            loop_count += 1
            self.logger.linfo(f"@-------------{loop_count}/{total_loop_count}-------------@")
            future = asyncio.ensure_future(self._fuzz(loop_start, loop_end+1))
            loop.run_until_complete(future)

            if loop_end == hard_end:
                break
            loop_start = loop_end + 1
            loop_end += self.interval
            if loop_end > hard_end:
                loop_end = hard_end
            if loop_start > loop_end:
                loop_start = loop_end

        self.stats.get_end_time()
        self.stats.export_results()


    def get_urls(self, url: str, dictionary_path: str, ask: bool = False, inject: bool = True):
        """
        Build urls to test

        Parameters
        ----------
        url: str
            You may add "[*] to set a custom injection point,
            for example:

                "https://[*].example.com/" will be:
                "https://<word>.example.com/"

            by default, it will go at the end of the url:

                "https://www.example.com/[*]"

        dictionary_path: str
            Path to the file with the words to test.

            Dictionary must have one word per line.
            Example:

                "/example/files/dictionary.txt"

        ask: bool
            ask before using an injection "[*]".
            Set True only when using CLI.

        inject: bool
            if ask = False, set this to False to
            avoid using injections by default.
        """
        url_build = UrlBuilder(url, dictionary_path, self.start, self.end, ask, inject)
        self.stats.base_url = url
        self.urls = url_build.urls

    def reset_urls(self):
        """Reset (delete) the existing url list"""
        self.urls = []

    def set_intervals(self, start: int, end: int, interval_count: int = 0):
        """
        Set execution intervals.

        Use this before get_urls or
        use reset_urls after building urls
        to be able to use this.

        Parameters
        ----------
        start: int
            Index of the first word in the dictionary to use.
            Defaults to 0.
        end: int
            Index of the last word to use.
            Defaults to the last word in the dictionary.
        interval_count: int
            Set custom execution intervals to avoid
            performance issues. This parameter indicates
            the number of requests per interval.
            Defaults to the total number of requests creating
            only 1 execution interval.
        """
        # Check parameters.
        if self.urls:
            raise ConfigError("Cannot set intervals after building urls, use reset_urls.")

        params = [start, end, interval_count]
        for param in params:
            if not isinstance(param, int):
                raise ConfigError("Parameters must be int type.")
        del params

        if start < 0 or end < 0 or interval_count < 0:
            raise ConfigError("Parameters must be positive numbers.")
        if start >= end:
            raise ConfigError("start parameter must be smaller than end.")
        if end - start < interval_count:
            raise ConfigError("interval_count must not be grater than the difference bethween start and end.")

        # Set intervals.
        self.start = start
        self.end = end
        if interval_count == 0:
            self.interval = end - start
        else:
            self.interval = interval_count
