"""
Copyright (c) 2020 Diego Moraes. MIT license, see LICENSE file.
"""
from .client import Client


class Fuzzer:

    def __init__(self, urls, workers, logger, stats, timeout):
        self.log = logger
        self.stats = stats
        self.timeout = timeout
        self.urls = urls.urls
        self.workers = workers


    async def fuzz(self, start, end):
        data = await self.get_results(start, end)
        return data


    async def get_results(self, start, end):
        client = Client(self.log, self.stats)
        data = await client.get_data(self.urls[start:end], self.workers, self.timeout)
        return data
