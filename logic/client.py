import sys
import requests
import asyncio
import threading
import argparse

from concurrent.futures import ThreadPoolExecutor
from timeit import default_timer

import logging

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

START_TIME = default_timer()

class Client:

    def make_request(self, session, base_url):
        try:
            with session.get(base_url, timeout=5) as response:
                data = response.text
                if response.status_code == 200:
                    print("SUCCESS::{0}".format(base_url))
                    elapsed = default_timer() - START_TIME
                    time_completed_at = "{:5.2f}s".format(elapsed)
                    print("{0:<30} {1:>20}".format(base_url, time_completed_at))

                return {
                    'status': response.status_code,
                    'url': response.url
                    }

        except Exception as ex:
            logging.warning(ex)



    async def get_data(self, urls, words, workers):
        tasks = await self.get_tasks(urls, words, workers)
        data = []
        for response in await asyncio.gather(*tasks):
            data.append(response);
        print('TOTAL TIME', default_timer() - START_TIME)
        return data

    async def get_tasks(self, urls, words, workers):
        with ThreadPoolExecutor(max_workers=workers) as executor:
            with requests.Session() as session:
                # Set any session parameters here before calling `fetch`
                loop = asyncio.get_event_loop()
                START_TIME = default_timer()
                tasks = [
                    loop.run_in_executor(
                        executor,
                        self.make_request,
                        *(session, base_url) # Allows us to pass in multiple argument=s to `fetch`
                    )
                    for base_url in urls[:words]
                ]
                return tasks
