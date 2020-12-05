import sys
from math import ceil

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
    # parser.add_argument('-w', '--word', type=int, help='Numbers of words')
    parser.add_argument('-t', '--workers', type=int, help='Numbers of workers', default=50)
    parser.add_argument('-s', '--start', type=int, help='Start in n dictionary', default=0)
    parser.add_argument('-e', '--end', type=int, help='End in n dictionary', default=100)
    parser.add_argument('-i', '--interval', type=int, help='Task interval', required=True)
    # group = parser.add_mutually_exclusive_group(required=True)

    args = parser.parse_args()

    if args.interval > args.end - args.start:
        parser.error("--interval must not be grater than the difference bethween --start and --end")

    fuzzer = Fuzzer(args.url, args.dir)

    interval = args.interval
    start = args.start
    end = start + interval
    hard_end = args.end
    stop = False

    urls = fuzzer.get_urls(start, hard_end)
    loop = asyncio.get_event_loop()

    vueltas = int(ceil((hard_end - start) / interval))
    vuelta = 0
    while True:
        vuelta += 1
        print("@-------------{0}/{1}-------------@".format(vuelta, vueltas))
        future = asyncio.ensure_future(fuzzer.fuzz(urls[start:end+1], args.workers))
        loop.run_until_complete(future)

        if end == hard_end:
            break
        if stop:
            break
        start = end + 1
        end += interval
        if end > hard_end:
            end = hard_end
            stop = True
        if start > end:
            start = end

    print("END.")

    # rs = (grequests.get(u) for u in urlsmap = grequests.map(rs)

main()
