"""
LICENCIA
"""
import asyncio
from timeit import default_timer
import aiohttp
from aiohttp import ClientSession
# from aiohttp_socks import ProxyType, ProxyConnector, ChainProxyConnector


START_TIME = default_timer()
REQUESTS = 0


class Client:

    def __init__(self, logger):
        self.log = logger

    async def fetch(self, session, base_url):
        try:
            async with session.get(base_url, timeout=10) as response:

                if response.status == 200:
                    elapsed = default_timer() - START_TIME
                    time_completed_at = f"{elapsed:5.2f}s"
                    log_message = f"{base_url:<30} {time_completed_at:>20}"
                    self.log.lsuccess(log_message)
                else:
                    self.log.lstatus(str(response.status), base_url)

                return await response.text()

        except UnicodeError:
            self.log.ldebug('Unicode error')
        except Exception as exc:
            # TODO: Agarrar específicas de conexión.
            # BUG: Las de asyncio quedan vacías (exc = "").
            self.log.lexc(exc, False, base_url)
        # except Exception as error:
        #     self.log.exc(error, True)

    async def bound_fetch(self, sem, session, url):
        async with sem:
            await self.fetch(session, url)

    async def get_data(self, urls, workers):
        tasks = []
        sem = asyncio.Semaphore(workers)

        async with ClientSession() as session:

            for base_url in urls:
                task = asyncio.ensure_future(self.bound_fetch(sem, session, base_url))
                tasks.append(task)

            responses = asyncio.gather(*tasks)
            await responses
