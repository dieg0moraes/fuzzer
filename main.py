import sys

import asyncio
import argparse

from logic.fuzzer import Fuzzer

from timeit import default_timer


import asyncio
from aiohttp import ClientSession


def main():
    parser = argparse.ArgumentParser(description='Add querystring parameters')
    parser.add_argument('-u', '--url', help='Base url', required=True)
    parser.add_argument('-d', '--dir', help='dictionary wordlist path', required=True)
    parser.add_argument('-w', '--word', type=int, help='Numbers of words')
    parser.add_argument('-t', '--workers', type=int, help='Numbers of workers', default=50)
    parser.add_argument('-s', '--start', type=int, help='Start in n dictionary', default=0)
    parser.add_argument('-e', '--end', type=int, help='End in n dictionary', default=100)
    #group = parser.add_mutually_exclusive_group(required=True)

    args = parser.parse_args()

    fuzzer = Fuzzer(args.url, args.dir)

    urls = fuzzer.get_urls(args.start, args.end)
    loop = asyncio.get_event_loop()

    future = asyncio.ensure_future(fuzzer.fuzz(urls, args.workers))
    loop.run_until_complete(future)

    #rs = (grequests.get(u) for u in urlsmap = grequests.map(rs)

main()
