# Fuzzer

Copyright (c) 2020 Diego Moraes. MIT license, see LICENSE file.

### Set up

- cd to Fuzzer directory.

- python3 -m pip install -r requirements.txt

### Usage

```
Usage: python3 main.py [args]

Arguments

-h (--help)           Show help message and exit.

Required arguments:

-u (--url) -> Url like http://www.example.com/
You may add [*] to inject the word in a specific place, like http://[*].example.com/
By default it is http://www.example.com/[*]
Notice you should add the "/" at the end, or it will be http://www.example.com[*]

-d (--dir)            Path to dictionary wordlist.

Performance options:

-w (--workers)        Number of workers (50 by default).
-s (--start)          Index of word to start in the dictionary (defaults to 0, the first word of the dictionary).
-e (--end)            Index of the last word of the dictionary to test (defaults to the last word of the dictionary).
-i (--interval)       Number of requests per interval.
-t (--timeout)        Timeout for each request (Defaults to 3)

Connection options:
--tor                 Perform requests over the Tor network
--proxy               Custom proxy url
--checkSSL            Check SSL certificates
                      0: Use default
                      1: Force check
                      2: Disable

Log options:

--exceptions          Show exception and error messages
--rstatus             Show response http status code messages (200 status code is always logged)
--noinfo              Do not show info messages (Not recommended)
--debug               Show debug messages
--logall              Log everything
--logfile             Log output to app.log
--nocolors            Disable colored logs

Other:

-g (--save)           Save results to csv file
                      This will save any status code in settings.STATUS_TO_SAVE
```
