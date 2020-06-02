import sys
import requests
import asyncio
import threading
import argparse
from logic.fuzzer import Fuzzer

from concurrent.futures import ThreadPoolExecutor
from timeit import default_timer

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

    loop = asyncio.get_event_loop()
    sub =  True if args.s is not None else False
    future = asyncio.ensure_future(fuzzer.fuzz(sub, args.word, args.workers))
    loop.run_until_complete(future)


main()
