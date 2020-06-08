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
    parser.add_argument('-w', '--word', type=int, help='Numbers of words', required=True)
    parser.add_argument('-t', '--workers', type=int, help='Numbers of workers', default=50)
    #group = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument('-s', '-sub', help='Search subdomains')

    args = parser.parse_args()

    fuzzer = Fuzzer(args.url, args.dir)
    sub =  True if args.s is not None else False
    urls = fuzzer.get_urls(sub)
    loop = asyncio.get_event_loop()

    future = asyncio.ensure_future(fuzzer.fuzz(urls, args.word, args.workers))
    loop.run_until_complete(future)

    #rs = (grequests.get(u) for u in urlsmap = grequests.map(rs)

main()
