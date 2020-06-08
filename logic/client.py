import sys

import asyncio
import argparse
import aiohttp
from timeit import default_timer

import logging
from aiohttp import ClientSession

from aiohttp_socks import ProxyType, ProxyConnector, ChainProxyConnector



logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

START_TIME = default_timer()
REQUESTS = 0

class Client:

    async def fetch(self, session, base_url):
        try:
            async with session.get(base_url, timeout=3, proxy='http://127.0.0.1:8081') as response:
                REQUESTS = REQUESTS + 1
                print(REQUESTS)
                if response.status == 200:
                    print("SUCCESS::{0}".format(base_url))
                    elapsed = default_timer() - START_TIME
                    time_completed_at = "{:5.2f}s".format(elapsed)
                    print("{0:<30} {1:>20}".format(base_url, time_completed_at))
                #delay = response.headers.get("DELAY")
                #date = response.headers.get("DATE")
                #print("{}:{} with delay {}".format(date, response.url, delay))
                return await response.text()
        except aiohttp.ClientProxyConnectionError:
            print('conn')
        except UnicodeError:
            print('unicode')
        except:
            pass

    async def bound_fetch(self, sem, session, url):
        async with sem:
            await self.fetch(session, url)

    async def get_data(self, urls, words, workers):
        tasks = []
        sem = asyncio.Semaphore(workers)
        #conn = ProxyConnector(remote_resolve=False)
        connector = ChainProxyConnector.from_urls([
            'http://127.0.0.1:8081',
            'socks5://localhost:9050',
        ])
        async with ClientSession() as session:
            for base_url in urls[:words]:
                task = asyncio.ensure_future(self.bound_fetch(sem, session, base_url))
                tasks.append(task)

            responses = asyncio.gather(*tasks)
            await responses

























"""
    async def get_tasks(self, urls, words, workers):
        async with ClientSession() as session:
            tasks = []
            START_TIME = default_timer()
            for base_url in urls[:words]:
                task = asyncio.ensure_future(self.bound_fetch(sem, session, base_url))
                tasks.append(task)
            return tasks

"""












                #data = response.text
                #if response.status_code == 200:
                #    print("SUCCESS::{0}".format(base_url))
                #    elapsed = default_timer() - START_TIME
                #    time_completed_at = "{:5.2f}s".format(elapsed)
                #    print("{0:<30} {1:>20}".format(base_url, time_completed_at))
                #
                #return {
                #    'status': response.status_code,
                #    'url': response.url
                #}

        #except Exception as ex:
        #    logging.warning(ex)
