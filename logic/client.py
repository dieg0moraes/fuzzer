"""
Copyright (c) 2020 Diego Moraes. MIT license, see LICENSE file.
"""
import asyncio
from sys import platform
from timeit import default_timer
from aiohttp import ClientSession
from aiohttp_socks import SocksConnector, ProxyConnector, ProxyConnectionError, SocksConnectionError


START_TIME = default_timer()

# Solution to issue #5
if platform == "darwin":
    # False: No ssl check.
    ssl_enabled = False
else:
    # None: Default ssl check.
    ssl_enabled = None


class Client:

    def __init__(self, logger, stats):
        self.log = logger
        self.stats = stats

    async def fetch(self, session, base_url, timeout):
        try:
            async with session.get(base_url, timeout=timeout, allow_redirects=True, ssl=ssl_enabled) as response:

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
            self.log.lerr('Unicode error')
            self.stats.iexception()
        except (ProxyConnectionError, SocksConnectionError) as exc:
            if not self.log.enabled:
                raise exc
            self.log.lcritical("Proxy or Tor Error")
        except Exception as exc:
            if not self.log.enabled:
                raise exc
            self.log.lexc(type(exc), base_url)
            self.stats.iexception()

    async def bound_fetch(self, sem, session, url, timeout):
        async with sem:
            await self.fetch(session, url, timeout)

    async def get_data(self, urls, workers, timeout, tor, proxy):
        tasks = []
        sem = asyncio.Semaphore(workers)
        if tor:
            connector = SocksConnector.from_url('socks5://localhost:9050')
        elif proxy:
            connector = ProxyConnector.from_url(proxy)
        else:
            connector = None
        async with ClientSession(connector=connector) as session:

            for base_url in urls:
                task = asyncio.ensure_future(self.bound_fetch(sem, session, base_url, timeout))
                tasks.append(task)

            responses = asyncio.gather(*tasks)
            await responses
