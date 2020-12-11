"""
Copyright (c) 2020 Diego Moraes. MIT license, see LICENSE file.
"""
import asyncio
from timeit import default_timer
from aiohttp import ClientSession
from .settings import EXCEPTION_CODE, ERROR_CODE

# from aiohttp_socks import ProxyType, ProxyConnector, ChainProxyConnector


START_TIME = default_timer()


class Client:

    def __init__(self, logger, stats):
        self.log = logger
        self.stats = stats

    async def fetch(self, session, base_url, timeout):
        try:
            async with session.get(base_url, timeout=timeout) as response:

                if response.status == 200:
                    elapsed = default_timer() - START_TIME
                    time_completed_at = f"{elapsed:5.2f}s"
                    log_message = f"{base_url:<30} {time_completed_at:>20}"
                    self.log.lsuccess(log_message)
                    self.stats.isuccess()
                else:
                    self.log.lstatus(str(response.status), base_url)
                    self.stats.ifail()
                return await response.text()

        except UnicodeError:
            self.log.ldebug('Unicode error')
            self.stats.iexception()
        except Exception as exc:
            # TODO: Agarrar específicas de conexión.
            self.log.lexc(type(exc), EXCEPTION_CODE, base_url)
            self.stats.iexception()
        # except Exception as error:
        #     self.log.exc(type(exc), ERROR_CODE)

    async def bound_fetch(self, sem, session, url, timeout):
        async with sem:
            await self.fetch(session, url, timeout)

    async def get_data(self, urls, workers, timeout):
        tasks = []
        sem = asyncio.Semaphore(workers)

        async with ClientSession() as session:

            for base_url in urls:
                task = asyncio.ensure_future(self.bound_fetch(sem, session, base_url, timeout))
                tasks.append(task)

            responses = asyncio.gather(*tasks)
            await responses
