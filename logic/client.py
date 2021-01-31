"""
Copyright (c) 2020 Diego Moraes. MIT license, see LICENSE file.
"""
import asyncio
from aiohttp import ClientSession
from aiohttp_socks import SocksConnector, ProxyConnector, ProxyConnectionError, SocksConnectionError


class Client:

    def __init__(self, logger, stats, ssl_check):
        self.log = logger
        self.stats = stats
        self.ssl = ssl_check

    async def fetch(self, session, url, timeout):
        try:
            async with session.get(url, timeout=timeout, allow_redirects=True, ssl=self.ssl) as response:

                if str(response.status)[0] == "2":
                    self.stats.isuccess(url, str(response.status))
                else:
                    self.stats.ifail(url, str(response.status))
                await response.text()

        # Estas except podrían irse para fuzzer.run().
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
            self.log.lexc(type(exc), url)
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

            for url in urls:
                task = asyncio.ensure_future(self.bound_fetch(sem, session, url, timeout))
                tasks.append(task)

            responses = asyncio.gather(*tasks)
            await responses
