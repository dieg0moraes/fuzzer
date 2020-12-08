"""
LICENCIA
"""
import asyncio
import argparse
from math import ceil
from logic.log import LogWrapper
from logic.fuzzer import Fuzzer


def main():
    """Main --> Fuzzer"""
    # Arguments #
    parser = argparse.ArgumentParser(description='Fuzzer parameters')
    required = parser.add_argument_group(title='Basic arguments')
    performance = parser.add_argument_group(title='Performance options')
    log_options = parser.add_argument_group(title='Log options')

    required.add_argument('-u', '--url', help='Base url', required=True)
    required.add_argument('-d', '--dir', help='dictionary wordlist path', required=True)
    performance.add_argument('-t', '--workers', type=int, help='Numbers of workers', default=50)
    performance.add_argument('-s', '--start', type=int, help='Start in n dictionary', default=0)
    performance.add_argument('-e', '--end', type=int, help='End in n dictionary', default=1000000)  # TODO: Issue #1.
    performance.add_argument('-i', '--interval', type=int, help='Task interval', required=True)
    log_options.add_argument('--exceptions', help='Show exception messages', action='store_true')
    log_options.add_argument('--rstatus', help='Show response http status code messages', action='store_true')
    log_options.add_argument('--noinfo', help='Do not show info messages', action='store_false')
    log_options.add_argument('--debug', help='Show debug messages', action='store_true')
    log_options.add_argument('--logall', help='Log everything', action='store_true')
    log_options.add_argument('--logfile', help='Log Output to app.log', action='store_true')

    args = parser.parse_args()

    if args.interval > args.end - args.start:
        parser.error("--interval must not be grater than the difference bethween --start and --end")

    # Log Setup #
    if args.logall:
        log_config = [args.logfile, "ALL"]
    else:
        log_config = [args.logfile, args.noinfo, args.rstatus, args.exceptions, args.debug]
    main_logger = LogWrapper("main_log", log_config)

    # Setup #
    fuzzer = Fuzzer(args.url, args.dir, main_logger)

    interval = args.interval
    start = args.start
    end = start + interval
    hard_end = args.end
    stop = False

    urls = fuzzer.get_urls(start, hard_end)
    loop = asyncio.get_event_loop()

    vueltas = int(ceil((hard_end - start) / interval))
    vuelta = 0

    # Start #
    main_logger.linfo("Starting")
    while True:
        vuelta += 1
        main_logger.linfo(f'@-------------{vuelta}/{vueltas}-------------@')
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

    main_logger.linfo("END.")
    # rs = (grequests.get(u) for u in urlsmap = grequests.map(rs)


main()
