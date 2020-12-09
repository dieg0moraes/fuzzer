"""
LICENCIA
"""
import asyncio
from timeit import default_timer
import aiohttp
from aiohttp import ClientSession
# from aiohttp_socks import ProxyType, ProxyConnector, ChainProxyConnector


START_TIME = default_timer()
global stats
stats = [0, 0, 0]


class Client:

    def __init__(self, logger):
        self.log = logger

    async def fetch(self, session, base_url):
        try:
            async with session.get(base_url, timeout=3) as response:

                if response.status == 200:
                    elapsed = default_timer() - START_TIME
                    time_completed_at = f"{elapsed:5.2f}s"
                    log_message = f"{base_url:<30} {time_completed_at:>20}"
                    self.log.lsuccess(log_message)
                    stats[0] += 1
                else:
                    self.log.lstatus(str(response.status), base_url)
                    stats[1] += 1

                return await response.text()

        except UnicodeError:
            self.log.ldebug('Unicode error')
        except Exception as exc:
            # TODO: Agarrar específicas de conexión.
            self.log.lexc(type(exc), 0, base_url)
            stats[2] += 1
        # except Exception as error:
        #     self.log.exc(type(exc), 1)

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
