import sys

import asyncio
import argparse
import aiohttp
from timeit import default_timer

import logging
from aiohttp import ClientSession

from aiohttp_socks import ProxyType, ProxyConnector, ChainProxyConnector

from colorama import init, Fore


logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

START_TIME = default_timer()
REQUESTS = 0
init(autoreset=True)

class Client:

    async def fetch(self, session, base_url):
        try:
            async with session.get(base_url, timeout=3) as response:

                if response.status == 200:
                    print(Fore.LIGHTGREEN_EX + "SUCCESS::", end="")
                    # print("SUCCESS::{0}".format(base_url))
                    elapsed = default_timer() - START_TIME
                    time_completed_at = "{:5.2f}s".format(elapsed)
                    print("{0:<30} {1:>20}".format(base_url, time_completed_at))
                else:
                    pass
                    #print(Fore.RED + "FAIL({0})::{1}".format(response.status, base_url))
                return await response.text()
        except UnicodeError:
            print('unicode error')
        except Exception as e:
            print(Fore.LIGHTYELLOW_EX + "EXCEPTION({0})::{1}".format(e, Fore.RESET + base_url))

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
