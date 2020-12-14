"""
Copyright (c) 2020 Diego Moraes. MIT license, see LICENSE file.
"""
import asyncio
import argparse
import datetime
from math import ceil
from logic.log import LogWrapper
from logic.fuzzer import Fuzzer
from logic.stats import Stats
from logic.builder import UrlBuilder
from logic.settings import END_DEFAULT


def main():
    """Main --> Fuzzer"""
    # Arguments #
    parser = argparse.ArgumentParser(description='Fuzzer parameters')
    required = parser.add_argument_group(title='Basic arguments')
    performance = parser.add_argument_group(title='Performance options')
    log_options = parser.add_argument_group(title='Log options')

    required.add_argument('-u', '--url', help='Base url', required=True)
    required.add_argument('-d', '--dir', help='dictionary wordlist path', required=True)

    performance.add_argument('-w', '--workers', type=int, help='Numbers of workers', default=50)
    performance.add_argument('-s', '--start', type=int, help='Start in n dictionary', default=0)
    performance.add_argument('-e', '--end', type=int, help='End in n dictionary', default=END_DEFAULT)
    performance.add_argument('-i', '--interval', type=int, help='Execution interval', required=True)
    performance.add_argument('-t', '--timeout', type=float, help='Timeout for each request (Default=3)', default=3)

    log_options.add_argument('--exceptions', help='Show exception and error messages', action='store_true')
    log_options.add_argument('--rstatus', help='Show response http status code messages', action='store_true')
    log_options.add_argument('--noinfo', help='Do not show info messages', action='store_false')
    log_options.add_argument('--debug', help='Show debug messages', action='store_true')
    log_options.add_argument('--logall', help='Log everything', action='store_true')
    log_options.add_argument('--logfile', help='Log Output to app.log', action='store_true')
    log_options.add_argument('--nocolors', help='Disable colored logs', action='store_false')

    args = parser.parse_args()

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

    # Setup #
    stats = Stats()
    urls = UrlBuilder(args.url, args.dir, args.start, args.end, main_logger)
    fuzzer = Fuzzer(urls, args.workers, main_logger, stats, args.timeout)

    interval = args.interval
    start = 0
    end = interval
    stop = False

    # urls = fuzzer.get_urls(args.start, args.end)
    loop = asyncio.get_event_loop()

    hard_end = len(urls.urls) - 1

    vueltas = int(ceil((args.end - args.start) / interval))
    vuelta = 0

    # Start #
    main_logger.linfo(f"Starting at {datetime.datetime.now()}")
    while True:
        vuelta += 1
        main_logger.linfo(f"@-------------{vuelta}/{vueltas}-------------@")
        future = asyncio.ensure_future(fuzzer.fuzz(start, end+1))
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

    main_logger.linfo(f"Total found: {stats.success}")
    main_logger.linfo(f"Total fails: {stats.fail}")
    main_logger.linfo(f"Total exceptions: {stats.exception}")
    main_logger.linfo(f"Ending at {datetime.datetime.now()}")
    main_logger.linfo("***********END***********")
    # rs = (grequests.get(u) for u in urlsmap = grequests.map(rs)


main()
