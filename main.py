"""
Copyright (c) 2020 Diego Moraes. MIT license, see LICENSE file.
"""
import argparse
from logic.fuzzer import Fuzzer
from logic.fuzzer import TIMEOUT, WORKERS
from logic.settings import END_DEFAULT


def main():
    """Main --> Fuzzer"""
    # Arguments #
    parser = argparse.ArgumentParser(description='Fuzzer parameters')
    required = parser.add_argument_group(title='Basic arguments')
    performance = parser.add_argument_group(title='Performance options')
    connection = parser.add_argument_group(title='Connection options')
    log_options = parser.add_argument_group(title='Log options')
    other = parser.add_argument_group(title='Other options')

    required.add_argument('-u', '--url', help='Base url', required=True)
    required.add_argument('-d', '--dir', help='dictionary wordlist path', required=True)

    performance.add_argument('-w', '--workers', type=int, help='Numbers of workers', default=WORKERS)
    performance.add_argument('-s', '--start', type=int, help='Start in n dictionary', default=0)
    performance.add_argument('-e', '--end', type=int, help='End in n dictionary', default=END_DEFAULT)
    performance.add_argument('-i', '--interval', type=int, help='Execution interval', default=0)
    performance.add_argument('-t', '--timeout', type=float, help='Timeout for each request (Default=3)', default=TIMEOUT)

    connection.add_argument('--tor', help='Perform requests over the Tor network', action='store_true')
    connection.add_argument('--proxy', type=str, help='Custom proxy url')
    connection.add_argument('--checkSSL', type=int, help='0 = Default, 1 = Force check, 2 = Disable', default=0)

    log_options.add_argument('--exceptions', help='Show exception and error messages', action='store_true')
    log_options.add_argument('--rstatus', help='Show response http status code messages', action='store_true')
    log_options.add_argument('--noinfo', help='Do not show info messages', action='store_false')
    log_options.add_argument('--debug', help='Show debug messages', action='store_true')
    log_options.add_argument('--logall', help='Log everything', action='store_true')
    log_options.add_argument('--logfile', help='Log Output to app.log', action='store_true')
    log_options.add_argument('--nocolors', help='Disable colored logs', action='store_false')

    other.add_argument('-g', '--save', help='Save results to csv file', action='store_true')

    args = parser.parse_args()

    # Check arguments #
    if args.end != END_DEFAULT:
        if args.start >= args.end:
            parser.error("--end must be grater than --start")
        if args.interval > args.end - args.start:
            parser.error("--interval must not be grater than the difference bethween --start and --end")
    if args.timeout < 1:
        parser.error("--timeout must be grater than 0")
    if args.workers < 1:
        parser.error("--workers must be grater than 0")
    if args.tor and args.proxy:
        parser.error("Cannot use a Proxy and Tor at the same time")

    if args.checkSSL == 0:
        ssl = None
    elif args.checkSSL == 1:
        ssl = True
    elif args.checkSSL == 2:
        ssl = False
    else:
        parser.error("Invalid value for checkSSL")

    # Log Config #
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

    # Fuzzer setup #
    fuzzer = Fuzzer(args.save, log_config, True)

    main_logger = fuzzer.logger

    # Url building #
    try:
        fuzzer.set_target(args.dir, args.url, args.start, args.end)
        fuzzer.build_urls(ask=True)
    except FileNotFoundError:
        main_logger.lcritical(f"{args.dir} Not found")

    main_logger.linfo(f"Number of urls to test: {len(fuzzer.urls)}")
    fuzzer.tor = args.tor
    fuzzer.proxy = args.proxy
    fuzzer.timeout = args.timeout
    fuzzer.workers = args.workers

    # Start execution #
    fuzzer.run(args.interval, ssl)

    fuzzer.print_stats()

    main_logger.linfo("***********END***********")


main()
