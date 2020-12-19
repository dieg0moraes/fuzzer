"""
Copyright (c) 2020 Diego Moraes. MIT license, see LICENSE file.
"""
import asyncio
import argparse
import datetime
from math import ceil
from utils import query_yes_no
from logic.log import LogWrapper
from logic.fuzzer import Fuzzer
from logic.stats import Stats
from logic.builder import UrlBuilder
from logic.settings import END_DEFAULT, TIMEOUT, WORKERS


def main():
    """Main --> Fuzzer"""
    # Arguments #
    parser = argparse.ArgumentParser(description='Fuzzer parameters')
    required = parser.add_argument_group(title='Basic arguments')
    performance = parser.add_argument_group(title='Performance options')
    connection = parser.add_argument_group(title='Connection options')
    log_options = parser.add_argument_group(title='Log options')

    required.add_argument('-u', '--url', help='Base url', required=True)
    required.add_argument('-d', '--dir', help='dictionary wordlist path', required=True)

    performance.add_argument('-w', '--workers', type=int, help='Numbers of workers', default=WORKERS)
    performance.add_argument('-s', '--start', type=int, help='Start in n dictionary', default=0)
    performance.add_argument('-e', '--end', type=int, help='End in n dictionary', default=END_DEFAULT)
    performance.add_argument('-i', '--interval', type=int, help='Execution interval', required=True)
    performance.add_argument('-t', '--timeout', type=float, help='Timeout for each request (Default=3)', default=TIMEOUT)

    connection.add_argument('--tor', help='Perform requests over the Tor network', action='store_true')
    connection.add_argument('--proxy', type=str, help='Custom proxy url')

    log_options.add_argument('--exceptions', help='Show exception and error messages', action='store_true')
    log_options.add_argument('--rstatus', help='Show response http status code messages', action='store_true')
    log_options.add_argument('--noinfo', help='Do not show info messages', action='store_false')
    log_options.add_argument('--debug', help='Show debug messages', action='store_true')
    log_options.add_argument('--logall', help='Log everything', action='store_true')
    log_options.add_argument('--logfile', help='Log Output to app.log', action='store_true')
    log_options.add_argument('--nocolors', help='Disable colored logs', action='store_false')

    args = parser.parse_args()

    # Auto default end parameter #
    if args.end == END_DEFAULT:
        with open(args.dir, 'r') as dictionary:
            total_lines = 0
            for line in dictionary:
                total_lines += 1
            args.end = total_lines

    # Check arguments #
    if args.start >= args.end:
        parser.error("--end must be grater than --start")
    if args.interval > args.end - args.start:
        parser.error("--interval must not be grater than the difference bethween --start and --end")
    if args.timeout <= 0:
        parser.error("--timeout must be grater than 0")
    if args.tor and args.proxy:
        parser.error("Cannot use a Proxy and Tor at the same time")

    # Log Setup #
    if args.logall:
        log_config = {
            "info": True,
            "status": True,
            "exceptions": True,
            "debug": True
        }
    else:
        log_config = {
            "info": args.noinfo,
            "status": args.rstatus,
            "exceptions": args.exceptions,
            "debug": args.debug,
        }
    log_config["file"] = args.logfile
    log_config["colors"] = args.nocolors

    main_logger = LogWrapper("main_log", log_config)

    # Fuzzer setup #
    stats = Stats()

    urls = UrlBuilder(args.url, args.dir, args.start, args.end)
    total_urls = len(urls.urls)
    main_logger.linfo(f"Number of urls to test: {total_urls}")

    fuzzer = Fuzzer(urls.urls, args.workers, main_logger, stats, args.timeout, args.tor, args.proxy)

    interval = args.interval
    start = 0
    end = interval
    hard_end = total_urls - 1

    vueltas = int(ceil((args.end - args.start) / interval))
    vuelta = 0

    loop = asyncio.get_event_loop()

    # Start #
    main_logger.linfo(f"Starting at {datetime.datetime.now()}")
    while True:
        try:
            vuelta += 1
            main_logger.linfo(f"@-------------{vuelta}/{vueltas}-------------@")
            # stats.start_rpm()
            future = asyncio.ensure_future(fuzzer.fuzz(start, end+1))
            loop.run_until_complete(future)
            # main_logger.linfo(f"Requests per minute: aprox. {stats.get_rpm()}")
            # stats.get_rpm()

            if end == hard_end:
                break
            start = end + 1
            end += interval
            if end > hard_end:
                end = hard_end
            if start > end:
                start = end
        except KeyboardInterrupt:
            stop = query_yes_no('Stop - Save current state? ')
            # TODO: Guardar estado.
            break

    main_logger.linfo(f"Total found: {stats.success}")
    main_logger.linfo(f"Total fails: {stats.fail}")
    main_logger.linfo(f"Total exceptions: {stats.exception}")
    main_logger.linfo(f"Ending at {datetime.datetime.now()}")
    main_logger.linfo("***********END***********")


main()
