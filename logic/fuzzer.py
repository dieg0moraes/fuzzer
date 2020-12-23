"""
Copyright (c) 2020 Diego Moraes. MIT license, see LICENSE file.
"""
from .client import Client
import asyncio
from aiohttp import ClientSession

class Fuzzer:

    def __init__(self, urls, workers, logger, stats, timeout):
        self.log = logger
        self.stats = stats
        self.timeout = timeout
        self.urls = urls
        self.workers = workers


    async def fuzz(self, start, end):
        data = await self.get_results(start, end)
        return data


    async def get_results(self, start, end):
        client = Client(self.log, self.stats)
        data = None
        try:
            tasks = []
            sem = asyncio.Semaphore(self.workers)
            async  with ClientSession() as session:
                for url in self.urls[start: end]:
                    task = asyncio.ensure_future(
                        client.bound_fetch(sem, session, url, self.timeout)
                    )
                    tasks.append(task)
                responses = asyncio.gather(*tasks)
                await  self.handle_responses(responses)

        except Exception as e:
            raise e
        return data

    async def handle_responses(self, responses):
        loop = asyncio.get_event_loop()
        results = loop.run_until_complete(responses)
        for response in results:
            response = await  response
            if response.status == 200:
                elapsed = default_timer() - START_TIME
                time_completed_at = f"{elapsed:5.2f}s"
                log_message = f"{base_url:<30} {time_completed_at:>20}"
                self.log.lsuccess(log_message)
                self.stats.isuccess()
            else:
                self.log.lstatus(str(response.status), base_url)
                self.stats.ifail()
